import type { ReactNode, CSSProperties } from 'react';
/**
 * Scene frame: cream ground, canvas-scoped tokens, safe area, pinned source chip.
 */
export interface ShSceneProps {
  /** 9x16 (1080x1920, default) or 16x9 (1920x1080). Sets the token scope. */
  aspect?: '9x16' | '16x9';
  /** Rendered width in px. The 1080/1920 stage is scaled to fit it. Default: native. */
  width?: number;
  /** Source line for the pinned sh-chip. Omit only on scenes that state no claim. */
  chip?: string;
  /** center (default) for hook/ingredient/evidence/endcard; left for rows/steps/compare/quote. */
  align?: 'center' | 'left';
  children?: ReactNode;
  style?: CSSProperties;
}
export declare function ShScene(props: ShSceneProps): JSX.Element;
