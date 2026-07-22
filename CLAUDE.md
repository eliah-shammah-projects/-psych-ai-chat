# Psicologia AI — Claude API Lab

App web dedicado a abordagens psicológicas via Claude API.
O usuário escolhe uma abordagem terapêutica e conversa com ela.
Foco: demonstrar prompt engineering com personas complexas e contrastantes (portfólio).

---

## Status atual (2026-07-21)

### ✅ MVP completo e funcionando localmente
- **Backend**: `app.py`, `services/claude_service.py`, `routes/chat.py`, `routes/auth.py` — todos implementados
- **Frontend**: tela de seleção + chat — implementados (`index.html`, `style.css`, `script.js`)
- **Autenticação**: login por senha via `APP_PASSWORD` env var — `login.html` + guard `before_request`
- **python-dotenv**: `load_dotenv()` no `app.py` lê `.env` automaticamente
- **Ilustração**: `frontend/static/illustration.jpg` com CSS filter azul-verde + `mix-blend-mode: multiply`
- **7 personas**: todas com `temperature`, `descricao_curta` formal, `bibliografia` e `abertura`

### ✅ Personas concluídas (todas testadas e aprovadas no `personas.json`)
- Psicólogo › Psicanalista 🛋️
- Psicólogo › CBT 📋
- Psicólogo › Humanista 🤝
- Psicólogo › NLP 🔄
- Psicólogo › Gestalt 🎯
- Psicólogo › Existencial 🌌
- Psicólogo › ACT 🌿

### 🔜 Próximos passos — CI/CD e deploy AWS
1. **Testes automatizados** — `pytest` em `tests/test_routes.py` e `tests/test_service.py`
2. **Dockerfile** + `.dockerignore` — containerizar o app Flask
3. **Terraform** — provisionar infra AWS: ECR, ECS Fargate, VPC, ALB, Secrets Manager, IAM, CloudWatch
4. **GitHub Actions** — `.github/workflows/deploy.yml`: roda testes → build Docker → push ECR → deploy ECS
5. **Secrets na AWS** — `ANTHROPIC_API_KEY`, `APP_PASSWORD`, `FLASK_SECRET_KEY` no Secrets Manager

---

## CI/CD — Testes e Deploy AWS

### Pipeline (a implementar após MVP funcional)
1. **Testes automatizados** — `pytest` cobrindo rotas Flask e chamadas ao `claude_service`
2. **GitHub Actions** — workflow que roda os testes a cada push/PR na branch `main`
3. **Deploy AWS** — app containerizado (Docker) publicado via:
   - **ECR** para o registro da imagem
   - **ECS Fargate** (ou Elastic Beanstalk) para rodar o container
   - Variáveis sensíveis (`ANTHROPIC_API_KEY`) em **AWS Secrets Manager** ou **Parameter Store**
4. **Deploy automático** — Actions faz push do container e atualiza o serviço ECS somente se os testes passarem

### Ordem sugerida
- Escrever testes unitários antes de subir pra AWS
- Criar `Dockerfile` junto com a finalização do backend
- Configurar workflow do GitHub Actions (`.github/workflows/deploy.yml`)
- Provisionar infra AWS (ECR + ECS) antes do primeiro deploy

> Para rodar localmente: configurar `.env` com `ANTHROPIC_API_KEY`, `APP_PASSWORD` e `FLASK_SECRET_KEY=dev`, depois `python app.py`.

---

## Abordagens (todas aprovadas)

| Nome | Emoji | Comportamento |
|---|---|---|
| Psicanalista | 🛋️ | Nunca responde direto — aponta pro inconsciente, infância, desejos reprimidos. Termina com pergunta na maioria das vezes. |
| CBT | 📋 | Identifica distorções cognitivas, nomeia, questiona evidência ou propõe ação concreta. |
| Humanista | 🤝 | Escuta ativa pura — reflete o que você disse de volta. Quando pede solução, conduz pra você mesmo chegar. |
| NLP | 🔄 | Reframe constante — devolve o que você disse com outro ângulo. Tom de coach, orientado a possibilidades. |
| Gestalt | 🎯 | Foco no corpo e no momento presente. Propõe exercícios práticos (cadeira vazia, respiração, nomear sensações). |
| Existencial | 🌌 | Vai na questão existencial por trás do problema — liberdade, significado, finitude. Filosófico sem ser pedante. |
| ACT | 🌿 | Separa você do pensamento — "você está tendo o pensamento de X, não é X". Aponta pra ação baseada em valores. |

---

## Diferenças importantes entre abordagens similares

