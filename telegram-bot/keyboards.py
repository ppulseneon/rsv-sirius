from telebot import types

menu_keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
menu_keyboard.row(
        types.KeyboardButton('Завышенная социальная цена', ),
)
menu_keyboard.row(
        types.KeyboardButton('Социальная цена отсутствует'),
)
menu_keyboard.row(
        types.KeyboardButton('Мои заявки')
)

hide_markup = types.ReplyKeyboardRemove(selective=False)