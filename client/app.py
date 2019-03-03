from flask import Flask, render_template, jsonify
import asyncio
import socketio

from pomodoro import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

sio = socketio.AsyncClient()

pom = Pomodoro(debug=True)


@sio.on("update")
async def on_update(data):
    print("I received a message!")


# @skywriter.flick()
# def flick(start, finish):
#     sio.emit("message", {
#         "start": start,
#         "finish": finish,
#     })
#     print('Got a flick!', start, finish)


@app.route('/')
def index():
    return render_template('./index.html', time=pom.elapsed)


@app.route('/info')
def get_info():
    return jsonify(pom.info)


@app.route('/start', methods=['POST'])
def start():
    pom.start()
    return "ok"
