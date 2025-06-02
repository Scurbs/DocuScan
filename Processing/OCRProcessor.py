import cv2
import pytesseract
import numpy as np
from pytesseract import Output
from settings import *

class OCRProcessor:
    def __init__(self, tesseract_path, base_path, config='--psm 6 --oem 3 eng+deu', debug_mode=None):
        self.tesseract_path = tesseract_path
        self.base_path = base_path
        self.config = config
        self.debug_mode = debug_mode
        self.search_terms= ["SCAN","SYS"]
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_path

    def load_image(self, image_path):
        return cv2.imread(image_path)

    def preprocess_image(self, img):
        """Preprocesses the image for OCR."""
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.GaussianBlur(img, (5, 5), 0)
        img = cv2.bilateralFilter(img, 9, 75, 75)
        kernel = np.ones((1, 1), np.uint8)
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
        return img
       
    def get_keyword_positions(self):
        """Searches for the keywords and returns the found keywords with their positions."""
        positions = {}
        for i, word in enumerate(self.data_image['text']):
            #print(word)
            for keyword in self.search_terms:
                if keyword.lower() in word.lower():
                    (x, y, w, h) = (self.data_image['left'][i], self.data_image['top'][i], self.data_image['width'][i], self.data_image['height'][i])
                    entry = f"{keyword}_{i}" 
                    positions[entry] = (x, y, w, h)
        
        if self.debug_mode == 1:
            for entry, (x, y, w, h) in positions.items():
                keyword = entry.split('_')[0]
                print(f"Keyword '{keyword}' found at position: {(x, y, w, h)}")
        elif self.debug_mode == 1:
            print(f'{RED}No keywords found{RESET}')
        
        return positions

    def extract_values(self, stamp_start_height, coordinates):
        """
        Extract values from the measuring stripes based on coordinates.
        """
        values = []
        image_height, image_width, _ = self.image.shape

        WIDTH_MULTIPLIER = 4.9  
        END_HEIGHT_MULTIPLIER = 0.02
        SHIFT_LEFT_RIGHT = 0.3  
        SHIFT_UP_DOWN = 0.01  

        x, y, width, height = coordinates

        x_start_roi = x - int(width * SHIFT_LEFT_RIGHT)
        x_end_roi = x + int(width * WIDTH_MULTIPLIER)
        y_start_roi = y - int(height * 7) - int(height * SHIFT_UP_DOWN)
        y_end_roi = stamp_start_height - int(stamp_start_height * END_HEIGHT_MULTIPLIER)

        x_start_roi = max(0, x_start_roi)
        x_end_roi = min(image_width, x_end_roi)
        y_start_roi = max(0, y_start_roi)
        y_end_roi = min(image_height, y_end_roi)

        if x_end_roi > x_start_roi and y_end_roi > y_start_roi:
            roi = self.image[y_start_roi:y_end_roi, x_start_roi:x_end_roi]
            if self.debug_mode == 1:
                print("image width is:", image_width, "| image height is:", image_height)
                print("x_start:", x_start_roi, "| y_start:", y_start_roi, "| x_end:", x_end_roi, "| y_end:", y_end_roi)
            values = pytesseract.image_to_string(roi, config=self.config)
            if self.debug_mode == 1:
                print(values)
        else:
            if self.debug_mode == 1:
                print(f"Skipping invalid ROI: x_start={x_start_roi}, x_end={x_end_roi}, y_start={y_start_roi}, y_end={y_end_roi}")

        return values
    
    def get_values_height(self,coordinates):
        sorted_coordinates = sorted(coordinates[0].items(), key=lambda item: item[1][0])

        x_threshold = 200

        y_distance_dict = {}
        for i in range(len(sorted_coordinates) - 1):
            key, (x, y, w, h) = sorted_coordinates[i]
            next_key, (next_x, next_y, next_w, next_h) = sorted_coordinates[i + 1]
            
            if next_x > x + x_threshold:
                
                y_distance_dict[key] = None
                
            else:
                y_distance = abs(next_y - y)
                y_distance_dict[key] = y_distance

        last_key = sorted_coordinates[-1][0]
        y_distance_dict[last_key] = None
        return(y_distance_dict)
    
    def process_image_for_ocr(self, image_path, page_count):
        """
        Extract all values from one page with multiple measuring stripes.
        """
        self.image = self.load_image(image_path)
        processed_image = self.preprocess_image(self.image)
        
        self.data_image = pytesseract.image_to_data(processed_image, lang='eng', output_type=Output.DICT,config=CONFIG_OCR)

        keywords = self.get_keyword_positions()

        
        #If a Keyword is "SYS" then its the Nullfiltertest
        if "SYS" in keywords.keys():
            empty_dict = {
                "Nullfilter": "SYSTEM",
                "Seite": page_count
            }
            empty_list = []
            return empty_list.append(empty_dict)
        
        #Methods are Recovery, Integral or Scanning
        value_stripes_list = []        
        for stripe_name, coordinates in keywords.items():
            x, y, width, height = coordinates
            stamp_start_height = self.get_stamp_start_height((x, y, width, height))
            
            if stamp_start_height is not None:
                value_stripe = self.extract_values(stamp_start_height, coordinates)
                stripe_dict = {
                    stripe_name: value_stripe,
                    "Seite": page_count
                }
                value_stripes_list.append(stripe_dict)
        
        if self.debug_mode == 1:
            print(value_stripes_list)
        
        return value_stripes_list
    
    def get_stamp_start_height(self,keyword_position):
        """Searches the image for the largest gap between two horizontal lines. Largest gap is where the stamp is located. Returns the height (y) of the starting point of the stamp.

        Args:
            image (image): Image to process
            keyword_position (dict): Contains the methods as keywords and its values

        Returns:
            max_start (int): Height of the stamp
        """
        # Extract coordinates and width from keyword_position
        x, y, width, height = keyword_position

        # Define the region to crop: x, y, width, and height
        crop_x_start = x
        crop_x_end = x + 2 * width
        crop_y_start = 0
        crop_y_end = self.image.shape[0]  # full height of the image

        # Ensure the crop coordinates are within the image dimensions
        crop_x_end = min(crop_x_end, self.image.shape[1])
        crop_y_end = min(crop_y_end, self.image.shape[0])

        # Crop the image based on the defined coordinates
        cropped_image = self.image[crop_y_start:crop_y_end, crop_x_start:crop_x_end]

        # Convert cropped image to grayscale
        gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

        # Apply binary thresholding
        _, binary_image = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

        # Calculate horizontal projection profile
        horizontal_projection = np.sum(binary_image, axis=1)

        # Threshold the projection profile to find text lines
        threshold = 50  # Adjust based on your image
        line_indices = np.where(horizontal_projection > threshold)[0]

        # Group continuous lines into text blocks
        lines = []
        start_idx = None

        for i in range(len(line_indices) - 1):
            if start_idx is None:
                start_idx = line_indices[i]
            
            if line_indices[i + 1] - line_indices[i] > 1:
                lines.append((start_idx, line_indices[i]))
                start_idx = None

        # Append the last detected line
        if start_idx is not None:
            lines.append((start_idx, line_indices[-1]))

        # Find the block with the highest height
        max_height = 0
        max_block = None

        for (start, end) in lines:
            height = end - start
            if height > max_height:
                max_height = height
                max_block = (start, end)

        if max_block is not None:
            max_start, max_end = max_block
            max_height = max_end - max_start
            
            #cv2.rectangle(cropped_image, (0, max_start), (cropped_image.shape[1], max_end), (0, 0, 255), 2)
            # cv2.namedWindow("Detected Text Lines", cv2.WINDOW_NORMAL)
            # cv2.resizeWindow("Detected Text Lines", 600, 800)
            # cv2.imshow("Detected Text Lines", cropped_image)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            # Return the start position of the block with the highest height in the cropped image
            #sprint("Start Block at height: ", max_start)
            return max_start
        else:
            if self.debug_mode == 1:
                print("No text blocks detected.")
 

