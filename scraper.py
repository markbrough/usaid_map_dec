# This is a template for a Python scraper on Morph (https://morph.io)
# including some code snippets below that you should find helpful

# import scraperwiki
# import lxml.html
#
# # Read in a page
# html = scraperwiki.scrape("http://foo.com")
#
# # Find something on the page using css selectors
# root = lxml.html.fromstring(html)
# root.cssselect("div[align='left']")
#
# # Write out to the sqlite database using scraperwiki library
# scraperwiki.sqlite.save(unique_keys=['name'], data={"name": "susan", "occupation": "software developer"})
#
# # An arbitrary query against the database
# scraperwiki.sql.select("* from data where 'name'='peter'")

# You don't have to do things with the ScraperWiki and lxml libraries. You can use whatever libraries are installed
# on Morph for Python (https://github.com/openaustralia/morph-docker-python/blob/master/pip_requirements.txt) and all that matters
# is that your final data is written to an Sqlite database called data.sqlite in the current working directory which
# has at least a table called data.

import scraperwiki
from lxml import html
import urllib2
import re
import string
import json
import pprint

import os
if not 'MORPH_API_KEY' in os.environ:
  exit()
else:
  apikey=os.environ['MORPH_API_KEY']


pp = pprint.PrettyPrinter(indent=4)
URL = "https://api.morph.io/markbrough/usaid_test/data.json?key=%s&query=select public_name from 'data' limit 10 offset 10"
DEC_URL = "https://dec.usaid.gov/api/qsearch.ashx?q=%s&rtype=json"
TITLE_SEARCH = "(Documents.Document_Title:(%s))"

def fixdata(data):
    newdata = data.lstrip('(')
    newdata = newdata.rstrip(');')
    return newdata

req = urllib2.Request(URL % (apikey))
webfile = urllib2.urlopen(req)
data = webfile.read()

thedata = json.loads(fixdata(data))

for project in thedata:
    print project['public_name']
    query = TITLE_SEARCH % (project['public_name'])
    base64_query  = str(query.encode("base64"))
    print base64_query
    decreq = urllib2.Request(DEC_URL % (base64_query))
    decwebfile = urllib2.urlopen(decreq)
    decdata = decwebfile.read()
    thedecdata = decdata.read(json.loads(decdata))
    print len(thedecdata)
