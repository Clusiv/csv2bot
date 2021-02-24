#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import logging
import time
import flask
import telebot
import os.path
import resource
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telegram_bot_pagination import InlineKeyboardPaginator
import openpyxl
from table_tools import get_data
from config import *

API_TOKEN = TOKEN

WEBHOOK_HOST = IP
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Path to the ssl private key

# Quick'n'dirty SSL certificate generation:
#
# openssl genrsa -out webhook_pkey.pem 2048
# openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem
#
# When asked for "Common Name (e.g. server FQDN or YOUR name)" you should reply
# with the same value in you put in WEBHOOK_HOST

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(API_TOKEN)

app = flask.Flask(__name__)

# Empty webserver index, return nothing, just http 200
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'Hello'

# Process webhook calls
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

clients = {}

def using(point=""):
    usage=resource.getrusage(resource.RUSAGE_SELF)
    return '''%s: usertime=%s systime=%s mem=%s mb
           '''%(point,usage[0],usage[1],
                usage[2]/1024.0 )

def msg(pers):
    # print(pers)
    _msg = f"ФИО: {pers[1]}\nДокумент: {pers[2]}\nСальдо: {pers[3]}p"
    return _msg

pers = None
data = None

print(using('Before'))

if os.path.isfile('base.xlsx'):
    data = get_data()

print(using('After'))

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    chat_id = message.chat.id
    if chat_id not in ADMIN_CHAT_ID:
        bot.send_message(chat_id, 'Неавторизован')
        return
    bot.send_message(chat_id, "Загрузка на сервер...")
    downloaded_file = bot.download_file(bot.get_file(message.document.file_id).file_path)
    with open('base.xlsx','wb') as new_file:
        new_file.write(downloaded_file)
    global data
    data = get_data()
    bot.send_message(chat_id, "Найдено " + str(len(data) - 2) + " строк")
    print(using('File imported'))

start = """
Этот бот для поиска задолженности по арендным платежам 
за земельные участки в Курчалоевском районе.
Отправьте Фамилию (с большой буквы) и бот пришлет сумму оплаты.
"""

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, start)

@bot.message_handler(commands=['clients'])
def send_clients(message):
    if chat_id not in ADMIN_CHAT_ID:
        bot.reply_to(message, 'Неавторизован')
        return
    bot.reply_to(message, len(clients))

@bot.message_handler(func=lambda message: True)
def echo_all(message):

    chat_id = message.chat.id
    print(chat_id)
    global clients
    
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
    clients[chat_id] = pers
    if pers and len(pers) == 1:
        # print(pers)
        bot.send_message(chat_id, msg(pers[0]), parse_mode='html')
        print(using('Info sent'))
    elif pers and len(pers) > 1:
        send_character_page(message)
        print(using('Paginator sent'))
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
    global clients
    if not clients[chat_id]:
        bot.send_message(chat_id, 'База пуста, отправьте файл. Информация /start')
        return
    paginator = InlineKeyboardPaginator(
        len(clients[chat_id])//6 + 1,
        current_page=page,
        data_pattern='character#{page}'
    )

    for i in clients[chat_id][6 * (page - 1):6 * page]:
        paginator.add_before(InlineKeyboardButton(str(i[0]) + ':' + i[1], callback_data=f'pers:{i[0]}'))

    print(page)
    
    bot.send_message(
        message.chat.id,
        msg(clients[chat_id][page-1]),
        reply_markup=paginator.markup,
        parse_mode='Markdown'
    )

# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()

time.sleep(0.5)

# Set webhook
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

if os.path.isfile('./app.pid'):
    print('Bot is already running. Run ./stop.sh to stop current bot.')
    sig = getattr(signal, "SIGKILL", signal.SIGTERM)
    os.kill(os.getpid(), sig)
else:
    PID = str(os.getpid())
    with open('./app.pid', 'w') as file:
        file.write(PID)
    # Start flask server
    app.run(host=WEBHOOK_LISTEN,
            port=WEBHOOK_PORT,
            ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV),
            debug=True)
