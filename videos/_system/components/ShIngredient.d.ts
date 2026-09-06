/**
 * sh-ingredient — the subject card: name, INCI name, one line of function.
 */
export interface ShIngredientProps {
  /** Ingredient name, Title Case, DejaVu Serif at --t-display. */
  name: string;
  /** INCI name, uppercase, muted. */
  inci?: string;
  /** One line of what it does. */
  function?: string;
  /** Clay on the name — use only when this scene spends its accent here. */
  accent?: boolean;
}
export declare function ShIngredient(props: ShIngredientProps): JSX.Element;
