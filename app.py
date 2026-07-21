import os

from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, render_template, request, session, url_for

load_dotenv()

from routes.auth import bp as auth_bp
from routes.chat import bp as chat_bp


def create_app() -> Flask:
    app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")
    app.secret_key = os.environ["FLASK_SECRET_KEY"]
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)

    @app.before_request
    def require_auth():
        public = ("/login", "/static")
        if session.get("authenticated"):
            return
        if any(request.path.startswith(p) for p in public):
            return
        if request.is_json:
            return jsonify({"error": "não autenticado"}), 401
        return redirect(url_for("auth.login"))

    @app.route("/")
    def index():
        return render_template("index.html")

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
