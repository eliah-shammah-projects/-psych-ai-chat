import json
from pathlib import Path

import anthropic

_PERSONAS_PATH = Path(__file__).parent.parent / "personas.json"
_MODEL = "claude-sonnet-4-6"


def load_all_personas() -> list[dict]:
    with open(_PERSONAS_PATH, encoding="utf-8") as f:
        return json.load(f)["personas"]


def load_persona(nome: str) -> dict:
    for p in load_all_personas():
        if p["nome"] == nome:
            return p
    raise ValueError(f"Persona não encontrada: {nome}")


def chat(persona_nome: str, history: list[dict], user_message: str) -> str:
    persona = load_persona(persona_nome)
    client = anthropic.Anthropic()  # lê ANTHROPIC_API_KEY do ambiente
    messages = history + [{"role": "user", "content": user_message}]
    response = client.messages.create(
        model=_MODEL,
        max_tokens=1024,
        system=persona["system_prompt"],
        messages=messages,
        temperature=persona["temperature"],
    )
    return response.content[0].text
