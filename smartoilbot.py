from constants import bot_token, admin_id
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, MessageHandler, filters
import logging
import json

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

logger = logging.getLogger(__name__)

# Define states for the conversation handler
MENU, SUBMENU, REQUEST = range(3)

# Start command handler
def start(update: Update, context: CallbackContext) -> int:
    user = update.effective_user
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Привет, {user.first_name}! Чем я могу помочь?")
    return menu(update, context)

# Menu command handler
def menu(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [InlineKeyboardButton("Подобрать моторное масло", callback_data='smartoil')],
        [InlineKeyboardButton("Оставить заявку", callback_data='send')],
        [InlineKeyboardButton("Перейти в интернет-магазин", callback_data='tosite')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Выберите один из пунктов меню:', reply_markup=reply_markup)
    return MENU

# Submenu command handler
def submenu(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    if query.data == 'smartoil':
        keyboard = [
            [InlineKeyboardButton("Тойота", callback_data='toyota')],
            [InlineKeyboardButton("Камаз", callback_data='kamaz')],
            [InlineKeyboardButton("Уаз", callback_data='uaz')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text='Выберите марку вашей машины:', reply_markup=reply_markup)
        return SUBMENU
    elif query.data == 'send':
        query.edit_message_text(text='Введите текст заявки:')
        return REQUEST
    elif query.data == 'tosite':
        keyboard = [
            [InlineKeyboardButton("Масла", url='https://smartoil96.ru/Oils')],
            [InlineKeyboardButton("Присадки", url='https://www.smartoil96.ru/Oils6')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text='Выберите раздел сайта:', reply_markup=reply_markup)
        return ConversationHandler.END

# Motor oil selection handler
def motor_oil(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    brand = query.data
    with open('car_brands.json') as file:
        data = json.load(file)
        if brand in data['brands']:
            oil = data['brands'][brand]
            query.edit_message_text(text=oil)
        else:
            query.edit_message_text(text='Рекомендуемое масло для выбранной марки автомобиля не найдено.')
    return ConversationHandler.END

# Request submission handler
def request(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    user = update.effective_user
    admin_chat_id = admin_id  # Replace with the actual admin chat ID
    context.bot.send_message(chat_id=admin_chat_id, text=f"Новая заявка от пользователя {user.first_name}:\n{text}\n\nОтветить: t.me/{user.username}")
    update.message.reply_text('Ваша заявка отправлена. Мы свяжемся с вами в ближайшее время.')
    return ConversationHandler.END

# Cancel command handler
def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Отменено.')
    return ConversationHandler.END

def main() -> None:
    # Create the Updater and pass it your bot's token
    updater = Updater(bot_token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Create the conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MENU: [CallbackQueryHandler(submenu)],
            SUBMENU: [CallbackQueryHandler(motor_oil)],
            REQUEST: [MessageHandler(Filters.text & ~Filters.command, request)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Add the conversation handler to the dispatcher
    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()