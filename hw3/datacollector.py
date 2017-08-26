from html.parser import HTMLParser
from urllib.request import urlopen
from urllib.parse import quote


class MainTextParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.text = False
        self.main_text = False
        self.other_div = False
        self.data = ""

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.text = True
        if tag == 'div' and any([(k, v) == ('id', 'mw-content-text') for k, v in attrs]):
            self.main_text = True
        elif tag == 'div' and self.main_text:
            self.other_div = True

    def handle_endtag(self, tag):
        if self.text and tag == 'p':
            self.text = False
        if self.main_text and self.other_div is True and tag == 'div':
            self.other_div = False
        elif self.main_text and self.other_div is False and tag == 'div':
            self.main_text = False

    def handle_data(self, data):
        if self.main_text and self.text and self.other_div is False:
            self.data = self.data + data

    def error(self, message):
        print(message)


def get_data(filename):
    base_url = 'http://ru.lotr.wikia.com/wiki/'
    countries = ['Гондор', 'Рохан', 'Шир', 'Лотлориэн', 'Мориа',
                 'Мордор', 'Валинор', 'Эльдамар', 'Нуменор', 'Дориат']
    cities = ['Минас_Тирит', 'Эсгарот', 'Эдорас', 'Барад-дур', 'Изенгард',
              'Тирион', 'Гондолин', 'Нарготронд', 'Ривенделл', 'Бри']
    places = countries + cities
    for place in places:
        place_url = quote(place)
        conn = urlopen(base_url + place_url)
        data = conn.read()
        html = data.decode('utf-8')
        with open(filename, "a") as f:
            parser = MainTextParser()
            parser.feed(html)
            f.write(parser.data)
        conn.close()


def main(filename):
    get_data(filename)

if __name__ == '__main__':
    main("data")
