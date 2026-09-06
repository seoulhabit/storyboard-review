Scene frame — wraps every scene so the cream ground, the token scope for the canvas, the safe area and the source chip are never re-authored.

```jsx
<ShScene aspect="9x16" width={360} chip="J. Cosmet. Dermatol. 2019" align="left">
  <ShRows rows={rows} active={1} />
</ShScene>
```

`aspect="16x9"` switches type and space to the 1920 canvas and moves the safe area to x 6–94% / y 8–92%. `width` scales the whole 1080- or 1920-wide stage down for previews and cards. `align="left"` for rows, steps, compare and quote; the default centre for hook, ingredient, evidence and endcard.
