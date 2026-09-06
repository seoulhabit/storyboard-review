import React from 'react';

export function ShQuote({ line, attribution }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--s3)', width: '100%', textAlign: 'left' }}>
      <div style={{ width: '100%', height: 'var(--hairline-w)', background: 'var(--hairline)' }}></div>
      <div style={{
        font: '700 calc(var(--t-display) * 0.8)/var(--lh-display) var(--font-subject)',
        textWrap: 'pretty'
      }}>{line}</div>
      {attribution ? (
        <div style={{
          font: 'var(--w-meta) var(--t-meta)/1.2 var(--font-work)',
          letterSpacing: 'var(--track-upper)', textTransform: 'uppercase',
          color: 'var(--text-secondary)'
        }}>{attribution}</div>
      ) : null}
    </div>
  );
}
