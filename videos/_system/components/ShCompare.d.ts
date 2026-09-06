/**
 * sh-compare — two columns split by a brass rule; clay marks one winning side per row.
 */
export interface ShCompareAttribute { label: string; aValue: string; bValue: string; favours?: 'a' | 'b' }
export interface ShCompareProps {
  /** Left column header. */
  a: string;
  /** Right column header. */
  b: string;
  /** Three attribute rows maximum. No ticks, no crosses, never both sides. */
  attributes: ShCompareAttribute[];
}
export declare function ShCompare(props: ShCompareProps): JSX.Element;
