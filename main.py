import telebot
from telebot import types
import sqlite3 as sqlite
import time
bot = telebot.TeleBot('5876724521:AAEdb8t0XbWe8n0ml3DavWarb_sUaz6yfvg')

with sqlite.connect('telegram.db') as db:
    cursor = db.cursor()
    
    tables = """
    CREATE TABLE IF NOT EXISTS user(
    name VARCHAR(30) NOT NULL,
    age INTEGER NOT NULL,
    description TEXT(300) NULLr
    );
    """
    cursor.executescript(tables)


@bot.message_handler(content_types=['text'])
def registration(message):

    if message.text == 'Регистрация':
            user_name_message = bot.send_message(message.chat.id, 'Напишите свое имя')
            bot.register_next_step_handler(user_name_message, get_user_name)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('Регистрация'))
        bot.send_message(message.chat.id, 'Нажмите на кнопку для продолжения "Регистрация" либо же сами напишите "Регистрация"', reply_markup=markup)


def get_user_name(message):
    if message.text == 'Регистрация':
        user_name_message = bot.send_message(message.chat.id, 'Напишите свое имя')
        bot.register_next_step_handler(user_name_message, get_user_name)

    else:
        try:
            with sqlite.connect('telegram.db') as db:
                cursor = db.cursor()
                cursor.execute("INSERT INTO user(name) VALUES(?)", [message.text])
            bot.send_message(message.chat.id, f"Твое имя: {message.text}")
            time.sleep(1.5)
            user_age = bot.send_message(message.chat.id, 'Напишите свой возраст (исключительно цифры в пределах разумного)')
            bot.register_next_step_handler(user_age, get_user_age)
        except sqlite.Error as e:
            bot.send_message(message.chat.id, e)
def get_user_age(message):
    try:
        with sqlite.connect('telegram.db') as db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO user(age) VALUES (?)", [message.text])
        bot.send_message(message.chat.id, f"Твой возраст: {message.text}")
    except sqlite.Error as e:
        bot.send_message(message.chat.id, e)

bot.polling()
