# Разобраться с прокси сервером. Выдает ошибку
# Версия модуля 13.15
# Версия 20+ не давала возможность запустить, бота из за разных ошибок
from anketa import (anketa_start, anketa_name, anketa_rating,
                    anketa_comment, anketa_skip, anketa_dontknow)
import logging
import pytz
from datetime import time
from telegram.ext.jobqueue import Days
from telegram.bot import Bot
from telegram.ext import messagequeue as mq
from telegram.utils.request import Request
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          Filters, ConversationHandler)
import settings
from jobs import send_updates
from handlers import (greet_user, guess_number, send_cat_picture,
                      user_coordinates, talk_to_me, check_user_photo,
                      subscribe, unsubscribe, set_alarm)


logging.basicConfig(filename='bot.log', level=logging.INFO)


class MQBot(Bot):
    def __init__(self, *args, is_queued_def=True, msg_queue=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = msg_queue or mq.MessageQueue()

    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass

    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        return super().send_message(*args, **kwargs)


def main():
    request = Request(con_pool_size=8)
    bot = MQBot(settings.API_KEY, request=request)
    mybot = Updater(bot=bot, use_context=True)

    jq = mybot.job_queue
    target_time = time(12, 0, tzinfo=pytz.timezone('Europe/Moscow'))
    target_days = (Days.MON, Days.WED, Days.FRI)
    jq.run_daily(send_updates, target_time, target_days)
    jq.run_repeating(send_updates, interval=10, first=0)

    dp = mybot.dispatcher
    anketa = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Заполнить анкету)$'), anketa_start)
            ],
        states={
            'name': [MessageHandler(Filters.text, anketa_name)],
            'rating': [
                MessageHandler(Filters.regex('^(1|2|3|4|5)$'), anketa_rating)
                ],
            'comment': [
                CommandHandler('skip', anketa_skip),
                MessageHandler(Filters.text, anketa_comment)
            ]
            },
        fallbacks=[
            MessageHandler(Filters.text | Filters.video | Filters.document |
                           Filters.location, anketa_dontknow)
        ]
    )
    dp.add_handler(anketa)
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('guess', guess_number))
    dp.add_handler(CommandHandler('cat', send_cat_picture))
    dp.add_handler(CommandHandler('subscribe', subscribe))
    dp.add_handler(CommandHandler('unsubscribe', unsubscribe))
    dp.add_handler(CommandHandler('alarm', set_alarm))
    dp.add_handler(MessageHandler(Filters.regex('^(Покажи котика)$'),
                                  send_cat_picture))
    dp.add_handler(MessageHandler(Filters.regex('^(Давай поиграем)$'),
                                  guess_number))
    dp.add_handler(MessageHandler(Filters.photo, check_user_photo))
    dp.add_handler(MessageHandler(Filters.location, user_coordinates))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()
# Запустилась только после включение Юникода (utf-8).
# Разобраься в данном вопросе!


if __name__ == '__main__':
    main()
