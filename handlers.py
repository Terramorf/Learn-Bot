from glob import glob
from random import choice
from utils import get_smile, play_random_numbers, main_keyboard
def greet_user(update,context):
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(
        f'Привет бродяга, Михалыч в здании! {context.user_data["emoji"]}',
        reply_markup = main_keyboard()
    )

def talk_to_me(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    username = update.effective_user.first_name
    text = update.message.text
    update.message.reply_text(
        f"Здравствуй, {username} {context.user_data['emoji']}! Ты написал: {text}", 
        reply_markup = main_keyboard()
    )

def guess_number(update,context):
    print(context.args)
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except(TypeError,ValueError):
            message = 'Введите целое число'
    else:
        message = "Напиши мне /guess и любое число. Например /guess 10"
    update.message.reply_text(message, reply_markup = main_keyboard())

def send_cat_picture(update,context):
    cat_photos_list = glob('images/cat*.jp*g')
    cat_pic_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'),reply_markup = main_keyboard())
    
def user_coordinates(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    coords = update.message.location
    update.message.reply_text(
        f"Ваши координаты {coords} {context.user_data['emoji']}!",
        reply_markup=main_keyboard()
    )
    