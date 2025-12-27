from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, send
import random

app = Flask(__name__, static_folder="static", static_url_path="/")
app.config["SECRET_KEY"] = "YOUR_SECRET_KEY"

socketio = SocketIO(app, cors_allowed_origins="*")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username")
    password = request.form.get("password")

    if username == "harshit" and password == "123":
        session["logged_in"] = True
        session["username"] = username
        return redirect(url_for("room"))

    return "Incorrect username or password"


@app.route("/room")
def room():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    return render_template("room.html", username=session["username"])


@app.route("/chat")
def chat():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    room_key = str(random.randint(1000, 9999))
    username = session["username"]

    return render_template("chat.html", key=room_key, username=username)




@socketio.on("message")
def handle_message(data):
    username = data["user"]
    text = data["text"]

    send({"user": username, "text": text}, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", debug=True)
