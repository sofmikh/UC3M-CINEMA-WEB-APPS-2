from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import flask_login

from . import db
from . import model

bp = Blueprint("auth", __name__)


# ---------- Registro ----------

@bp.route("/signup")
def signup():
    return render_template("auth/signup.html")


@bp.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    password_repeat = request.form.get("password_repeat")

    # 1. Las dos contraseñas tienen que coincidir
    if password != password_repeat:
        flash("Passwords do not match.")
        return redirect(url_for("auth.signup"))

    # 2. El email no puede estar ya registrado
    query = db.select(model.User).where(model.User.email == email)
    if db.session.execute(query).scalar_one_or_none():
        flash("That email is already registered.")
        return redirect(url_for("auth.signup"))

    # 3. Guardamos el usuario con la contraseña cifrada (nunca en texto plano)
    user = model.User(
        email=email,
        name=username,
        password=generate_password_hash(password),
    )
    db.session.add(user)
    db.session.commit()

    flash("Account created. You can log in now.")
    return redirect(url_for("auth.login"))


# ---------- Inicio de sesión ----------

@bp.route("/login")
def login():
    return render_template("auth/login.html")


@bp.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")

    query = db.select(model.User).where(model.User.email == email)
    user = db.session.execute(query).scalar_one_or_none()

    if user is None or not check_password_hash(user.password, password):
        flash("Wrong email or password.")
        return redirect(url_for("auth.login"))

    flask_login.login_user(user)

    # Si venía de una página protegida (por ejemplo, reservar), le devolvemos allí
    next_page = request.form.get("next")
    if next_page and next_page.startswith("/") and not next_page.startswith("//"):
        return redirect(next_page)
    return redirect(url_for("main.index"))


# ---------- Cerrar sesión ----------

@bp.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for("main.index"))