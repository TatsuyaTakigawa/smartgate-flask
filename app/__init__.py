from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv
from app.models.user import get_user_by_id
import os

load_dotenv()  # .envファイルから環境変数を読み込み

login_manager = LoginManager()  # Flask-LoginのLoginManagerインスタンスを作成
mail = Mail()  # Flask-MailのMailインスタンスを作成

@login_manager.user_loader
def load_user(user_id):
    # Flask-LoginがユーザーIDからユーザーオブジェクトを読み込むための関数
    return get_user_by_id(int(user_id))  # ユーザーIDでDBからユーザーを取得

def create_app():
    app = Flask(__name__)  # Flaskアプリケーションの作成
    app.secret_key = os.getenv("SECRET_KEY", "devkey")  # 秘密鍵を環境変数から設定。なければ'devkey'を使用

    # Flask-Mail用のメールサーバー設定を環境変数から取得して設定
    app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT", 587))
    # TLSを使うかどうかの設定（環境変数は文字列なので小文字に変換し、True判定）
    app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS", "true").lower() in ["true", "1"]
    # SSLを使うかどうかの設定（こちらも文字列で判定）
    app.config['MAIL_USE_SSL'] = os.getenv("MAIL_USE_SSL", "false").lower() in ["true", "1"]
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")  # メール送信用のユーザー名
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")  # メール送信用のパスワード
    # 送信元メールアドレス。環境変数がなければユーザー名を代わりに使用
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER", os.getenv("MAIL_USERNAME"))

    # Flask拡張機能（Flask-Login, Flask-Mail）をアプリに紐付けて初期化
    login_manager.init_app(app)
    mail.init_app(app)

    # Blueprintの登録
    from .routes.passcode import passcode_bp  # passcode用ルートをインポート
    from .routes.auth import auth_bp  # 認証関連ルートをインポート
    from .routes.home import home_bp
    from .routes.dashboard import dashboard_bp
    from .routes.code import code_bp
    app.register_blueprint(passcode_bp)  # パスコード用Blueprintを登録
    app.register_blueprint(auth_bp, url_prefix="/auth")  # 認証用Blueprintを /auth にマウント
    app.register_blueprint(home_bp) 
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(code_bp, url_prefix="/code")

    # ログイン関係の設定
    login_manager.login_view = 'auth.login'  # 未ログイン時に飛ばすログインページ
    login_manager.login_message_category = "info"
    login_manager.login_message = "ログインが必要です。"


    return app  # 作成したFlaskアプリケーションを返す
