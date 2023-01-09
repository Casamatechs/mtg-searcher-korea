from bs4 import BeautifulSoup
import requests
import re
import sys

class Rolling_Dice:

    BASE_SEARCH_URL: str = 'http://www.mtgrollingdice.com/index.php?mode=listtext&name={}&rarity=&type=normal&ln={}&ctype=&porder=&color=&page={}'
    COOKIES = {
        'rd_lang':'en'
    }
    FLAGS = {
        'images/home/16xNxko.png.pagespeed.ic.0lGpTtbfkf.png' : 'KR',
        'images/home/16xNxen.png.pagespeed.ic.wVMvDDn15j.png' : 'ENG',
        'images/home/16xNxja.png.pagespeed.ic.WxsX2mixDt.webp' : 'JP',
        './images/home/ja.png' : 'JP',
        'images/home/16xNxja.png.pagespeed.ic.aHOulN-fWf.png' : 'JP'
    }
    PAG = 1

    def run(self):
        input_name = 'Negate' if len(sys.argv) == 1 else sys.argv[1] if len(sys.argv) == 2 else ' '.join(sys.argv[1:]) # Python evaluates from right to left
        self.search_card_prices(input_name)
        if self.PAG > 1:
            for p in range(2,self.PAG+1):
                self.search_card_prices(input_name,p)

    def search_card_prices(self, name: str, page = 1):

        url = self.BASE_SEARCH_URL.format(name,20,page)
        r = requests.get(url=url,cookies=self.COOKIES)
        soup = BeautifulSoup(r.text, 'html.parser')
        # Update PAG variable
        if self.PAG == 1:
            pag_ul = soup.find('ul',attrs={'class':'pagination'})
            self.PAG = int(re.sub(r'[^0-9]','',pag_ul.contents[-1] # We want the last element of the list as it will always be 'Last Page'
                .find('a').attrs['onclick']))
        # RD (and hopefully Nyang Card) use a unique CSS class to display cards. We can use it to iterate.
        for div in soup.find_all('div',attrs={'class':'col-sm-12'}):
            # The relevant information is stored in divs with class 'col-sm-5'.
            # First one will contain the name and second one will contain the price and stock info.
            card_name, stock_price = div.find_all('div',attrs={'class':'col-sm-5'})
            # 0 -> Card Name [ENG,KO]
            # 1 -> Edition
            # 2 -> Card Type
            card_name = card_name.contents[0].contents[0].getText() # Only ENG name
            stock_table = stock_price.contents[0] # Table containing stock and price for each condition
            # For now, will only consider NM condition
            nm_info = stock_table.contents[0]
            # nm_info[0] -> Condition (NM) and price
            price = nm_info.contents[0].get_text()
            if 'No Information' in price:
                break
            price: int = int(re.sub(r'[^0-9]','',price))
            # nm_info[1] -> Composed table containing language of the card and stock.
            for tr in nm_info.contents[1].find_all('tr'):
                if tr.getText() == 'We have not enough inventories.':
                    break # No stock, we can stop here
                # tr[0] -> LANG
                # tr[1] -> STOCK
                # tr[2] -> PRICE (DUPLICATED)
                # tr[3] -> CART (DONT USE)
                flag = tr.contents[0].find('img').attrs['src']
                lang = self.FLAGS[flag] if flag in self.FLAGS else '?'
                if lang == 'KR':
                    continue # For now we are only looking for non-KR cards
                stock = tr.contents[1].getText()
                stock: int = int(re.sub(r'[^0-9]','',stock))
                print(card_name, '({})'.format(lang), '-', f'{price:,}'+'원', '(Stock: {})'.format(stock))
            # print(stock_price)

if __name__ == '__main__':
    rd = Rolling_Dice()
    rd.run()