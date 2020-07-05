import telebot
import threading
import requests
from lxml import etree
import sqlite3
from config import BOT_TOKEN
from config import USER_TELEGRAM_ID
from config import TIMEOUT

bot = telebot.TeleBot(BOT_TOKEN)


def check():
    conn = sqlite3.connect('torrents.db')
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM exception WHERE trash = 0")
    temp = cursor.fetchall()
    excepts = []
    for t in temp:
        excepts.append(t[0])
    cursor.execute("SELECT * FROM items WHERE trash = 0")
    results = cursor.fetchall()
    for res in results:
        id = res[0]
        name = res[1]
        url = res[2]
        selector = res[3]
        value = res[4]
        r = requests.get(url=url)
        tree = etree.HTML(r.text)
        tag = tree.xpath(selector)
        if len(tag) < 1:
            continue
        text = tag[0].text
        text = text.replace("'", '"')
        if text in excepts:
            continue
        if text != value:
            sql = "update items set value = '{}' where id = {};".format(text, id)
            cursor.execute(sql)
            conn.commit()
            bot.send_message(USER_TELEGRAM_ID, "{}\n{}\n{}\n\n".format(name, text, url))
    cursor.close()
    conn.close()
    threading.Timer(TIMEOUT, check).start()

check()

