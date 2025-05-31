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

def center_window(window_name, image=None):
    """Center a named window on the screen based on the image dimensions.
    
    Args:
        window_name: The name of the window to center
        image: The image being displayed (optional), used to determine window dimensions
    """
    # Estimate screen resolution - adjust these values based on your target screen
    screen_width = 1920  # Default screen width
    screen_height = 1080  # Default screen height
    
    # If image is provided, use its dimensions, otherwise use default size
    if isinstance(image, np.ndarray):
        height, width = image.shape[:2]
    else:
        width, height = 640, 480  # Default window size
    
    # Calculate center position
    x_pos = (screen_width - width) // 2
    y_pos = (screen_height - height) // 2
    
    # Ensure window is not positioned off-screen
    x_pos = max(0, x_pos)
    y_pos = max(0, y_pos)
    
    # Set window to normal mode so it can be moved and resized
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.moveWindow(window_name, x_pos, y_pos)

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
    # Enhance contrast by normalizing to full range
    roi = cv2.normalize(roi, None, 0, 255, cv2.NORM_MINMAX)
    cv2.imwrite(path, roi)

def is_contour_contained(contour1, contour2, margin_percent=0.1):
    """Check if two contours overlap by checking if they share any area.
    
    Args:
        contour1: First contour to check
        contour2: Second contour to check
        margin_percent: Not used in this version
    """
    # Create a blank image to draw contours on
    img = np.zeros((1000, 1000), dtype=np.uint8)
    
    # Draw first contour
    cv2.drawContours(img, [contour1], -1, 255, -1)  # Fill first contour
    area1 = cv2.countNonZero(img)
    
    # Draw second contour
    cv2.drawContours(img, [contour2], -1, 255, -1)  # Fill second contour
    area2 = cv2.countNonZero(img)
    
    # If the total area is less than the sum of individual areas, they overlap
    return area2 < (area1 + cv2.contourArea(contour2))

def detect_contours(form, form_w, form_h, error_margin=0.2, form_type=None):
    """Helper function to detect contours in the form."""
    if form_type == "withdraw":
        account_number_size = (form_w * 2) // 3
        name_box_width = (form_w * 2) // 3
        name_box_height = form_h // 20
        amount_box_width = -1
        amount_box_height = -1
        min_area = name_box_width * name_box_height * 0.4
        error_margin = 0.2
        # print("Using custom parameters for withdraw form detection", 
        #       f"account_number_size: {account_number_size}, "
        #       f"name_box_width: {name_box_width}, name_box_height: {name_box_height}, "
        #       f"min_area: {min_area}")
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
        # print(f"Contour found with area: {area}, width: {w}, height: {h}, aspect ratio: {ar:.2f}")
        # debug_img = form.copy()
        # cv2.drawContours(debug_img, [c], -1, (0, 255, 0), 3)
        # cv2.imshow("Detected Form Contour", debug_img)
        # cv2.waitKey(500)  # Show for 0.5 seconds
        # cv2.destroyWindow("Detected Form Contour")
        
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
        elif len(approx) == 4 and abs(name_box_width - w) < error_margin * name_box_width and abs(name_box_height - h) < 5 * error_margin * name_box_height and 5 < ar <= 9:
            name_box_countours.append(c)

    return account_number_contours, amount_box_contours, name_box_countours

