import csv
import telebot
# Для создания меню
from telebot import types
# Импортируем токен
from constants import bot_token
from constants import group_username

bot = telebot.TeleBot(bot_token)

# forwardmessage
@bot.message_handler(commands=["send"])
def send_forward_message(message):
    msg = bot.send_message(message.chat.id, "Напиши свое сообщение ниже:")
    bot.register_next_step_handler(msg, process_msg)

def process_msg(message):  
    bot.forward_message(group_username, message.chat.id, message.message_id)

# start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.from_user.id, "Привет! Я чат-бот интернет-магазина https://SmartOil96.ru") 
    # create the welcome menu
    main_menu = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton("Отправить сообщение", callback_data="send")
    button2 = types.InlineKeyboardButton("Перейти на сайт", url="http://SmartOil96.ru")
    button3 = types.InlineKeyboardButton("Подобрать моторное масло", callback_data="smart")
    main_menu.add(button1, button2, button3)
    bot.send_message(message.from_user.id, "Чем я могу тебе помочь:", reply_markup=main_menu)

# forwardmessage from mainmenu
@bot.callback_query_handler(func=lambda call: call.data == "send")
def callback_send(call):
    send_forward_message(call.message)

# import brands_recomend
brands_recomend = {}
with open('brands_recomend.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        # Добавляем пару ключ-значение в словарь
        brands_recomend[row['brand']] = row['recomend']

@bot.callback_query_handler(func=lambda call: True)
def callback_car_brands(call):
    """Обрабатываем пункты меню подбора масла"""
    if call.data == "smart":
        bot.send_message(call.message.chat.id, "Давай подберем тебе масло")
        smartoil_menu = types.InlineKeyboardMarkup(row_width=4)
        buttons = [types.InlineKeyboardButton(button_data, callback_data=button_data) for button_data in brands_recomend.keys()]
        smartoil_menu.add(*buttons)
        bot.send_message(call.message.chat.id, "Выбери марку автомобиля:", reply_markup=smartoil_menu)
    else:
        """Выдаем рекомендации по маслу"""
        for button_data in list(brands_recomend.keys()):
            if call.data == button_data:
                if brands_recomend[button_data] == "recomend":
                    bot.send_message(call.message.chat.id, f"Для подбора масла для автомобиля марки {button_data} пожалуйста оставьте заявку нашему консультанту /send")        
                else:
                    bot.send_message(call.message.chat.id, f"Наши рекомендации для автомобиля {button_data}:") 
                    bot.send_message(call.message.chat.id, brands_recomend[button_data])
                break

bot.polling(none_stop=True, interval=0)