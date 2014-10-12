import cStringIO
import codecs
import csv
import sys

from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

def parse_html_from_url(url):
    html = urlopen(url).read()
    return BeautifulSoup(html)

def write_csv_for_each_table_in_html(html):
    for i, table in enumerate(html("table")):
        with open("table_{}.csv".format(i), "wb") as csvfile:
            writer = UnicodeWriter(csvfile)
            for row in table("tr"):
                writer.writerow([column.text for column in row("td")])

if __name__ == "__main__":
    url = sys.argv[1]
    html = parse_html_from_url(url)
    write_csv_for_each_table_in_html(html)
