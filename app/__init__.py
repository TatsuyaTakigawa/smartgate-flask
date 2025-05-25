# app/__init__.py

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv
from app.models.user import get_user_by_id
import os

# 環境変数を読み込み（.env）
load_dotenv()

# Flask拡張機能の初期化
login_manager = LoginManager()
mail = Mail()

# Flask-LoginがユーザーIDからユーザー情報を取得する関数
@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(int(user_id))

def create_app():
    """
    Flaskアプリケーションを作成・設定・初期化して返す関数。
    - 環境変数の読み込み
    - 拡張機能の初期化
    - Blueprintの登録
    """
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "devkey")  # セッションやトークン生成に使う秘密鍵

    # Flask-Mail 設定
    app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT", 587))
    app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS", "true").lower() in ["true", "1"]
    app.config['MAIL_USE_SSL'] = os.getenv("MAIL_USE_SSL", "false").lower() in ["true", "1"]
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER", os.getenv("MAIL_USERNAME"))

    # 拡張機能のアプリケーションへの紐付け
    login_manager.init_app(app)
    mail.init_app(app)

    # Blueprintの登録（3つに統合後の構成）
    from .routes.passcode import passcode_bp
    from .routes.auth import auth_bp
    from .routes.code import code_bp

    app.register_blueprint(passcode_bp)                # トップ（/）と/welcome
    app.register_blueprint(auth_bp, url_prefix="/auth")  # ログイン、登録、ダッシュボードなど
    app.register_blueprint(code_bp, url_prefix="/code")  # コード生成

    # Flask-Loginの設定
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = "info"
    login_manager.login_message = "ログインが必要です。"

    return app
