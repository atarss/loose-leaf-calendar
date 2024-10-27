import os
from glob import glob
import concurrent.futures

from tqdm import tqdm
import pdfkit

BASEDIR = os.path.realpath(".")
OUTPUT_DIR = BASEDIR + "/pdf"
WORKERS = 10

CONFIG = {
    'page-size': 'A5',
    'margin-top': '0.25in',
    'margin-right': '0.4in',
    'margin-bottom': '0.25in',
    'margin-left': '0.4in',
    'encoding': "UTF-8",
    'no-outline': None,
}

def foo(input_html_path):
    basename = os.path.basename(input_html_path)
    output_path = OUTPUT_DIR + "/" + basename + ".pdf"

    pdfkit.from_file(input_html_path, output_path, options=CONFIG)

def main():
    input_html_list = sorted(glob(BASEDIR + "/html/*.html"))
    cc = concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS)
    task_list = []
    for input_html_path in input_html_list:
        task_list.append(cc.submit(foo, input_html_path))

    for future in concurrent.futures.as_completed(task_list):
        pass

if __name__ == "__main__":
    main()
