from flask import Flask, render_template
import asyncio
import socketio


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
sio = socketio.AsyncClient()


@sio.on("message")
async def on_message(data):
    print("I received a message!")


@app.route('/')
def index():
    return render_template('./index.html')
