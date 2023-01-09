from bs4 import BeautifulSoup
import requests
import re
import sys
from urllib.parse import urlparse, parse_qs

class Openbinder:
    
    BASE_URL = 'https://openbinder.co.kr/'
    BASE_SEARCH_URL = 'https://openbinder.co.kr/index.php?page=search&cname={}'

    FLAGS = {
        'flag/Nx20xen.png.pagespeed.ic.9nFGTBPnvk.png' : 'ENG',
        'flag/Nx20xko.png.pagespeed.ic.SQ6MPfgFC-.png' : 'KR',
        'flag/Nx20xja.png.pagespeed.ic.e0vM4KWyoN.png' : 'JP',
        'flag/Nx20xge.png.pagespeed.ic.raJ410vWQh.png' : 'GER',
        'flag/Nx20xru.png.pagespeed.ic.fJ-01jLnWY.png' : 'RU',
        './flag/ru.png' : 'RU'
    }

    CONDITION = {
        'image/xNM.png.pagespeed.ic.wb3yXzgE3v.png' : 'NM',
        'image/NM.png' : 'NM',
        'image/xEX.png.pagespeed.ic.7hqskDn8dg.png' : 'EX',
        'image/EX.png' : 'EX',
        'image/xVG.png.pagespeed.ic.WO_VI12K7S.png' : 'VG',
        'image/VG.png' : 'VG',
        'image/xG.png.pagespeed.ic.EuAcxfDloy.png' : 'G',
        'image/G.png' : 'G'
    }

    def run(self):
        input_name = 'Swamp' if len(sys.argv) == 1 else sys.argv[1] if len(sys.argv) == 2 else ' '.join(sys.argv[1:]) # Python evaluates from right to left
        self.search_card_prices(input_name)

    def search_card_prices(self, name: str):

        url = self.BASE_SEARCH_URL.format(name)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        div = soup.find('div',attrs={'class':'dark__bg-dark'}) # We can find the stock available directly inside the card SSR page, so we just navigate into the first card we find.
        parent = div.parent
        href = parent.attrs['onclick'].split('"')[1]
        self.get_instock_urls(self.BASE_URL + href, name)

    def search_card_price(self, url: str, name: str, set_id: str):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        normal = soup.find('div',attrs={'id':'tab-normal'}) # Normal stock
        foil = soup.find('div',attrs={'id':'tab-foil'}) # Foil stock
        for store in normal.find_all('div',attrs={'class','card-body'}):
            flag, condition = store.find_all('img')[1:] # First image is the store picture, not necessary.
            flag = self.FLAGS[flag.attrs['src']]
            condition = self.CONDITION[condition.attrs['src']]
            store_name = store.find('a').getText()
            price, stock = store.find('p').getText().split(' (')
            stock = stock.split(')')[0][5:-1]
            print(store_name, '::', '[{}]'.format(condition), name, '({})'.format(flag), '-', price, '(Stock: {})'.format(stock), '||', set_id)
        for store in foil.find_all('div',attrs={'class','card-body'}):
            flag, condition = store.find_all('img')[1:] # First image is the store picture, not necessary.
            flag = self.FLAGS[flag.attrs['src']]
            condition = self.CONDITION[condition.attrs['src']]
            store_name = store.find('a').getText()
            price, stock = store.find('p').getText().split(' (')
            stock = stock.split(')')[0][5:-1]
            print(store_name, '::', '[{}]'.format(condition), name, '({}-FOIL)'.format(flag),'-', price, '(Stock: {})'.format(stock), '||', set_id)

    def get_instock_urls(self, url: str, name: str):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        in_stock = [i for i in soup.find('div',attrs={'class':'cardsets'}).find_all('tr') if '등록수' in str(i) and 'class="othersets"' not in str(i)]
        for card in in_stock:
            href = card.find('a').attrs['href'][2:]
            set_id = card.find('div',attrs={'style':'float:right;'}).getText()
            self.search_card_price(self.BASE_URL + href, name, set_id)
        

            



if __name__ == '__main__':
    o = Openbinder()
    o.run()