import telebot
import openpyxl
import os, os.path

data = None

if os.path.isfile('base.xlsx'):
    data = list(openpyxl.load_workbook("base.xlsx").active.iter_rows(values_only=True))

bot = telebot.TeleBot("1543078251:AAHCkuKqo_0cjDUJe-AxS5mK7ViTukwCeLY")

@bot.message_handler(content_types=['document'])
def handle_docs_audio(message):
    chat_id = message.chat.id
    downloaded_file = bot.download_file(bot.get_file(message.document.file_id).file_path)
    with open('base.xlsx','wb') as new_file:
        new_file.write(downloaded_file)
    global data
    data = list(openpyxl.load_workbook("base.xlsx").active.iter_rows(values_only=True))
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
        bot.send_message(chat_id, pers[0][2])
    elif len(pers) > 1:
        bot.send_message(chat_id, "Found " + str(len(pers)) + " lines")
    else:
        bot.send_message(chat_id, "Not found")

bot.polling()