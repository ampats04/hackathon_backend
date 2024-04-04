from flask import Flask, Blueprint, request, jsonify
from functools import wraps
import uuid
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO

# modules
from admin.admin import admin
from users.users import users
from events.events import events
from apply_event.apply_event import apply_events

app = Flask(__name__)
CORS(app)
SocketIO(app)

app.config["SECRET_KEY"] = uuid.uuid4().hex
app.config["CORS_HEADERS"] = "Content-Type"


app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(users, url_prefix="/user")
app.register_blueprint(events, url_prefix="/event")
app.register_blueprint(apply_events, url_prefix="/apply")


@app.route("/")
def home():
    return "hello world"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
