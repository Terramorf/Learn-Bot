from db import db, get_or_create_user, subscribe_user, unsubscribe_user
from glob import glob
from jobs import alarm
import os
from random import choice
from utils import play_random_numbers, main_keyboard


def greet_user(update, context):
    user = get_or_create_user(
        db, update.effective_user, update.message.chat.id
        )
    print("Кто-то ввалился в хату")
    update.message.reply_text(
        f'Привет бродяга, Михалыч в здании! {user["emoji"]}',
        reply_markup=main_keyboard()
    )


def talk_to_me(update, context):
    user = get_or_create_user(
        db, update.effective_user, update.message.chat.id
        )
    username = update.effective_user.first_name
    text = update.message.text
    update.message.reply_text(
        f"Здравствуй,{username} {user['emoji']}! Ты написал: {text}",
        reply_markup=main_keyboard()
    )


def guess_number(update, context):
    print(context.args)
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except (TypeError, ValueError):
            message = 'Введите целое число'
    else:
        message = "Напиши мне /guess и любое число. Например /guess 10"
    update.message.reply_text(message, reply_markup=main_keyboard())


def send_cat_picture(update, context):
    cat_photos_list = glob('images/cat*.jp*g')
    cat_pic_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'),
                           reply_markup=main_keyboard())


def user_coordinates(update, context):
    user = get_or_create_user(
        db, update.effective_user, update.message.chat.id
        )
    coords = update.message.location
    update.message.reply_text(
        f"Ваши координаты {coords} {user['emoji']}!",
        reply_markup=main_keyboard()
    )


def check_user_photo(update, context):
    update.message.reply_text('Обрабатываем фото')
    os.makedirs('downloads', exist_ok=True)
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    file_name = os.path.join('downloads',
                             f'{update.message.photo[-1].file_id}.jpg')
    photo_file.download(file_name)
    update.message.reply_text('Файл сохранен')


def subscribe(update, context):
    user = get_or_create_user(
        db, update.effective_user, update.message.chat.id
        )
    subscribe_user(db, user)
    update.message.reply_text('Ты теперь член семьи, Добро пожаловать!')


def unsubscribe(update, context):
    user = get_or_create_user(
        db, update.effective_user, update.message.chat.id
        )
    unsubscribe_user(db, user)
    update.message.reply_text('Не забывай про семью. Прощай!')


def set_alarm(update, context):
    try:
        seconds = abs(int(context.args[0]))
        context.job_queue.run_one(alarm, seconds,
                                  context=update.message.chat.id)
        update.messgage.reply_text(f'Чудо произойдет через {seconds} секунд')
    except (ValueError, TypeError):
        update.messgage.reply_text('Введите целое число секунд после команды')
