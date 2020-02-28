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
        for h2set in h2sets:
            print(h2set.text)
            if "CAPEC-" in h2set.text:
                print("legal")
                dictn = {}
                dictn["threat"] = h2set.text
                cap = soup.find("div", id="CAPECDefinition")
                print(cap.children)
                skip=0
                for child in cap.children:
                    #print(child)
                    if skip<3:
                        skip+=1
                        continue
                    if type(child) is NavigableString:
                        continue
                    print(child)
                    #print(child.div.text)
                    dictn[child.div.text] = str(child.text).replace(child.div.text, "")

                #
                # ninth = soup.find("div", id="Likelihood_Of_Attack")
                # if ninth:
                #     print(ninth)
                #     dictn[ninth.div.text] = str(ninth.text).replace(ninth.div.text, "")
                # else:
                #     print("missing")
                #
                # second = soup.find("div", id="Typical_Severity")
                # if second:
                #     print(second)
                #     dictn[second.div.text] = str(second.text).replace(second.div.text, "")
                # else:
                #     print("missing")
                #
                # third = soup.find("div", id="Relationships")
                # if third:
                #     print(third)
                #     dictn[third.div.text] = str(third.text).replace(third.div.text, "")
                # else:
                #     print("missing")
                #
                # fourth = soup.find("div", id="Prerequisites")
                # if fourth:
                #     print(fourth)
                #     dictn[fourth.div.text] = str(fourth.text).replace(fourth.div.text, "")
                # else:
                #     print("missing")
                #
                # fifth = soup.find("div", id="Resources_Required")
                # if fifth:
                #     print(fifth)
                #     dictn[fifth.div.text] = str(fifth.text).replace(fifth.div.text, "")
                # else:
                #     print("missing")
                #
                # sixth = soup.find("div", id="Mitigations")
                # if sixth:
                #     print(sixth)
                #     dictn[sixth.div.text] = str(sixth.text).replace(sixth.div.text, "")
                # else:
                #     print("missing")
                #
                # seventh = soup.find("div", id="Related_Weaknesses")
                # if seventh:
                #     print(seventh)
                #     dictn[seventh.div.text] = str(seventh.text).replace(seventh.div.text, "")
                # else:
                #     print("missing")
                #
                # eighth = soup.find("div", id="Content_History")
                # if eighth:
                #     print(eighth)
                #     dictn[eighth.div.text] = str(eighth.text).replace(eighth.div.text, "")
                # else:
                #     print("missing")



                elast.insert(dictn)
                pp.pprint(dictn)

        for link in soup.find_all("a"):
            url = parse.urljoin(self.base_url, link.get("href"))
            checkhash = url.split("/")
            if "#" in checkhash[-1]:
                continue
            if "data/definitions" not in url or "capec.mitre" not in url:
                continue
            self.links.add(url)
            print("------------------------------------------------------"+url)

    def page_links(self):
        return self.links

