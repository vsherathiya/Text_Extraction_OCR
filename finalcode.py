import os
import re
import cv2
import easyocr
import pytesseract

import numpy as np
from flask import Flask, request, render_template, redirect, url_for
from PIL import Image, ImageEnhance

app = Flask(__name__)


# Configure EasyOCR
reader = easyocr.Reader(['en'])

# Define the upload folder and allowed extensions
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with a strong secret key

# Define the square yard area calculation function
def calculate_area(dimensions):
    feet_inches_pattern = r'(\d{1,2})[\'\"]?\s?[-.]?\s?(\d{1,2})[\'\"]?"\s?[xX*]\s?(\d{1,2})[\'\"]?\s?[-.]?\s?(\d{1,2})[\'\"]?'
    match = re.match(feet_inches_pattern, dimensions)

    if match:
        feet1, inches1, feet2, inches2 = map(int, match.groups())
        total_inches = (feet1 * 12 + inches1) * (feet2 * 12 + inches2)
        sqft = total_inches / 144.0
        sqyd = sqft * 0.111111
        return round(sqyd)
    else:
        return None

# Function to process the uploaded image
def process_image(file_path):
    # Load the original image
    original_image = cv2.imread(file_path)
    darkness_factor = 1.25

    # Read the image with OpenCV
    image = cv2.imread(file_path)

    # Convert the OpenCV image to a Pillow image
    pillow_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Create an ImageEnhance object
    enhancer = ImageEnhance.Brightness(pillow_image)

    # Darken the image
    darkened_pillow_image = enhancer.enhance(darkness_factor)

    # Convert the darkened Pil  low image back to a NumPy array
    darkened_image = cv2.cvtColor(np.array(darkened_pillow_image), cv2.COLOR_RGB2BGR)

    # Perform text extraction
    result = reader.readtext(darkened_image)

    # Initialize a list to store extracted data and regions
    extracted_data = []

    # Define a regex pattern to match dimensions like "11'-0" x 13'-0" and square yard areas like "200 sq. yd"
    pattern = r'(\d{1,2}[\'\"]?\s?[-.]?\s?\d{1,2}[\'\"]?"\s?[xX*]\s?\d{1,2}[\'\"]?\s?[-.]?\s?\d{1,2}[\'\"]?)|(\d+\.?\d*)\s?sq\.?\s?yd'

    # Define an avoidance pattern to skip certain patterns during extraction
    avoid_pattern = r'^\d{4}\s?[*xX]\s?\d{4}$'

    # Iterate through the results of text extraction
    for detection in result:
        text = detection[1].strip()
        bbox = np.array(detection[0]).astype(int)

        # Replace 'A' with '4' for area calculation
        text = text.replace('A', '4')
        text = text.replace('o', '0')
        text = text.replace('O', '0')

        # Check if the text matches the desired pattern using regex
        match = re.search(pattern, text)

        if match:
            # If the match is a dimension pattern
            if match.group(1):
                # Calculate the square yard area
                dimensions = re.findall(r'(\d{1,2}[\'\"]?\s?[-.]?\s?\d{1,2}[\'\"]?"\s?[xX*]\s?\d{1,2}[\'\"]?\s?[-.]?\s?\d{1,2}[\'\"]?)', text)
                area = 1.0  # Default value
                if dimensions:
                    # Extract the dimensions and calculate the area
                    area = calculate_area(dimensions[0])

                extracted_data.append({'text': text, 'bbox': bbox, 'sqyd_area': area})

            # If the match is a square yard area pattern
            elif match.group(2):
                sqyd_area = float(match.group(2))
                extracted_data.append({'text': text, 'bbox': bbox, 'sqyd_area': sqyd_area})

        # Check if the text matches the avoidance pattern and skip it
        elif re.search(avoid_pattern, text):
            pass
        else:
            extracted_data.append({'text': text, 'bbox': bbox})

    # Create a copy of the original image for drawing boxes and text annotations
    output_image = original_image.copy()

    for data in extracted_data:
        bbox = data['bbox']
        x1, y1, x2, y2 = int(bbox[0][0]), int(bbox[0][1]), int(bbox[2][0]), int(bbox[2][1])
        text_to_write = data['text']

        # Calculate the background size to match the text
        (text_width, text_height), _ = cv2.getTextSize(text_to_write, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
        background_width = text_width + 10  # Add some padding
        background_height = text_height + 10
        background_color = (255, 255, 255)  # White background color
        font_color = (0, 0, 255)  # Red text color for square yard area
        cv2.rectangle(output_image, (x1, y1 - background_height), (x1 + background_width, y1), background_color, -1)
        cv2.putText(output_image, text_to_write, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.8, font_color, 2, cv2.LINE_AA, False)

    # Draw boxes and text for square yard area above the original text
    for data in extracted_data:
        bbox = data['bbox']
        x1, y1, x2, y2 = int(bbox[0][0]), int(bbox[0][1]), int(bbox[2][0]), int(bbox[2][1])
        text_to_write = data['text']

        if data.get('sqyd_area') is not None:
            # Calculate the background size to match the text
            (text_width, text_height), _ = cv2.getTextSize(text_to_write, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
            background_width = text_width + 5  # Add some padding
            background_height = text_height + 10
            background_color = (255, 255, 255)
            font_color = (0, 0, 255)  # Red text color

            # Calculate the coordinates for the rectangle
            rectangle_x1 = x1
            rectangle_y1 = y2  # Place the rectangle below the text
            rectangle_x2 = rectangle_x1 + background_width
            rectangle_y2 = rectangle_y1 + background_height

            # Draw the rectangle
            cv2.rectangle(output_image, (rectangle_x1, rectangle_y1), (rectangle_x2, rectangle_y2), background_color, -1)

            # Calculate the coordinates for the text
            text_x = x1   # Adjust the x-coordinate to leave some space inside the rectangle
            text_y = y2 + 30  # Adjust the y-coordinate for text position within the rectangle

            # Draw the text
            cv2.putText(output_image, f'SqYd: {data["sqyd_area"]:.2f}', (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, font_color, 2, cv2.LINE_AA, False)

    # Calculate the total square yard area
    total_sqyd_area = round(sum(data['sqyd_area'] for data in extracted_data if data.get('sqyd_area') is not None), 2)
    total_sqyd_text = f"Total Square Yard Area: {total_sqyd_area} sqyd (approx.)"

    # Create a copy of the enhanced image for adding the total area text
    output_image_with_total_area = output_image.copy()

    # Calculate the background size for the total area text
    (total_area_text_width, total_area_text_height), _ = cv2.getTextSize(total_sqyd_text, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 5)
    total_area_background_width = total_area_text_width + 40  # Add some padding
    total_area_background_height = total_area_text_height + 20
    total_area_background_color = (0, 0, 0)  # Black background color
    total_area_font_color = (255, 255, 255)  # White text color

    # Calculate the coordinates for the total area background
    total_area_x1 = 20  # Adjust as needed for horizontal placement
    total_area_y1 = 20  # Adjust as needed for vertical placement
    total_area_x2 = total_area_x1 + total_area_background_width
    total_area_y2 = total_area_y1 + total_area_background_height

    # Draw the total area background
    cv2.rectangle(output_image_with_total_area, (total_area_x1, total_area_y1), (total_area_x2, total_area_y2), total_area_background_color, -1)

    # Calculate the coordinates for the total area text
    total_area_text_x = total_area_x1 + 10  # Adjust for horizontal placement within the background
    total_area_text_y = total_area_y1 + 40  # Adjust for vertical placement within the background

    # Draw the total area text
    cv2.putText(output_image_with_total_area, total_sqyd_text, (total_area_text_x, total_area_text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, total_area_font_color, 5, cv2.LINE_AA, False)

    # Save the image with the total area text
    output_file_with_total_area = 'static/' + os.path.basename(file_path)  # Adjust the output file path as needed
    cv2.imwrite(output_file_with_total_area, output_image_with_total_area)

    return output_file_with_total_area, extracted_data



# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for the upload page
@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # Check if a file is provided
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        # Check if the file has an allowed extension
        if file and allowed_file(file.filename):
            # Save the uploaded image to the upload folder
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)

            # Process the uploaded image
            processed_image, extracted_data = process_image(filename)

            # Calculate the total square yard area
            total_sqyd_area = sum(data['sqyd_area'] for data in extracted_data if data.get('sqyd_area') is not None)
            print(filename)
            return render_template('result.html', uploaded_image_url=filename, masked_image_url=processed_image,
                                   matched_dimensions=extracted_data, total_sqyd_area=round(total_sqyd_area))

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(port=3000,debug=True)
