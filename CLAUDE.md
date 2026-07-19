# Psicologia AI — Claude API Lab

App web dedicado a abordagens psicológicas via Claude API.
O usuário escolhe uma abordagem terapêutica e conversa com ela.
Foco: demonstrar prompt engineering com personas complexas e contrastantes (portfólio).

---

## Status atual (2026-07-19)

### ✅ Personas concluídas (todas testadas e aprovadas no `personas.json`)
- Psicólogo › Psicanalista 🛋️
- Psicólogo › CBT 📋
- Psicólogo › Humanista 🤝
- Psicólogo › NLP 🔄
- Psicólogo › Gestalt 🎯
- Psicólogo › Existencial 🌌
- Psicólogo › ACT 🌿

Cada persona tem: `nome`, `emoji`, `categoria`, `descricao_curta`, `descricao_longa`, `system_prompt` (com tags `<persona>`, `<tom>`, `<formato>`, `<evitar>`), e `mensagens_extremas` (4 frases por persona — 2 genéricas + 2 específicas da abordagem).

### ⚠️ Pendências antes de implementar o backend (ainda abertas)
- **Abertura obrigatória** — em toda primeira mensagem da conversa, a persona se apresenta: diz qual abordagem é e em poucas palavras como vai funcionar. Aplicar em todas as 7 personas (adicionar regra no `system_prompt` de cada uma).
- **Verificar temperaturas** — definir temperatura ideal para cada persona e adicionar campo `"temperature"` no `personas.json`. Personas criativas = temperatura alta, personas precisas = temperatura baixa.

### 🔜 Próximos passos (MVP) — nenhum implementado ainda
1. Resolver as 2 pendências acima no `personas.json`
2. Implementar `services/claude_service.py` — função que carrega persona do JSON e chama a API com histórico
3. Implementar `routes/chat.py` — rota `POST /chat` com histórico em sessão Flask + `POST /reset`
4. Implementar `app.py` — entry point Flask
5. Construir frontend (HTML/CSS/JS): seleção de abordagem + interface de chat
6. Testar o app completo no browser

> Todos os arquivos de backend e frontend existem mas estão **vazios** — só a estrutura de pastas foi criada.

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

## Abordagens futuras
- ACT já incluído ✅
- Considerar adicionar mais abordagens no futuro (ex: Sistêmica, Junguiana)

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
psicologia_ai/
├── app.py                  # entry point Flask (vazio — a implementar)
├── personas.json           # definição das 7 abordagens ✅
├── routes/
│   └── chat.py             # POST /chat + POST /reset (vazio — a implementar)
├── services/
│   └── claude_service.py   # chama Claude API com system_prompt + histórico (vazio — a implementar)
├── tests/
│   ├── test_personas.py    # chat interativo de refinamento ✅
│   └── prompt_log.json     # histórico de versões e observações ✅
└── frontend/
    ├── templates/index.html   # (a implementar)
    └── static/
        ├── script.js          # (a implementar)
        └── style.css          # (a implementar)
```

---

## Stack

- Backend: Flask + Anthropic SDK
- Modelo: `claude-sonnet-4-6`
- Frontend: HTML/CSS/JS simples (seleção de abordagem + chat)
- Sem banco de dados no MVP — personas em JSON, histórico em sessão Flask
