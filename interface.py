from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import sys
import webbrowser

from spider import Spider
from user import User
from config import Config

class Interface(QWidget):

    def __init__(self):
        self.rooms = " "
        self.pr_from = " "
        self.pr_to = " "
        self.loc = " "
        self.href = []
        self.number_of_floats = " "
        super().__init__()
        self.initUI()


    def initUI(self):
        #App icon
        self.setWindowIcon(QIcon('OLX-Logo.png'))

        #Choose number of rooms
        self.rooms_lbl = QLabel("Ilość pokoi", self)

        rooms = QComboBox(self)
        rooms.addItem("Kawalerka")
        rooms.addItem("2 pokoje")
        rooms.addItem("3 pokoje")
        rooms.addItem("4 i więcej")

        rooms.move(40, 25)
        self.rooms_lbl.move(40, 10)
        self.rooms = str(rooms.currentText())
        rooms.activated[str].connect(self.onActivated_rooms)

        #Choose localization
        self.loc_lbl = QLabel("Dzielnica Wrocławia", self)

        loc = QComboBox(self)
        loc.addItem("Krzyki")
        loc.addItem("Fabryczna")
        loc.addItem("Psie Pole")
        loc.addItem("Śródmieście")
        loc.addItem("Stare Miasto")

        loc.move(160, 25)
        self.loc_lbl.move(160, 10)
        self.loc = str(loc.currentText())
        loc.activated[str].connect(self.onActivated_loc)


        #Choose pice from
        self.price_from_lbl = QLabel("Cena od", self)

        pr_from = QComboBox(self)
        pr_from.addItem("600")
        pr_from.addItem("800")
        pr_from.addItem("1000")
        pr_from.addItem("1200")
        pr_from.addItem("1400")
        pr_from.addItem("1600")
        pr_from.addItem("1800")
        pr_from.addItem("2000")
        pr_from.addItem("2200")
        pr_from.addItem("2400")
        pr_from.addItem("2600")
        pr_from.addItem("2800")
        pr_from.addItem("3000")

        pr_from.move(50,100)
        self.price_from_lbl.move(50,85)
        self.pr_from = str(pr_from.currentText())
        pr_from.activated[str].connect(self.onActivated_pr_from)

        #Choose pice to
        self.price_to_lbl = QLabel("Cena do", self)

        pr_to = QComboBox(self)
        pr_to.addItem("600")
        pr_to.addItem("800")
        pr_to.addItem("1000")
        pr_to.addItem("1200")
        pr_to.addItem("1400")
        pr_to.addItem("1600")
        pr_to.addItem("1800")
        pr_to.addItem("2000")
        pr_to.addItem("2200")
        pr_to.addItem("2400")
        pr_to.addItem("2600")
        pr_to.addItem("2800")
        pr_to.addItem("3000")

        pr_to.move(175,100)
        self.price_to_lbl.move(175,85)
        self.pr_to = str(pr_to.currentText())
        pr_to.activated[str].connect(self.onActivated_pr_to)


        #Button to pick filtrs
        btn = QPushButton('Zatwierdź', self)
        btn.resize(btn.sizeHint())
        btn.move(215, 135)
        btn.clicked.connect(self.on_pushButton_clicked)

        #Button to open browser
        text = open("print_link.txt", "r")
        links = text.readlines()
        #num = len(links)

        btn2 = QPushButton('Otwórz', self)
        btn2.resize(btn.sizeHint())
        btn2.move(125, 135)
        btn2.clicked.connect(self.open_browser)

        #App setWindowIcon
        self.resize(300, 160)
        self.center()
        self.setWindowTitle('FILTRY')
        self.show()

    def open_browser(self):
        i = 0
        num = len(self.href)
        while i != num:
            webbrowser.open(self.href[i])
            i += 1

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def onActivated_rooms(self, text):
        self.rooms = text

    def onActivated_loc(self, text):
        self.loc = text

    def onActivated_pr_from(self, text):
        self.pr_from = text

    def onActivated_pr_to(self, text):
        self.pr_to = text

    def on_pushButton_clicked(self):

        checked_links = []
        with open("link_config.txt", mode = "r") as conf:
            for x in conf:
                checked_links.append(x[:-1])


        user_input = User(self.rooms, self.pr_from, self.pr_to, self.loc)

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
        user_config.delete_shown()

        links_in_config = []
        f = open("link_config.txt", "r")
        for x in f:
            links_in_config.append(x[:-1])


        for i in scanning.target_links:
            if i not in links_in_config:
                user_config.save_shown_links(i)
                user_config.save_print_link(i)
                self.href.append(str(i))

        self.number_of_floats = len(self.href)



if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Interface()
    sys.exit(app.exec_())
