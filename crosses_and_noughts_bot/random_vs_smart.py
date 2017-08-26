#!/usr/bin/env python3

from crosses_and_noughts_bot import CrossesAndNoughts


def main():
    can = CrossesAndNoughts()
    smart_win = 0
    random_win = 0
    draw = 0
    N = 1000
    for game in range(N):
        can.newGame()
#        crosses are smart, noughts are random if game % 2 == 0
        for turn in range(9):
            if turn % 2 == 0:
                if game % 2 == 0:
                    can.smartMove()
                else:
                    can.randomMove()
            else:
                if game % 2 == 0:
                    can.randomMove()
                else:
                    can.smartMove()
            res = can.checkFinish()
            if res is not None:
                if res == CrossesAndNoughts.X_WIN:
                    if game % 2 == 0:
                        smart_win = smart_win + 1
                    else:
                        random_win = random_win + 1
                if res == CrossesAndNoughts.O_WIN:
                    if game % 2 == 0:
                        random_win = random_win + 1
                    else:
                        smart_win = smart_win + 1
                if res == CrossesAndNoughts.FINAL_DRAW:
                    draw = draw + 1
                break
    print("wins:", smart_win / N)
    print("draws:", draw / N)
    print("loses:", random_win / N)

if __name__ == '__main__':
    main()
