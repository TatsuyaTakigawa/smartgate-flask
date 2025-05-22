from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

def init_db():
    """
    ユーザーデータベース（users.db）を初期化し、
    usersテーブルを作成する。すでに存在する場合は何もしない。
    """
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  # ユーザーID（自動増分）
            username TEXT UNIQUE NOT NULL,         # ユーザー名（一意制約あり）
            email TEXT UNIQUE NOT NULL,            # メールアドレス（一意制約あり）
            password TEXT NOT NULL,                 # ハッシュ化されたパスワード
            is_active INTEGER DEFAULT 0            # アカウント有効フラグ（デフォルト無効）
        )
    """)
    conn.commit()
    conn.close()

class User(UserMixin):
    """
    Flask-Login用のユーザークラス。
    UserMixinを継承し、必要な属性・メソッドを持つ。
    """
    def __init__(self, id, username, email, password, is_active):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self._is_active = bool(is_active)  # プライベート変数でis_activeを管理

    @property
    def is_active(self):
        """
        Flask-Loginが利用するアカウント有効フラグ。
        """
        return self._is_active

    @is_active.setter
    def is_active(self, value):
        self._is_active = bool(value)

    def check_password(self, password):
        """
        入力されたパスワードをハッシュと比較して検証する。
        """
        return check_password_hash(self.password, password)

def get_user_by_email(email):
    """
    メールアドレスをキーにユーザー情報をDBから取得し、
    Userオブジェクトを返す。なければNoneを返す。
    """
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    row = c.fetchone()
    conn.close()
    return User(*row) if row else None

def get_user_by_id(user_id):
    """
    ユーザーIDをキーにユーザー情報をDBから取得し、
    Userオブジェクトを返す。なければNoneを返す。
    """
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return User(*row) if row else None

def add_user(username, email, password_hash):
    """
    新規ユーザーをDBに追加する。
    パスワードはハッシュ化済みのものを受け取る。
    """
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
              (username, email, password_hash))
    conn.commit()
    conn.close()

def activate_user(email):
    """
    指定メールアドレスのユーザーのis_activeフラグを1（有効）に更新する。
    """
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("UPDATE users SET is_active = 1 WHERE email = ?", (email,))
    conn.commit()
    conn.close()
