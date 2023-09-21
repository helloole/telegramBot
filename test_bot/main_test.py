import json
import telebot
# Для создания меню
from telebot import types
from telebot.types import CallbackQuery
# Импортируем токен
from contest import bot_token

from telegram.ext import CallbackQueryHandler

bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
	#bot.reply_to(message, "Привет!")
    bot.send_message(message.from_user.id, "Привет! Я чат-бот интернет-магазина https://SmartOil96.ru") 
    # create the welcome menu
    main_menu = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton("Отправить сообщение", callback_data="send")
    button2 = types.InlineKeyboardButton("Перейти на сайт", url="http://SmartOil96.ru")
    button3 = types.InlineKeyboardButton("Подобрать моторное масло", callback_data="smart")
    main_menu.add(button1, button2, button3)
    bot.send_message(message.from_user.id, "Чем я могу тебе помочь:", reply_markup=main_menu)


with open('car_brands.json', 'r') as f:
    car_brands_info = json.load(f)
buttons = car_brands_info["buttons"]

@bot.callback_query_handler(func=lambda call: True)
def callback_car_brands(call):
    """Обрабатываем пункты меню подбора масла"""
    if call.data == "smart":
        bot.send_message(call.message.chat.id, "Давай подберем тебе масло")
        #buttons = car_brands_info["buttons"]
        smartoil_menu = types.InlineKeyboardMarkup(row_width=2)
        for button_data in buttons:
            button = types.InlineKeyboardButton(button_data['text'], callback_data=button_data['callback_data'])
            smartoil_menu.add(button)
        bot.send_message(call.message.chat.id, "Выбери марку автомобиля:", reply_markup=smartoil_menu)
    elif call.data == "send":
        """Обрабатываем пункт Отправить сообщение"""
        bot.send_message(call.message.chat.id, "Свяжись с нами для этого\nвведи сообщение ниже:")
        # Сохраняем состояние пользователя, чтобы в следующем сообщении ожидать сообщение
        bot.register_next_step_handler(call.message, send_message_to_admin)
    else:
        """Выдаем рекомендации по маслу"""
        for button_data in buttons:
            if call.data == button_data['callback_data']:
                bot.send_message(call.message.chat.id, button_data['recomend'])
                break

def send_message_to_admin(message):
    # ID администратора (замените на нужный вам ID)
    # -1001626076787
    # smartoil96
    group_username = "1001626076787"
    user_name = "smartoil96"
    user_id = message.from_user.id
    user_message = message.text
    #full_message = f"Пользователь {user_id} написал: {user_message}"
    #bot.send_message(admin_id, full_message)
    bot.send_message('@' + group_username, message.text)
    bot.send_message('-' + group_username, message.text)
    bot.send_message(group_username, message.text)
    bot.send_message(user_name, message.text)
    bot.send_message(user_name, message.text)

"""@bot.callback_query_handler(func=lambda call: True)
def callback_car_recomend(call):
    
    #buttons = car_brands_info['buttons']
    for button_data in buttons:
        if call.data == button_data['callback_data']:
            bot.send_message(call.message.chat.id, button_data['recomend'])
            break
"""

"""@bot.callback_query_handler(func=lambda call: call.data in car_brands_info["buttons"]["text"])
def callback_smartoil_recomend(call):
    bot.send_message(call.message.chat.id, "Давай подберем тебе масло")   
    for brand_command in car_brands_info["buttons"]["text"]:
        bot.send_message(call.message.chat.id, f"Твоя команда {call.data}") """

""" 
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "smart":
        bot.send_message(call.message.chat.id, "Давай подберем тебе масло\nвыбери марку автомобиля")
        smartoil_menu = types.InlineKeyboardMarkup(row_width=1)
        button1 = types.InlineKeyboardButton("Рено", callback_data="reno")
        button2 = types.InlineKeyboardButton("Перейти на сайт", url="http://SmartOil96.ru")
        button3 = types.InlineKeyboardButton("Пежо", callback_data="Peugot")
        smartoil_menu.add(button1, button2, button3)
        bot.send_message(call.message.chat.id, "Выбери марку автомобиля", reply_markup=smartoil_menu)
    elif call.data == "send":
        bot.send_message(call.message.chat.id, "Оставьте заявку,\n наш менеджер свяжестя с вами.") 
"""
         

'''@bot.message_handler(content_types=['text'])
def get_text_message(message):
    #bot.send_message(message.from_user.id, "Привет!")
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Чем я могу тебе помочь?")
    elif message.text == "/smart":
        bot.send_message(message.from_user.id, "Я напишу тебе что-нибудь про масло")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю... Напиши /help.")
'''

bot.polling(none_stop=True, interval=0)