from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

testUser = {"name": 'shj', 'age': "18", 'event': 'hackton'}
users = {'2': testUser}

events = {}

# save data with deleting
# json.dump(users,open("data/users.json","w"))


conn = psycopg2.connect(
    "host='ec2-54-247-85-251.eu-west-1.compute.amazonaws.com'dbname='d8m4ltkkld2uie'user='dxkdifktnjbjpe'password='409b146b8f14513ee691d3a17f9918ca66623c1e97eff24f8ada5e2003360d7d'")
cursor = conn.cursor()

cursor.execute("CREATE TABLE if NOT EXISTS events (id INTEGER PRIMARY KEY ,data varchar, name varchar ,text varchar )")
conn.commit()

@app.route("/")
def hi():
    return "hello world!"

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


@app.route("/getDB", methods=['POST'])
def getDB():
    return jsonify(cursor.fetchall())

@app.route("/getList", methods=['POST'])
def getList():
    return jsonify(cursor.execute("select id,name,data from events"))

@app.route("/getEvent", methods=['POST'])
def getEvent():
    id = request.get_gson(force=True)['id']
    return jsonify(cursor.execute("select * from events where id = " + str(id)))

app.route("/")
def start():
    return "hello world!"

if __name__ == '__main__':
    app.run(debug=True, port=5000)