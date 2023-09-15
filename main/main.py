import telebot
from constants import bot_token
bot = telebot.TeleBot(bot_token)
# @bot.message_handler(func=lambda message: True)
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Рады вас видеть в Маслоботе. Мы подберем масло для вашего автомобиля")
bot.infinity_polling()