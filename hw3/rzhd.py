from html.parser import HTMLParser
from urllib.request import urlopen
from urllib.parse import quote

class MainTextParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.is_cost_tag = False
        self.costs = []

    def handle_starttag(self, tag, attrs):
        #if tag == 'div':
            #print(attrs)
        if tag == 'div' and any([(k, v) == ('class', 'car-type__cost') for k, v in attrs]):
            print("here is openning tag")
            self.is_cost_tag = True

    def handle_endtag(self, tag):
        if tag == 'div' and self.is_cost_tag:
            self.is_cost_tag = False

    def handle_data(self, data):
        if self.is_cost_tag:
            print(data)

    def error(self, message):
        print(message)


def get_data():
    base_url = 'https://pass.rzd.ru/tickets/public/ru?layer_name=e3-route&' \
               'st0=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0&code0=2000000&st1=' \
               '%D0%90%D0%93%D0%A0%D0%AB%D0%97&code1=2060533&dt0=09.06.2017&tfl=3&checkSeats=1'
    conn = urlopen(base_url)
    data = conn.read()
    html = data.decode('utf-8')
    with open('/home/nimloth/data.html', 'w') as f:
        f.write(html)
    parser = MainTextParser()
    parser.feed(html)
    conn.close()


def main(filename):
    get_data()

if __name__ == '__main__':
    main("data")
