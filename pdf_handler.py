from tempfile import TemporaryDirectory, gettempdir
from os import path

import fitz


class file:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.pdf_document = fitz.open(self.pdf_path)

    def get_pages(self):
        pdf_pages = []
        for page_num in range(self.pdf_document.page_count):
            page = self.pdf_document.load_page(page_num)
            pdf_pages.append(page)
        return pdf_pages

    def to_images(self, resolution=300):
        for page_num in range(self.pdf_document.page_count):
            page = self.pdf_document.load_page(page_num)
            image = page.get_pixmap(
                matrix=fitz.Matrix(resolution / 72, resolution / 72)
            )
            image.save(f"{gettempdir()}/{page_num}.jpeg")

    def extract_page(self, page):
        file_name = path.basename(self.pdf_path).replace(".pdf", "")
        pdf_writer = fitz.open()
        pdf_writer.insert_pdf(self.pdf_document, from_page=page, to_page=page)
        pdf_writer.save(f"{file_name}-page-{page}-out.pdf")
        pdf_writer.close()

    def extract_array(self, new_pages):
        file_name = path.basename(self.pdf_path).replace(".pdf", "")
        file_dir = path.dirname(self.pdf_path)
        pdf_writer = fitz.open()
        for page in new_pages:
            pdf_writer.insert_pdf(self.pdf_document, from_page=page, to_page=page)
        pdf_writer.save(file_dir + f"/{file_name}-{len(new_pages)}-pages-out.pdf")
        pdf_writer.close()

    def close_document(self):
        self.pdf_document.close()
