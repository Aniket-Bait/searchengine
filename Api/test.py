from pprint import pprint

from lxml import html
from lxml import etree
import requests

from bs4 import BeautifulSoup

xmlDict = {}
url_data = requests.get("https://capec.mitre.org/sitemap.html")
url = requests.get("https://nvd.nist.gov/vuln/data-feeds#JSON_FEED")

data = url_data.text

# soup = BeautifulSoup(data, "html.parser")
soup = BeautifulSoup(url.text, "html.parser")
nvd_data = soup.findAll("table", {"class": "xml-feed-table table table-striped table-condensed"})
for i in nvd_data:
    print(i)
# sitemapTags = soup.findAll("table", {"class": "sitemap"})

# for sitemap in sitemapTags:
#     # print(sitemap)

# doc = html.document_fromstring(url_data)
# title_element = doc.xpath("//title")
# website_title = title_element[0].text_content().strip()
# meta_description_element = doc.xpath("//meta")
# website_meta_description = meta_description_element[0].text_content().strip()
# print("title: ",website_title)
# print("meta: ",website_meta_description)

# root = etree.fromstring(url_data.content)
# for sitemap in root:
#     children = sitemap.getchildren()
#     xmlDict[children[0].text] = children[1].text
#
# pprint(xmlDict)