'use strict';

/* ─── DOM refs ──────────────────────────────────────────────────── */
const $ = id => document.getElementById(id);

const selectScreen        = $('select-screen');
const chatScreen          = $('chat-screen');
const cardsGrid           = $('cards-grid');
const chatMessages        = $('chat-messages');
const chatInput           = $('chat-input');
const chatIcon            = $('chat-icon');
const chatName            = $('chat-name');
const chatCategory        = $('chat-category');
const btnSend             = $('btn-send');
const btnBack             = $('btn-back');
const btnReset            = $('btn-reset');
const btnSobre            = $('btn-sobre');
const bibliographyPanel   = $('bibliography-panel');
const bibliographyContent = $('bibliography-content');

/* ─── State ─────────────────────────────────────────────────────── */
let personas = [];
let activePersona = null;

/* ─── SVG icon paths (viewBox 0 0 40 40) ───────────────────────── */
const ICONS = {
  // Divã — perfil de chaise longue
  'Psicólogo › Psicanalista': `
    <path d="M6 30 H34"/>
    <path d="M6 24 V30"/>
    <path d="M34 30 V14 H18"/>`,

  // Dois nós conectados: pensamento → comportamento
  'Psicólogo › CBT': `
    <circle cx="11" cy="20" r="7"/>
    <path d="M18 20 H22 M20 17.5 L23 20 L20 22.5"/>
    <circle cx="29" cy="20" r="7"/>`,

  // Dois arcos abertos um para o outro — escuta ativa
  'Psicólogo › Humanista': `
    <path d="M15 10 Q6 20 15 30"/>
    <path d="M25 10 Q34 20 25 30"/>`,

  // Prisma: linha entra, duas saem — reframe
  'Psicólogo › NLP': `
    <polygon points="20,8 8,32 32,32"/>
    <line x1="3"  y1="22" x2="10" y2="22"/>
    <line x1="28" y1="20" x2="37" y2="14"/>
    <line x1="30" y1="26" x2="37" y2="30"/>`,

  // Círculo incompleto (¾) — princípio do fechamento
  'Psicólogo › Gestalt': `
    <path d="M33 20 A13 13 0 1 0 20 33"/>`,

  // Linha de horizonte + ponto — presença no mundo
  'Psicólogo › Existencial': `
    <line x1="6" y1="28" x2="34" y2="28"/>
    <circle cx="20" cy="17" r="4"/>`,

  // Self (círculo grande) + pensamento flutuando ao lado — defusão
  'Psicólogo › ACT': `
    <circle cx="13" cy="27" r="9"/>
    <circle cx="31" cy="14" r="6"/>
    <circle cx="22.5" cy="21"   r="1.8" fill="currentColor"/>
    <circle cx="26"   cy="17.5" r="1.8" fill="currentColor"/>`,
};

/* ─── Init ──────────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', async () => {
  try {
    const res = await fetch('/personas');
    if (!res.ok) throw new Error();
    personas = await res.json();
    renderCards();
  } catch {
    cardsGrid.innerHTML =
      '<p style="color:var(--muted);text-align:center;padding:24px;width:100%">' +
      'Não foi possível carregar as abordagens. Verifique se o servidor está rodando.</p>';
  }
});

/* ─── Cards ─────────────────────────────────────────────────────── */
function renderCards() {
  cardsGrid.innerHTML = '';
  personas.forEach(p => {
    const shortName  = p.nome.split(' › ')[1] || p.nome;
    const iconPaths  = ICONS[p.nome] || '';

    const btn = document.createElement('button');
    btn.className = 'card';
    btn.setAttribute('role', 'listitem');
    btn.setAttribute('aria-label', `Conversar com ${shortName}`);
    btn.innerHTML = `
      <svg class="card-icon" viewBox="0 0 40 40" fill="none" stroke="currentColor"
           stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
           aria-hidden="true">${iconPaths}</svg>
      <span class="card-name">${shortName}</span>
      <span class="card-desc">${p.descricao_curta}</span>`;
    btn.addEventListener('click', () => startChat(p));
    cardsGrid.appendChild(btn);
  });
}

