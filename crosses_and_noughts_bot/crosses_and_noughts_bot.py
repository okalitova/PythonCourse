#!/usr/bin/env python3

import re
from random import randint
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Handler
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from telegram.replykeyboardhide import ReplyKeyboardHide
import logging


class CrossesAndNoughts:
    FREE = "0"
    X = "1"
    O = "2"
    LOSE = "0"
    WIN = "1"
    DRAW = "2"
    X_WIN = "X won"
    O_WIN = "O won"
    FINAL_DRAW = "Draw"

    def __init__(self):
        self.field = [[self.FREE for _ in range(3)] for _ in range(3)]
        self.x_move = True
        self.o_move = False
        self.xStrategy()

    def newGame(self):
        self.field = [[self.FREE for _ in range(3)] for _ in range(3)]
        self.x_move = True
        self.o_move = False

    def fieldToMask(self):
        mask = ""
        for row in self.field:
            for cell in row:
                mask = mask + cell
        return mask

    def checkFinish(self):
        mask = self.fieldToMask()
        return self.isFinished(mask)

    def move(self, i, j):
        if self.field[i][j] != self.FREE:
            return "Incorrect move, cell is already occupied"
        else:
            if self.x_move:
                self.field[i][j] = self.X
                self.x_move = False
                self.o_move = True
                return "Your turn!"
            else:
                self.field[i][j] = self.O
                self.o_move = False
                self.x_move = True
                return "Your turn!"

    def randomMove(self):
        available_cells = []
        for i in range(3):
            for j in range(3):
                if self.field[i][j] == self.FREE:
                    available_cells.append((i, j))
        rand = randint(0, len(available_cells) - 1)
        i, j = available_cells[rand]
        self.move(i, j)

    def smartMove(self):
        mask = ""
        for row in self.field:
            for cell in row:
                mask = mask + cell
        v = int(mask, 3)
        to = self.strategy_tree[v]
        for i in range(3):
            for j in range(3):
                self.field[i][j] = to[i * 3 + j]
        self.x_move = not self.x_move
        self.o_move = not self.o_move

    def getNiceField(self):
        nice_field = [["_" for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                if self.field[i][j] == self.X:
                    nice_field[i][j] = "X"
                elif self.field[i][j] == self.O:
                    nice_field[i][j] = "O"
                elif self.field[i][j] == self.FREE:
                    nice_field[i][j] = "_"
                    nice_field[i][j] = nice_field[i][j] + " " + str(i) + " " + str(j)
        return nice_field

    def digitToChar(self, digit):
        if digit < 10:
            return str(digit)
        return chr(ord('a') + digit - 10)

    def strBase(self, number, base):
        if number < 0:
            return '-' + self.strBase(-number, base)
        (d, m) = divmod(number, base)
        if d > 0:
            return self.strBase(d, base) + self.digitToChar(m)
        return self.digitToChar(m)

    def isFinished(self, mask):
        for i in range(3):
            o_res = 0
            x_res = 0
            for j in range(3):
                if mask[i * 3 + j] == self.X:
                    x_res = x_res + 1
                if mask[i * 3 + j] == self.O:
                    o_res = o_res + 1
            if x_res == 3:
                return self.X_WIN
            if o_res == 3:
                return self.O_WIN
        for j in range(3):
            o_res = 0
            x_res = 0
            for i in range(3):
                if mask[i * 3 + j] == self.X:
                    x_res = x_res + 1
                if mask[i * 3 + j] == self.O:
                    o_res = o_res + 1
            if x_res == 3:
                return self.X_WIN
            if o_res == 3:
                return self.O_WIN
        o_res = 0
        x_res = 0
        for i in range(3):
            if mask[i * 4] == self.X:
                x_res = x_res + 1
            if mask[i * 4] == self.O:
                o_res = o_res + 1
        if x_res == 3:
            return self.X_WIN
        if o_res == 3:
            return self.O_WIN
        o_res = 0
        x_res = 0
        for i in range(3):
            if mask[2 + i * 2] == self.X:
                x_res = x_res + 1
            if mask[2 + i * 2] == self.O:
                o_res = o_res + 1
        if x_res == 3:
            return self.X_WIN
        if o_res == 3:
            return self.O_WIN
        for m in mask:
            if m == self.FREE:
                return None
        return self.FINAL_DRAW

    def buildStrategy(self, mask, x=True):
        res = self.isFinished(mask)
        if res is not None:
            if res == self.FINAL_DRAW:
                return self.DRAW
            if x and res == self.X_WIN:
                return self.WIN
            if x and res == self.O_WIN:
                return self.LOSE
            if not x and res == self.X_WIN:
                return self.LOSE
            if not x and res == self.O_WIN:
                return self.WIN
        else:
            results = []
            for i, m in enumerate(mask):
                if m == self.FREE:
                    if x:
                        new_mask = list(mask)
                        new_mask[i] = self.X
                        results.append((new_mask, self.buildStrategy(new_mask, x=False)))
                    else:
                        new_mask = list(mask)
                        new_mask[i] = self.O
                        results.append((new_mask, self.buildStrategy(new_mask, x=True)))
            mask = ''.join(mask)
            for res in results:
                new_mask = ''.join(res[0])
                if res[1] == self.LOSE:
                    self.strategy_tree[int(mask, 3)] = new_mask
                    return self.WIN
            for res in results:
                new_mask = ''.join(res[0])
                if res[1] == self.DRAW:
                    self.strategy_tree[int(mask, 3)] = new_mask
                    return self.DRAW
            for res in results:
                new_mask = ''.join(res[0])
                if res[1] == self.WIN:
                    self.strategy_tree[int(mask, 3)] = new_mask
                    return self.LOSE

    def xStrategy(self):
        self.strategy_tree = ["" for _ in range(3 ** 9)]
        self.buildStrategy(["0" for _ in range(9)])

    def getStrField(self):
        str_field = ""
        for i in range(3):
            for j in range(3):
                if self.field[i][j] == self.X:
                    str_field = str_field + "X"
                elif self.field[i][j] == self.O:
                    str_field = str_field + "O"
                elif self.field[i][j] == self.FREE:
                    str_field = str_field + "_"
            str_field = str_field + "\n"
        return str_field


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

can = CrossesAndNoughts()


def gameFinish(bot, update):
    chat_id = update.message.chat_id
    ans = can.checkFinish()

    bot.sendMessage(chat_id=chat_id,
                    text=ans)
    bot.sendMessage(chat_id=chat_id,
                    text=can.getStrField())

    reply_markup = ReplyKeyboardHide()
    bot.sendMessage(chat_id=chat_id, text="Game over", reply_markup=reply_markup)


def start(bot, update):
    update.message.reply_text('Hi, would you like to play crosses and noughts?:) yes/no')
    can.newGame()


def help(bot, update):
    update.message.reply_text('')


def echo(bot, update):
    msg = update.message.text
    chat_id = update.message.chat_id

    pattern = re.compile("(X|O|_) \d \d")

    if msg == "no":
        bot.sendMessage(chat_id=chat_id, text="See you next time!")
        return
    if msg == "yes":
        bot.sendMessage(chat_id=chat_id, text="Would you like to be crosses or noughts?")
        return
    if msg == "crosses":
        custom_keyboard = can.getNiceField()
        reply_markup = ReplyKeyboardMarkup(custom_keyboard)
        bot.sendMessage(chat_id=chat_id,
                        text="Lets start! Your turn!",
                        reply_markup=reply_markup)
        return
    if msg == "noughts":
        can.smartMove()
        custom_keyboard = can.getNiceField()
        reply_markup = ReplyKeyboardMarkup(custom_keyboard)
        bot.sendMessage(chat_id=chat_id,
                        text="I started! Your turn!",
                        reply_markup=reply_markup)
        return
    if not re.match(pattern, msg):
        bot.sendMessage(chat_id=chat_id, text="Incorrect format :C")
        return
    if re.match(pattern, msg):
        i = int(msg[2])
        j = int(msg[4])
        ans = can.move(i, j)
        if ans != "Your turn!":
            bot.sendMessage(chat_id=chat_id, text=ans)
            return
        if can.checkFinish() is not None:
            gameFinish(bot, update)
        else:
            can.smartMove()

            if can.checkFinish() is not None:
                gameFinish(bot, update)
            else:
                custom_keyboard = can.getNiceField()
                reply_markup = ReplyKeyboardMarkup(custom_keyboard)
                bot.sendMessage(chat_id=chat_id,
                                text=ans,
                                reply_markup=reply_markup)
        return


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("398956652:AAHxdhePm6x9FgBwFgQ0feM2_e4j1RzhoQ0")
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    # on noncommand
    dp.add_handler(MessageHandler(Filters.all, echo))
    # log all errors
    dp.add_error_handler(error)
    # start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
