import socketio
import engineio
import eventlet
import json

from pomodoro import *


client = socketio.Client()
client.connect("http://localhost:3000")


def send_pom_info(info):
    print("Info sending", info)
    client.emit("info", json.dumps(info))


pom = Pomodoro(poll_callback=send_pom_info)

while True:
    continue
