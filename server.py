from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World! <a href='/stats'>Статистика</a>"


@app.route("/stats")
def stats():
    return {
        'messages_count': 500
    }



app.run()