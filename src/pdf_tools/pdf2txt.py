import PyPDF2
from pdf2image import convert_from_path
import cv2
import os

def pdf_to_text_and_images(pdf_path, txt_path, img_dir):
    # Extract text from PDF
    with open(pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfFileReader(pdf_file)
        text = ''
        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            text += page.extractText()

    # Save text to txt file
    with open(txt_path, 'w') as txt_file:
        txt_file.write(text)

    # Convert PDF to images
    images = convert_from_path(pdf_path)

    # Save images to img_dir
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    for i, img in enumerate(images):
        img.save(os.path.join(img_dir, f'image_{i}.png'), 'PNG')