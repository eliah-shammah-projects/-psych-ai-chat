from flask import Blueprint, request, jsonify, session

from services.claude_service import chat, load_all_personas, load_persona

bp = Blueprint("chat", __name__)


@bp.route("/personas", methods=["GET"])
def get_personas():
    personas = load_all_personas()
    return jsonify([
        {
            "nome": p["nome"],
            "emoji": p["emoji"],
            "categoria": p["categoria"],
            "descricao_curta": p["descricao_curta"],
            "abertura": p["abertura"],
        }
        for p in personas
    ])


@bp.route("/chat", methods=["POST"])
def post_chat():
    body = request.get_json(silent=True) or {}
    persona_nome = body.get("persona", "").strip()
    user_message = body.get("message", "").strip()

    if not persona_nome or not user_message:
        return jsonify({"error": "campos 'persona' e 'message' são obrigatórios"}), 400

    try:
        load_persona(persona_nome)  # valida que a persona existe
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

    # troca de persona → reseta histórico automaticamente
    if session.get("persona") != persona_nome:
        session["persona"] = persona_nome
        session["history"] = []

    history = session["history"]
    reply = chat(persona_nome, history, user_message)

    session["history"] = history + [
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": reply},
    ]

    return jsonify({"reply": reply})


@bp.route("/reset", methods=["POST"])
def post_reset():
    session.pop("persona", None)
    session.pop("history", None)
    return jsonify({"status": "ok"})
