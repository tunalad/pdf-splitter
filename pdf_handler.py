#!/usr/bin/env python
from tempfile import TemporaryDirectory, gettempdir
from os import path

from PyPDF2 import PdfFileReader, PdfFileWriter
from pdf2image import convert_from_path


class file():
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

        # self.pdf_path = "Blender 2.9 Shortcuts v1.1.pdf"

        self.pdf_in = open(pdf_path, "rb")
        print(path.dirname(pdf_path))
        self.pdf_reader = PdfFileReader(self.pdf_in)

    def get_pages(self):
        pdf_pages = []
        for page in range(self.pdf_reader.numPages):
            pdf_pages.append(self.pdf_reader.getPage(page))
        return pdf_pages

    def to_images(self):
        pdf_icons = convert_from_path(self.pdf_path, 50)
        for icon in range(len(pdf_icons)):
            pdf_icons[icon].save(f"{gettempdir()}/{icon}.jpeg", "JPEG")

    def extract_page(self, all_pages, page):
        file_name = path.basename(self.pdf_path).replace(".pdf", "")
        pdf_writer = PdfFileWriter()

        pdf_writer.addPage(all_pages[page])

        pdf_out = open(f"{file_name}-page-{page}-out.pdf", "wb")
        pdf_writer.write(pdf_out)

        pdf_out.close()

    def extract_array(self, all_pages, new_pages):
        file_name = path.basename(self.pdf_path).replace(".pdf", "")
        file_dir = path.dirname(self.pdf_path)
        pdf_writer = PdfFileWriter()

        for i in new_pages:
            pdf_writer.addPage(all_pages[i])

        pdf_out = open(file_dir + f"/{file_name}-{len(new_pages)}-pages-out.pdf", "wb")
        pdf_writer.write(pdf_out)
        pdf_out.close()
