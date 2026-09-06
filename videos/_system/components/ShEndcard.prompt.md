The closing card. 2.4s, and it carries the video's one shader at `boundary − 0.25`.

```jsx
<ShEndcard cta="More at seoulhabit.com" />
```

서울의 습관, the SEOULHABIT wordmark, one CTA line. Nothing else, ever.

**Deviation from source, ruled this WO (C-6):** the "one shader at boundary
minus 0.25" clause above is the design system's own stated behaviour, and
this compiler does not implement it — WO-FVC-005's T1 spike could not prove
local/cloud shader-boundary parity without spending HeyGen credits, so the
WO's own pre-written fail branch fired: hard cuts only, no shader chain,
anywhere. The end card here is a hard cut in and a 0.25s fade out, same as
every other scene's sanctioned exit. If C-6 is ever reversed, this is the
one component whose behaviour changes back.
