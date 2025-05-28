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

ROOT_SAVE_PATH = "./"

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

def is_contour_contained(inner_contour, outer_contour, margin_percent=0.1):
    """Check if inner_contour is contained within outer_contour by checking if each corner
    is within margin_percent of the outer contour's boundaries.
    
    Args:
        inner_contour: The contour to check if it's contained
        outer_contour: The contour to check against
        margin_percent: The percentage of the outer contour's dimensions to use as margin (default 10%)
    """
    # Get the corners of the inner contour
    peri = cv2.arcLength(inner_contour, True)
    inner_corners = cv2.approxPolyDP(inner_contour, 0.02 * peri, True)
    
    # Get the bounding rectangle of the outer contour
    x2, y2, w2, h2 = cv2.boundingRect(outer_contour)
    
    # Calculate margins
    x_margin = int(w2 * margin_percent)
    y_margin = int(h2 * margin_percent)
    
    # Check if each corner of the inner contour is within the outer contour's bounds
    for corner in inner_corners:
        x, y = corner[0]
        # Check if the point is within margin_percent of the outer contour's boundaries
        if (abs(x - x2) > x_margin and 
            abs(x - (x2 + w2)) > x_margin and 
            abs(y - y2) > y_margin and 
            abs(y - (y2 + h2)) > y_margin):
            return False
    
    return True

