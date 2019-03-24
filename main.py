import traceback
import events
import psycopg2
import threading
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

conn = psycopg2.connect( "host='ec2-54-247-85-251.eu-west-1.compute.amazonaws.com'dbname='d8m4ltkkld2uie'user='dxkdifktnjbjpe'password='409b146b8f14513ee691d3a17f9918ca66623c1e97eff24f8ada5e2003360d7d'")
cursor = conn.cursor()

# cursor.execute("DROP TABLE events")
# conn.commit()

# cursor.execute("CREATE TABLE if NOT EXISTS tusers (ID SERIALIZABLE PRIMARY KEY, tid integer , subc boolean)")
# conn.commit()

cursor.execute("CREATE TABLE if NOT EXISTS events (ID varchar, title varchar, date varchar , about varchar, picture varchar, yes varchar , no varchar)")
conn.commit()

def f(f_stop):
    p = (events.GetAnnouncements())
    n = 0

    for i in p:
        try:
            n += 1
            cursor.execute('SELECT * FROM events WHERE title=%s', (i["title"],))
            title = (cursor.fetchone())
            print(n)
            print(title)

            if title is None:
                print("NOOONE")
                cursor.execute("INSERT INTO events VALUES (%s, %s, %s, %s, %s, %s, %s) ", [n, i["title"], i["date"], i["about"], i["picture"], 0, 0])
                conn.commit()

        except Exception:

            cursor.execute("ROLLBACK")
            conn.commit()
            print('Error:\n', traceback.format_exc())
            print('---------------------------------')

    conn.commit()
    if not f_stop.is_set():
        # call f() again in 100 seconds
        threading.Timer(100, f, [f_stop]).start()

@app.route("/vote", methods=['POST'])
def vote():

    data = request.get_json(force=True)
    id = data['id']
    result = data['result']

    yes = 0
    no = 0

    cursor.execute("SELECT * FROM events")
    rows = cursor.fetchall()
    for row in rows:
        yes = int(row[5])
        no = int(row[6])

    if result == "yes":
        y = 1 + yes
    else:
        y = 1 + no

    try:
        cursor.execute("UPDATE events SET " + result + " = %s WHERE id = %s", (y, id))
        conn.commit()

    except Exception:

        cursor.execute("ROLLBACK")
        conn.commit()
        print('Error:\n', traceback.format_exc())
        print('---------------------------------')

    return jsonify("OK")

@app.route("/events")
def Events():
    events = []
    try:
        cursor.execute("SELECT * FROM events")
        rows = cursor.fetchall()
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

@app.route("/")
def start():
    f_stop = threading.Event()
    # start calling f now and every 60 sec thereafter
    f(f_stop)

    return jsonify("OK")

if __name__ == '__main__':
    app.run(debug=True, port=5000)



# НЕ ЮЗАЕМ:

# def newEvent(title, date, about, picture):
#     params = (title, date, about, picture, 0, 0)
#     cursor.execute("INSERT INTO events VALUES (%s, %s, %s, %s, %s, %s)", params)
#     conn.commit()
#     return jsonify("OK")

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


# @app.route("/event/<id>", methods=['GET'])
# def getEvent(id):
#     jsn = {}
#     id = str(id)
#     print("in event", id)
#     data = str(id)
#     print('data got')
#     id = data[0]
#     print(id)
#
#     try:
#
#         cursor.execute('SELECT * FROM events WHERE id=%s', (id,))
#         print('exec')
#         data = (cursor.fetchone())
#         print(data)
#
#         jsn['id'] = data[0]
#         jsn['date'] = data[1]
#         jsn['name'] = data[2]
#         jsn['text'] = data[3]
#
#     except Exception:
#
#         cursor.execute("ROLLBACK")
#         conn.commit()
#         print('Error:\n', traceback.format_exc())
#         print('---------------------------------')

    # return jsonify(jsn)
