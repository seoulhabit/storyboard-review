import React from 'react';
// one clay word per scene — never bold, italic, underline or a box
function accented(text, word) {
  if (!word) return text;
  const parts = String(text).split(new RegExp('(' + String(word).replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'i'));
  let done = false;
  return parts.map((p, i) => {
    if (!done && p.toLowerCase() === String(word).toLowerCase()) {
      done = true;
      return React.createElement('span', { key: i, style: { color: 'var(--accent)' } }, p);
    }
    return p;
  });
}

export function ShHook({ line, accentWord }) {
  return (
    <h1 style={{
      margin: 0, maxWidth: '100%',
      font: 'var(--w-hook) var(--t-hook)/var(--lh-tight) var(--font-work)',
      letterSpacing: 'var(--track-upper)', textTransform: 'uppercase',
      textWrap: 'balance', color: 'var(--text-primary)'
    }}>{accented(line, accentWord)}</h1>
  );
}
