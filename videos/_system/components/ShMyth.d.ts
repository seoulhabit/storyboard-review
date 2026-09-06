/**
 * sh-myth — correction without red and green: struck claim, then the correction.
 */
export interface ShMythProps {
  /** The claim, muted, struck through by a 2px ink rule over 0.4s. */
  claim: string;
  /** The correction, uppercase label step. */
  correction: string;
  /** One clay word inside the correction. */
  accentWord?: string;
  /** false renders the strike at zero width for the timeline to draw. Default true. */
  struck?: boolean;
}
export declare function ShMyth(props: ShMythProps): JSX.Element;
