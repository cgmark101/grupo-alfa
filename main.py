from flask import Flask, render_template
from image import get_personal
from tinydb import TinyDB

db = TinyDB('db.json')

app = Flask(__name__)

@app.route("/")
def index():
    img = db.all()
    data = []
    for i in img:
        if len(i) != 0:
            data.append({
                'url':i['url'],
                'nombre':i['nombre'],
                'cargo':i['cargo'],
            })
    return render_template('index.html', data=data) 

@app.route("/404.html")
def error():
    return render_template("404.html")

if __name__ == "__main__":
    app.run(port=8000)