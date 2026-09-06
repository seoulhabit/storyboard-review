import React from 'react';

export function ShChip({ source, pinned = true }) {
  return (
    <div style={{
      position: pinned ? 'absolute' : 'static',
      left: pinned ? 'var(--safe-x)' : undefined,
      bottom: pinned ? 'var(--safe-bottom)' : undefined,
      opacity: 'var(--chip-opacity)',
      borderLeft: 'var(--hairline-w) solid var(--hairline)',
      paddingLeft: 'var(--s1)',
      font: 'var(--w-chip) var(--t-chip)/1.2 var(--font-work)',
      letterSpacing: 'var(--track-upper)',
      textTransform: 'uppercase',
      color: 'var(--text-secondary)',
      textAlign: 'left'
    }}>{source}</div>
  );
}
