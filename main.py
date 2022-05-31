#!/usr/bin/env python
from os import system, mkdir, path

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


if __name__ == "__main__":
    pdf_path = "Blender 2.9 Shortcuts v1.1.pdf"

    temp_dir()
    pdf_to_img(pdf_path)


