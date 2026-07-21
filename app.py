import os

from flask import Flask, render_template

from routes.chat import bp as chat_bp


def create_app() -> Flask:
    app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")
    app.secret_key = os.environ["FLASK_SECRET_KEY"]
    app.register_blueprint(chat_bp)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
