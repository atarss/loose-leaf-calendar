#!/usr/bin/env python3

from datetime import datetime, timedelta
from tabulate import tabulate
import numpy as np

YEAR = 2025
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Note"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


OUTPUT_DIR = "./html/"

BLANK_HTML = "<html><body></body></html>"

def generate_html_page(canvas, header, title, mode):
    html_str = "<html><head>\n"
    html_str += '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">'
    html_str += "<style>"

    # add style here
    html_str += """
table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
}
table {
    width: 98%;
    height: 90%;
}
td {
    text-align: left;
    vertical-align: top;
    font-size: x-large;
}
th {
    text-align: center;
    width: 24%;
    height: 16px;
    vertical-align: top;
}
"""
    html_str += "</style></head>\n"
    html_str += "<body>\n"

    html_content = generate_table_html_from_inside(canvas, header, title, mode)
    html_str += html_content
    html_str += "</body></html>"

    return html_str


def generate_table_html_from_inside(canvas, header, title, mode):
    h, w = canvas.shape

    html_str = ""
    html_str += "<h2>{}</h2>\n".format(title)
    html_str += "<table>"

    # build header
    html_str += "<tr>"
    for i in header:
        html_str += "<th>{}</th>".format(i)
    html_str += "</tr>\n"

    # build content
    for h_idx in range(h):
        html_str += "<tr>"
        for w_idx in range(w):
            table_content = canvas[h_idx, w_idx]
            if table_content == 0:
                table_content = "&nbsp;"
            table_content = str(table_content)

            style_str = ""
            if mode == "right" and w_idx == 3 and ( 0 <= h_idx < h - 1) :
                style_str += "border-bottom: none; "
            if mode == "right" and w_idx == 3 and ( 1 <= h_idx < h ) :
                style_str += "border-top: none; "

            html_str += "<td style='{}'><p>{}</p></td>".format(style_str, table_content)
        html_str += "</tr>"
        html_str += "\n"
    html_str += "</table>"

    return html_str

def main():
    # generate blank HTML
    with open(OUTPUT_DIR + "/00.blank.html", "w") as f:
        print(BLANK_HTML, file=f)

    for month in range(1, 13):
        this_date = datetime.fromisoformat("{}-{:02d}-01".format(YEAR, month))
        start_point = this_date.weekday()

        canvas = np.zeros((6, 8), "uint8")

        while this_date.month == month:
            this_day = this_date.day  # range 1 - 31, so need to -1 when calculating position
            h = (this_day + start_point - 1) // 7
            w = (this_day + start_point - 1) - 7 * h

            canvas[h, w] = this_day
            this_date = this_date + timedelta(days=1)

        for _ in range(2):
            if sum(canvas[-1]) == 0: canvas = canvas[:-1]

        print(YEAR, month)
        left_page_canvas = canvas[:, :4]
        html_content = generate_html_page(left_page_canvas, WEEKDAYS[:4], str(month) + " - " + MONTHS[month-1], "left")
        with open(OUTPUT_DIR + "{:02d}.left.html".format(month), "w") as f:
            print(html_content, file=f)
        right_page_canvas = canvas[:, 4:]
        html_content = generate_html_page(right_page_canvas, WEEKDAYS[4:], "&nbsp;", "right")
        with open(OUTPUT_DIR + "{:02d}.right.html".format(month), "w") as f:
            print(html_content, file=f)

if __name__ == "__main__":
    main()