- **Psicanalista vs Existencial**: ambos são profundos e não dão solução direta. O Psicanalista vai pro inconsciente e passado. O Existencial vai pro significado e liberdade — sem falar de passado.
- **CBT vs ACT**: CBT corrige o pensamento distorcido. ACT não corrige — aceita o pensamento e muda a relação com ele.
- **Humanista vs Gestalt**: Humanista valida e reflete. Gestalt traz pro corpo e pro presente, e propõe exercícios.
- **NLP vs CBT**: CBT chama o pensamento de distorção. NLP não chama nada de errado — só oferece outro ângulo.

---

## README (a fazer)

Criar `README.md` na raiz do repo. Deve cobrir:
- O que é o app e o objetivo (portfólio de prompt engineering)
- Screenshot ou GIF da interface
- Como rodar localmente (`.env`, dependências, `python app.py`)
- As 7 abordagens e suas diferenças
- Stack utilizada
- Link pro deploy (quando estiver na AWS)

Fazer após o CI/CD estar funcionando, junto com a versão em inglês.

---

## Versão em inglês (portfólio)

Criar um repo separado com o mesmo app totalmente em inglês — frontend, personas e `system_prompt`. O backend não muda. Prioridade: fazer após o CI/CD estar funcionando neste repo.

O que muda:
- Todos os textos do frontend (HTML, placeholders, disclaimer, login)
- `system_prompt`, `descricao_curta`, `abertura`, `bibliografia` de cada persona — reescrever em inglês
- Nomes das personas: "Psychologist › Psychoanalyst", "Psychologist › CBT" etc.

---

## Abordagens futuras
- ACT já incluído ✅
- Considerar adicionar mais abordagens no futuro (ex: Sistêmica, Junguiana)
- **Psiquiatra** — persona que explica opções de medicamento pra o quadro descrito, como age no cérebro, efeitos colaterais e quando buscar avaliação presencial. Diferente das abordagens psicológicas: entra no campo farmacológico. Exige atenção redobrada no prompt pra não substituir consulta real (disclaimer forte).

---

## Ideias futuras para o app
- Explicação de cada abordagem no app — o usuário não vai saber a diferença entre elas sem contexto
- Conversas genéricas de demo com a mesma mensagem enviada pra todas as 7 abordagens, mostrando respostas lado a lado — evidencia as diferenças de forma imediata
- Verificação automática com IA — usar o próprio Claude pra avaliar se as respostas estão dentro do comportamento esperado de cada abordagem

---

## Ciclo de refinamento de prompt

1. Escrever `system_prompt` no `personas.json`
2. Rodar `python tests/test_personas.py`, escolher abordagem pelo número
3. Conversar livremente, observar falhas de tom, tamanho ou comportamento
4. Digitar observação → salva automaticamente no `prompt_log.json`
5. Ajustar prompt baseado no log
6. Repetir até aprovar

---

## Log de testes (`tests/prompt_log.json`)

```json
{
  "timestamp": "2026-07-16T00:00:00",
  "persona": "Psicólogo › CBT",
  "modo": "chat_livre",
  "system_prompt": "...",
  "observacao": "o que notei, o que ajustar"
}
```

---

## Arquitetura

```
psych-ai-chat/
├── app.py                        # entry point Flask ✅
├── personas.json                 # 7 abordagens completas ✅
├── .env                          # ANTHROPIC_API_KEY, APP_PASSWORD, FLASK_SECRET_KEY (não commitado)
├── routes/
│   ├── chat.py                   # GET /personas, POST /chat, POST /reset ✅
│   └── auth.py                   # GET/POST /login ✅
├── services/
│   └── claude_service.py         # chama Claude API com system_prompt + histórico ✅
├── tests/
│   ├── test_personas.py          # chat interativo de refinamento ✅
│   └── prompt_log.json           # histórico de versões e observações ✅
├── frontend/
│   ├── templates/
│   │   ├── index.html            # SPA: seleção + chat ✅
│   │   └── login.html            # tela de login ✅
│   └── static/
│       ├── script.js             # lógica do frontend ✅
│       ├── style.css             # design completo ✅
│       └── illustration.jpg      # ilustração hero ✅
├── Dockerfile                    # (a implementar)
├── terraform/                    # (a implementar)
└── .github/workflows/deploy.yml  # (a implementar)
```

---

## Stack

- Backend: Flask + Anthropic SDK
- Modelo: `claude-sonnet-4-6`
- Frontend: HTML/CSS/JS simples (seleção de abordagem + chat)
- Sem banco de dados no MVP — personas em JSON, histórico em sessão Flask
