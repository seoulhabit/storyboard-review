import React from 'react';

export function ShIngredient({ name, inci, function: fn, accent = false }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--s2)', alignItems: 'inherit' }}>
      <div style={{
        font: 'var(--w-display) var(--t-display)/var(--lh-display) var(--font-subject)',
        color: accent ? 'var(--accent)' : 'var(--text-primary)', textWrap: 'balance'
      }}>{name}</div>
      {inci ? (
        <div style={{
          font: 'var(--w-meta) var(--t-meta)/1.2 var(--font-work)',
          letterSpacing: 'var(--track-upper)', textTransform: 'uppercase',
          color: 'var(--text-secondary)'
        }}>{inci}</div>
      ) : null}
      {fn ? (
        <div style={{
          marginTop: 'var(--s2)', maxWidth: '90%',
          font: 'var(--w-body) var(--t-body)/var(--lh-body) var(--font-work)',
          color: 'var(--text-primary)', textWrap: 'pretty'
        }}>{fn}</div>
      ) : null}
    </div>
  );
}