/* ─── Start chat ────────────────────────────────────────────────── */
async function startChat(persona) {
  activePersona = persona;

  await fetch('/reset', { method: 'POST' }).catch(() => {});

  const shortName = persona.nome.split(' › ')[1] || persona.nome;

  chatIcon.innerHTML = ICONS[persona.nome] || '';
  chatName.textContent     = shortName;
  chatCategory.textContent = persona.categoria;

  chatMessages.innerHTML = '';
  appendMessage('ai', persona.abertura);

  renderBibliography(persona);
  bibliographyPanel.classList.add('hidden');
  btnSobre.setAttribute('aria-expanded', 'false');
  btnSobre.classList.remove('active');

  selectScreen.classList.add('hidden');
  chatScreen.classList.remove('hidden');
  chatInput.focus();
}

/* ─── Messages ──────────────────────────────────────────────────── */
function appendMessage(role, text) {
  const wrap = document.createElement('div');
  wrap.className = `message ${role}`;
  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.textContent = text;
  wrap.appendChild(bubble);
  chatMessages.appendChild(wrap);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTyping() {
  const wrap = document.createElement('div');
  wrap.className = 'message ai';
  wrap.id = 'typing-indicator';
  wrap.innerHTML = `
    <div class="bubble typing-bubble">
      <span class="typing-dot"></span>
      <span class="typing-dot"></span>
      <span class="typing-dot"></span>
    </div>`;
  chatMessages.appendChild(wrap);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTyping() {
  const el = $('typing-indicator');
  if (el) el.remove();
}

/* ─── Send ──────────────────────────────────────────────────────── */
async function sendMessage() {
  const text = chatInput.value.trim();
  if (!text || !activePersona) return;

  chatInput.value = '';
  setInputDisabled(true);
  appendMessage('user', text);
  showTyping();

  try {
    const res  = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ persona: activePersona.nome, message: text }),
    });
    const data = await res.json();
    removeTyping();
    appendMessage('ai', res.ok ? data.reply : `Erro: ${data.error}`);
  } catch {
    removeTyping();
    appendMessage('ai', 'Não foi possível conectar ao servidor.');
  } finally {
    setInputDisabled(false);
    chatInput.focus();
  }
}

function setInputDisabled(v) {
  chatInput.disabled = v;
  btnSend.disabled   = v;
}

/* ─── Reset ─────────────────────────────────────────────────────── */
async function resetConversation() {
  const name = activePersona?.nome.split(' › ')[1] || 'esta conversa';
  if (!confirm(`Reiniciar a conversa com ${name}?`)) return;
  await fetch('/reset', { method: 'POST' }).catch(() => {});
  chatMessages.innerHTML = '';
  appendMessage('ai', activePersona.abertura);
}

/* ─── Bibliography ──────────────────────────────────────────────── */
function renderBibliography(persona) {
  const b = persona.bibliografia;
  bibliographyContent.innerHTML = [
    { label: 'Origem',               text: b.origem },
    { label: 'Ideia central',        text: b.ideia_central },
    { label: 'Como funciona',        text: b.como_funciona },
    { label: 'Para quem é indicado', text: b.para_quem },
  ].map(s => `
    <div class="bib-section">
      <h3 class="bib-label">${s.label}</h3>
      <p class="bib-text">${s.text}</p>
    </div>`).join('');
}

function toggleBibliography() {
  const isOpen = !bibliographyPanel.classList.contains('hidden');
  bibliographyPanel.classList.toggle('hidden', isOpen);
  btnSobre.setAttribute('aria-expanded', String(!isOpen));
  btnSobre.classList.toggle('active', !isOpen);
}

/* ─── Back ──────────────────────────────────────────────────────── */
async function goBack() {
  await fetch('/reset', { method: 'POST' }).catch(() => {});
  chatScreen.classList.add('hidden');
  selectScreen.classList.remove('hidden');
}

/* ─── Events ────────────────────────────────────────────────────── */
btnSend.addEventListener('click', sendMessage);
btnBack.addEventListener('click', goBack);
btnReset.addEventListener('click', resetConversation);
btnSobre.addEventListener('click', toggleBibliography);
chatInput.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});
