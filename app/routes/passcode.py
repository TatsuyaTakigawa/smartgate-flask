from flask import Blueprint, render_template, request, redirect, session, url_for
import os

# パスコード認証用のBlueprint
passcode_bp = Blueprint("passcode", __name__)

@passcode_bp.route("/", methods=["GET", "POST"])
def passcode():
    """
    パスコード入力画面の表示と認証処理。
    POST時に入力されたパスコードを環境変数の正解パスコードと比較。
    合っていればsessionにフラグを立ててウェルカムページへリダイレクト。
    間違っていればエラーメッセージを表示。
    GET時は入力フォームを表示。
    """
    correct_passcode = os.getenv("PASSCODE", "123456")  # デフォルトは123456

    if request.method == "POST":
        entered = request.form.get("passcode")
        if entered == correct_passcode:
            session["passed_passcode"] = True  # パスコード認証通過のフラグをセット
            return redirect(url_for("passcode.welcome"))
        else:
            # エラーメッセージを渡して再表示
            return render_template("passcode.html", error="パスコードが違います。")

    # GET時はパスコード入力フォームを表示
    return render_template("passcode.html")

@passcode_bp.route("/welcome")
def welcome():
    """
    パスコード認証通過後にアクセス可能なウェルカムページ。
    通過していなければパスコード入力ページにリダイレクト。
    """
    if not session.get("passed_passcode"):
        return redirect(url_for("passcode.passcode"))
    # 認証済みの場合はregister.htmlを表示（必要に応じて変更可能）
    return redirect("/home")

