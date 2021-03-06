import requests
import re
import urllib.parse

from user import User

class Spider():

    def __init__(self, target_url, target_links):
        self.target_url = target_url
        self.target_links = target_links
        self.next_pages = [target_url]

    def extract_links(self):
        response = requests.get(self.target_url)
        html = response.content.decode('utf-8')
        return re.findall('(?:href=")(.*?)"', html)

    def crowl(self):
        href_links = self.extract_links()


        for link in href_links:
            link = urllib.parse.urljoin(self.target_url, link)

            if "#" in link:
                link = link.split("#")[0]

                if "https://www.olx.pl/oferta" in link and link not in self.target_links:
                    #print(link)
                    self.target_links.append(link)


    def number_of_pages(self):
        response = requests.get(self.target_url)
        html = response.content.decode('utf-8')
        existance_page = re.findall('(?:&page=)(.*?)" data-cy="page-link-last">', html)
        return(existance_page)

    def add_pages(self):
        number = self.number_of_pages()
        if len(number)==0:
            pass
        else:
            amount = number[0]
            i = 2
            while i <= int(amount):
                link = self.target_url + "&page=" + str(i)
                self.next_pages.append(link)
                i += 1
