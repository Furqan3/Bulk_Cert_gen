import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.colors import white, black
from reportlab.lib.utils import ImageReader
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
import io
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the CSV file
csv_path = 'output.csv'  # Replace 'output.csv' with your CSV file containing member data
if not os.path.exists(csv_path):
    logging.error(f"CSV file not found: {csv_path}")
    exit(1)

df = pd.read_csv(csv_path)

# Create the 'certificates' folder if it doesn't exist
certificates_dir = 'certificates'
if not os.path.exists(certificates_dir):
    os.makedirs(certificates_dir)

# Path to the certificate template
template_path = 'Certificate.png'
if not os.path.exists(template_path):
    logging.error(f"Certificate template not found: {template_path}")
    exit(1)

# Path to the font file
font_path = 'Fontt/Montserrat-SemiBold.ttf'
if not os.path.exists(font_path):
    logging.error(f"Font file not found: {font_path}")
    exit(1)

# Function to create a certificate
def create_certificate(name, category, output_path):
    try:
        # Open the PNG image
        template_image = Image.open(template_path)
        image_width, image_height = template_image.size

        # Convert the image to PDF
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=(image_width, image_height))  # Set canvas size same as image
        pdfmetrics.registerFont(TTFont('Montserrat-Bold', font_path))

        # Draw the template image onto the canvas
        can.drawImage(ImageReader(template_image), 0, 0, width=image_width, height=image_height)

        # Define the border dimensions
        border_x = 915
        border_y = 1160-280
        border_width = 2790 - 915
        border_height = 1335 - 1160

        # Draw the border with 0% opacity
        can.setStrokeColor(black)
        can.setFillColor(black)
        can.rect(border_x, border_y, border_width, border_height, stroke=0, fill=0)  # Set fillOpacity to 0 for 0% opacity

        # Format the text
        text = f"{name} ({category})"

        # Define the position and style of the text
        font_size = 80  # Initial font size
        max_font_size = 80  # Maximum font size
        min_font_size = 20  # Minimum font size

        while font_size >= min_font_size:
            text_width = pdfmetrics.stringWidth(text, "Montserrat-Bold", font_size)
            if text_width <= border_width - 20:  # Leave some margin within the border
                break
            font_size -= 2  # Decrease the font size

        # Calculate the position to center the text within the border
        name_x = border_x + (border_width - text_width) / 2
        name_y = border_y + (border_height / 2) - (font_size / 4)

        # Set the font and size for the text
        can.setFont("Montserrat-Bold", font_size)
        can.setFillColor(white)
        can.drawString(name_x, name_y, text)

        # Save the canvas with the drawn text
        can.save()

        # Move to the beginning of the BytesIO buffer
        packet.seek(0)

        # Read the canvas as a new PDF
        new_pdf = PdfReader(packet)

        # Create a new PDF writer
        output_pdf = PdfWriter()

        # Add the page with the template and the text
        output_pdf.add_page(new_pdf.pages[0])

        # Save the new PDF to the output path
        with open(output_path, 'wb') as output_file:
            output_pdf.write(output_file)

        logging.info(f"Certificate created for {name} in category {category}")

    except Exception as e:
        logging.error(f"Failed to create certificate for {name} in category {category}: {e}")

# Iterate over each row in the CSV file
for index, row in df.iterrows():
    try:
        name = row['members']  # Assuming the column name for member names is 'members', modify accordingly
        category = row['category']  # Assuming the column name for categories is 'category', modify accordingly

        # Replace slashes with underscores in category name
        category = category.replace('/', '_')

        # Create a folder for the category if it doesn't exist
        category_folder = os.path.join(certificates_dir, category)
        if not os.path.exists(category_folder):
            os.makedirs(category_folder)

        # Generate the output path for the certificate
        output_path = os.path.join(category_folder, f"{name}_{category}.pdf")

        # Create the certificate
        create_certificate(name, category, output_path)

    except KeyError as e:
        logging.error(f"Missing column in CSV: {e}")
    except Exception as e:
        logging.error(f"Failed to process row {index}: {e}")

logging.info("Certificates have been created.")
