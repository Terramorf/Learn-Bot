from emoji import emojize
from random import choice, randint
import settings
from telegram import ReplyKeyboardMarkup,KeyboardButton




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
    
def main_keyboard():
    return ReplyKeyboardMarkup(
        [
            ['Приветствие', KeyboardButton('Мои координаты',request_location=True)] ,
            ['Покажи котика','Давай поиграем']
            ])
