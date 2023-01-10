from bs4 import BeautifulSoup
import requests
import re
import sys
from typing import List

# To avoid import errors
sys.path.append('..')
sys.path.append('.')

from grpc_stubs.card_pb2 import Card

class Kindle:

    BASE_SEARCH_URL: str = 'http://www.mtgkindleshop.com/kindle/search_result.php'

    def run(self):
        input_name = 'Negate' if len(sys.argv) == 1 else sys.argv[1] if len(sys.argv) == 2 else ' '.join(sys.argv[1:]) # Python evaluates from right to left
        ret = self.search_card_prices(input_name.replace('\'',''))
        for c in ret:
            if c.foil:
                print(c.store, '::', '[NM]', c.name, '({}-FOIL)'.format('ENG'),'-', f'{c.price:,}'+'원', '(Stock: {})'.format(c.stock))
            else:
                print(c.store, '::', '[NM]', c.name, '({})'.format('ENG'), '-', f'{c.price:,}'+'원', '(Stock: {})'.format(c.stock))

    def server_call(self, name: str) -> List[Card]:
        return self.search_card_prices(name.replace('\'',''))
    

    def search_card_prices(self, name: str):
        # POST parameters
        params = {
            'search' : name,
            'limit' : 200, # High enough number to avoid having several pages
            'offset' : 0,
            'ko' : 1,
            'foilcard': '',
            'reset' : 'ok'
        }
        # Kindle webpage returns a lot of JS code together with the HTML, handle carefully.
        r = requests.post(self.BASE_SEARCH_URL, data=params)
        # Instance of BeautifulSoup using Python's built-in HTML parser
        soup = BeautifulSoup(r.text, 'html.parser')
        # Card ID - It is hardcoded in Kindle's SSR and can be used to find stock and price information
        c_id = 1001
        # We have to iterate over all divs with id = cardStyle. These divs contain all the useful information we need.
        cards: List[Card]= []
        for div in soup.find_all('div', attrs={'id':'cardStyle'}):
            scrapped_name = div.find(id='enName').get_text()
            if 'Art Series' not in scrapped_name and name in scrapped_name:
                stocks = []
                prices = []
                stock_div = div.find(id=str(c_id))
                for st in stock_div.find_all(id='typeName'):
                    stock: str = st.get_text()
                    stocks.append(int(stock.split(' / ')[0].split(' : ')[1])) # Stock of non-korean cards in NM condition. Structure: 'NM(영문) : 6 / NM(한글) : -'
                price_div = div.find(id='kindlePrice')
                for pr in price_div.find_all(id='kindlePriceMax'):
                    price: str = re.sub(r'[^0-9]','',pr.get_text())
                    prices.append(int(price) if price != '' else 0)
                for idx in range(len(stocks)):
                    if stocks[idx] > 0:
                        if idx == 0: # NM
                            cards.append(Card(name=scrapped_name,store='Kindle',price=prices[idx],stock=stocks[idx],foil=False))
                            # print(scrapped_name, '-', f'{prices[idx]:,}'+'원', '(Stock: {})'.format(stocks[idx]))
                        if idx == 1: # FOIL
                            cards.append(Card(name=scrapped_name,store='Kindle',price=prices[idx],stock=stocks[idx],foil=True))
                            # print(scrapped_name, '(FOIL)', '-', f'{prices[idx]:,}'+'원', '(Stock: {})'.format(stocks[idx]))
            c_id += 1001
        return cards


if __name__ == '__main__':
    k = Kindle()
    k.run()