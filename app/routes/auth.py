import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_mail import Message
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from app.models.user import add_user, get_user_by_email, activate_user
from app import mail

# 認証関連のルートをまとめたBlueprint
auth_bp = Blueprint("auth", __name__)

def get_serializer():
    """
    トークンの生成・検証に使うシリアライザを取得する関数。
    FlaskのSECRET_KEYを元にインスタンスを生成。
    """
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

def is_strong_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):  # 大文字
        return False
    if not re.search(r"[a-z]", password):  # 小文字
        return False
    if not re.search(r"\d", password):     # 数字
        return False
    if not re.search(r"[!@#$%^&*()_+]", password):  # 記号
        return False
    return True

@auth_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    ユーザー登録処理。
    POST時はフォームの情報を受け取り、新規登録とメール認証メール送信を行う。
    GET時は登録フォームの表示。
    """
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # メールアドレスがすでに登録済みかチェック
        if get_user_by_email(email):
            flash("そのメールアドレスはすでに登録されています。")
            return redirect(url_for("auth.register"))
        
        if not is_strong_password(password):
            flash("パスワードは8文字以上で、大文字・小文字・数字・記号を含めてください。")
            return redirect(url_for("auth.register"))

        # メール確認用トークンを生成
        token = get_serializer().dumps(email, salt="email-confirm")
        confirm_url = url_for("auth.confirm_email", token=token, _external=True)

        # メールメッセージを作成して送信
        msg = Message("SmartGate メール認証", recipients=[email])
        msg.body = f"以下のリンクをクリックしてアカウントを有効化してください:\n{confirm_url}"
        msg.html = render_template("mail/confirm_email.html", token=token)
        mail.send(msg)

        # パスワードをハッシュ化してDBにユーザーを追加
        hashed_pw = generate_password_hash(password)
        add_user(username, email, hashed_pw)

        flash("確認メールを送信しました。受信ボックスをご確認ください。")
        return redirect(url_for("auth.login"))

    # GETリクエスト時は登録フォームを表示
    return render_template("register.html")

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

        # ログイン処理
        login_user(user)
        flash("ログインに成功しました。")
        return redirect(url_for("dashboard.dashboard"))  # ログイン後の遷移先

    return render_template("login.html")

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ログアウトしました。5秒後にトップページに戻ります。')
    return redirect(url_for('auth.logout_notice'))

@auth_bp.route('/logout_notice')
def logout_notice():
    return render_template('logout_notice.html')
