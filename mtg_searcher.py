from scrappers.openbinder import Openbinder
from scrappers.kindle import Kindle

import requests
import sys

from simple_term_menu import TerminalMenu

if __name__ == '__main__':
    k = Kindle()
    o = Openbinder()

    if len(sys.argv) < 2:
        print('No card provided')
        sys.exit(1)
    else:
        input_name = ' '.join(sys.argv[1:])
    search_results = [c['value'] for c in requests.get('https://openbinder.co.kr/cardnameonlysearch.php?term={}'.format(input_name)).json() if '(Art)' not in c['value']]

    terminal_menu = TerminalMenu(search_results)
    choice_index = terminal_menu.show()

    k.run(search_results[choice_index] if '//' not in search_results[choice_index] else search_results[choice_index].replace('//','-'))
    o.run(search_results[choice_index])