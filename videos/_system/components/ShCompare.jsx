import React from 'react';

const head = {
  font: 'var(--w-label) var(--t-label)/var(--lh-tight) var(--font-work)',
  letterSpacing: 'var(--track-upper)', textTransform: 'uppercase'
};
const val = { font: 'var(--w-body) var(--t-body)/var(--lh-body) var(--font-work)' };
const lbl = {
  font: 'var(--w-meta) var(--t-meta)/1.2 var(--font-work)',
  letterSpacing: 'var(--track-upper)', textTransform: 'uppercase', color: 'var(--text-secondary)'
};

export function ShCompare({ a, b, attributes = [] }) {
  return (
    <div style={{ position: 'relative', display: 'grid', gridTemplateColumns: '1fr 1fr', columnGap: 'var(--s5)', width: '100%', textAlign: 'left' }}>
      <div style={{ position: 'absolute', left: '50%', top: 0, bottom: 0, width: 'var(--hairline-w)', background: 'var(--hairline)' }}></div>
      <div style={head}>{a}</div>
      <div style={head}>{b}</div>
      {attributes.map((at, i) => (
        <React.Fragment key={i}>
          <div style={{ marginTop: 'var(--s4)', display: 'flex', flexDirection: 'column', gap: 'var(--s1)' }}>
            <div style={lbl}>{at.label}</div>
            <div style={{ ...val, color: at.favours === 'a' ? 'var(--accent)' : 'var(--text-primary)' }}>{at.aValue}</div>
          </div>
          <div style={{ marginTop: 'var(--s4)', display: 'flex', flexDirection: 'column', gap: 'var(--s1)' }}>
            <div style={lbl}>{at.label}</div>
            <div style={{ ...val, color: at.favours === 'b' ? 'var(--accent)' : 'var(--text-primary)' }}>{at.bValue}</div>
          </div>
        </React.Fragment>
      ))}
    </div>
  );
}
