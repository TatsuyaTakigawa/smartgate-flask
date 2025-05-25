# --- auth.py ---
# 認証・ユーザー管理、ホーム画面、ダッシュボード画面を担当

import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_mail import Message
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from app.models.user import add_user, get_user_by_email, activate_user
from app import mail

# Blueprint登録（認証と関連画面を担当）
auth_bp = Blueprint("auth", __name__)

# トークン生成用のシリアライザ

def get_serializer():
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

# パスワード強度チェック関数
def is_strong_password(password):
    return (
        len(password) >= 8 and
        re.search(r"[A-Z]", password) and
        re.search(r"[a-z]", password) and
        re.search(r"\d", password) and
        re.search(r"[!@#$%^&*()_+]", password)
    )

# ホーム画面
@auth_bp.route("/home")
def home():
    return render_template("home.html")

# ダッシュボード（ログイン後）
@auth_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

# 新規登録
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        if get_user_by_email(email):
            flash("そのメールアドレスはすでに登録されています。")
            return redirect(url_for("auth.register"))

        if not is_strong_password(password):
            flash("パスワードは8文字以上で、大文字・小文字・数字・記号を含めてください。")
            return redirect(url_for("auth.register"))

        token = get_serializer().dumps(email, salt="email-confirm")
        confirm_url = url_for("auth.confirm_email", token=token, _external=True)
        msg = Message("SmartGate メール認証", recipients=[email])
        msg.body = f"以下のリンクをクリックしてアカウントを有効化してください:\n{confirm_url}"
        msg.html = render_template("mail/confirm_email.html", token=token)
        mail.send(msg)

        hashed_pw = generate_password_hash(password)
        add_user(username, email, hashed_pw)

        flash("確認メールを送信しました。受信ボックスをご確認ください。")
        return redirect(url_for("auth.login"))

    return render_template("register.html")

# メール確認
@auth_bp.route("/confirm/<token>")
def confirm_email(token):
    try:
        email = get_serializer().loads(token, salt="email-confirm", max_age=3600)
    except SignatureExpired:
        flash("トークンの有効期限が切れています。再度登録してください。")
        return redirect(url_for("auth.register"))
    except BadSignature:
        flash("無効なトークンです。")
        return redirect(url_for("auth.register"))

    activate_user(email)
    flash("メール確認が完了しました。ログインできます。")
    return redirect(url_for("auth.login"))

# ログイン
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = get_user_by_email(email)

        if user is None:
            flash("ユーザーが見つかりません。")
            return redirect(url_for("auth.login"))

        if not user.is_active:
            flash("メール認証が完了していません。メールをご確認ください。")
            return redirect(url_for("auth.login"))

        if not user.check_password(password):
            flash("パスワードが違います。")
            return redirect(url_for("auth.login"))

        login_user(user)
        flash("ログインに成功しました。")
        return redirect(url_for("auth.dashboard"))

    return render_template("login.html")

# ログアウト
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ログアウトしました。5秒後にトップページに戻ります。')
    return redirect(url_for('auth.logout_notice'))

@auth_bp.route('/logout_notice')
def logout_notice():
    return render_template('logout_notice.html')
