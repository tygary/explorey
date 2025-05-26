# import the necessary packages
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import imutils
import cv2
import time

FORM_OPEN_ACCOUNT = 'open_account'
FORM_TELLER = 'teller'
FORM_DEPOSIT = 'deposit'
FORM_TRANSFER = 'transfer'
FORM_WITHDRAW = 'withdraw'

class FormInfo(object):
    def __init__(self, type, to_account_number=None, from_account_number=None, amount_file_path=None, name_file_path=None):
        self.type = type
        self.from_account_number = from_account_number
        self.to_account_number = to_account_number
        self.amount_file_path = amount_file_path
        self.name_file_path = name_file_path

def write_image_for_contour(contour, image, path):
    x, y, w, h = cv2.boundingRect(contour)
    roi = image[y:y+h, x:x+w]
    cv2.imwrite(path, roi)


def detect_contours(form, form_w, form_h, error_margin=0.2, form_type=None):
    """Helper function to detect contours in the form."""
    if form_type == "withdraw":
        account_number_size = (form_w * 2) // 3
    else:
        account_number_size = form_w // 3
    amount_box_width = form_w // 3
    amount_box_height = form_h // 10
    name_box_width = (form_w * 2) // 3
    name_box_height = form_h // 10

    contours = imutils.grab_contours(cv2.findContours(form.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE))
    innerCnts = sorted(contours, key=cv2.contourArea, reverse=True)

    account_number_contours = []
    amount_box_contours = []
    name_box_countours = []

    for c in innerCnts:
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        # print(f"Contour: {c}, Area: {cv2.contourArea(c)}, Width: {w}, Height: {h}, Aspect Ratio: {ar:.2f}")
        if len(approx) == 4 and abs(account_number_size - w) < error_margin * account_number_size and abs(account_number_size - h) < error_margin * account_number_size and ar >= 0.9 and ar <= 1.1:
            account_number_contours.append(c)
        elif len(approx) == 4 and abs(amount_box_width - w) < error_margin * amount_box_width and abs(amount_box_height - h) < error_margin * amount_box_height and ar > 4 and ar <= 4.5:
            amount_box_contours.append(c)
        elif len(approx) == 4 and abs(name_box_width - w) < error_margin * name_box_width and abs(name_box_height - h) < error_margin * name_box_height and 8 < ar <= 9:
            name_box_countours.append(c)

    return account_number_contours, amount_box_contours, name_box_countours

