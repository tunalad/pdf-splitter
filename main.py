#!/usr/bin/env python
from os import system, mkdir, path

import pdf_handler


def temp_dir():
    try:
        mkdir(path.join(".", "tempfiles"))
    except OSError as e:
        print(e)


if __name__ == "__main__":
    pdf_path = "Blender 2.9 Shortcuts v1.1.pdf"

    pdf = pdf_handler.file(pdf_path)
    pages = pdf.get_pages()

    pdf.to_images()
    pdf.extract_page(pages, 0)
    pdf.extract_array(pages, [0, 2, 4])

    system("notify-send 'process finished with exit code 0'")
