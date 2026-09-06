/**
 * sh-rows — the mapped list. Three to five rows; clay marks the active row only.
 */
export interface ShRow { left: string; right: string }
export interface ShRowsProps {
  /** 3-5 rows. Past five it is two scenes, or the wrong list. */
  rows: ShRow[];
  /** Index of the clay row. -1 (default) renders every row at full opacity. */
  active?: number;
  /** How many rows are on screen — drives the 0.8s stagger. Default: all. */
  revealed?: number;
}
export declare function ShRows(props: ShRowsProps): JSX.Element;
