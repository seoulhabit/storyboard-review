import React from 'react';

export function ShRows({ rows = [], active = -1, revealed }) {
  const shown = typeof revealed === 'number' ? revealed : rows.length;
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--s3)', width: '100%', textAlign: 'left' }}>
      {rows.slice(0, Math.max(0, shown)).map((r, i) => {
        const isActive = i === active;
        return (
          <div key={i} style={{
            display: 'grid', gridTemplateColumns: 'minmax(0,auto) minmax(var(--s2),1fr) minmax(0,auto)',
            alignItems: 'center',
            opacity: isActive || active < 0 ? 1 : 'var(--row-dim)'
          }}>
            <div style={{
              font: 'var(--w-label) var(--t-label)/var(--lh-tight) var(--font-work)',
              letterSpacing: 'var(--track-upper)', textTransform: 'uppercase',
              color: isActive ? 'var(--accent)' : 'var(--text-primary)', minWidth: 0
            }}>{r.left}</div>
            <div style={{ width: '100%', minWidth: 'var(--s2)', height: 'var(--hairline-w)', background: 'var(--hairline)' }}></div>
            <div style={{
              font: '700 var(--t-label)/var(--lh-tight) var(--font-subject)',
              color: isActive ? 'var(--accent)' : 'var(--text-primary)', textAlign: 'right', minWidth: 0
            }}>{r.right}</div>
          </div>
        );
      })}
    </div>
  );
}
