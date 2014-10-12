import sys

from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
from unicodewriter import UnicodeWriter

def parse_html_from_url(url):
    html = urlopen(url).read()
    return BeautifulSoup(html)

def write_csv_for_each_table_in_the_html(html):
    for i, table in enumerate(html("table")):
        with open("table_{}.csv".format(i), "wb") as csvfile:
            writer = UnicodeWriter(csvfile)
            for row in table("tr"):
                writer.writerow([column.text for column in row("td")])

if __name__ == "__main__":
    url = sys.argv[1]
    html = parse_html_from_url(url)
    write_csv_for_each_table_in_the_html(html)
