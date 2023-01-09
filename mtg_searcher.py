from openbinder import Openbinder
from kindle import Kindle

if __name__ == '__main__':
    k = Kindle()
    o = Openbinder()
    print("=== KINDLE ===")
    k.run()
    print("=== OPENBINDER ===")
    o.run()