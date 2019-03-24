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

            if title is None:
                cursor.execute("INSERT INTO events VALUES (%s, %s, %s, %s, %s, %s, %s) ", [str(n), i["title"], i["date"], i["about"], i["picture"], 0, 0])
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

    y = 0

    data = request.get_json(force=True)
    id = data['id']
    result = data['result']

    yes = 0
    no = 0

    cursor.execute("SELECT * FROM events WHERE id=%s", id)
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


def comment(id,name,date,text):
    cursor.execute("INSERT INTO comments (id,name,date,text) VALUES(%s,%s,%s,%s)",(int(id),name,date,text))
    conn.commit()

#добавление нового комментария к записи используя id записи
@app.route("/comment",methods=['POST'])
def comm():
    data = request.get_json(force=True)
    comment(data['id'],data['name'],data['date'],data['text'])

    return jsonify({'status':'ok'})

#get all comments to this events using id of event
@app.route("/comments/<id>")
def comms(id):
    cursor.execute("SELECT * FROM comments WHERE id = %s",(int(id),))
    data = cursor.fetchall()
    return jsonify(data)

@app.route("/event/<id>")
def Event(id):

    cursor.execute("SELECT * FROM events WHERE id = %s", (id,))
    row = cursor.fetchone()
    print(row)
    rw={}

    rw['id'] = row[0]
    rw['title'] = row[1]
    rw['date'] = row[2]
    rw['about'] = row[3]
    rw['picture'] = row[4]
    rw['yes'] = row[5]
    rw['no'] = row[6]

    return jsonify(rw)

@app.route("/events")
def Events():
    events = []
    try:
        cursor.execute("SELECT * FROM events")
        rows = cursor.fetchall()
        for row in rows:
            rw = {}
            rw['id'] = str(row[0])
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