def detect_contours(form, form_w, form_h, error_margin=0.2, form_type=None):
    """Helper function to detect contours in the form."""
    if form_type == "withdraw":
        account_number_size = (form_w * 2) // 3
        name_box_width = (form_w * 2) // 3
        name_box_height = form_h // 20
        amount_box_width = -1
        amount_box_height = -1
        min_area = name_box_width * name_box_height * 0.5
        error_margin = 0.1
    else:
        account_number_size = form_w // 3
        name_box_width = (form_w * 2) // 3
        name_box_height = form_h // 10
        amount_box_width = form_w // 3
        amount_box_height = form_h // 10
        min_area = amount_box_width * amount_box_height * 0.5

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
        area = cv2.contourArea(approx)
        if area < min_area:
            continue
        debug_img = form.copy()
        cv2.drawContours(debug_img, [c], -1, (0, 255, 0), 3)
        cv2.imshow("Detected Form Contour", debug_img)
        cv2.waitKey(500)  # Show for 0.5 seconds
        cv2.destroyWindow("Detected Form Contour")
        
        if len(approx) == 4 and abs(account_number_size - w) < error_margin * account_number_size and abs(account_number_size - h) < error_margin * account_number_size and ar >= 0.8 and ar <= 1.2:
            # Check if this contour is contained within any existing account number contours
            is_contained = False
            for existing_contour in account_number_contours:
                if is_contour_contained(c, existing_contour):
                    print(f"Skipping Contour is contained within an existing account number contour")
                    is_contained = True
                    break
            
            if not is_contained:
                print(f"Found account number contour")
                account_number_contours.append(c)
        elif amount_box_width > 0 and len(approx) == 4 and abs(amount_box_width - w) < error_margin * amount_box_width and abs(amount_box_height - h) < error_margin * amount_box_height and ar > 3 and ar <= 5:
            amount_box_contours.append(c)
        elif len(approx) == 4 and abs(name_box_width - w) < error_margin * name_box_width and abs(name_box_height - h) < error_margin * name_box_height and 7 < ar <= 9:
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
    
    # Enhanced preprocessing
    # 1. Apply bilateral filter to reduce noise while preserving edges
    grid_roi = cv2.bilateralFilter(grid_roi, 9, 75, 75)
    
    # 2. Enhance contrast using CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    grid_roi = clahe.apply(grid_roi)
    
    # 3. Apply Gaussian blur to reduce noise
    grid_roi = cv2.GaussianBlur(grid_roi, (3, 3), 0)
    
    # 4. Use adaptive thresholding with larger block size and constant
    binary_grid = cv2.adaptiveThreshold(
        grid_roi,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        21,  # Larger block size
        10   # Larger constant
    )
    
    # 5. Clean up small artifacts using morphological operations
    kernel = np.ones((3,3), np.uint8)
    binary_grid = cv2.morphologyEx(binary_grid, cv2.MORPH_OPEN, kernel)
    binary_grid = cv2.morphologyEx(binary_grid, cv2.MORPH_CLOSE, kernel)
    
    # 6. Remove very small connected components
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_grid, connectivity=8)
    min_size = 50  # Minimum size of connected component to keep
    binary_grid = np.zeros_like(binary_grid)
    for i in range(1, num_labels):  # Skip background (0)
        if stats[i, cv2.CC_STAT_AREA] >= min_size:
            binary_grid[labels == i] = 255

    # Create a copy of the grayscale image for visualization
    vis_image = cv2.cvtColor(grayscale_image, cv2.COLOR_GRAY2BGR)
    
    # Show the thresholded grid in the visualization
    vis_grid = cv2.cvtColor(binary_grid, cv2.COLOR_GRAY2BGR)
    vis_image[y:y+h, x:x+w] = vis_grid

    num_rows, num_cols = 4, 4
    cell_width = w // num_cols
    cell_height = h // num_rows

    # Calculate margins to avoid grid lines
    margin = int(min(cell_width, cell_height) * 0.18)  # 18% margin

    cells = []
    for row in range(num_rows):
        for col in range(num_cols):
            cell_x = col * cell_width + margin
            cell_y = row * cell_height + margin
            cell_w = cell_width - 2 * margin
            cell_h = cell_height - 2 * margin
            cell = (cell_x, cell_y, cell_w, cell_h)
            cells.append(cell)

    # Display the thresholded image
    cv2.imshow("Thresholded Grid", binary_grid)
    cv2.waitKey(1000)  # Show for 1 second
    cv2.destroyWindow("Thresholded Grid")
    # Visualize the grayscale image with cell contours
    vis_grid = cv2.cvtColor(grid_roi, cv2.COLOR_GRAY2BGR)
    for i, (cx, cy, cw, ch) in enumerate(cells):
        # Draw rectangle for each cell
        cv2.rectangle(vis_grid, (cx, cy), (cx + cw, cy + ch), (0, 255, 0), 2)
        # Add cell number
        cv2.putText(vis_grid, str(i), (cx + 5, cy + 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    
    cv2.imshow("Grid with Cell Contours", vis_grid)
    cv2.waitKey(1000)  # Show for 1 second
    cv2.destroyWindow("Grid with Cell Contours")

    # determine which quadrants are filled
    filled_quadrants = []
    for i, (cx, cy, cw, ch) in enumerate(cells):
        # Extract the cell from the already thresholded grid
        binary_quad = binary_grid[cy:cy+ch, cx:cx+cw]
        
        # Visualize the binary quadrant
        # cv2.imshow(f"Binary Quadrant {i}", binary_quad)
        # cv2.waitKey(100)  # Show for 0.1 seconds
        
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
            # Draw a red rectangle around empty cells
            # cv2.rectangle(vis_image, (x+cx-margin, y+cy-margin), 
            #             (x+cx+cw+margin, y+cy+ch+margin), (0, 0, 255), 2)
        
        # cv2.destroyWindow(f"Binary Quadrant {i}")

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
    # cv2.imshow("orginal image", image)
    # cv2.waitKey(500)  # Show for 0.5 seconds
    # cv2.destroyWindow("orginal image")
    # Crop 20% from left/right and 10% from top/bottom
    h, w = image.shape[:2]
    left = int(0.14 * w)
    right = int(0.85 * w)
    top = int(0.18 * h)
    bottom = int(0.87 * h)
    image = image[top:bottom, left:right]

    # cv2.imshow("Detected image", image)
    # cv2.waitKey(500)  # Show for 0.5 seconds
    # cv2.destroyWindow("Detected image")

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

    # --- Improved Form Detection ---
    # Use Canny edge detection for better contour detection
    edges = cv2.Canny(blurred, 50, 150)
    kernel = np.ones((5, 5), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=2)
    edges = cv2.erode(edges, kernel, iterations=1)

    # Find contours from edges
    canny_cnts = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    canny_cnts = imutils.grab_contours(canny_cnts)
    canny_cnts = sorted(canny_cnts, key=cv2.contourArea, reverse=True)

    form_contour = None
    image_area = image.shape[0] * image.shape[1]
    for c in canny_cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = w / float(h)
            area = cv2.contourArea(approx)
            # print("contour area: ", area, " aspect ratio: ", aspect_ratio, "min image area: ", 0.1 * image_area)
            if area < (0.1 * image_area):
                continue
            # debug_img = image.copy()
            # cv2.drawContours(debug_img, [c], -1, (0, 255, 0), 3)
            # cv2.imshow("Detected Contour", debug_img)
            # cv2.waitKey(500)  # Show for 0.5 seconds
            # cv2.destroyWindow("Detected Contour")
            # Check aspect ratio and area (form should be large and roughly rectangular)
            # if 1.2 < aspect_ratio < 1.8 and area > 0.1 * image_area:
            form_contour = approx
            break

    # Debug visualization: draw detected contour
    # if form_contour is not None:
    #     debug_img = image.copy()
    #     cv2.drawContours(debug_img, [form_contour], -1, (0, 255, 0), 3)
    #     cv2.imshow("Detected Form Contour", debug_img)
    #     cv2.waitKey(500)  # Show for 0.5 seconds
    #     cv2.destroyWindow("Detected Form Contour")
    # If not found, fallback to old method
    # if form_contour is None:
    #     # Old method: adaptive thresholding and area/black ratio checks
    #     for c in cnts:
    #         peri = cv2.arcLength(c, True)
    #         approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    #         if len(approx) != 4:
    #             continue
    #         x, y, w, h = cv2.boundingRect(approx)
    #         aspect_ratio = w / float(h)
    #         if not (aspect_min <= aspect_ratio <= aspect_max):
    #             continue
    #         roi = binary[y:y+h, x:x+w]
    #         black_pixels = cv2.countNonZero(roi)
    #         total_pixels = w * h
    #         black_ratio = black_pixels / float(total_pixels)
    #         if black_ratio < black_ratio_min or black_ratio > black_ratio_max:
    #             continue
    #         form_contour = approx
    #         break

    if form_contour is None:
        print("No form found")
        return None

    # apply a four point perspective transform to both the
    # original image and grayscale image to obtain a top-down
    # birds eye view of the paper
    paper = four_point_transform(image, form_contour.reshape(4, 2))
    warped = four_point_transform(gray, form_contour.reshape(4, 2))

    # Convert warped image to pure black and white
    # Apply median blur to remove salt-and-pepper noise
    warped_denoised = cv2.medianBlur(warped, 3)
    
    # Apply adaptive thresholding with adjusted parameters
    warped_binary = cv2.adaptiveThreshold(warped_denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                        cv2.THRESH_BINARY_INV, 15, 5)
    
    # Clean up small noise using morphological operations
    kernel = np.ones((2,2), np.uint8)
    warped_binary = cv2.morphologyEx(warped_binary, cv2.MORPH_OPEN, kernel)
    warped_binary = cv2.morphologyEx(warped_binary, cv2.MORPH_CLOSE, kernel)
    
    # apply Otsu's thresholding method to binarize the warped
    # piece of paper
    form = cv2.threshold(warped_binary, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    
    (form_x, form_y, form_w, form_h) = cv2.boundingRect(form)
    
    # Initial contour detection
    account_number_contours, amount_box_contours, name_box_countours = detect_contours(form, form_w, form_h, form_type=form_type)

    # Check if form is upside down and rotate if needed
    needs_rotation = False
    
    # For account number forms, check if account numbers are in top 20%
    if len(account_number_contours) > 0 and form_type != "withdraw":
        for contour in account_number_contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            if y > form_h * 0.2:  # If top of contour is below top 20%
                needs_rotation = True
                break
    
    # For open account form, check if name is in top 20%
    elif len(name_box_countours) > 0:
        for contour in name_box_countours:
            (x, y, w, h) = cv2.boundingRect(contour)
            if (form_type == "withdraw" and y < form_h * 0.5) or (form_type != "withdraw" and y > form_h * 0.5):  # If top of name box is below top 50%
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
        name_path = f"{ROOT_SAVE_PATH}temp_name.jpg"
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
        amount_path = f"{ROOT_SAVE_PATH}temp_amount.jpg"
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
        amount_path = f"{ROOT_SAVE_PATH}temp_amount.jpg"
        write_image_for_contour(amount_box_contours[0], warped, amount_path)
        print("From Account Number: ", from_account_num, " To Account Number: ", to_account_num)
        return FormInfo(FORM_TRANSFER, from_account_number=from_account_num, to_account_number=to_account_num, amount_file_path=amount_path)
    elif (len(account_number_contours) == 1 and len(amount_box_contours) == 0 and len(name_box_countours) == 1):
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
            temp_image = f"{ROOT_SAVE_PATH}temp_image.jpg"
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
            # cv2.imshow('ATM Camera', frame)

def start():
    scanner = FormScanner()
    scanner.start_scanning() # 'withdraw'
    while True:
        scanner.update()
        time.sleep(0.1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    scanner.stop_scanning()


# start()