#!/bin/bash

python3 generate-html.py
python3 convert.py
pdfunite pdf/*.pdf output.pdf
