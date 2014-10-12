from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen

import sys

html = urlopen(sys.argv[1]).read()
print html
