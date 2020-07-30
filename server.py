from telegram.ext import Updater, CommandHandler
import logging
import requests
import os


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def exception_worker(func):
    """ Общая обработка ошибок методов бота """
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(str(e))
    return wrapper


def get_message_by_args(args):
    """ Склеить фразу из переданных аргументов """
    message = ''
    for word in args:
        message = message + ' ' + str(word)
    return message if message else False


def start(update, context):
    """ Обработчик команды /start """
    update.message.reply_text('Хехееей! Используй команды бота и веселись :)')


@exception_worker
def get_cat(update, context):
    """ Получение рандомной картинки с котом """
    with open('cat.jpg', 'wb') as f:
        f.write(requests.get('https://cataas.com/cat').content)
    update.message.reply_photo(photo=open('cat.jpg', 'rb'))


@exception_worker
def get_cat_gif(update, context):
    """ Получение рандомной гифки с котом """
    with open('cat.gif', 'wb') as f:
        f.write(requests.get('https://cataas.com/cat/gif').content)
    update.message.reply_animation(open('cat.gif', 'rb'))


@exception_worker
def get_cat_gif_say(update, context):
    """ Получение гифки с надписью """
    message = get_message_by_args(context.args)
    if not message:
        return update.message.reply_text('После команды напиши фразу. Пример:\n\n /say_gif Проверка')
    with open('cat.gif', 'wb') as f:
        f.write(requests.get('https://cataas.com/cat/gif/says/{}'.format(message)).content)
    update.message.reply_animation(open('cat.gif', 'rb'))


@exception_worker
def get_cat_say(update, context):
    """ Получение картинки с надписью """
    message = get_message_by_args(context.args)
    if not message:
        return update.message.reply_text('После команды напиши фразу. Пример:\n\n /say Проверка')
    with open('cat.jpg', 'wb') as f:
        f.write(requests.get('https://cataas.com/cat/says/{}'.format(message)).content)
    update.message.reply_photo(open('cat.jpg', 'rb'))


def main():
    updater = Updater(os.getenv('BOT_ID'), use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", start))
    dp.add_handler(CommandHandler("photo", get_cat))
    dp.add_handler(CommandHandler("say", get_cat_say,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=False))
    dp.add_handler(CommandHandler("gif", get_cat_gif))
    dp.add_handler(CommandHandler("say_gif", get_cat_gif_say,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=False))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
