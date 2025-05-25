# app/routes/passcode.py

"""
passcode.py

このモジュールは、SmartGateのパスコード認証に関するルーティングを担当します。
訪問者が一時的なパスコードでアクセスできるようにするための認証処理を提供します。
"""

from flask import Blueprint, render_template, request, redirect, session, url_for
import os

# Blueprintの作成（'passcode' という名前のルートグループ）
passcode_bp = Blueprint("passcode", __name__)

@passcode_bp.route("/", methods=["GET", "POST"])
def passcode():
    """
    パスコード入力ページと認証処理を提供。

    - GET: パスコード入力フォームを表示
    - POST: 入力パスコードを検証し、正しければセッションに通過フラグを保存
    - 誤りがあればエラーメッセージ付きで再表示
    """
    correct_passcode = os.getenv("PASSCODE", "123456")  # 環境変数からパスコード取得（デフォルト123456）

    if request.method == "POST":
        entered = request.form.get("passcode")
        if entered == correct_passcode:
            session["passed_passcode"] = True  # 成功したらフラグをセッションに保存
            return redirect(url_for("passcode.welcome"))
        else:
            return render_template("passcode.html", error="パスコードが違います。")

    return render_template("passcode.html")  # GET時

@passcode_bp.route("/welcome")
def welcome():
    """
    パスコード認証後のリダイレクト用ページ。

    - 認証を通過していない場合は再度パスコード入力ページへ。
    - 通過していれば '/home' にリダイレクト。
    """
    if not session.get("passed_passcode"):
        return redirect(url_for("passcode.passcode"))
    return redirect("/home")
