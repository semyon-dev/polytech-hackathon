import traceback

from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(
    "host='ec2-54-247-85-251.eu-west-1.compute.amazonaws.com'dbname='d8m4ltkkld2uie'user='dxkdifktnjbjpe'password='409b146b8f14513ee691d3a17f9918ca66623c1e97eff24f8ada5e2003360d7d'")
cursor = conn.cursor()

# cursor.execute("DROP TABLE events")

cursor.execute("CREATE TABLE if NOT EXISTS events (ID SERIAL PRIMARY KEY ,data varchar, name varchar ,text varchar )")
conn.commit()

@app.route("/newEvent", methods=['POST'])
def newUser():
    global count
    sl = "\'"
    zp = ","
    data = request.get_json(force=True)
    name = data['name']
    data = data['data']
    text = data['text']

    cursor.execute(
        "insert into events (data,name,text) values (" + sl + name + sl + zp + sl + data + sl + zp + sl + text + sl + ")")
    conn.commit()
    count += 1
    return "OK"


@app.route("/all", methods=['GET'])
def getDB():
    try:
        cursor.execute("SELECT * FROM events")
        rows = cursor.fetchall()
        all_users = []
        for row in rows:
            all_users.append(row)

    except Exception:
        cursor.execute("ROLLBACK")
        conn.commit()

        print('Error:\n', traceback.format_exc())
        print('---------------------------------')
        all_users = 'error'

    return jsonify(
        {
            'users': all_users
        }
    )

@app.route("/events", methods=['GET'])
def getList():
    return jsonify(cursor.execute("select id,name,data from events"))

@app.route("/event", methods=['POST'])
def getEvent():
    id = request.get_gson(force=True)['id']
    return jsonify(cursor.execute("select * from events where id = " + str(id)))

@app.route("/")
def start():

    cursor.execute(
    "INSERT INTO EVENTS (data,name,text) VALUES ('12.05.2018','SOME EVENT','WQERXTCFGKVLUKDJYCKLILHKUTGHKDT')")
    conn.commit()

    return "чейкате доки в беседе"

if __name__ == '__main__':
    app.run(debug = True, port = 5000)