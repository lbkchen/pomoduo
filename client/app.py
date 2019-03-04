# from flask import Flask, render_template, jsonify
import socketio
import engineio
import eventlet
import json

from pomodoro import *

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Client that connects to the main server that serves all players
client = socketio.Client()
client.connect("http://localhost:3000")

# Server that opens the connection to the JS display interface
server = socketio.Server(logger=True)
server_app = socketio.WSGIApp(server, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'},
    '/static/assets/stylesheets/milligram.min.css': {
        'content_type': 'text/css',
        'filename': 'static/assets/stylesheets/milligram.min.css',
    },
    '/static/assets/stylesheets/normalize.css': {
        'content_type': 'text/css',
        'filename': 'static/assets/stylesheets/normalize.css',
    },
    '/static/assets/stylesheets/style.css': {
        'content_type': 'text/css',
        'filename': 'static/assets/stylesheets/style.css',
    },
    '/static/client.js': {
        'content_type': 'text/javascript',
        'filename': 'static/client.js',
    },
    '/static/node_modules/socket.io-client/dist/socket.io.js': {
        'content_type': 'text/javascript',
        'filename': 'static/node_modules/socket.io-client/dist/socket.io.js',
    },
})
connected_ids = []


def send_pom_info(info):
    print("Info sending", info)
    print("Connected ids", connected_ids)
    for sid in connected_ids:
        server.emit("info", json.dumps(info), room=sid)
    server.send("aaweofijawefoiaw")


pom = Pomodoro(debug=True, poll_callback=send_pom_info)


# Connections with client-side JS


@server.on('connect')
def connect(sid, environ):
    print('A client connected:', sid)
    connected_ids.append(sid)
    server.emit("info", json.dumps(1))


@server.on("start")
def on_start(sid, message):
    pom.start()
    print("Received start")
    client.emit("message", "Client started.")
    client.send("HELLO")
    server.send("FUCKKKKKK")
    return "ok"


@server.on("message")
def on_message(six, message):
    print("Server side catch all for message", message)


# Connection to server that knows all the clients


@client.on("update")
def on_update(data):
    print("I received a message!")


# @skywriter.flick()
# def flick(start, finish):
#     client.emit("message", {
#         "start": start,
#         "finish": finish,
#     })
#     print('Got a flick!', start, finish)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(
        ('localhost', 5000)), server_app)
