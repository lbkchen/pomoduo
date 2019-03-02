from flask import Flask, render_template
import asyncio
import socketio


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
sio = socketio.AsyncClient()


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
    return render_template('./index.html')
