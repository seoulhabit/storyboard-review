import React from 'react';

export function ShSteps({ steps = [] }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', width: '100%', textAlign: 'left' }}>
      {steps.map((s, i) => (
        <div key={i} style={{ display: 'grid', gridTemplateColumns: 'auto minmax(0,1fr)', columnGap: 'var(--s3)' }}>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <div style={{
              font: 'var(--w-display) calc(var(--t-display) * 0.6)/1 var(--font-subject)',
              color: 'var(--accent)', fontVariantNumeric: 'tabular-nums'
            }}>{s.n != null ? s.n : i + 1}</div>
            {i < steps.length - 1 ? (
              <div style={{ flex: 1, width: 'var(--hairline-w)', background: 'var(--hairline)', margin: 'var(--s1) 0' }}></div>
            ) : null}
          </div>
          <div style={{ paddingBottom: i < steps.length - 1 ? 'var(--s3)' : 0, display: 'flex', flexDirection: 'column', gap: 'var(--s1)' }}>
            <div style={{
              font: 'var(--w-label) var(--t-label)/var(--lh-tight) var(--font-work)',
              letterSpacing: 'var(--track-upper)', textTransform: 'uppercase'
            }}>{s.action}</div>
            {s.note ? (
              <div style={{
                font: 'var(--w-body) var(--t-body)/var(--lh-body) var(--font-work)',
                color: 'var(--text-secondary)', textWrap: 'pretty'
              }}>{s.note}</div>
            ) : null}
          </div>
        </div>
      ))}
    </div>
  );
}
