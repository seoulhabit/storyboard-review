import React from 'react';

export function ShThumbnail({ words = [], accentIndex = -1, aspect = '9x16', width }) {
  const [bw, bh] = aspect === '16x9' ? [1920, 1080] : [1080, 1920];
  const k = (width || bw) / bw;
  return (
    <div style={{ position: 'relative', width: bw * k, height: bh * k, overflow: 'hidden', background: 'var(--bg)' }}>
      <div data-canvas={aspect} style={{
        position: 'absolute', top: 0, left: 0, width: bw, height: bh,
        transform: 'scale(' + k + ')', transformOrigin: 'top left',
        background: 'var(--bg)', padding: '0 var(--safe-x)',
        display: 'flex', flexDirection: 'column',
        justifyContent: aspect === '16x9' ? 'center' : 'flex-start',
        paddingTop: aspect === '16x9' ? 0 : '12%', boxSizing: 'border-box'
      }}>
        <div style={{
          font: '700 calc(var(--t-display) * 1.1)/1.02 var(--font-subject)',
          color: 'var(--ink)', textWrap: 'balance'
        }}>
          {words.slice(0, 3).map((w, i) => (
            <span key={i} style={{ color: i === accentIndex ? 'var(--accent)' : 'inherit' }}>{i ? ' ' : ''}{w}</span>
          ))}
        </div>
      </div>
    </div>
  );
}
