#Разобраться с прокси сервером. Выдает ошибку 
#Версия модуля 13.15. Версия 20+ не давала возможность запустить бота из за разных ошибок
from emoji import emojize
from glob import glob
import logging
from telegram.ext import Updater,CommandHandler, MessageHandler,Filters 
from random import choice, randint
import settings


logging.basicConfig(filename='bot.log', level=logging.INFO)

def greet_user(update,context):
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(f'Привет бродяга, Михалыч в здании! {context.user_data["emoji"]}')
    
def talk_to_me(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    username = update.effective_user.first_name
    text = update.message.text
    update.message.reply_text(
        f"Здравствуй, {username} {context.user_data['emoji']}! Ты написал: {text}"
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
        message = "Введите число"
    update.message.reply_text(message)

def play_random_numbers(user_number):
    bot_number = randint(user_number -10, user_number +10)
    if user_number > bot_number:
        message = f"Ваше число {user_number}, мое число {bot_number}. Вы выйграли!"
    elif user_number == bot_number:
        message =  message = f"Ваше число {user_number}, мое число {bot_number}. Ничья!"
    else:
        message =  message = f"Ваше число {user_number}, мое число {bot_number}. Вы проиграли!"
    return message

def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, use_aliases=True)
    return user_data['emoji']

def send_cat_picture(update,context):
    cat_photos_list = glob('images/cat*.jp*g')
    cat_pic_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'))

def main():   
    mybot = Updater(settings.API_KEY, use_context=True)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('guess',guess_number))
    dp.add_handler(CommandHandler('cat',send_cat_picture))
    dp.add_handler(MessageHandler(Filters.text,talk_to_me))
    
    
    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()
# Запустилась только после включение Юникода (utf-8). Разобраься в данном вопросе!  
if __name__ == '__main__':
    main()