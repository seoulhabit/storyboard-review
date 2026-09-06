import React from 'react';
import { ShChip } from '../furniture/ShChip.jsx';

const CANVAS = { '9x16': [1080, 1920], '16x9': [1920, 1080] };

export function ShScene({ aspect = '9x16', width, chip, align = 'center', children, style }) {
  const [bw, bh] = CANVAS[aspect] || CANVAS['9x16'];
  const k = (width || bw) / bw;
  return (
    <div style={{ position: 'relative', width: bw * k, height: bh * k, overflow: 'hidden', background: 'var(--bg)', ...style }}>
      <div
        data-canvas={aspect}
        style={{
          position: 'absolute', top: 0, left: 0, width: bw, height: bh,
          transform: 'scale(' + k + ')', transformOrigin: 'top left',
          background: 'var(--scene-bg)', color: 'var(--text-primary)',
          fontFamily: 'var(--font-work)', WebkitFontSmoothing: 'antialiased'
        }}
      >
        <div style={{
          position: 'absolute', left: 'var(--safe-x)', right: 'var(--safe-x)',
          top: 'var(--safe-top)', bottom: 'var(--safe-bottom)',
          display: 'flex', flexDirection: 'column', justifyContent: 'center',
          alignItems: align === 'center' ? 'center' : 'stretch',
          textAlign: align === 'center' ? 'center' : 'left',
          gap: 'var(--rhythm-within)'
        }}>
          {children}
        </div>
        {chip ? <ShChip source={chip} /> : null}
      </div>
    </div>
  );
}
