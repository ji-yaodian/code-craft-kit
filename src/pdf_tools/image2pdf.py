"""
image list to pdf
pip install pypdf
"""

import sys

from pypdf import PdfWriter, PageObject
from PIL import Image
import img2pdf


def image2pdf(image_path) -> str:
    """
    :param image: image path
    :return: pdf path
    """
    pdf_path = image_path.replace('.jpg', '.pdf')
    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert([image_path]))
    return pdf_path


if __name__ == '__main__':
    image_path = sys.argv[1]
    pdf_path = image2pdf(image_path)
    print(pdf_path)
