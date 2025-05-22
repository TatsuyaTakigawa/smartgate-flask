from flask import Blueprint, render_template

home_bp = Blueprint("home", __name__)  # "home" という名前のBlueprintを定義

@home_bp.route("/home")
def home():
    return render_template("home.html")