# Psych AI Chat — Psychological Approaches via Claude API

A web app that lets you choose a therapeutic approach and have a conversation with it. Each approach has a distinct personality, communication style, and set of techniques — making the differences between them immediately tangible through conversation.

Built as a **prompt engineering portfolio project**: demonstrating how carefully crafted system prompts can produce complex, consistent, and contrasting AI personas using the Claude API.

> This is the **original Portuguese version** (personas and interface in Portuguese). For the English version, see [`psych-ai-chat--english`](https://github.com/eliah-shammah-projects/-psych-ai-chat---English-version).

**Live demo:** `http://13.61.109.17`

---

## The 7 Approaches

Each approach is a distinct therapeutic persona with its own worldview, communication style, and technique set.

| Approach | Emoji | What it does |
|---|---|---|
| **Psychoanalyst** | 🛋️ | Never answers directly. Points toward the unconscious, childhood, and repressed desires. Ends with a deepening question most of the time. |
| **CBT** | 📋 | Identifies cognitive distortions (catastrophizing, all-or-nothing thinking, mind reading), names them, and challenges them with evidence. |
| **Humanist** | 🤝 | Pure active listening. Reflects what you said back to you in different words. When you ask for a solution, guides you to find it yourself. |
| **NLP** | 🔄 | Constant reframing. Returns what you said from a different angle. Coach tone, future-oriented, focused on possibilities. |
| **Gestalt** | 🎯 | Focused on the body and the present moment. Proposes practical exercises (empty chair, conscious breathing, naming sensations). |
| **Existential** | 🌌 | Goes to the existential question behind the problem — freedom, meaning, mortality. Philosophical without being pedantic. |
| **ACT** | 🌿 | Separates you from the thought: "you are *having* the thought that X, you are not X". Points toward values-based action. |

### Key differences between similar approaches

- **Psychoanalyst vs. Existential** — both are deep and don't give direct solutions. The Psychoanalyst goes to the unconscious and the past. The Existential goes to meaning and freedom — without touching the past.
- **CBT vs. ACT** — CBT corrects the distorted thought. ACT doesn't correct — it accepts the thought and changes your relationship with it.
- **Humanist vs. Gestalt** — Humanist validates and reflects. Gestalt brings it to the body and the present, and proposes exercises.
- **NLP vs. CBT** — CBT calls the thought a distortion. NLP doesn't call anything wrong — it just offers another angle.

---

## Stack

- **Backend:** Python / Flask
- **AI:** Claude API (`claude-sonnet-4-6`) via Anthropic SDK
- **Frontend:** HTML + CSS + vanilla JS (no framework)
- **Auth:** Password-based login via `APP_PASSWORD` env var
- **Session history:** Flask server-side session (no database)
- **Personas:** `personas.json` — each with `system_prompt`, `temperature`, `descricao_curta`, and `abertura`
- **CI/CD:** GitHub Actions → Docker → ECR → EC2
- **Infrastructure:** AWS EC2 + ECR, provisioned via Terraform

---

## How to run locally

**1. Clone and install dependencies**

```bash
git clone https://github.com/eliah-shammah-projects/-psych-ai-chat.git
cd psych-ai-chat
pip install -r requirements.txt
```

**2. Set up `.env`**

```env
ANTHROPIC_API_KEY=your_key_here
APP_PASSWORD=any_password_you_choose
FLASK_SECRET_KEY=any_random_string
```

**3. Run**

```bash
python app.py
```

Open `http://localhost:5000` — you'll be prompted for the password, then taken to the approach selection screen.

---

## Architecture

```
psych-ai-chat/
├── app.py                        # Flask entry point
├── personas.json                 # 7 therapeutic approaches
├── routes/
│   ├── chat.py                   # GET /personas, POST /chat, POST /reset
│   └── auth.py                   # GET/POST /login
├── services/
│   └── claude_service.py         # Claude API calls (system_prompt + history)
├── tests/
│   ├── test_routes.py
│   └── test_service.py
├── frontend/
│   ├── templates/
│   │   ├── index.html            # Approach selector + chat UI
│   │   └── login.html
│   └── static/
│       ├── script.js
│       ├── style.css
│       └── illustration.jpg
├── terraform/                    # AWS infra (ECR + EC2 + security group)
└── .github/workflows/ci.yml      # CI/CD pipeline
```

**Request flow:** Browser → Flask route → `claude_service.py` → Anthropic API → response streamed back

Each conversation holds its history in the Flask session. Switching approaches resets the session.

---

## CI/CD Pipeline

On every push to `master`:

1. Run `pytest` (tests must pass before any deploy step)
2. Terraform applies infra changes (idempotent — creates ECR/EC2 if not exists)
3. Build Docker image, push to AWS ECR
4. Push image to Docker Hub (public portfolio)
5. SSH into EC2, pull new image, restart container on port 5000

The deploy step is skipped on pull requests — only tests run.

---

## Prompt engineering details

Each persona in `personas.json` has:

- `system_prompt` — the core instruction set, structured with `<persona>`, `<tom>`, `<formato>`, and `<evitar>` tags
- `temperature` — tuned per approach (0.4 for CBT's clinical precision, 0.9 for Psychoanalyst's ambiguity)
- `descricao_curta` — short description shown in the UI
- `abertura` — the label shown in the approach picker

The prompts were developed iteratively using `tests/test_personas.py`, a CLI tool that lets you chat freely with each approach and log observations to `prompt_log.json`.

---

## What this project demonstrates

- Prompt engineering: producing distinct, consistent, and contrasting personas from a single model
- System prompt structure and persona design
- Context management: maintaining therapeutic consistency across a multi-turn conversation
- Temperature tuning by use case
- Full-stack deployment: Flask app containerized and served on AWS with automated CI/CD
