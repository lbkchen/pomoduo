import engineio
import eventlet
import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})


@sio.on('connect')
def connect(sid, environ):
    print('connect ', sid)


@sio.on('message')
def message(sid, data):
    print('message ', data)


@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 3000)), app)
