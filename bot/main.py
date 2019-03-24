import json
import traceback
from datetime import datetime
import psycopg2
import requests
import telebot
import configs

bot = telebot.TeleBot(configs.token)
print("Get me:\n", bot.get_me(), "==========")
def log(message, answer):
    print("----------")
    print(datetime.now())
    print("{0} {1}, {2}, {3}\n{4}\n{5}".format(
        message.from_user.first_name,
        message.from_user.last_name,
        message.from_user.username,
        message.from_user.id,
        message.text,
        answer))

def adduser(uid):
    bconn = psycopg2.connect(configs.database)
    bcursor = bconn.cursor()

    bcursor.execute("CREATE TABLE if NOT EXISTS tusers (tid integer , subc integer)")
    bconn.commit()
    try:
        bcursor.execute("SELECT tid FROM tusers")
        rows = bcursor.fetchall()
        isin = False
        for row in rows:
            if uid in row:
                isin = True
        if not isin:
            bcursor.execute("INSERT INTO tusers VALUES (%s, %s)", [uid, 0])
            bconn.commit()
        bcursor.execute("SELECT * FROM tusers")
        rows = bcursor.fetchall()
        print(rows)
        bconn.close()

    except Exception:
        bcursor.execute("ROLLBACK")
        bconn.commit()
        print('Error:\n', traceback.format_exc())
        print('---------------------------------')
        bconn.close()

@bot.message_handler(commands=['start'])
def handle_text(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True)
    replybutton1 = telebot.types.KeyboardButton("Последнее событие в списке")
    replybutton2 = telebot.types.KeyboardButton("Последние 5 событий в списке")
    user_markup.row(replybutton1)
    user_markup.row(replybutton2)
    answer = "Привет!"
    bot.send_message(message.chat.id, answer, reply_markup=user_markup)
    log(message, answer)
    adduser(message.chat.id)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    global y
    global n
    if message.text == "Последнее событие в списке":
        response = requests.get("https://politex.herokuapp.com/events")
        answer = ""
        for i in response.json():
            if i["id"]=="1":
                answer = "Название: " + i["title"]
                answer = answer + "\nДата: " + i["date"]
                answer = answer + "\n\nОписание: " + i["about"]
                y = i["yes"]
                n = i["no"]
        my_inline = telebot.types.InlineKeyboardMarkup(True)
        btn = [telebot.types.InlineKeyboardButton(text="Иду (" + str(y) + ")", callback_data="yes"), telebot.types.InlineKeyboardButton(text="Не иду (" + str(n) + ")", callback_data="no")]
        my_inline.row(*btn)
        bot.send_photo(message.chat.id, "https://www.spbstu.ru/upload/resize_cache/iblock/89f/248_166_2/250.jpg", answer, reply_markup=my_inline)
        log(message, answer)
    elif message.text == "Последние 5 событий в списке":
        response = requests.get("https://politex.herokuapp.com/events")
        answer = ""
        for c in range(5):
            for i in response.json():
                if i["id"]==str(c):
                    answer = answer + "Название: " + i["title"]
                    answer = answer + "\nДата: " + i["date"]
                    answer = answer + "\nОписание: " + i["about"] + "\n\n"
        bot.send_message(message.chat.id, answer)
        log(message, answer)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "yes":
            payload = {"id": "1", "result": "yes"}
            print(requests.post("https://politex.herokuapp.com/vote", data=json.dumps(payload)))
            my_inline = telebot.types.InlineKeyboardMarkup(True)
            my_inline.row(telebot.types.InlineKeyboardButton(text="ok", callback_data="pass"))
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          reply_markup=my_inline)
        if call.data == "no":
            payload = {"id": "1", "result": "no"}
            print(requests.post("https://politex.herokuapp.com/vote", data=json.dumps(payload)))
            my_inline = telebot.types.InlineKeyboardMarkup(True)
            my_inline.row(telebot.types.InlineKeyboardButton(text="ok", callback_data="pass"))
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          reply_markup=my_inline)
        if call.data == "pass":
            pass

@bot.message_handler(content_types=['audio', 'video', 'document', 'photo', 'sticker'])
def handle_text(message):
    answer = vars.answers["nottext"]
    bot.send_message(message.chat.id, answer)
    log(message, answer)

if __name__ == "__main__":
    y = "0"
    n = "0"
    bot.polling(none_stop=True)