/**
 * sh-chip — always-on source furniture. No source, no claim.
 */
export interface ShChipProps {
  /** Journal name and year, a standard ("CIR 2015"), or SEOULHABIT.COM. */
  source: string;
  /** true (default) pins it bottom-left inside the safe area; false renders inline. */
  pinned?: boolean;
}
export declare function ShChip(props: ShChipProps): JSX.Element;
