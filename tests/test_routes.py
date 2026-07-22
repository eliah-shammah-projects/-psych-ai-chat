import pytest
from unittest.mock import patch

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test-secret"
    with app.test_client() as c:
        yield c


@pytest.fixture
def auth_client(client):
    """Cliente já autenticado."""
    with patch.dict("os.environ", {"APP_PASSWORD": "senha-teste"}):
        client.post("/login", json={"password": "senha-teste"})
    return client


# ── Auth ──────────────────────────────────────────────────────────────────────

def test_login_correct_password(client):
    with patch.dict("os.environ", {"APP_PASSWORD": "senha-teste"}):
        res = client.post("/login", json={"password": "senha-teste"})
    assert res.status_code == 200
    assert res.get_json()["ok"] is True


def test_login_wrong_password(client):
    with patch.dict("os.environ", {"APP_PASSWORD": "senha-teste"}):
        res = client.post("/login", json={"password": "errada"})
    assert res.status_code == 401


def test_unauthenticated_html_redirects_to_login(client):
    res = client.get("/")
    assert res.status_code == 302
    assert "/login" in res.headers["Location"]


def test_unauthenticated_json_returns_401(client):
    res = client.post("/chat", json={"persona": "x", "message": "oi"})
    assert res.status_code == 401


# ── /personas ─────────────────────────────────────────────────────────────────

def test_get_personas_returns_seven(auth_client):
    res = auth_client.get("/personas")
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) == 7


def test_get_personas_fields(auth_client):
    res = auth_client.get("/personas")
    for p in res.get_json():
        for field in ("nome", "emoji", "categoria", "descricao_curta", "abertura", "bibliografia"):
            assert field in p, f"campo '{field}' faltando em {p.get('nome')}"


# ── /chat ─────────────────────────────────────────────────────────────────────

def test_chat_missing_fields_returns_400(auth_client):
    res = auth_client.post("/chat", json={"persona": "Psicólogo › CBT"})
    assert res.status_code == 400


def test_chat_unknown_persona_returns_404(auth_client):
    res = auth_client.post("/chat", json={"persona": "Inexistente", "message": "oi"})
    assert res.status_code == 404


def test_chat_valid_request_returns_reply(auth_client):
    with patch("routes.chat.chat", return_value="resposta simulada"):
        res = auth_client.post("/chat", json={
            "persona": "Psicólogo › CBT",
            "message": "oi",
        })
    assert res.status_code == 200
    assert res.get_json()["reply"] == "resposta simulada"


# ── /reset ────────────────────────────────────────────────────────────────────

def test_reset_returns_ok(auth_client):
    res = auth_client.post("/reset")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


def test_reset_clears_session(auth_client):
    with patch("routes.chat.chat", return_value="x"):
        auth_client.post("/chat", json={"persona": "Psicólogo › CBT", "message": "oi"})

    auth_client.post("/reset")

    with auth_client.session_transaction() as sess:
        assert "persona" not in sess
        assert "history" not in sess
