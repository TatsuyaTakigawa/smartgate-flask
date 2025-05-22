# app/routes/code.py
from flask import Blueprint, render_template
from flask_login import login_required

code_bp = Blueprint("code", __name__)

@code_bp.route("/generate")
@login_required
def generate():
    return render_template("generate.html")
