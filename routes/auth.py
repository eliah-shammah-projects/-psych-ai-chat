import os

from flask import Blueprint, jsonify, render_template, request, session

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        body = request.get_json(silent=True) or {}
        if body.get("password") == os.environ["APP_PASSWORD"]:
            session["authenticated"] = True
            return jsonify({"ok": True})
        return jsonify({"error": "Senha incorreta"}), 401
    return render_template("login.html")
