import telegram
bot = telegram.Bot(token='829992269:AAHyL9GAswU2aGi7FzlRB9ORCEweVDU-hB4')
chat_id = '@486441898,'
# тест новости
chat_text = 'Новая новость на <a href="http://здесь-урл-сайта.ru">сайте</a>:\n <b>{}</b>'.format(h2s[k])
# отправка поста в канал. Маленькая тонкость - используется HTML разметка
bot.send_message(chat_id=chat_id, text=chat_text, parse_mode=telegram.ParseMode.HTML)

