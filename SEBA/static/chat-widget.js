/* ── S.E.B.A. Chat Sidebar — Visual Card Engine v3 ─────────────── */
(function () {

/* ── CSS ─────────────────────────────────────────────────────────── */
document.head.insertAdjacentHTML('beforeend', `<style>
#sc-bd{display:none;position:fixed;inset:0;background:rgba(0,0,0,.55);backdrop-filter:blur(4px);z-index:99997;opacity:0;transition:opacity .25s}
#sc-bd.on{display:block}#sc-bd.vis{opacity:1}
#sc-dw{
  position:fixed;top:0;right:0;width:390px;max-width:100vw;height:100vh;
  background:#080810;border-left:1px solid rgba(99,102,241,.15);
  box-shadow:-16px 0 60px rgba(0,0,0,.8);
  display:flex;flex-direction:column;z-index:99998;
  transform:translateX(100%);transition:transform .3s cubic-bezier(.4,0,.2,1);
}
#sc-dw.on{transform:translateX(0)}
/* Header */
.sc-hd{display:flex;align-items:center;gap:10px;padding:13px 14px;background:rgba(99,102,241,.07);border-bottom:1px solid rgba(99,102,241,.13);flex-shrink:0}
.sc-logo{width:34px;height:34px;border-radius:9px;background:linear-gradient(135deg,#6366f1,#4338ca);display:flex;align-items:center;justify-content:center;font-size:1rem;box-shadow:0 3px 10px rgba(99,102,241,.4)}
.sc-ht{flex:1}.sc-hn{font-size:.88rem;font-weight:700;color:#f0f0f8}.sc-hs{font-size:.63rem;color:#6366f1;display:flex;align-items:center;gap:4px;margin-top:1px}
.sc-dot{width:5px;height:5px;border-radius:50%;background:#22c55e;box-shadow:0 0 5px #22c55e;animation:scP 2s infinite}
@keyframes scP{0%,100%{opacity:1}50%{opacity:.4}}
.sc-cl{width:28px;height:28px;border-radius:7px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.07);color:#6b6b8a;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:.85rem;transition:all .18s;flex-shrink:0}
.sc-cl:hover{background:rgba(224,62,92,.15);border-color:rgba(224,62,92,.3);color:#e03e5c}
/* Body */
.sc-bd{flex:1;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:10px;min-height:0}
.sc-bd::-webkit-scrollbar{width:3px}.sc-bd::-webkit-scrollbar-thumb{background:rgba(99,102,241,.25);border-radius:99px}
/* Welcome */
.sc-wl{background:linear-gradient(135deg,rgba(99,102,241,.1),rgba(67,56,202,.05));border:1px solid rgba(99,102,241,.18);border-radius:14px;padding:14px}
.sc-wt{font-size:.9rem;font-weight:700;color:#f0f0f8;margin-bottom:5px}
.sc-ws{font-size:.72rem;color:#6b6b8a;line-height:1.55;margin-bottom:12px}
.sc-chips{display:flex;flex-wrap:wrap;gap:6px}
.sc-chip{padding:6px 12px;border:1px solid rgba(99,102,241,.22);border-radius:99px;background:rgba(99,102,241,.07);color:#a5b4fc;font-size:.7rem;font-weight:500;cursor:pointer;transition:all .18s;font-family:inherit}
.sc-chip:hover{background:rgba(99,102,241,.2);border-color:rgba(99,102,241,.5);color:#fff;transform:translateY(-1px)}
/* User bubble */
.sc-row{display:flex;gap:8px;animation:scUp .22s ease}.sc-row.me{flex-direction:row-reverse}
@keyframes scUp{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
.sc-av{width:26px;height:26px;border-radius:7px;display:flex;align-items:center;justify-content:center;font-size:.8rem;flex-shrink:0;margin-top:2px}
.sc-av-b{background:rgba(99,102,241,.2);border:1px solid rgba(99,102,241,.3)}
.sc-av-u{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1)}
.sc-ub{max-width:82%;padding:9px 13px;border-radius:11px 2px 11px 11px;background:linear-gradient(135deg,#6366f1,#4338ca);color:#fff;font-size:.8rem;line-height:1.55}
/* Cards */
.sc-cards{display:flex;flex-direction:column;gap:7px;max-width:96%}

/* STAT card */
.sc-sc{
  display:grid;grid-template-columns:1fr 1fr;gap:6px;
}
.sc-sv{
  background:rgba(99,102,241,.09);border:1px solid rgba(99,102,241,.18);border-radius:11px;
  padding:11px 12px;display:flex;flex-direction:column;gap:2px;
  animation:scUp .28s ease;
}
.sc-sv.danger{background:rgba(224,62,92,.08);border-color:rgba(224,62,92,.25)}
.sc-sv.good{background:rgba(34,197,94,.07);border-color:rgba(34,197,94,.22)}
.sc-sv.warn{background:rgba(245,158,11,.07);border-color:rgba(245,158,11,.22)}
.sc-sv-ico{font-size:1.1rem}
.sc-sv-val{font-size:1.25rem;font-weight:800;color:#fff;line-height:1.1;margin-top:4px}
.sc-sv-lbl{font-size:.62rem;color:#6b6b8a;text-transform:uppercase;letter-spacing:.5px;margin-top:1px}

/* INSIGHT pill */
.sc-ip{
  border-radius:10px;padding:9px 12px;font-size:.76rem;line-height:1.55;
  border-left:3px solid;animation:scSlide .28s ease;
}
@keyframes scSlide{from{opacity:0;transform:translateX(-6px)}to{opacity:1;transform:translateX(0)}}
.sc-ip.danger{background:rgba(224,62,92,.08);border-color:#e03e5c;color:#fca5a5}
.sc-ip.warn{background:rgba(245,158,11,.07);border-color:#f59e0b;color:#fcd34d}
.sc-ip.good{background:rgba(34,197,94,.07);border-color:#22c55e;color:#86efac}
.sc-ip.info{background:rgba(99,102,241,.08);border-color:#6366f1;color:#c7d2fe}
.sc-ip.neutral{background:rgba(255,255,255,.04);border-color:rgba(255,255,255,.1);color:#c4c4d4}
.sc-ip strong{color:#fff}
.sc-ip-hd{font-weight:700;color:#fff;margin-bottom:3px;display:flex;align-items:center;gap:5px;font-size:.78rem}

/* TIP card */
.sc-tip{
  background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);
  border-radius:10px;padding:9px 12px;
  display:flex;gap:9px;align-items:flex-start;
  font-size:.76rem;line-height:1.6;color:#b4b4cc;animation:scSlide .32s ease;
}
.sc-tip-ico{font-size:1rem;flex-shrink:0;margin-top:.1rem}
.sc-tip strong{color:#f0f0f8}

/* Typing */
.sc-ty{display:flex;align-items:center;gap:8px;background:rgba(99,102,241,.07);border:1px solid rgba(99,102,241,.15);border-radius:10px;padding:11px 13px}
.sc-d{width:6px;height:6px;border-radius:50%;background:#6366f1;animation:scBl 1.2s infinite}
.sc-d:nth-child(2){animation-delay:.18s}.sc-d:nth-child(3){animation-delay:.36s}
@keyframes scBl{0%,80%,100%{opacity:.2;transform:scale(.8)}40%{opacity:1;transform:scale(1)}}
.sc-ty-txt{font-size:.7rem;color:#6b6b8a}

/* Error */
.sc-err{background:rgba(224,62,92,.08);border:1px solid rgba(224,62,92,.2);border-radius:10px;padding:10px 13px;font-size:.77rem;color:#fca5a5;line-height:1.5}

/* API banner */
.sc-apib{display:none;margin:6px 12px 0;padding:7px 11px;background:rgba(239,68,68,.08);border:1px solid rgba(239,68,68,.2);border-radius:8px;font-size:.7rem;color:#fca5a5;flex-shrink:0}
/* Footer */
.sc-ft{display:flex;gap:7px;align-items:flex-end;padding:10px 11px;border-top:1px solid rgba(255,255,255,.06);background:rgba(4,4,12,.95);flex-shrink:0}
.sc-in{flex:1;padding:9px 12px;border:1.5px solid rgba(99,102,241,.18);border-radius:9px;background:rgba(0,0,0,.55);color:#f0f0f8;font-size:.8rem;outline:none;transition:border-color .2s;font-family:inherit;resize:none;min-height:38px;max-height:90px;line-height:1.5}
.sc-in:focus{border-color:#6366f1;box-shadow:0 0 0 2px rgba(99,102,241,.12)}
.sc-in::placeholder{color:#2a2a42}
.sc-sb{width:38px;height:38px;border:none;border-radius:9px;flex-shrink:0;background:linear-gradient(135deg,#6366f1,#4338ca);color:#fff;font-size:1rem;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(99,102,241,.35);transition:all .2s}
.sc-sb:hover{transform:scale(1.07);box-shadow:0 6px 18px rgba(99,102,241,.5)}
.sc-sb:disabled{opacity:.3;cursor:not-allowed;transform:none;box-shadow:none}
</style>`);

/* ── HTML ─────────────────────────────────────────────────────────── */
document.body.insertAdjacentHTML('beforeend', `
<div id="sc-bd"></div>
<div id="sc-dw" role="dialog" aria-label="S.E.B.A. Assistant">
  <div class="sc-hd">
    <div class="sc-logo">🧠</div>
    <div class="sc-ht">
      <div class="sc-hn">S.E.B.A. Assistant</div>
      <div class="sc-hs"><span class="sc-dot"></span>Online</div>
    </div>
    <button class="sc-cl" onclick="toggleChat()" title="Close">✕</button>
  </div>
  <div class="sc-apib" id="scApi">⚠️ Groq API key not set. Add <strong>GROQ_API_KEY</strong> to Render.</div>
  <div class="sc-bd" id="scBd">
    <div class="sc-wl">
      <div class="sc-wt">👋 Your AI finance coach</div>
      <div class="sc-ws">Tap a card below for instant insights — answers appear as visual cards, not paragraphs.</div>
      <div class="sc-chips">
        <button class="sc-chip" onclick="scAsk('summary')">📊 My summary</button>
        <button class="sc-chip" onclick="scAsk('categories')">🏆 Top categories</button>
        <button class="sc-chip" onclick="scAsk('impulse')">⚡ Impulse check</button>
        <button class="sc-chip" onclick="scAsk('savings')">💰 How to save</button>
        <button class="sc-chip" onclick="scAsk('health')">❤️ Health score</button>
        <button class="sc-chip" onclick="scAsk('weekends')">🗓️ Weekends</button>
        <button class="sc-chip" onclick="scAsk('invest')">📈 Where to invest</button>
      </div>
    </div>
  </div>
  <div class="sc-ft">
    <textarea class="sc-in" id="scIn" placeholder="Ask anything…" rows="1"
      onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();scSend()}"
      oninput="this.style.height='auto';this.style.height=Math.min(this.scrollHeight,90)+'px'"></textarea>
    <button class="sc-sb" id="scBtn" onclick="scSend()">➤</button>
  </div>
</div>`);

/* ── State ─────────────────────────────────────────────────────────── */
let _chatSess; try { _chatSess = JSON.parse(localStorage.getItem('sebaUser') || ''); } catch(e) {}
const U = (_chatSess && _chatSess.user_id) ? _chatSess.user_id : null;
let hist = [], userCtx = null, isOpen = false;

/* ── Toggle ────────────────────────────────────────────────────────── */
window.toggleChat = function () {
  isOpen = !isOpen;
  const bd = document.getElementById('sc-bd'), dw = document.getElementById('sc-dw');
  if (isOpen) {
    bd.classList.add('on');
    requestAnimationFrame(() => { dw.classList.add('on'); bd.classList.add('vis'); });
    setTimeout(() => document.getElementById('scIn')?.focus(), 320);
    if (!userCtx) loadCtx();
  } else {
    dw.classList.remove('on'); bd.classList.remove('vis');
    setTimeout(() => bd.classList.remove('on'), 300);
  }
};
document.getElementById('sc-bd').onclick = window.toggleChat;
document.addEventListener('keydown', e => { if (e.key === 'Escape' && isOpen) window.toggleChat(); });

/* Patch FABs */
document.querySelectorAll('.chat-fab,.fab').forEach(b => {
  if ((b.getAttribute('onclick') || '').includes("'/chat'") || (b.getAttribute('onclick') || '').includes('"/chat"'))
    b.setAttribute('onclick', 'toggleChat()');
});

/* ── Open chat after upload with greeting + chips ───────────────────── */
window.openChatAfterUpload = function(importedCount) {
  // Open the panel if not already open
  if (!isOpen) {
    isOpen = true;
    const bd = document.getElementById('sc-bd'), dw = document.getElementById('sc-dw');
    bd.classList.add('on');
    requestAnimationFrame(() => { dw.classList.add('on'); bd.classList.add('vis'); });
  }

  // Reload user context fresh from new data
  userCtx = null;
  loadCtx();

  // Inject greeting card into chat body
  const chatBd = document.getElementById('scBd');
  const greeting = document.createElement('div');
  greeting.className = 'sc-row';
  greeting.innerHTML = `
    <div class="sc-av sc-av-b">🧠</div>
    <div class="sc-cards">
      <div class="sc-ip info" style="border-left-color:#6366f1;background:rgba(99,102,241,.1)">
        <div class="sc-ip-hd">🎉 Statement uploaded${importedCount ? ' — ' + importedCount + ' transactions added' : ''}!</div>
        Hey! Wanna know how you could go about understanding your spendings?
      </div>
      <div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:8px">
        <button class="sc-chip" onclick="scAsk('Give me a full breakdown of my spending categories')">📊 Spending breakdown</button>
        <button class="sc-chip" onclick="scAsk('Where am I overspending the most?')">🔍 Where I overspend</button>
        <button class="sc-chip" onclick="scAsk('How much did I spend this month vs last month?')">📅 Month comparison</button>
        <button class="sc-chip" onclick="scAsk('Which purchases were impulsive and how can I cut them?')">⚡ Impulse buys</button>
        <button class="sc-chip" onclick="scAsk('How much can I realistically save each month?')">💰 Savings potential</button>
        <button class="sc-chip" onclick="scAsk('Give me 3 specific tips to improve my financial health score')">❤️ Improve health score</button>
      </div>
    </div>`;
  chatBd.appendChild(greeting);
  chatBd.scrollTop = chatBd.scrollHeight;
};

/* ── Load context ───────────────────────────────────────────────────── */
async function loadCtx() {
  try {
    const fmt = n => '₹' + new Intl.NumberFormat('en-IN', { maximumFractionDigits: 0 }).format(n || 0);
    const [d, p] = await Promise.all([
      fetch(`/analytics/dashboard/${U}`).then(r => r.json()).catch(() => null),
      fetch(`/analytics/patterns/${U}`).then(r => r.json()).catch(() => null),
    ]);
    if (!d) { userCtx = 'No data.'; return; }
    const today = new Date().toISOString().split('T')[0], mo = today.slice(0, 7);
    const cats = Object.entries(d.by_category || {}).sort(([, a], [, b]) => b - a)
      .slice(0, 5).map(([k, v]) => `${k}=${fmt(v)}`).join(', ');
    const mos = Object.entries(d.monthly_breakdown || {}).sort(([a], [b]) => b.localeCompare(a))
      .slice(0, 4).map(([k, v]) => `${k}=${fmt(v)}`).join(', ');
    userCtx = [
      `DATE=${today}`, `TOTAL_SPENT=${fmt(d.total_spent)}`,
      `THIS_MONTH=${fmt(d.monthly_breakdown?.[mo] || 0)}`,
      `TRANSACTIONS=${d.transaction_count}`,
      `IMPULSIVE_COUNT=${d.impulsive_count}`, `IMPULSIVE_AMT=${fmt(d.impulsive_total)}`,
      `CATEGORIES=${cats}`, `MONTHLY=${mos}`,
      p ? `WEEKEND_RISK=${p.weekend_risk ? Math.round((p.weekend_avg_per_tx / p.weekday_avg_per_tx - 1) * 100) + '%_more_on_weekends' : 'no'}` : '',
      p?.top_impulsive_category ? `TOP_IMPULSE_CAT=${p.top_impulsive_category}` : '',
    ].filter(Boolean).join('\n');
  } catch { userCtx = 'Error loading data.'; }
}

/* ── System prompt ──────────────────────────────────────────────────── */
function buildSystem() {
  return {
    parts: [{
      text: `You are S.E.B.A., a calm, subtle, and highly perceptive personal finance coach. 
Your goal is to guide the user gently toward better financial habits without sounding robotic or blunt. 
When asked subjective questions (like "Can I buy an iPhone?"), NEVER give a flat "yes" or "no". Instead, provide nuanced, empowering coaching (e.g., "Yes, you can make this work if you adjust these two habits...", or "It's possible within 3 months if we cut back your recent impulsive spends"). 

Reply ONLY using these exact card tags. Never use raw paragraphs or prose.

RULES:
- STAT cards: For highlighting key numbers from their data. Max 4.
- INSIGHT cards: For coaching, observations, and subtle advice. Make the tone warm and empowering, but direct. Max 4. Mark type: [warn], [danger], [good], [info].
- TIP cards: For specific, actionable habit changes (e.g., "Try the 10-minute rule before buying..."). Max 3.
- Keep every card under 20-25 words. Be a bit more conversational but maintain the card format.
- NO introduction, NO conclusion, NO filler text outside of the tags.

FORMAT (use exactly):
STAT|<emoji>|<value>|<short label>
INSIGHT|[type]|<emoji>|<one or two coaching sentences>
TIP|<emoji>|<one specific action to take>

Example:
STAT|💸|₹10,600|April Spend
INSIGHT|[info]|📱|You can definitely afford that iPhone if we make a slight adjustment to your weekend spending.
INSIGHT|[warn]|📉|Right now, your recent impulse buys are eating into what could be your gadget fund.
TIP|💡|Try pausing your restaurant spending for just two weeks to free up the cash.

User data:
${userCtx || 'No data loaded yet.'}`
    }]
  };
}

/* ── User message ───────────────────────────────────────────────────── */
function addUser(q) {
  const bd = document.getElementById('scBd');
  bd.insertAdjacentHTML('beforeend', `
    <div class="sc-row me">
      <div class="sc-av sc-av-u">👤</div>
      <div class="sc-ub">${q.replace(/</g, '&lt;')}</div>
    </div>`);
  bd.scrollTop = bd.scrollHeight;
}

/* ── Typing ─────────────────────────────────────────────────────────── */
function showTyping() {
  const bd = document.getElementById('scBd');
  bd.insertAdjacentHTML('beforeend', `
    <div class="sc-row" id="scTy">
      <div class="sc-av sc-av-b">🧠</div>
      <div class="sc-ty"><div class="sc-d"></div><div class="sc-d"></div><div class="sc-d"></div><span class="sc-ty-txt">Thinking…</span></div>
    </div>`);
  bd.scrollTop = bd.scrollHeight;
}
function hideTyping() { document.getElementById('scTy')?.remove(); }

/* ── Response card renderer ─────────────────────────────────────────── */
function renderCards(text) {
  const bd = document.getElementById('scBd');
  const wrap = document.createElement('div');
  wrap.className = 'sc-row';
  wrap.innerHTML = `<div class="sc-av sc-av-b">🧠</div><div class="sc-cards" id="cc${Date.now()}"></div>`;
  bd.appendChild(wrap);
  const cc = wrap.querySelector('.sc-cards');

  const lines = text.split('\n').map(l => l.trim()).filter(Boolean);
  const stats = [];
  let rendered = 0;

  lines.forEach(line => {
    const parts = line.split('|').map(p => p.trim());

    /* STAT */
    if (parts[0] === 'STAT' && parts.length >= 4) {
      const [, ico, val, lbl] = parts;
      stats.push({ ico, val, lbl });
      return;
    }
    /* Flush stat grid when we hit a non-stat */
    if (stats.length && parts[0] !== 'STAT') flushStats();

    /* INSIGHT */
    if (parts[0] === 'INSIGHT' && parts.length >= 4) {
      flushStats();
      const type = (parts[1].match(/\w+/) || ['info'])[0];
      const ico = parts[2], txt = parts[3];
      cc.insertAdjacentHTML('beforeend', `<div class="sc-ip ${type}"><div class="sc-ip-hd">${ico} </div>${txt}</div>`);
      rendered++;
    }

    /* TIP */
    if (parts[0] === 'TIP' && parts.length >= 3) {
      flushStats();
      const ico = parts[1], txt = parts[2];
      cc.insertAdjacentHTML('beforeend', `<div class="sc-tip"><span class="sc-tip-ico">${ico}</span><span>${txt}</span></div>`);
      rendered++;
    }
  });

  flushStats();

  /* Fallback if nothing parsed */
  if (!rendered && !stats.length) {
    const clean = text.replace(/\*\*/g, '').replace(/\n/g, ' ').substring(0, 200).trim();
    cc.insertAdjacentHTML('beforeend', `<div class="sc-ip neutral">${clean}</div>`);
  }

  bd.scrollTop = bd.scrollHeight;

  function flushStats() {
    if (!stats.length) return;
    const grid = document.createElement('div');
    grid.className = 'sc-sc';
    stats.splice(0).forEach(s => {
      const tone = /impuls|danger|high|over/i.test(s.lbl) ? 'danger' : /good|save|safe/i.test(s.lbl) ? 'good' : /warn|risk/i.test(s.lbl) ? 'warn' : '';
      grid.insertAdjacentHTML('beforeend', `
        <div class="sc-sv ${tone}">
          <div class="sc-sv-ico">${s.ico}</div>
          <div class="sc-sv-val">${s.val}</div>
          <div class="sc-sv-lbl">${s.lbl}</div>
        </div>`);
    });
    cc.appendChild(grid);
    rendered++;
  }
}

/* ── Ask / Send ─────────────────────────────────────────────────────── */
window.scAsk = q => { document.getElementById('scIn').value = q; scSend(); };

window.scSend = async function () {
  const inp = document.getElementById('scIn'), btn = document.getElementById('scBtn');
  const q = inp.value.trim(); if (!q) return;
  inp.value = ''; inp.style.height = 'auto'; btn.disabled = true;
  addUser(q);
  hist.push({ role: 'user', parts: [{ text: q }] });
  showTyping();
  if (!userCtx) await loadCtx();

  try {
    const res = await fetch('/chat/ai', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ system_instruction: buildSystem(), contents: hist })
    });
    const data = await res.json();
    hideTyping();

    if (res.status === 503) {
      document.getElementById('scApi').style.display = 'block';
      renderCards('INSIGHT|[danger]|⚠️|Groq API key not configured on server');
    } else if (res.ok) {
      const text = data.candidates?.[0]?.content?.parts?.[0]?.text || '';
      renderCards(text);
      hist.push({ role: 'model', parts: [{ text }] });
      if (hist.length > 20) hist = hist.slice(-20);
    } else {
      renderCards(`INSIGHT|[danger]|❌|${data.detail || 'Something went wrong — please try again'}`);
    }
  } catch {
    hideTyping();
    renderCards('INSIGHT|[danger]|📡|Network error — is the backend running?');
  } finally { btn.disabled = false; }
};

})();
