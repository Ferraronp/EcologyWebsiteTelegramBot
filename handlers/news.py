import requests

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

MAX_LEN = 3000


def print_news(update, context):
    url = 'http://127.0.0.1:8000/api/news/get_news'
    news = requests.get(url).json()[-1]
    if len(news['content']) > MAX_LEN:
        news['content'] = news['content'][:MAX_LEN] + '...'
    text = f"*{news['title']}*" + '\n' + news['content'] + '\nИсточник: ' + news['url']

    markup = InlineKeyboardMarkup([[InlineKeyboardButton(text='Предыдущая новость', callback_data=str(news['id'] - 1)),
                                    InlineKeyboardButton(text='Следующая новость', callback_data=str(news['id'] + 1))]])
    update.message.reply_text(text, reply_markup=markup, parse_mode="Markdown")


def callback(update, context):
    dict_ = update.to_dict()
    id_news = int(dict_['callback_query']['data'])
    url = 'http://127.0.0.1:8000/api/news/get_news_by_id'
    params = {"news_id": id_news}
    news = requests.get(url, params=params)
    if news.status_code == 200:
        news = news.json()
        markup = InlineKeyboardMarkup([[InlineKeyboardButton(text='Предыдущая новость', callback_data=str(news['id'] - 1)),
                                        InlineKeyboardButton(text='Следующая новость', callback_data=str(news['id'] + 1))]])
        if len(news['content']) > MAX_LEN:
            news['content'] = news['content'][:MAX_LEN] + '...'
        text = f"*{news['title']}*" + '\n' + news['content'] + '\nИсточник: ' + news['url']
        context.bot.edit_message_text(text=text,
                                      chat_id=update.effective_user['id'],
                                      message_id=dict_['callback_query']['message']['message_id'],
                                      reply_markup=markup,
                                      parse_mode="Markdown")
    else:
        markup = InlineKeyboardMarkup([[InlineKeyboardButton(text='Последняя новость', callback_data=str(id_news - 1))]])
        context.bot.edit_message_text(text='Новых новостей нет',
                                      chat_id=update.effective_user['id'],
                                      message_id=dict_['callback_query']['message']['message_id'],
                                      reply_markup=markup,
                                      parse_mode="Markdown")

