#Разобраться с прокси сервером. Выдает ошибку 
#Версия модуля 13.15. Версия 20+ не давала возможность запустить бота из за разных ошибок
import logging
from telegram.ext import Updater,CommandHandler, MessageHandler,Filters 
import settings
from handlers import (greet_user,guess_number, send_cat_picture,
                      user_coordinates,talk_to_me)
logging.basicConfig(filename='bot.log', level=logging.INFO)

def main():   
    mybot = Updater(settings.API_KEY, use_context=True)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('guess',guess_number))
    dp.add_handler(CommandHandler('cat',send_cat_picture))
    dp.add_handler(MessageHandler(Filters.regex('^(Покажи котика)$'), send_cat_picture))
    dp.add_handler(MessageHandler(Filters.regex('^(Давай поиграем)$'), guess_number ))# Дать выбор из чисел для игры
    dp.add_handler(MessageHandler(Filters.regex('^(Приветствие)$'), greet_user ))
    dp.add_handler(MessageHandler(Filters.location, user_coordinates))
    dp.add_handler(MessageHandler(Filters.text,talk_to_me))
    
    
    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()
# Запустилась только после включение Юникода (utf-8). Разобраься в данном вопросе!  
if __name__ == '__main__':
    main()