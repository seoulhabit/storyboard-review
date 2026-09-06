import React from 'react';

export function ShEvidence({ figure, caption, source }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--s3)', alignItems: 'inherit' }}>
      <div data-sh-count style={{
        font: 'var(--w-hook) var(--t-hook)/1 var(--font-work)',
        letterSpacing: 'var(--track-upper)', color: 'var(--accent)',
        fontVariantNumeric: 'tabular-nums'
      }}>{figure}</div>
      {caption ? (
        <div style={{
          maxWidth: '90%', font: 'var(--w-body) var(--t-body)/var(--lh-body) var(--font-work)',
          textWrap: 'pretty'
        }}>{caption}</div>
      ) : null}
      {source ? (
        <div style={{
          font: 'var(--w-chip) var(--t-chip)/1.2 var(--font-work)',
          letterSpacing: 'var(--track-upper)', textTransform: 'uppercase',
          color: 'var(--text-secondary)'
        }}>{source}</div>
      ) : null}
    </div>
  );
}
