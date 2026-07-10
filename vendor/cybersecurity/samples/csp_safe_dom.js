/** FSOT code-genome sample — CSP-safe DOM updates. */
function fsotSetText(el, text) {
  if (!el) return;
  el.textContent = String(text);
}

async function fsotFetchJson(url) {
  const res = await fetch(url, { credentials: "same-origin" });
  if (!res.ok) throw new Error("fetch failed");
  return res.json();
}

module.exports = { fsotSetText, fsotFetchJson };