const el = (id) => document.getElementById(id);

async function generate() {
  const payload = {
    topic: el("topic").value,
    audience: el("audience").value,
    tone: el("tone").value,
  };

  const res = await fetch('/api/generate-post', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    el("post").textContent = `Error: ${res.status}`;
    return;
  }

  const data = await res.json();
  el("post").textContent = data.post;
  el("imagePrompt").textContent = JSON.stringify(data.image_prompt, null, 2);

  const trendsEl = el("trends");
  trendsEl.innerHTML = '';
  data.trends.forEach((t) => {
    const li = document.createElement('li');
    li.textContent = `${t.title} — ${t.source}`;
    trendsEl.appendChild(li);
  });
}

el("generate").addEventListener('click', generate);
