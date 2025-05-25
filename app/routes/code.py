# app/routes/code.py

"""
code.py

このモジュールは、SmartGateにおけるパスコード生成関連のルーティングを担当します。
現在は、認証済みユーザーがパスコード生成ページ（generate.html）にアクセスするルートのみを定義しています。
"""

from flask import Blueprint, render_template
from flask_login import login_required

# Blueprintの作成（'code' という名前のルートグループ）
code_bp = Blueprint("code", __name__)

@code_bp.route("/generate")
@login_required
def generate():
    """
    パスコード生成ページの表示。

    - 認証済みユーザーのみアクセス可能（@login_required）
    - generate.html をレンダリングして表示する
    """
    return render_template("generate.html")