def find_account_number(area, grayscale_image, paper=None):
    # split into 16 quadrants
    # (4 rows, 4 columns)
    x, y, w, h = cv2.boundingRect(area)

    # trim off the outer edges
    x += 10
    y += 10
    w -= 20
    h -= 20

    # Extract the entire grid region
    grid_roi = grayscale_image[y:y+h, x:x+w]
    
    # Enhance contrast
    grid_roi = cv2.equalizeHist(grid_roi)
    
    # Light blur to reduce noise
    grid_roi = cv2.GaussianBlur(grid_roi, (3, 3), 0)
    
    # Apply Otsu's thresholding
    _, binary_grid = cv2.threshold(grid_roi, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Create a copy of the grayscale image for visualization
    vis_image = cv2.cvtColor(grayscale_image, cv2.COLOR_GRAY2BGR)
    
    # Show the thresholded grid in the visualization
    vis_grid = cv2.cvtColor(binary_grid, cv2.COLOR_GRAY2BGR)
    vis_image[y:y+h, x:x+w] = vis_grid

    num_rows, num_cols = 4, 4
    cell_width = w // num_cols
    cell_height = h // num_rows

    # Calculate margins to avoid grid lines
    margin = int(min(cell_width, cell_height) * 0.15)  # 15% margin

    cells = []
    for row in range(num_rows):
        for col in range(num_cols):
            cell_x = col * cell_width + margin
            cell_y = row * cell_height + margin
            cell_w = cell_width - 2 * margin
            cell_h = cell_height - 2 * margin
            cell = (cell_x, cell_y, cell_w, cell_h)
            cells.append(cell)

    # determine which quadrants are filled
    filled_quadrants = []
    for i, (cx, cy, cw, ch) in enumerate(cells):
        # Extract the cell from the already thresholded grid
        binary_quad = binary_grid[cy:cy+ch, cx:cx+cw]
        
        # Count non-zero pixels in the binarized quadrant
        non_zero_count = cv2.countNonZero(binary_quad)
        percentage_filled = (non_zero_count / (cw * ch)) * 100
        # print(f"Quadrant {i}: {percentage_filled:.2f}% filled")
        
        # If more than 40% black pixels (non-zero after inversion), consider it filled
        if percentage_filled > 40:
            filled_quadrants.append(i)
            # Draw a green rectangle around filled cells
            # cv2.rectangle(vis_image, (x+cx-margin, y+cy-margin), 
            #             (x+cx+cw+margin, y+cy+ch+margin), (0, 255, 0), 2)
        # else:
        #     # Draw a red rectangle around empty cells
        #     cv2.rectangle(vis_image, (x+cx-margin, y+cy-margin), 
        #                 (x+cx+cw+margin, y+cy+ch+margin), (0, 0, 255), 2)

    # Save the visualization
    # cv2.imwrite("account_number_visualization.jpg", vis_image)
    
    # convert the filled quadrants to binary
    filled_quadrants_binary = [1 if i in filled_quadrants else 0 for i in range(16)]
    # convert the binary to integer
    filled_quadrants_decimal = int("".join(map(str, filled_quadrants_binary)), 2)
    print(f"Filled quadrants (binary): {filled_quadrants_binary}")
    print(f"Filled quadrants (decimal): {filled_quadrants_decimal}")

    return filled_quadrants_decimal

def parse_form_image(image_path, form_type=None):
    # load the image, convert it to grayscale, blur it
    # slightly, then find edges
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Convert to pure black and white using adaptive thresholding
    binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                 cv2.THRESH_BINARY_INV, 11, 2)
    
    # Clean up the image to remove small noise
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    
    # Find all contours
    cnts = cv2.findContours(cleaned.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    # Sort contours by area in descending order
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    if form_type == "withdraw":
        aspect_min = 1.4
        aspect_max = 1.8
        black_ratio_min = 0.3
        black_ratio_max = 0.8
    else:
        aspect_min = 1.4
        aspect_max = 1.8
        black_ratio_min = 0.1
        black_ratio_max = 0.5

    # Look for the form (largest white rectangle with content)
    form_contour = None
    for c in cnts:
        # Approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        
        # Must be a quadrilateral
        if len(approx) != 4:
            continue
            
        # Get the bounding rectangle
        x, y, w, h = cv2.boundingRect(approx)
        
        # Check aspect ratio (approximately 5:8)
        aspect_ratio = w / float(h)
        # print(f"Aspect Ratio: {aspect_ratio:.2f}")
        if not (aspect_min <= aspect_ratio <= aspect_max):
            continue
            
        # Extract the ROI
        roi = binary[y:y+h, x:x+w]
        
        # The form should have significant content inside
        # Count the number of black pixels (form content)
        black_pixels = cv2.countNonZero(roi)
        total_pixels = w * h
        black_ratio = black_pixels / float(total_pixels)

        # print(f"Black Ratio: {black_ratio:.2f}")
        
        # The form should have between 10% and 50% black pixels
        # (too few means it's just white paper, too many means it's not a form)
        if black_ratio < black_ratio_min or black_ratio > black_ratio_max:
            continue
            
        # Found a good candidate
        form_contour = approx
        break

    if form_contour is None:
        print("No form found")
        return None

    # apply a four point perspective transform to both the
    # original image and grayscale image to obtain a top-down
    # birds eye view of the paper
    paper = four_point_transform(image, form_contour.reshape(4, 2))
    warped = four_point_transform(gray, form_contour.reshape(4, 2))

    # Convert warped image to pure black and white
    warped_binary = cv2.adaptiveThreshold(warped, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                        cv2.THRESH_BINARY_INV, 11, 2)
    
    # apply Otsu's thresholding method to binarize the warped
    # piece of paper
    form = cv2.threshold(warped_binary, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    
    (form_x, form_y, form_w, form_h) = cv2.boundingRect(form)
    
    # Initial contour detection
    account_number_contours, amount_box_contours, name_box_countours = detect_contours(form, form_w, form_h, form_type=form_type)

    # Check if form is upside down and rotate if needed
    needs_rotation = False
    
    # For account number forms, check if account numbers are in top 20%
    if len(account_number_contours) > 0:
        for contour in account_number_contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            if y > form_h * 0.2:  # If top of contour is below top 20%
                needs_rotation = True
                break
    
    # For open account form, check if name is in top 20%
    elif len(name_box_countours) > 0:
        for contour in name_box_countours:
            (x, y, w, h) = cv2.boundingRect(contour)
            if y > form_h * 0.2:  # If top of name box is below top 20%
                needs_rotation = True
                break
    
    if needs_rotation:
        print("Form is upside down, rotating...")
        # Rotate the images 180 degrees
        paper = cv2.rotate(paper, cv2.ROTATE_180)
        warped = cv2.rotate(warped, cv2.ROTATE_180)
        form = cv2.rotate(form, cv2.ROTATE_180)
        
        # Re-detect contours after rotation
        account_number_contours, amount_box_contours, name_box_countours = detect_contours(form, form_w, form_h)
    elif len(account_number_contours) > 0:
        print("Form is not upside down")

    # print("[INFO] countours found: ", len(account_number_contours))
    if (len(account_number_contours) > 0):
        print("[INFO] account number countours found: ", len(account_number_contours))
    if (len(amount_box_contours) > 0):
        print("[INFO] amount box countours found: ", len(amount_box_contours))
    if (len(name_box_countours) > 0):
        print("[INFO] name box countours found: ", len(name_box_countours))

    if (len(account_number_contours) == 0 and len(amount_box_contours) == 0 and len(name_box_countours) > 0):
        print("Found Open Account Form")
        name_path = "/home/admin/temp_name.jpg"
        write_image_for_contour(name_box_countours[0], warped, name_path)

        return FormInfo(FORM_OPEN_ACCOUNT, name_file_path=name_path)
    elif (len(account_number_contours) == 1 and len(amount_box_contours) == 0 and len(name_box_countours) == 0):
        print("Found Teller Form")
        account_num = find_account_number(account_number_contours[0], warped)
        print("Account Number: ", account_num)
        return FormInfo(FORM_TELLER, to_account_number=account_num)
    elif (len(account_number_contours) == 1 and len(amount_box_contours) >= 1 and len(name_box_countours) == 0):
        print("Found Deposit Form")
        account_num = find_account_number(account_number_contours[0], warped)
        amount_path = "/home/admin/temp_amount.jpg"
        write_image_for_contour(amount_box_contours[0], warped, amount_path)
        print("Account Number: ", account_num)
        return FormInfo(FORM_DEPOSIT, to_account_number=account_num, amount_file_path=amount_path)
    elif (len(account_number_contours) == 2 and len(amount_box_contours) >= 1 and len(name_box_countours) == 0):
        print("Found Transfer Form")
        if (cv2.boundingRect(account_number_contours[0])[0] < cv2.boundingRect(account_number_contours[1])[0]):
            sorted_account_number_contours = [account_number_contours[0], account_number_contours[1]]
        else:
            sorted_account_number_contours = [account_number_contours[1], account_number_contours[0]]
        from_account_num = find_account_number(sorted_account_number_contours[0], warped)
        to_account_num = find_account_number(sorted_account_number_contours[1], warped)
        amount_path = "/home/admin/temp_amount.jpg"
        write_image_for_contour(amount_box_contours[0], warped, amount_path)
        print("From Account Number: ", from_account_num, " To Account Number: ", to_account_num)
        return FormInfo(FORM_TRANSFER, from_account_number=from_account_num, to_account_number=to_account_num, amount_file_path=amount_path)
    elif (len(account_number_contours) == 1 and len(amount_box_contours) == 0 and len(name_box_countours) == 0):
        print("Found Withdraw Form")
        account_num = find_account_number(account_number_contours[0], warped)
        print("Account Number: ", account_num)
        return FormInfo(FORM_WITHDRAW, to_account_number=account_num)
    else:
        print("Form not recognized")
        return None

NUM_FORM_MATCHES = 3


class FormScanner(object):
    def __init__(self): 
        self.is_scanning = False
        self.callback = None
        self.scanning_callback = None
        self.camera = None
        self.reset_form_data()

    def reset_form_data(self):
        self.form_data = None
        self.form_match_count = 0

    def start_scanning(self, form_type = None, callback = None):
        self.callback = callback
        self.form_type = form_type
        if self.is_scanning and self.camera is not None:
            print("Already scanning")
            return
        self.is_scanning = True
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            raise Exception("Could not open video device")
        self.reset_form_data()

    def stop_scanning(self):
        self.is_scanning = False
        self.callback = None
        self.reset_form_data()
        if self.camera is not None and self.camera.isOpened():
            self.camera.release()
            self.camera = None
        cv2.destroyAllWindows()

    def update(self):
        if self.is_scanning:
            # Capture frame-by-frame
            ret, frame = self.camera.read()
            if not ret:
                print("Failed to grab frame")
                return
            
            # Save the frame temporarily
            temp_image = "/home/admin/temp_image.jpg"
            cv2.imwrite(temp_image, frame)
            
            # Try to parse the account number
            new_form_data = parse_form_image(temp_image, self.form_type)
            if new_form_data and (self.form_type == None or new_form_data.type == self.form_type):
                if self.form_data is not None and self.form_data.to_account_number == new_form_data.to_account_number and self.form_data.from_account_number == new_form_data.from_account_number:
                    self.form_match_count += 1
                    print(f"Detected account number: {new_form_data.to_account_number}")
                    if self.form_match_count >= NUM_FORM_MATCHES:
                        print(f"Accepting form")
                        if self.callback:
                            self.callback(new_form_data)
                        self.stop_scanning()
                        return
                else:
                    self.form_data = new_form_data
                    self.form_match_count = 0
                    print(f"Detected Form: {new_form_data.type} with account number: {new_form_data.to_account_number}")
            
            # Display the frame
            cv2.imshow('ATM Camera', frame)

def start():
    scanner = FormScanner()
    scanner.start_scanning()
    while True:
        scanner.update()
        time.sleep(0.1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    scanner.stop_scanning()
