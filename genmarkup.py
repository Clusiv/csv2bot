from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def gen_markup(pers):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    for i in pers:
        markup.add(InlineKeyboardButton(str(i[0]) + ':' + i[1], callback_data=i[0]))
    return markup

