/**
 * sh-steps — ordered sequence for application and routine order, 3-4 steps.
 */
export interface ShStep { n?: number | string; action: string; note?: string }
export interface ShStepsProps {
  /** Three or four steps. Clay numerals, brass connector. */
  steps: ShStep[];
}
export declare function ShSteps(props: ShStepsProps): JSX.Element;
