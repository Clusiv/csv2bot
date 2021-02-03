import telebot
import openpyxl

wb = openpyxl.load_workbook("base.xlsx")
ws = wb.active

data = list(ws.iter_rows(values_only=True))

bot = telebot.TeleBot("1543078251:AAHCkuKqo_0cjDUJe-AxS5mK7ViTukwCeLY")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    chat_id = message.chat.id
    pers = [x for x in data if message.text in x[0]]
    if pers and len(pers) == 1:
        print(pers)
        bot.send_message(chat_id, pers[0][2])
    elif len(pers) > 1:
        bot.send_message(chat_id, ''.join(pers))
    else:
        bot.send_message(chat_id, "Not found")
bot.polling()   