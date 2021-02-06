from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def gen_markup(pers):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    # markup.add(InlineKeyboardButton("Процессор", callback_data="cb_cpu"),
    #            InlineKeyboardButton("Оперативная память", callback_data="cb_ram"),
    #            InlineKeyboardButton("Материнская плата", callback_data="cb_mp"),
    #            InlineKeyboardButton("SSD", callback_data="cb_ssd"),
    #            InlineKeyboardButton("HDD", callback_data="cb_hdd"),
    #            InlineKeyboardButton("Блок питания", callback_data="cb_psu"),
    #            InlineKeyboardButton("Кулер", callback_data="cb_cooler"),
    #            InlineKeyboardButton("Корпус", callback_data="cb_case"),
    #            InlineKeyboardButton("Монитор", callback_data="cb_monitor"),
    #            )
    for i in pers:
        markup.add(InlineKeyboardButton(i[0], callback_data=i[0]))
    return markup