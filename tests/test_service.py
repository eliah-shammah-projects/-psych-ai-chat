import pytest
from unittest.mock import MagicMock, patch

from services.claude_service import load_all_personas, load_persona, chat

REQUIRED_FIELDS = {"nome", "emoji", "categoria", "descricao_curta", "abertura",
                   "bibliografia", "system_prompt", "temperature"}


def test_load_all_personas_returns_seven():
    personas = load_all_personas()
    assert len(personas) == 7


def test_all_personas_have_required_fields():
    for p in load_all_personas():
        missing = REQUIRED_FIELDS - p.keys()
        assert not missing, f"{p.get('nome')} faltam campos: {missing}"


def test_all_temperatures_are_valid():
    for p in load_all_personas():
        assert isinstance(p["temperature"], (int, float))
        assert 0.0 <= p["temperature"] <= 1.0


def test_load_persona_finds_by_name():
    persona = load_persona("Psicólogo › CBT")
    assert persona["nome"] == "Psicólogo › CBT"


def test_load_persona_raises_for_unknown():
    with pytest.raises(ValueError, match="Persona não encontrada"):
        load_persona("Persona Inexistente")


def test_chat_calls_api_with_correct_params():
    fake_response = MagicMock()
    fake_response.content[0].text = "resposta simulada"

    with patch("services.claude_service.anthropic.Anthropic") as MockClient:
        MockClient.return_value.messages.create.return_value = fake_response

        result = chat("Psicólogo › CBT", [], "oi")

    assert result == "resposta simulada"

    call_kwargs = MockClient.return_value.messages.create.call_args.kwargs
    assert call_kwargs["model"] == "claude-sonnet-4-6"
    assert call_kwargs["messages"] == [{"role": "user", "content": "oi"}]
    assert "system" in call_kwargs
    assert "temperature" in call_kwargs


def test_chat_appends_history_to_messages():
    fake_response = MagicMock()
    fake_response.content[0].text = "ok"

    history = [
        {"role": "user", "content": "mensagem anterior"},
        {"role": "assistant", "content": "resposta anterior"},
    ]

    with patch("services.claude_service.anthropic.Anthropic") as MockClient:
        MockClient.return_value.messages.create.return_value = fake_response
        chat("Psicólogo › CBT", history, "nova mensagem")

    messages_sent = MockClient.return_value.messages.create.call_args.kwargs["messages"]
    assert messages_sent[0]["content"] == "mensagem anterior"
    assert messages_sent[-1]["content"] == "nova mensagem"
