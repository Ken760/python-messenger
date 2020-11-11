import time
from datetime import datetime


from flask import Flask, request, abort


app = Flask(__name__)


db = [
    {
        'text': 'Hello',
        'name': 'John',
        'time': time.time()
    }, {
        'text': 'Hello too',
        'name': 'Jane',
        'time': time.time()
    }
]


@app.route("/")
def hello():
    return "Hello, World! <a href='/status'>Статистика</a>"


@app.route("/status")
def stats():
    return {
        'status': True,
        'name': 'Messenger',
        'time': datetime.now().strftime('%H:%M:%S %d/%m/%Y')
    }


@app.route("/send", methods=['POST'])
def send_message():
    if not isinstance(request.json, dict):
        return abort(400)

    text = request.json.get('text')
    name = request.json.get('name')
    if not isinstance(text, str) or not isinstance(name, str):
        return abort(400)
    if text == '' or name == '':
        return abort(400)

    db.append({
        'text': text,
        'name': name,
        'time': time.time()
    })
    return {'ok': True}


@app.route("/messages")
def get_messages():
    if 'after' in request.args:
        try:
            # проверка формата after
            after = float(request.args['after'])
        except:
            print('error')
            return abort(400)
    else:
        # дефолтное поведение
        after = 0

    filtered_db = []
    for message in db:
        if message['time'] > after:
            filtered_db.append(message)
            # pagination - чтобы возвращать сообщения
            if len(filtered_db) >= 100:
                break

    return {'messages': filtered_db}


app.run()