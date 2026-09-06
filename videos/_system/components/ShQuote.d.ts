/**
 * sh-quote — one sentence pulled large under a brass hairline.
 */
export interface ShQuoteProps {
  /** The one line in the video worth slowing down for. */
  line: string;
  /** Optional attribution, uppercase and muted. */
  attribution?: string;
}
export declare function ShQuote(props: ShQuoteProps): JSX.Element;
