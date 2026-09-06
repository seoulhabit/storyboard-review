import React from 'react';

export function ShEndcard({ cta }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--s3)', alignItems: 'center', textAlign: 'center' }}>
      <div style={{ font: '700 var(--t-display)/var(--lh-display) var(--font-subject)', color: 'var(--text-primary)' }}>서울의 습관</div>
      <div style={{
        font: 'var(--w-label) var(--t-label)/1 var(--font-work)',
        letterSpacing: '0.18em', textTransform: 'uppercase', color: 'var(--accent)'
      }}>SEOULHABIT</div>
      <div style={{
        marginTop: 'var(--s3)',
        font: 'var(--w-meta) var(--t-meta)/1.3 var(--font-work)',
        letterSpacing: 'var(--track-upper)', textTransform: 'uppercase', color: 'var(--text-secondary)'
      }}>{cta}</div>
    </div>
  );
}
