
def pdf_merge(pdf_paths, output_path):
    """
    :param pdf_paths: pdf paths
    :param output_path: output path
    :return: output path
    """
    from PyPDF2 import PdfReader, PdfWriter
    pdf_writer = PdfWriter()
    for pdf_path in pdf_paths:
        pdf = PdfReader(pdf_path)
        for i in range(len(pdf.pages)):
            pdf_writer.add_page(pdf.pages[i])
    with open(output_path, "wb") as f:
        pdf_writer.write(f)
    return output_path