/**
 * sh-evidence — one figure or finding, counted up, with the study named beneath.
 */
export interface ShEvidenceProps {
  /** The figure, e.g. "0.3%" or "12 weeks". Counts up in the timeline. */
  figure: string;
  /** The finding in one line. */
  caption?: string;
  /** Study or standard, uppercase at --t-chip. */
  source?: string;
}
export declare function ShEvidence(props: ShEvidenceProps): JSX.Element;
