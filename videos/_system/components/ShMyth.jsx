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

export function ShMyth({ claim, correction, accentWord, struck = true }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--s5)', alignItems: 'inherit', width: '100%' }}>
      <div style={{ position: 'relative', display: 'inline-block' }}>
        <div style={{
          font: 'var(--w-body) var(--t-body)/var(--lh-body) var(--font-work)',
          color: 'var(--text-secondary)', textWrap: 'pretty'
        }}>{claim}</div>
        <div data-sh-strike style={{
          position: 'absolute', left: 0, top: '50%', width: struck ? '100%' : 0,
          height: 'var(--hairline-w)', background: 'var(--ink)', transformOrigin: 'left center'
        }}></div>
      </div>
      <div style={{
        font: 'var(--w-label) var(--t-label)/var(--lh-tight) var(--font-work)',
        letterSpacing: 'var(--track-upper)', textTransform: 'uppercase', textWrap: 'balance'
      }}>{accented(correction, accentWord)}</div>
    </div>
  );
}
