logged_in = False

from flask import Flask, jsonify, request, render_template, session
from flask_cors import CORS
import json
import os

app = Flask(__name__)
app.secret_key = "supersecret"
CORS(app)

DATA_FILE = "data.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


@app.route("/")
def index():
    global logged_in
    if not logged_in:
        return render_template("login.html")
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    global logged_in

    data = request.json
    password = data.get("password")

    if password == "1234":
        logged_in = True
        session["logged"] = True
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})


@app.route("/logout")
def logout():
    global logged_in
    logged_in = False
    session.clear()
    return jsonify({"success": True})


@app.route("/api/menu", methods=["GET"])
def get_menu():
    return jsonify(load_data())


@app.route("/api/menu", methods=["POST"])
def add_menu():
    if not session.get("logged"):
        return jsonify({"error": "Unauthorized"}), 401

    menu = load_data()
    new_item = request.json
    new_item["id"] = len(menu) + 1
    menu.append(new_item)
    save_data(menu)
    return jsonify(new_item)


@app.route("/api/menu/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    if not session.get("logged"):
        return jsonify({"error": "Unauthorized"}), 401

    menu = load_data()
    menu = [x for x in menu if x["id"] != item_id]
    save_data(menu)
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True)
