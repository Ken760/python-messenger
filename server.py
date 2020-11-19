import time
from datetime import datetime
from flask import Flask, request, abort

app = Flask(__name__)

db = [
    {
        'text': 'Hello',
        'name': 'None ',
        'time': time.time()
    }
]

format_date = '%d/%m/%Y %H:%M:%S'


def last_message():
    result = {}
    last_time = 0
    for message in db:
        if last_time < message['time']:
            last_time = message['time']
            result = message
    return result


def count_authors():
    authors = {}
    for message in db:
        if message['name'] in authors:
            authors[message['name']] += 1
        else:
            authors[message['name']] = 1
        return len(authors)


@app.route("/")
def hello():
    return "<a href='/status'>Статистика</a>"


@app.route("/status")
def get_status():
    last_mes = last_message()
    return f'<p>Название мессенджера:<b> Messenger<b></p>' \
        f'<p>Статус мессенджера:<b> В работе!<b></p>' \
        f'<p>Всего сообщений:<b> {len(db)}<b></p>' \
        f'<p>Всего авторов сообщений:<b> {count_authors()}<b></p>'\
        f'<p>Последнее сообщение:' \
        f'<p>{datetime.fromtimestamp(last_mes["time"]).strftime(format_date)} от {last_mes["name"]}</p>' \
        f'<p>{last_mes["text"]}</p>'\
        f'<br>'\
        f'<p>Время обновления информации на этой странице: {datetime.now().strftime(format_date)}'


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