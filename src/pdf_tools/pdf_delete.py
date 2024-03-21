
def pdf_delete(pdf_path, page_numbers):
    """
    :param pdf_path: pdf path
    :param page_numbers: page numbers
    :return: pdf path
    """
    from PyPDF2 import PdfReader, PdfWriter
    pdf = PdfReader(pdf_path)
    writer = PdfWriter()
    for i in range(len(pdf.pages)):
        if i not in page_numbers:
            writer.add_page(pdf.pages[i])
    with open(pdf_path, "wb") as f:
        writer.write(f)
    return pdf_path