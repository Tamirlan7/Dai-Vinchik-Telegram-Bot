import telebot
from telebot import types
import sqlite3 as sqlite
import time
bot = telebot.TeleBot('5876724521:AAEdb8t0XbWe8n0ml3DavWarb_sUaz6yfvg')

# username : @TamirlanBot

with sqlite.connect('telegram.db') as db:
    cursor = db.cursor()
    
    user_table = """
    CREATE TABLE IF NOT EXISTS user(
    "id" INTEGER PRIMARY KEY,
    "telegram_id" INTEGER,    
    "name" VARCHAR(30) DEFAULT noname,
    "age" INTEGER DEFAULT 8,
    "description" TEXT(300) DEFAULT nothing
    );
    """

    cursor.executescript(user_table)


@bot.message_handler(content_types=['text'])
def registration(message):

    if message.text == 'Регистрация':
        with sqlite.connect('telegram.db') as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT telegram_id FROM user WHERE telegram_id = {message.from_user.id}")
            if cursor.fetchone() is None:
                cursor.execute(f"INSERT INTO user(telegram_id) VALUES({message.from_user.id})")
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

        with sqlite.connect('telegram.db') as db:
            cursor = db.cursor()
            cursor.execute(f"""
            UPDATE user 
            SET 'name' = {message.text} 
            WHERE 'telegram_id' = {message.from_user.id};""")
        bot.send_message(message.chat.id, f"Твое имя: {message.text}")
        time.sleep(1.5)
        user_age = bot.send_message(message.chat.id, 'Напишите свой возраст (исключительно цифры в пределах разумного)')
        bot.register_next_step_handler(user_age, get_user_age)





def get_user_age(message):
    try:
        if type(message.text) is int:
            with sqlite.connect('telegram.db') as db:
                cursor = db.cursor()
                cursor.execute(f"UPDATE user SET age = {message.text} WHERE telegram_id = {message.from_user.id}")
            bot.send_message(message.chat.id, f"Твой возраст: {message.text}")
        elif int(message.text) > 100 and int(message.text) < 7:
            bot.send_message(message.chat.id, 'Ограничение возраста от 7 до 100')
        else:
            bot.send_message(message.chat.id, 'Пишите только цифры')
    except sqlite.Error as e:
        bot.send_message(message.chat.id, e)

bot.polling()
