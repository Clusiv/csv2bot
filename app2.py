import telebot
import openpyxl
import os, os.path
from genmarkup import gen_markup
from clear_col import clear_col, load_wb, get_ws
import resource
from telegram_bot_pagination import InlineKeyboardPaginator
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

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

def get_data(ws):
    return list(ws.iter_rows(values_only=True, min_row=2))
print(using('Before'))
if os.path.isfile('base.xlsx'):
    data = get_data(clear_col())
    # print(data[0][3])

bot = telebot.TeleBot("1543078251:AAHCkuKqo_0cjDUJe-AxS5mK7ViTukwCeLY")

print(using('After'))


@bot.message_handler(content_types=['document'])
def handle_docs(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Downloading to server...")
    downloaded_file = bot.download_file(bot.get_file(message.document.file_id).file_path)
    with open('base.xlsx','wb') as new_file:
        new_file.write(downloaded_file)
    global data
    data = get_data(clear_col())
    # print(data[0][3])
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
    global pers
    chat_id = message.chat.id
    pers = [x for x in data if message.text in x[1]]

    if pers and len(pers) == 1:
        # print(pers)
        bot.send_message(chat_id, msg(pers[0]), parse_mode='html')
    else:
        send_character_page(message, pers)
    # elif len(pers) > 1 and  len(pers) < 6:
    #     # print("##################")
    #     # print(pers)
    #     for p in pers:
    #         msg
    #     bot.send_message(chat_id, "Найдено " + str(len(pers)) + " позиций", reply_markup=gen_markup(pers))
    # elif len(pers) >= 6:
    #     bot.send_message(chat_id, "Найден " + str(len(pers)) + " позиций\n")
    # else:
    #     bot.send_message(chat_id, "Ничего не найдено")

@bot.callback_query_handler(func=lambda call: 'pers' in call.data)
def callback_query(call):
    print('callback_query call.data: ' + str(call.data))
    _id = int(call.data.split(':')[1])
    # print(type(_id))
    chat_id = call.from_user.id
    # print(data[0][3])
    pers = [x for x in data if _id == x[0]]
    # print(pers)
    bot.send_message(chat_id, msg(pers[0]))
    print(using('Call'))

@bot.callback_query_handler(func=lambda call: call.data.split('#')[0]=='character')
def characters_page_callback(call):

    print('characters_page_callback call.data ' + str(call.data))

    page = int(call.data.split('#')[1])
    bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )

    # print('characters_page_callback pers: ' + str(pers))
    global pers
    send_character_page(call.message, pers, page)

def send_character_page(message, pers, page=1):
    # print(pers)
    paginator = InlineKeyboardPaginator(
        len(pers)//3 + 1,
        current_page=page,
        data_pattern='character#{page}'
    )

    for i in pers[3 * (page - 1):3 * page]:
        # paginator.add_before(InlineKeyboardButton(str(i[0]) + ':' + i[1], callback_data='character#{i}'))
        paginator.add_before(InlineKeyboardButton(str(i[0]) + ':' + i[1], callback_data=f'pers:{i[0]}'))

    paginator.add_after(InlineKeyboardButton('Go back', callback_data='back'))

    print(page)
    
    bot.send_message(
        message.chat.id,
        msg(pers[page-1]),
        # character_pages[page:page-1],
        reply_markup=paginator.markup,
        parse_mode='Markdown'
    )


bot.polling()