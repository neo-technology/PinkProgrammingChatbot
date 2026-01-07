import os
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

from db import (
    create_user,
    fetch_user_by_username,
    list_user_chats,
    fetch_chat,
    QuerySyntaxError,
    create_chat_and_first_message,
    create_message,
)
from ai import generate_ai_response


def create_app() -> Flask:
    load_dotenv()
    app = Flask(__name__)

    # Config
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-me")

    # Routes
    @app.errorhandler(QuerySyntaxError)
    def handle_cypher_syntax(err: QuerySyntaxError):
        return render_template("error.html", message=str(err)), 400

    @app.route("/")
    def index():
        if session.get("user"):
            return redirect(url_for("chats"))
        return render_template("index.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            if not username or not password:
                flash("Username and password required", "error")
                return render_template("register.html")

            # Check if user exists
            existing = fetch_user_by_username(username)
            if existing:
                flash("User already exists. Please login.", "warning")
                return redirect(url_for("login"))

            password_hash = generate_password_hash(password, method="pbkdf2:sha256")
            user = create_user(username, password_hash)
            if not user:
                flash("Could not create user. Complete the Cypher TODOs.", "error")
                return render_template("register.html")

            session["user"] = {"username": user.get("username", username), "id": user.get("id")}
            flash("Registration successful!", "success")
            return redirect(url_for("chats"))
        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username", "")
            password = request.form.get("password", "")
            user = fetch_user_by_username(username)
            if not user:
                flash("User not found.", "error")
                return render_template("login.html")

            stored_hash = user.get("password_hash")
            if not stored_hash or not check_password_hash(stored_hash, password):
                flash("Invalid credentials.", "error")
                return render_template("login.html")

            session["user"] = {"username": user.get("username"), "id": user.get("id")}
            flash("Logged in!", "success")
            return redirect(url_for("chats"))
        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.pop("user", None)
        flash("Logged out.", "info")
        return redirect(url_for("index"))

    def login_required(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not session.get("user"):
                flash("Please log in first.", "warning")
                return redirect(url_for("login"))
            return fn(*args, **kwargs)
        return wrapper

    @app.route("/chats")
    @login_required
    def chats():
        user = session["user"]
        user_chats = list_user_chats(user_id=user.get("id", user.get("username")))
        return render_template("chats.html", chats=user_chats)

    @app.route("/chats/<chat_id>", methods=["GET", "POST"])
    @login_required
    def chat(chat_id: str):
        user = session["user"]
        if request.method == "POST":
            user_message = request.form.get("message", "").strip()
            if user_message:
                create_message(chat_id, role="user", content=user_message)
                ai_reply = generate_ai_response(user_message)
                if ai_reply:
                    create_message(chat_id, role="assistant", content=ai_reply)
        chat_obj = fetch_chat(chat_id)
        if not chat_obj:
            flash("Chat not found or Cypher TODO incomplete.", "error")
            return redirect(url_for("chats"))
        return render_template("chat.html", chat=chat_obj, user=user)

    @app.route("/chat/new", methods=["GET", "POST"])
    @login_required
    def chat_new():
        user = session["user"]
        if request.method == "POST":
            user_message = request.form.get("message", "").strip()
            if not user_message:
                flash("Please enter a message to start.", "warning")
                return render_template("chat_new.html")
            # Create chat with first user message
            user_identifier = user.get("id") or user.get("username")
            new_chat = create_chat_and_first_message(user_identifier, user_message)
            chat_id = new_chat.get("id") if new_chat else None
            # Generate AI reply and save as assistant message
            ai_reply = generate_ai_response(user_message)
            if chat_id and ai_reply:
                create_message(chat_id, role="assistant", content=ai_reply)
                return redirect(url_for("chat", chat_id=chat_id))
            flash("Chat created but could not determine chat id. Complete Cypher TODOs.", "warning")
            return redirect(url_for("chats"))
        return render_template("chat_new.html")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
