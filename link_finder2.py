from bs4 import BeautifulSoup, NavigableString
from urllib import parse
import pprint
import elast
import nltk
import re
nltk.download('stopwords')
from nltk.corpus import stopwords
en_stops = set(stopwords.words('english'))
pp = pprint.PrettyPrinter(indent=1, width=80, depth=None, stream=None, compact=False)

class LinkFinder2():

    def __init__(self, base_url, page_url):
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    def feed(self, htmlstring, page_url):
        soup = BeautifulSoup(htmlstring, "html.parser")
        description_div = soup.find(id="Description")
        if description_div is not None:
            for child in description_div.children:
                description = child.get_text()

        # print("-----------------------------------------------------------------------------------------------------")

        h2sets = soup.find_all("h2")
        # print(page_url)
        print("in feed")
        for h2set in h2sets:
            # print(h2set.text)
            if "CAPEC-" in h2set.text and "DEPRECATED" not in h2set.text:
                main_content_div = soup.find(id="CAPECDefinition")
                # print(main_content_div.get_text(" ", strip=True))
                main_content = main_content_div.get_text(" ", strip=True)
                keywords = self.get_keywords(main_content)
                # print(keywords)
                # print("legal")
                # print("boom capec")
                dictn = {}
                dictn["threat"] = h2set.text
                dictn["url"] = page_url
                dictn["description"] = description
                dictn["keywords"] = str(keywords)
                # cap = soup.find("div", id="CAPECDefinition")
                # #print(cap.children)
                # skip=0
                # for child in cap.children:
                #     #print(child)
                #     if skip<3:
                #         skip+=1
                #         continue
                #     if type(child) is NavigableString:
                #         continue
                #     #print(child)
                #     #print(child.div.text)
                #     dictn[child.div.text] = str(child.text).replace(child.div.text, "")
                elast.insert(dictn, h2set.text)
                #pp.pprint(dictn)

            if "CWE-del" in h2set.text and "DEPRECATED" not in h2set.text:
                main_content_div = soup.find(id="CWEDefinition")
                # print(main_content_div.get_text(" ", strip=True))
                main_content = main_content_div.get_text(" ", strip=True)
                keywords = self.get_keywords(main_content)
                # print(keywords)
                # print("legal")
                # print("boom cwe")
                dictn = {}
                dictn["threat"] = h2set.text
                dictn["url"] = page_url
                dictn["description"] = description
                dictn["keywords"] = str(keywords)

                elast.insert(dictn, h2set.text)
                #pp.pprint(dictn)

                
        for link in soup.find_all("a"):
            url = parse.urljoin(self.base_url, link.get("href"))
            checkhash = url.split("/")
            if "#" in checkhash[-1]:
                continue

            if "data/definitions" not in url and ("capec.mitre" not in url or "cwe.mitre" not in url):
                continue
            self.links.add(url)
            # print("------------------------------------------------------"+url)

    def page_links(self):
        return self.links

    def get_keywords(self, main_content):
        keywords = []
        pattern = re.compile("([a-zA-Z])\w+(-)(\d+)")
        # word_tokens = word_tokenize(main_content)
        word_tokens = str(main_content).lower().split(" ")
        # word_tokens = [word for word in word_tokens if word.isalpha()]
        for word in word_tokens:
            if word.isalpha():
                if (word not in en_stops) and (word not in keywords):
                    print("- not found", word)
                    keywords.append(word)
            else:
                if pattern.match(word):
                    print("- found: ",word)
                    keywords.append(word)
        return keywords

