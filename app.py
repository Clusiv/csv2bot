import telebot
import openpyxl
import os, os.path
from genmarkup import gen_markup
from clear_col import clear_col, load_wb, get_ws

def msg(pers):
    print(pers)
    _msg = f"ФИО: <b>{pers[0][0]}<b> \nДокумент: {pers[0][1]}\nСальдо: {pers[0][2]}p"
    return _msg

data = None
def get_data(ws):
    return list(ws.iter_rows(values_only=True, min_row=2))

if os.path.isfile('base.xlsx'):
    data = get_data(clear_col())

bot = telebot.TeleBot("1543078251:AAHCkuKqo_0cjDUJe-AxS5mK7ViTukwCeLY")

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Downloading to server...")
    downloaded_file = bot.download_file(bot.get_file(message.document.file_id).file_path)
    with open('base.xlsx','wb') as new_file:
        new_file.write(downloaded_file)
    global data
    data = get_data(clear_col())
    print(data[0][0])
    bot.send_message(chat_id, "Found " + str(len(data) - 2) + " lines")

start = """
Этот бот для поиска сальдо по фамилии.
Отправьте фамилию и бот пришлет Сальдо
Отправьте новый файл таблицы, для обновления данных"""

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, start)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # print(data)
    chat_id = message.chat.id
    pers = [x for x in data if message.text in x[0]]
    if pers and len(pers) == 1:
        # print(pers)
        bot.send_message(chat_id, msg(pers), parse_mode='html')
    elif len(pers) > 1:
        print("##################")
        print(pers)
        bot.send_message(chat_id, "Found " + str(len(pers)) + " lines", reply_markup=gen_markup(pers))
    else:
        bot.send_message(chat_id, "Not found")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.from_user.id
    pers = [x for x in data if call.data in x[0]]
    # print(pers)
    bot.send_message(chat_id, msg(pers))
bot.polling()