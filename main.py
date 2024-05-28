import logging

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from handlers.news import print_news, callback

logging.basicConfig(filename='logs.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')


def main():
    token = open('parametrs.txt', mode='r').read()
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("news", print_news, run_async=True))
    dp.add_handler(CallbackQueryHandler(callback, run_async=True))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        pass
