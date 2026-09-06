/**
 * sh-hook — one uppercase line, clay on the single load-bearing word.
 */
export interface ShHookProps {
  /** 3-8 words. Cut words rather than drop a type step. */
  line: string;
  /** The one word rendered in clay. This is the scene's whole accent budget. */
  accentWord?: string;
}
export declare function ShHook(props: ShHookProps): JSX.Element;
