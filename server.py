from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, cors_allowed_origins="*")

# SID: MAC
clients = {}


@socketio.on("connect")
def handle_connect():
    print("Client connected", request.sid)


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected", request.sid)
    socketio.emit(
        "tunnel-data", {"mac_address": clients[request.sid], "status": "offline"}
    )

    if request.sid in clients:
        del clients[request.sid]


@socketio.on("stream")
def handle_stream(msg):
    print("Received stream message", msg)
    if request.sid not in clients:
        clients[request.sid] = msg["mac_address"]
    print("Clients", clients)
    socketio.emit("tunnel-data", msg)


@app.route("/")
def index():
    server_url = request.url_root
    return render_template("index.html", server_url=server_url)


if __name__ == "__main__":
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True, host="0.0.0.0")
