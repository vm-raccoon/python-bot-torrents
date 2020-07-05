import telebot
import threading
import requests
from lxml import etree
import sqlite3
# импорт пользовательских настроек
from config import BOT_TOKEN
from config import USER_TELEGRAM_ID
from config import TIMEOUT


# инициализация бота
bot = telebot.TeleBot(BOT_TOKEN)


# функция проверки торрент-раздач на наличие обновления
def check():
    conn = sqlite3.connect('torrents.db')
    cursor = conn.cursor()
    # выбираем список исключений (сообщение от торрент-раздачи, которое является ошибочное)
    cursor.execute("SELECT value FROM exception WHERE trash = 0")
    temp = cursor.fetchall()
    excepts = []
    for t in temp:
        excepts.append(t[0])
    # выбираем список торрент-раздач
    cursor.execute("SELECT * FROM items WHERE trash = 0")
    results = cursor.fetchall()
    for res in results:
        id = res[0]
        name = res[1]
        url = res[2]
        selector = res[3]
        value = res[4]
        # запрос на страницу торрент-раздачи по указанной ссылке
        r = requests.get(url=url)
        tree = etree.HTML(r.text)
        # выбираем из ответа узел с текстовым сообщением (индикатор обновления раздачи).
        # для каждого трекета / каждой раздачи может быть индивидуальным.
        tag = tree.xpath(selector)
        if len(tag) < 1:
            continue
        text = tag[0].text
        text = text.replace("'", '"')
        # если текст является исключением - пропуск
        if text in excepts:
            continue
        # если текст на трекере обновился - раздача обновлена
        if text != value:
            sql = "update items set value = '{}' where id = {};".format(text, id)
            cursor.execute(sql)
            conn.commit()
            bot.send_message(USER_TELEGRAM_ID, "{}\n{}\n{}\n\n".format(name, text, url))
    cursor.close()
    conn.close()
    # повторный запуск функции через таймаут
    threading.Timer(TIMEOUT, check).start()

# запуск функции проверки торрент-раздач
check()

