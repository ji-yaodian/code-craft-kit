

def pdf_split(pdf_path, output_dir):
    """
    :param pdf_path: pdf path
    :param output_dir: output dir
    :return: pdf path
    """
    from PyPDF2 import PdfReader, PdfWriter
    import os
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    pdf = PdfReader(pdf_path)
    for i in range(len(pdf.pages)):
        writer = PdfWriter()
        writer.add_page(pdf.pages[i])
        writer.write(os.path.join(output_dir, f"{i}.pdf"))