import os, os.path
import resource
# import logging
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telegram_bot_pagination import InlineKeyboardPaginator
import openpyxl
from table_tools import get_data
from config import *

# logging.basicConfig(filename='current.log', encoding='utf-8', level=logging.CRITICAL)


# def using(point=""):
#     usage=resource.getrusage(resource.RUSAGE_SELF)
#     return '''%s: usertime=%s systime=%s mem=%s mb
#            '''%(point,usage[0],usage[1],
#                 usage[2]/1024.0 )

def msg(pers):
    # print(pers)
    _msg = f"ФИО: {pers[1]}\nДокумент: {pers[2]}\nСальдо: {pers[3]}p"
    return _msg

pers = None
data = None

# print(using('Before'))

if os.path.isfile('base.xlsx'):
    data = get_data()

bot = telebot.TeleBot(TOKEN)

# print(using('After'))

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Загрузка на серве...")
    downloaded_file = bot.download_file(bot.get_file(message.document.file_id).file_path)
    with open('base.xlsx','wb') as new_file:
        new_file.write(downloaded_file)
    global data
    data = get_data()
    bot.send_message(chat_id, "Найдено " + str(len(data) - 2) + " строк")

start = """
Этот бот для поиска сальдо по фамилии.
Отправьте фамилию и бот пришлет Сальдо
Отправьте новый файл таблицы, для обновления данных.

Формат таблицы:
2 Столбец - Адресат операции
6 Столбец - Основной документ
9 Столбец - Сальдо общее
Первые две строки пропускаются из-за информации о столбцах.
Бот ожидает увидеть именно эти столбцы именно в таком порядке.

Узнать свой id /idme
Добавить 
"""

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, start)

@bot.message_handler(func=lambda message: True)
def echo_all(message):

    chat_id = message.chat.id
    print(chat_id)
    if chat_id not in CHAT_ID:
        bot.send_message(chat_id, 'Неавторизован')
        return
    if message.text.isnumeric():
        bot.send_message(chat_id, 'Пришлите ФИО или часть от них')
        return
    global data
    if not data:
        bot.send_message(chat_id, 'База пуста, отправьте файл. Информация /start')
        return
    
    global pers
    # Если два чат айди сделают поиск, то один перезапишет этот список на другой.
    # Придется создать словарь из чатид:список
    pers = [x for x in data if message.text in x[1]]

    if pers and len(pers) == 1:
        # print(pers)
        bot.send_message(chat_id, msg(pers[0]), parse_mode='html')
    elif pers and len(pers) > 1:
        send_character_page(message)
    else:
        bot.send_message(chat_id, 'Ничего не найдено')

@bot.callback_query_handler(func=lambda call: 'pers' in call.data)
def callback_query(call):
    chat_id = call.from_user.id
    global data
    if not data:
        bot.send_message(chat_id, 'База пуста, отправьте файл. Информация /start')
        return
    
    print('callback_query call.data: ' + str(call.data))
    # bot.delete_message(call.message.chat.id, call.message.message_id - 1)
    _id = int(call.data.split(':')[1])
    pers = [x for x in data if _id == x[0]]
    bot.send_message(chat_id, msg(pers[0]))
    # print(using('Call'))

@bot.callback_query_handler(func=lambda call: call.data.split('#')[0]=='character')
def characters_page_callback(call):

    print('characters_page_callback call.data ' + str(call.data))

    page = int(call.data.split('#')[1])
    bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )
    
    send_character_page(call.message, page)

def send_character_page(message, page=1):
    # print(pers)
    chat_id = message.chat.id
    global pers
    if not pers:
        bot.send_message(chat_id, 'База пуста, отправьте файл. Информация /start')
        return
    paginator = InlineKeyboardPaginator(
        len(pers)//6 + 1,
        current_page=page,
        data_pattern='character#{page}'
    )

    for i in pers[6 * (page - 1):6 * page]:
        paginator.add_before(InlineKeyboardButton(str(i[0]) + ':' + i[1], callback_data=f'pers:{i[0]}'))

    print(page)
    
    bot.send_message(
        message.chat.id,
        msg(pers[page-1]),
        reply_markup=paginator.markup,
        parse_mode='Markdown'
    )

bot.polling()