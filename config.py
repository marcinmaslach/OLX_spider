import os
from user import User
from spider import Spider

class Config:

    def __init__(self, filtr, extracted_links, user, spider):
        self.filtr = filtr
        self.extracted_links = extracted_links
        self.user = user
        self.spider = spider

    def save_config_filtr(self):
        lst_filtr = self.user.make_config_list()
        with open("filtr_config.txt", mode = "a") as conf:
            for i in lst_filtr:
                conf.write(str(i) + "\n")
            conf.close()

    def delete_config_filtr(self):
        os.remove("filtr_config.txt")
        open("filtr_config.txt", mode = "x")

    def save_shown_links(self, url):
        with open("link_config.txt", mode = "a") as conf:
            conf.write(str(url) + "\n")

    def delete_shown(self):
        os.remove("print_link.txt")
        open("print_link.txt", mode = "x")

    def save_print_link(self, url):
        with open("print_link.txt", mode = "a") as conf:
            conf.write(str(url) + "\n")
