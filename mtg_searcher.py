from rolling_dice import Rolling_Dice
from kindle import Kindle

if __name__ == '__main__':
    k = Kindle()
    rd = Rolling_Dice()
    print("=== KINDLE ===")
    k.run()
    print("=== ROLLING DICE ===")
    rd.run()