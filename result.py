from spider import Spider
from user import User
from config import Config
from interface import Interface
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import sys




number_of_rooms = "Kawalerka"
price_from = "600"
price_to = "1200"
lokalization = "Krzyki"

user_input = User(number_of_rooms, price_from, price_to, lokalization)

checked_links = []
with open("link_config.txt", mode = "r") as conf:
    for x in conf:
        checked_links.append(x[:-1])
number_before_add_new = len(checked_links)

release_spider = Spider(user_input.make_taget_url(), checked_links)
release_spider.add_pages()
pages = len(release_spider.next_pages)
i = 0
while i < pages:
    scanning = Spider(release_spider.next_pages[i], checked_links)
    scanning.crowl()
    i += 1

user_config = Config(user_input.make_config_list(), scanning.target_links, user_input, scanning)
user_config.save_config_filtr()

lst = []
f = open("link_config.txt", "r")
for x in f:
    lst.append(x[:-1])

print(lst)


for i in scanning.target_links:
    if i not in lst:
        user_config.save_shown_links(i)
print(checked_links)
