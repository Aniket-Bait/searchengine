from bs4 import BeautifulSoup, NavigableString
from urllib import parse
import pprint
import elast

pp = pprint.PrettyPrinter(indent=1, width=80, depth=None, stream=None, compact=False)

class LinkFinder2():

    def __init__(self, base_url, page_url):
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    def feed(self, htmlstring):
        soup = BeautifulSoup(htmlstring, "html.parser")
        h2sets = soup.find_all("h2")
        print("in feed")
        for h2set in h2sets:
            print(h2set.text)
            if "CAPEC-" in h2set.text and "DEPRECATED" not in h2set.text:
                print("legal")
                print("boom capec")
                dictn = {}
                dictn["threat"] = h2set.text
                cap = soup.find("div", id="CAPECDefinition")
                #print(cap.children)
                skip=0
                for child in cap.children:
                    #print(child)
                    if skip<3:
                        skip+=1
                        continue
                    if type(child) is NavigableString:
                        continue
                    #print(child)
                    #print(child.div.text)
                    dictn[child.div.text] = str(child.text).replace(child.div.text, "")
                elast.insert(dictn, h2set.text)
                #pp.pprint(dictn)

            if "CWE-" in h2set.text and "DEPRECATED" not in h2set.text:
                print("legal")
                print("boom cwe")
                dictn = {}
                dictn["threat"] = h2set.text
                cap = soup.find("div", id="CWEDefinition")
                #print(cap.children)
                skip=0
                for child in cap.children:
                    #print(child)
                    if skip<3:
                        skip+=1
                        continue
                    if type(child) is NavigableString:
                        continue
                    #print(child)
                    #print(child.div.text)
                    dictn[child.div.text] = str(child.text).replace(child.div.text, "")

                elast.insert(dictn, h2set.text)
                #pp.pprint(dictn)

                #elast.insert(dictn)
                #pp.pprint(dictn)

        for link in soup.find_all("a"):
            url = parse.urljoin(self.base_url, link.get("href"))
            checkhash = url.split("/")
            if "#" in checkhash[-1]:
                continue
            if "data/definitions" not in url and ("capec.mitre" not in url or "cwe.mitre" not in url):
                continue
            self.links.add(url)
            print("------------------------------------------------------"+url)

    def page_links(self):
        return self.links

