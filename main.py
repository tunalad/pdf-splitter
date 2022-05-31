#!/usr/bin/env python
from os import system, mkdir, path
from pprint import pprint

from PyPDF2 import PdfFileReader, PdfFileWriter
from pdf2image import convert_from_path


def temp_dir():
    try:
        mkdir(path.join(".", "tempfiles"))
    except OSError as e:
        print(e)


def pdf_to_img(pdf_path):
    pdf_icons = convert_from_path(pdf_path, 50)
    for icon in pdf_icons:
        icon.save(f"tempfiles/{icon}-out.jpeg", "JPEG")


def pdf_extract_page(all_pages, page):
    pdf_writer = PdfFileWriter()

    pdf_writer.addPage(all_pages[page])

    pdf_out = open(f"page-{page}-out.pdf", "wb")
    pdf_writer.write(pdf_out)

    pdf_out.close()


def pdf_extract_array(all_pages, new_pages):
    pdf_writer = PdfFileWriter()

    for i in new_pages:
        pdf_writer.addPage(all_pages[i])

    pdf_out = open(f"{len(new_pages)}-pages-out.pdf", "wb")
    pdf_writer.write(pdf_out)
    pdf_out.close()


if __name__ == "__main__":
    pdf_path = "Blender 2.9 Shortcuts v1.1.pdf"
    pdf_in = open(pdf_path, "rb")
    pdf_reader = PdfFileReader(pdf_in)

    # temp_dir()
    # pdf_to_img(pdf_path)

    # add pages to an array
    pdf_pages = []
    for page in range(pdf_reader.numPages):
        pdf_pages.append(pdf_reader.getPage(page))

    # page
    pdf_extract_page(pdf_pages, 0)

    # pages
    pdf_selected = [0, 2, 4]
    pdf_extract_array(pdf_pages, pdf_selected)


    pdf_in.close()
    system("notify-send 'process finished with exit code 0'")