def find_account_number(area, grayscale_image, paper=None, form_type=None):
    # split into 16 quadrants
    # (4 rows, 4 columns)
    x, y, w, h = cv2.boundingRect(area)

    # trim off the outer edges
    x += int(w * .05)
    y += int(h * .05)
    w -= int(w * .1)
    h -= int(h * .1)

    # Extract the entire grid region
    grid_roi = grayscale_image[y:y+h, x:x+w]
    # Enhance contrast by normalizing to full range
    grid_roi = cv2.normalize(grid_roi, None, 0, 255, cv2.NORM_MINMAX)

    # cv2.imshow("Thresholded Grid", grid_roi)
    # center_window(f"Thresholded Grid", grid_roi)
    # cv2.waitKey(1000)  # Show for 1 second
    # cv2.destroyWindow("Thresholded Grid")
    
    # Enhanced preprocessing
    # 1. Apply bilateral filter to reduce noise while preserving edges
    grid_roi = cv2.bilateralFilter(grid_roi, 9, 75, 75)

    # cv2.imshow("Thresholded Grid", grid_roi)
    # center_window(f"Thresholded Grid", grid_roi)
    # cv2.waitKey(1000)  # Show for 1 second
    # cv2.destroyWindow("Thresholded Grid")
    
    # 2. Apply Gaussian blur to reduce noise
    grid_roi = cv2.GaussianBlur(grid_roi, (3, 3), 0)

    # cv2.imshow("Thresholded Grid", grid_roi)
    # center_window(f"Thresholded Grid", grid_roi)
    # cv2.waitKey(1000)  # Show for 1 second
    # cv2.destroyWindow("Thresholded Grid")
    
    # 3. Use simple thresholding with dynamic threshold value
    min_val = np.min(grid_roi)
    max_val = np.max(grid_roi)
    threshold = (int(min_val) + int(max_val)) // 2
    # print(f"Dynamic threshold: {threshold} (min: {min_val}, max: {max_val})")
    _, binary_grid = cv2.threshold(
        grid_roi,
        threshold,  # Dynamic threshold value
        255,  # Maximum value
        cv2.THRESH_BINARY_INV  # Invert so filled areas are white
    )

    # cv2.imshow("Thresholded Grid", binary_grid)
    # center_window("Thresholded Grid", binary_grid)
    # cv2.waitKey(1000)  # Show for 1 second
    # cv2.destroyWindow("Thresholded Grid")
    
    # 5. Clean up small artifacts using morphological operations
    kernel = np.ones((3,3), np.uint8)
    binary_grid = cv2.morphologyEx(binary_grid, cv2.MORPH_OPEN, kernel)
    binary_grid = cv2.morphologyEx(binary_grid, cv2.MORPH_CLOSE, kernel)
    
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
    # cv2.imshow("Thresholded Grid", binary_grid)
    # center_window(f"Thresholded Grid", binary_grid)
    # cv2.waitKey(1000)  # Show for 1 second
    # cv2.destroyWindow("Thresholded Grid")
    # # Visualize the grayscale image with cell contours
    # vis_grid = cv2.cvtColor(grid_roi, cv2.COLOR_GRAY2BGR)
    # for i, (cx, cy, cw, ch) in enumerate(cells):
    #     # Draw rectangle for each cell
    #     cv2.rectangle(vis_grid, (cx, cy), (cx + cw, cy + ch), (0, 255, 0), 2)
    #     # Add cell number
    #     cv2.putText(vis_grid, str(i), (cx + 5, cy + 20), 
    #                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    
    # cv2.imshow("Grid with Cell Contours", vis_grid)
    # cv2.waitKey(1000)  # Show for 1 second
    # cv2.destroyWindow("Grid with Cell Contours")

    # determine which quadrants are filled
    filled_quadrants = []
    for i, (cx, cy, cw, ch) in enumerate(cells):
        # Extract the cell from the already thresholded grid
        binary_quad = binary_grid[cy:cy+ch, cx:cx+cw]
        
        # Extract the cell from the original grayscale image
        grayscale_quad = grid_roi[cy:cy+ch, cx:cx+cw]
        
        # # Debug prints for pixel values
        # print(f"\nCell {i} stats:")
        # print(f"Grayscale min: {np.min(grayscale_quad)}, max: {np.max(grayscale_quad)}, mean: {np.mean(grayscale_quad):.2f}")
        # print(f"Binary unique values: {np.unique(binary_quad)}")
        
        # Count non-zero pixels in the binarized quadrant
        non_zero_count = cv2.countNonZero(binary_quad)
        percentage_filled = (non_zero_count / binary_quad.size) * 100
        # print(f"Cell {i}: {percentage_filled:.2f}% filled")
        
        # Create a side-by-side visualization of binary and grayscale
        # vis_quad = np.hstack((grayscale_quad, binary_quad))
        # cv2.imshow(f"Cell {i} - Grayscale | Binary", vis_quad)
        # center_window(f"Cell {i} - Grayscale | Binary", vis_quad)
        # cv2.waitKey(1000)  # Show for 0.1 seconds
        
        # If more than 40% black pixels (non-zero after inversion), consider it filled
        threshold = 60 if form_type == "withdraw" else 30
        if percentage_filled > 30:
            filled_quadrants.append(i)
            # Draw a green rectangle around filled cells
            # cv2.rectangle(vis_image, (x+cx-margin, y+cy-margin), 
            #             (x+cx+cw+margin, y+cy+ch+margin), (0, 255, 0), 2)
        # else:
        #     # Draw a red rectangle around empty cells
        #     cv2.rectangle(vis_image, (x+cx-margin, y+cy-margin), 
        #                 (x+cx+cw+margin, y+cy+ch+margin), (0, 0, 255), 2)
        
        # cv2.destroyWindow(f"Cell {i} - Grayscale | Binary")

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
    top = int(0.10 * h)
    bottom = int(0.84 * h)
    image = image[top:bottom, left:right]

    # cv2.imshow("Detected image", image)
    # cv2.waitKey(500)  # Show for 0.5 seconds
    # center_window("Detected image", image)
    # cv2.destroyWindow("Detected image")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Enhance contrast by normalizing to full range
    # gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
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

    if form_contour is None:
        print("No form contour detected.")
        return None

    # Apply a four-point perspective transform to get a top-down view of the paper
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
        return FormInfo(FORM_WITHDRAW, from_account_number=account_num, to_account_number=account_num)
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
        account_num = find_account_number(account_number_contours[0], warped, "withdraw")
        print("Account Number: ", account_num)
        return FormInfo(FORM_WITHDRAW, from_account_number=account_num, to_account_number=account_num)
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
        if form_type is "teller":
            form_type = "withdraw"
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
        try:
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
                if new_form_data and (self.form_type == None or new_form_data.type == self.form_type or (self.form_type == "withdraw" and new_form_data.type == FORM_TELLER)):
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
        except Exception as e:
            print(f"Error during scanning: {e}")

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