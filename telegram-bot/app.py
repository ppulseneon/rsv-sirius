import uuid
from datetime import datetime

import telebot
from keyboards import menu_keyboard, hide_markup
from database import *
from api import *
from models.user import *

API_TOKEN = '7167879358:AAEaW8nrP_MOQTWnNUfeY-t7M6fybGVTuis'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    greeting_text = "Добрый день. Вы успешно вошли в систему."
    msg = bot.send_message(message.chat.id, greeting_text, reply_markup=hide_markup)

    bot.send_message(message.chat.id, "Пожалуйста, выберите действие:", reply_markup=menu_keyboard)
    user = User(message.chat.id)
    add_user(user)
    set_token(message.chat.id, register(message.chat.id))


@bot.message_handler(content_types=['text'])
def handle_text(message):
    user = find_user(message.chat.id)
    text = message.text

    if text == 'Завышенная социальная цена':
        msg = bot.send_message(message.chat.id, '📌 Прикрепите геолокацию магазина', reply_markup=hide_markup)
        edit_status(message.chat.id, 'overprice-geo')
        return

    if text == 'Мои заявки':
        msg = bot.send_message(message.chat.id, 'Заявки', reply_markup=hide_markup)
        applications = get_applications(user)
        for app in applications['applications']:
            msg_app = f'<b>Заявка #{app["id"]}</b>: \n\n<b>Состояние: </b>В процессе 🟡\n\n<b>Категория: </b>{app["category"]}\n\n<b>Магазин по адресу:</b> {app["shop"]["address"]}'
            bot.send_message(message.chat.id, msg_app,  parse_mode='html', reply_markup=menu_keyboard)
        return

    if text == 'Социальная цена отсутствует':
        msg = bot.send_message(message.chat.id, '📌 Прикрепите геолокацию магазина', reply_markup=hide_markup)
        edit_status(message.chat.id, 'empty-geo')
        return

    if user.action == 'overprice-geo':
        coords = message.text.split(',')
        set_coords(message.chat.id, float(coords[0]), float(coords[1][1:]))
        edit_status(message.chat.id, 'overprice-photo')
        bot.send_message(message.chat.id,
                         f'✅ Магазин был определен.')
        bot.send_message(message.chat.id,
                         f'Пришлите фотографию ценника, который по вашему мнению завышен')
        return

    if user.action == 'empty-geo':
        coords = message.text.split(',')
        set_coords(message.chat.id, float(coords[0]), float(coords[1][1:]))
        edit_status(message.chat.id, 'empty-photo')
        bot.send_message(message.chat.id,
                         f'✅ Магазин был определен.')
        bot.send_message(message.chat.id,
                         f'Пришлите фотографию стилажа, где отсутствуют товары по соц. цене')
        return

    # else
    msg = bot.send_message(message.chat.id, 'Не смог распознать команду', reply_markup=menu_keyboard)

@bot.message_handler(content_types=['location'])
def handle_location(message):
    chat_id = message.chat.id
    latitude = message.location.latitude
    longitude = message.location.longitude

    user = find_user(message.chat.id)
    if user.action == 'overprice-geo':
        set_coords(message.chat.id, latitude, longitude)
        edit_status(message.chat.id, 'overprice-photo')
        bot.send_message(chat_id,
                         f'✅ Магазин был определен.')
        bot.send_message(chat_id,
                         f'Пришлите фотографию ценника, который по вашему мнению завышен')

    if user.action == 'empty-geo':
        set_coords(message.chat.id, latitude, longitude)
        edit_status(message.chat.id, 'empty-photo')
        bot.send_message(chat_id,
                         f'✅ Магазин был определен.')
        bot.send_message(chat_id,
                         f'Пришлите фотографию продуктового стилажа, где нет социальной цены')

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user = find_user(message.chat.id)

    if user.action == 'overprice-photo':
        bot.send_message(message.chat.id, "Ваше обращение обрабатывается..")
        file_id = message.photo[-1].file_id
        file = bot.get_file(file_id)
        file_path = file.file_path

        image = f'temp/{uuid.uuid4()}.jpg'

        with open(image, 'wb') as photo:
            photo.write(requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(API_TOKEN, file_path)).content)

        image_uri = uploadPhoto(user, image)
        result = add_application(user, image_uri)

        print(result)

        code = result.get('status_code', None)

        if code == 404:
            bot.send_message(message.chat.id, f'❌ {result["detail"]}')
            return

        created_at = result["created_at"]
        date_obj = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%f")
        formatted_date = date_obj.strftime("%d.%m.%Y")

        msg_result = f'<b>ℹ️ Информация об чеке:</b>\n\n<b>Категория товара:</b> {result["category"]}\n\n<b>Цена в магазине:</b> {result["price"]} руб.\n\n<b>Допустимая цена:</b> {result["max_price"]} руб.\n\n<b>Адрес:</b> {result["shop"]["address"]}\n\n\n<i>{result["shop"]["name"]}</i>'
        msg_result_2 = f'<b>Цена социального товара оказалась выше чем допустимая.</b>\nИнформация была передана для работы. Ожидайте снижения цены.\n\n<b>Номер вашего обращения:</b> {result["id"]}\nДата обращения: {formatted_date}'

        bot.send_message(message.chat.id, msg_result, parse_mode='html')
        bot.send_message(message.chat.id, msg_result_2, parse_mode='html', reply_markup=menu_keyboard)

        edit_status(message.chat.id, None)
    if user.action == 'empty-photo':
        bot.send_message(message.chat.id, f'❌ На полке присутствуют товары по социальной цене.', reply_markup=menu_keyboard)
        edit_status(message.chat.id, None)

print('start')
bot.polling()