import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.exceptions import BadRequest
from auth import hash_password, verify_password, needs_rehash
from db import init_db, create_user, get_user_by_username, update_user_password
import sqlite3

app = Flask(__name__)
app.secret_key = os.environ.get("APP_SECRET", "dev-change-me")
init_db()

def current_user():
    return session.get("user")

@app.get("/")
def home():
    return render_template("home.html", user=current_user())

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        if not username or not password:
            flash("Usuario y contraseña son obligatorios.")
            return redirect(url_for("register"))
        if len(password) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.")
            return redirect(url_for("register"))
        try:
            create_user(username, hash_password(password))
            flash("Usuario creado. Ahora puedes iniciar sesión.")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("El usuario ya existe. Elige otro nombre.")
            return redirect(url_for("register"))
    return render_template("register.html", user=current_user())

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        row = get_user_by_username(username)
        if not row or not verify_password(password, row["password_hash"]):
            flash("Credenciales inválidas.")
            return redirect(url_for("login"))

        if needs_rehash(row["password_hash"]):
            update_user_password(username, hash_password(password))
        session["user"] = username
        flash("Ingreso correcto.")
        return redirect(url_for("home"))
    return render_template("login.html", user=current_user())

@app.get("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada.")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
