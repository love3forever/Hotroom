from modules.create_app import init_app, init_socketio

if __name__ == '__main__':
    socketio = init_socketio()
    app = init_app()
    socketio.init_app(app)
    socketio.run(app, debug=True, port=11111)
