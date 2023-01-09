from bs4 import BeautifulSoup
import requests
import re
import sys
from urllib.parse import urlparse, parse_qs

class Openbinder:
    
    BASE_URL = 'https://openbinder.co.kr/'
    BASE_SEARCH_URL = 'https://openbinder.co.kr/index.php?page=search&cname={}&pg={}'

    PAG = 1

    FLAGS = {
        'flag/Nx20xen.png.pagespeed.ic.9nFGTBPnvk.png' : 'ENG',
        'flag/Nx20xko.png.pagespeed.ic.SQ6MPfgFC-.png' : 'KR',
        'flag/Nx20xja.png.pagespeed.ic.e0vM4KWyoN.png' : 'JP',
        'flag/Nx20xge.png.pagespeed.ic.raJ410vWQh.png' : 'GER'
    }

    CONDITION = {
        'image/xNM.png.pagespeed.ic.wb3yXzgE3v.png' : 'NM',
        'image/xEX.png.pagespeed.ic.7hqskDn8dg.png' : 'EX',
        'image/xVG.png.pagespeed.ic.WO_VI12K7S.png' : 'VG',
        'image/xG.png.pagespeed.ic.EuAcxfDloy.png' : 'G'
    }

    def run(self):
        input_name = 'Sol Ring' if len(sys.argv) == 1 else sys.argv[1] if len(sys.argv) == 2 else ' '.join(sys.argv[1:]) # Python evaluates from right to left
        self.search_card_prices(input_name)
        # if self.PAG > 1:
        #     for p in range(2,self.PAG+1):
        #         self.search_card_prices(input_name,p)

    def search_card_prices(self, name: str, page = 1):

        url = self.BASE_SEARCH_URL.format(name,page)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        divs = [div for div in soup.find_all('div',attrs={'class':'dark__bg-dark'}) if '없습니다' not in div.getText()]
        for div in divs:
            parent = div.parent
            href = parent.attrs['onclick'].split('"')[1]
            self.search_card_price(self.BASE_URL + href, name)

    def search_card_price(self, url: str, name: str):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        p_url = parse_qs(urlparse(url).query)
        set_id = p_url['set'][0] + '-' + p_url['code'][0]
        normal = soup.find('div',attrs={'id':'tab-normal'}) # Normal stock
        foil = soup.find('div',attrs={'id':'tab-foil'}) # Foil stock
        for store in normal.find_all('div',attrs={'class','card-body'}):
            flag, condition = store.find_all('img')[1:] # First image is the store picture, not necessary.
            flag = self.FLAGS[flag.attrs['src']]
            condition = self.CONDITION[condition.attrs['src']]
            store_name = store.find('a').getText()
            price, stock = store.find('p').getText().split(' (')
            stock = stock.split(')')[0][5:-1]
            print(store_name, '::', name, '-', price, '(Stock: {})'.format(stock), '||', set_id)
        for store in foil.find_all('div',attrs={'class','card-body'}):
            flag, condition = store.find_all('img')[1:] # First image is the store picture, not necessary.
            flag = self.FLAGS[flag.attrs['src']]
            condition = self.CONDITION[condition.attrs['src']]
            store_name = store.find('a').getText()
            price, stock = store.find('p').getText().split(' (')
            stock = stock.split(')')[0][5:-1]
            print(store_name, '::', name, '(FOIL)','-', price, '(Stock: {})'.format(stock), '||', set_id)

            



if __name__ == '__main__':
    o = Openbinder()
    o.run()