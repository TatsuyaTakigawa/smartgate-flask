# app/routes/code.py

"""
code.py

このモジュールは、SmartGateにおける「パスコード生成」および「クイズ機能」を担当します。

1. /generate   ：ログイン済みユーザーがパスコード生成ページを閲覧
2. /quiz       ：誰でもアクセス可能なクイズ画面
3. /submit     ：クイズ結果を処理し、全問正解時にパスコードを発行
"""

import os
from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required
from dotenv import load_dotenv
from app.utils.passcode_generator import create_passcode_if_correct

# 環境変数（.env）を読み込む
load_dotenv()

# Blueprintの作成（このモジュール全体のルートグループ）
code_bp = Blueprint("code", __name__)


@code_bp.route("/generate")
@login_required
def generate():
    """
    【ログイン必須】
    パスコード生成ページを表示するルート。

    - 認証済みのユーザーだけがアクセス可能。
    - generate.html を表示。
    """
    return render_template("generate.html")


@code_bp.route("/quiz", methods=["GET"])
def quiz():
    """
    クイズ画面を表示するルート。

    - 一般ユーザーがクイズに回答するための画面を表示。
    - quiz.html を表示。
    """
    return render_template("quiz.html")


@code_bp.route("/submit", methods=["POST"])
def submit_quiz():
    """
    クイズの回答を受け取り、正解判定を行うルート。

    - フォームから送信された回答を受け取り、.env に定義された正解と比較。
    - 全問正解時のみ、パスコードを生成してフラッシュ表示。
    - quiz ページにリダイレクト。
    """

    # ユーザー入力の取得
    name = request.form.get("name")
    valid_hours = request.form.get("valid_hours")
    q1 = request.form.get("q1")
    q2 = request.form.get("q2")
    q3 = request.form.get("q3")
    q4 = request.form.get("q4")

    # .envから正解を取得
    correct_answers = {
        "q1": os.getenv("CORRECT_Q1"),
        "q2": os.getenv("CORRECT_Q2"),
        "q3": os.getenv("CORRECT_Q3"),
        "q4": os.getenv("CORRECT_Q4"),
    }

    # 全問正解かどうかチェック
    if all([
        q1 == correct_answers["q1"],
        q2 == correct_answers["q2"],
        q3 == correct_answers["q3"],
        q4 == correct_answers["q4"]
    ]):
        # 正解時：パスコードを生成して通知
        passcode = create_passcode_if_correct()
        flash(f"正解です！ あなたのパスコードは: {passcode}（有効時間: {valid_hours}時間）", "success")
    else:
        # 不正解時：エラーメッセージ表示
        flash("残念！全問正解しないとパスコードは表示されません。", "danger")

    # クイズ画面に戻す
    return redirect(url_for("code.quiz"))
