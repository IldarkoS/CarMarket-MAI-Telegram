import telebot

from config import config

config = config.load_config()

bot = telebot.TeleBot(token=config.tg_bot.token)

@bot.message_handler(commands=["buy"])
def buy_start(message):
    pass