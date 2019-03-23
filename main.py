import traceback
import events
import time
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

conn = psycopg2.connect("host='ec2-54-247-85-251.eu-west-1.compute.amazonaws.com'dbname='d8m4ltkkld2uie'user"
                        "='dxkdifktnjbjpe'password='409b146b8f14513ee691d3a17f9918ca66623c1e97eff24f8ada5e2003360d7d"
                        "'")
cursor = conn.cursor()

cursor.execute("DROP TABLE events")

cursor.execute(
    "CREATE TABLE if NOT EXISTS events (ID SERIAL PRIMARY KEY , title varchar, date varchar , about varchar, picture varchar, yes integer, no integer)")
conn.commit()


def newEvent(title, date, about, picture):
    params = (title, date, about, picture, 0, 0)
    cursor.execute("INSERT INTO events VALUES (%s, %s, %s, %s, %s, %s)", params)
    conn.commit()
    return jsonify("OK")

@app.route("/events")
def getList():
    try:
        cursor.execute("SELECT * FROM events")
        rows = cursor.fetchall()
        events = []
        for row in rows:
            rw = {}
            rw['id'] = row[0]
            rw['title'] = row[1]
            rw['date'] = row[2]
            rw['about'] = row[3]
            rw['picture'] = row[4]
            rw['yes'] = row[5]
            rw['no'] = row[6]
            events.append(rw)

    except Exception:

        cursor.execute("ROLLBACK")
        conn.commit()
        print('Error:\n', traceback.format_exc())
        print('---------------------------------')

    return jsonify(events)


@app.route("/event/<id>", methods=['GET'])
def getEvent(id):
    jsn = {}
    id = str(id)
    print("in event", id)
    data = str(id)
    print('data got')
    id = data[0]
    print(id)

    try:

        cursor.execute('SELECT * FROM events WHERE id=%s', (id,))
        print('exec')
        data = (cursor.fetchone())
        print(data)

        jsn['id'] = data[0]
        jsn['date'] = data[1]
        jsn['name'] = data[2]
        jsn['text'] = data[3]

    except Exception:

        cursor.execute("ROLLBACK")
        conn.commit()
        print('Error:\n', traceback.format_exc())
        print('---------------------------------')

    return jsonify(jsn)

@app.route("/")
def start():
    cursor.execute(
        "INSERT INTO EVENTS (data,name,text) VALUES ('12.05.2018','SOME EVENT','WQERXTCFGKVLUKDJYCKLILHKUTGHKDT')")
    conn.commit()

    return jsonify("чейкате доки в беседе")

if __name__ == '__main__':
    app.run(debug=True, port=5000)

    def executeSomething():
        print(events.GetAnnouncements())
        time.sleep(10)

    while True:
        executeSomething()

# НЕ ЮЗАЕМ, ГОВНОКОД:

# @app.route("/all", methods=['GET'])
# def getDB():
#     try:
#         cursor.execute("SELECT * FROM events")
#         rows = cursor.fetchall()
#         all = []
#         for row in rows:
#             all.append(row)
#
#     except Exception:
#         cursor.execute("ROLLBACK")
#         conn.commit()
#
#         print('Error:\n', traceback.format_exc())
#         print('---------------------------------')
#         all = 'error'
#
#     return jsonify(
#         {
#             'events': all
#         }
#     )
