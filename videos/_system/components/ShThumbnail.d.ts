/**
 * Thumbnail — cream, three words or fewer, clay on one, no face and no border.
 */
export interface ShThumbnailProps {
  /** Three words or fewer. */
  words: string[];
  /** Index of the clay word. */
  accentIndex?: number;
  /** 9x16 places the text in the top 40%; 16x9 centres it. */
  aspect?: '9x16' | '16x9';
  /** Rendered width in px. */
  width?: number;
}
export declare function ShThumbnail(props: ShThumbnailProps): JSX.Element;
