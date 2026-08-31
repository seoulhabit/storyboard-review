import os

OUT = "compositions/frames"

FONTS = """
        @font-face { font-family: "EB Garamond"; font-weight: 400; font-style: normal;
          src: url("assets/fonts/eb-garamond-400.woff2") format("woff2"); font-display: block; }
        @font-face { font-family: "Inter"; font-weight: 800; font-style: normal;
          src: url("assets/fonts/inter-800.woff2") format("woff2"); font-display: block; }
        @font-face { font-family: "JetBrains Mono"; font-weight: 100 900; font-style: normal;
          src: url("assets/fonts/jetbrains-mono-500.woff2") format("woff2"); font-display: block; }
        @font-face { font-family: "Noto Sans KR Video"; font-weight: 500; font-style: normal;
          src: url("assets/fonts/NotoSansKR-500-subset.woff2") format("woff2"); font-display: block; }
"""

def tokens(ground):
    bg = "var(--paper)" if ground == "paper" else "var(--ink)"
    return f"""
        #root {{
          --paper: #F7F5F0; --ink: #131516; --aqua: #59B8AE; --leaf: #6F8F72; --coral: #C97A5C;
          --highlighter: #E0A32B; --ink-2: #6B6B6B; --ink-3: #9C978D; --ink-2-dark: #878B8C; --ink-3-dark: #7C8082;
          --white: #FCFBF9;
          --font-display: "EB Garamond", Georgia, "Times New Roman", serif;
          --font-body: "Inter", "Noto Sans KR Video", "Noto Sans KR", system-ui, -apple-system, Helvetica, Arial, sans-serif;
          --font-mono: "JetBrains Mono", ui-monospace, "SF Mono", Consolas, monospace;
          --font-kr: "Noto Sans KR Video", sans-serif;
          --t-hero: 96px; --t-figure: 60px; --t-frame: 50px; --t-body: 32px; --t-label: 24px; --t-chip: 22px; --t-floor: 20px;
          --safe-top: 120px; --safe-bottom: 360px; --safe-left: 60px; --safe-right: 162px;
          --e-out: cubic-bezier(0.215,0.61,0.355,1); --e-in: cubic-bezier(0.55,0.055,0.675,0.19); --e-inout: cubic-bezier(0.455,0.03,0.515,0.955);
          --d-snap: 180ms; --d-fast: 400ms; --d-base: 500ms;
          --elev-2: 0 18px 32px -20px rgba(19,21,22,0.35);
          --capsule-dark: rgba(19,21,22,0.80); --capsule-pad-y: 12px; --capsule-pad-x: 20px; --capsule-radius: 6px;

          position: relative; width: 1080px; height: 1920px; overflow: hidden;
          background: {bg}; font-family: var(--font-mono);
        }}
        .clip {{ position: absolute; inset: 0; }}

        /* full-bleed macro plate -- the presenter for this video (frame.md § Faceless) */
        .hero-media {{ position: absolute; inset: 0; background: var(--paper); overflow: hidden; }}
        .hero-media img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
        .hero-scrim {{ position: absolute; inset: 0; pointer-events: none; }}
"""

HABIT_STACK_CSS = """
        /* Persistent 5-habit tracker, center-left safe column, per the user's own brief
           ("bold, aesthetic font in the center-left"). Progress read via weight/contrast,
           not color proliferation -- only the ACTIVE row uses aqua, matching the system's
           "one aqua-family highlight per frame" law and "no success colour" rule (a done
           row is marked by a checkmark + full-opacity text, never green). Compact sizing so
           the stack, every frame's own accent content, and the caption band (top:1360,
           frame.md § Captions) all fit inside the safe-top/safe-bottom bounds together --
           the original larger sizing collided with the caption band on Frame 6, the
           densest layout. */
        .habit-stack { top: 170px; left: var(--safe-left); width: 560px; bottom: auto;
          display: flex; flex-direction: column; gap: 10px; }
        .habit-row { display: flex; align-items: center; gap: 12px;
          background: var(--capsule-dark); padding: 8px 16px;
          border-radius: var(--capsule-radius); transform-origin: 0% 50%; }
        .habit-badge { width: 30px; height: 30px; border-radius: 50%; flex: none;
          display: flex; align-items: center; justify-content: center;
          font-family: var(--font-mono); font-size: 18px; font-weight: 500; }
        .habit-word { font-family: var(--font-body); font-weight: 800; letter-spacing: 0.01em;
          font-size: 26px; }
        /* pending: dimmed via a paper-tinted (not ink-3) glyph colour -- ink-3 is a
           secondary-text token designed for LIGHT backgrounds; using it directly on this
           dark capsule measured 2.6:1 against WCAG's 4.5:1 floor. A translucent paper
           tone reads exactly as "de-emphasized" while actually passing on a dark ground. */
        .habit-row[data-state="pending"] .habit-badge { border: 2px solid rgba(247,245,240,0.55); color: rgba(247,245,240,0.72); }
        .habit-row[data-state="pending"] .habit-word { color: rgba(247,245,240,0.72); }
        .habit-row[data-state="done"] .habit-badge { background: var(--white); color: var(--ink); }
        .habit-row[data-state="done"] .habit-word { color: var(--white); }
        /* active: a slightly denser capsule behind the aqua text -- aqua-on-capsule-dark
           measured 4.25:1 against a 4.5:1 floor; darkening the backdrop (not the token
           colour itself, which is the system's own official --aqua value used channel-wide)
           closes the gap without inventing a new accent. */
        .habit-row[data-state="active"] { background: rgba(19,21,22,0.92); }
        .habit-row[data-state="active"] .habit-badge { border: 2px solid var(--aqua); color: var(--aqua); }
        .habit-row[data-state="active"] .habit-word { color: var(--aqua); }
        /* both glyphs always in the DOM; CSS (driven by the same data-state attribute the
           JS already sets via tl.set({attr:...})) decides which one paints -- no JS text
           update needed, so a mid-file state transition can never leave a stale digit. */
        .badge-check { display: none; }
        .habit-row[data-state="done"] .badge-num { display: none; }
        .habit-row[data-state="done"] .badge-check { display: inline; }
"""

HABITS = ["CLEANSE", "HYDRATE", "TREAT", "SEAL", "PROTECT"]

def habit_stack_html(states, ids_prefix):
    # states: list of 5 states ('done'|'active'|'pending') matching HABITS order
    rows = []
    for i, (word, state) in enumerate(zip(HABITS, states), start=1):
        rows.append(
            f'          <div class="habit-row" data-state="{state}" id="{ids_prefix}-row-{i}">'
            f'<span class="habit-badge"><span class="badge-num" data-layout-allow-overlap>{i}</span>'
            f'<span class="badge-check" data-layout-allow-overlap>&#10003;</span></span>'
            f'<span class="habit-word" data-layout-allow-overlap>{word}</span></div>'
        )
    return (
        f'        <div class="clip habit-stack" id="{ids_prefix}-stack" data-layout-allow-overlap>\n'
        + "\n".join(rows) + "\n        </div>"
    )

def wrap(comp_id, duration, ground, extra_css, body_html, js):
    return f"""<!DOCTYPE html>
<html>
  <head><meta charset="UTF-8"></head>
  <body>
    <template>
      <style>
{FONTS}
{tokens(ground)}
{extra_css}
      </style>

      <div id="root" data-composition-id="{comp_id}" data-width="1080" data-height="1920" data-duration="{duration}">
{body_html}
      </div>

      <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
      <script>
        window.__timelines = window.__timelines || {{}};
        const tl = gsap.timeline({{ paused: true }});
{js}
        tl.to({{}}, {{ duration: {duration} }}, 0);
        window.__timelines["{comp_id}"] = tl;
      </script>
    </template>
  </body>
</html>
"""

os.makedirs(OUT, exist_ok=True)
print("helpers loaded")

SCRIM = {"paper": "rgba(247,245,240,0.14)", "ink": "rgba(19,21,22,0.44)"}

def scrim_css(ground):
    return f".hero-scrim {{ background: {SCRIM[ground]}; }}"

# ---------------------------------------------------------------- FRAME 1 --
f1_css = scrim_css("paper") + """
        /* No caption-band collision: kicker (220) and payoff (1200) both clear the
           band at 960-1110 -- confirmed after the band moved up 400px (QC #1). */
        .ghost-kicker { top: 220px; left: 0; width: 100%; text-align: center; bottom: auto; }
        .ghost-kicker span { display: inline-block; background: rgba(252,251,249,0.85);
          color: var(--ink); font-family: var(--font-mono); font-size: 42px; font-weight: 500;
          letter-spacing: 0.12em; padding: 16px 32px; border-radius: var(--r-2, 6px); position: relative; }
        .strike-bar { position: absolute; left: 0; top: 50%; width: 100%; height: 8px;
          background: var(--coral); transform: scaleX(0); transform-origin: 0% 50%; }
        .f1-payoff { top: 1200px; left: 0; width: 100%; text-align: center; bottom: auto;
          font-family: var(--font-mono); font-size: var(--t-label); letter-spacing: 0.08em;
          color: var(--ink); }
"""
f1_body = """
        <div class="clip hero-media" id="f1-hero-a"><img src="assets/images/hook-clutter.png" alt="" width="781" height="1400" loading="eager" decoding="sync"></div>
        <div class="clip hero-media" id="f1-hero-b"><img src="assets/images/hook-swept.png" alt="" width="781" height="1400" loading="eager" decoding="sync"></div>
        <div class="clip hero-scrim"></div>
        <div class="clip ghost-kicker" id="f1-kicker"><span id="f1-kicker-text">10-STEP ROUTINE<div class="strike-bar" id="f1-strike"></div></span></div>
        <div class="clip f1-payoff" id="f1-payoff">FEWER STEPS. STRONGER BARRIER.</div>
"""
f1_js = """
        // frame zero is composed: hero-a is opaque and settled from t=0, hero-b's baseline
        // is registered here (not a bare gsap.set outside the timeline -- see the core
        // skill's own documented bleed bug) so an arbitrary seek before 4.6 never shows it.
        gsap.set("#f1-hero-b", { opacity: 0 });
        gsap.set("#f1-payoff", { opacity: 0, y: 10 });
        tl.set("#f1-strike", { scaleX: 0 }, 0);
        tl.fromTo("#f1-hero-a img", { scale: 1.06 }, { scale: 1.0, duration: 6.485, ease: "none" }, 0);
        tl.fromTo("#f1-kicker", { opacity: 0, y: -8 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, 0.3);

        // the coral strikethrough -- the single voltage moment for the whole video
        // (frame.md), timed to the corrected VO line's "wrecked" landing / buzzer SFX.
        tl.to("#f1-strike", { scaleX: 1, duration: 0.15, ease: "power2.out" }, 4.5);

        // hard cut to the swept-clear counter -- same white ground, so this is a safe
        // same-ground micro-transition, not the crossfade-across-a-ground-change bug.
        tl.to("#f1-hero-b", { opacity: 1, duration: 0.08, ease: "power2.out" }, 4.6);
        tl.fromTo("#f1-hero-b img", { scale: 1.05 }, { scale: 1.0, duration: 1.885, ease: "none" }, 4.6);
        tl.to("#f1-kicker", { opacity: 0, duration: 0.2, ease: "power2.in" }, 4.6);
        tl.to("#f1-payoff", { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, 5.0);
"""

# ---------------------------------------------------------------- FRAME 2 --
f2_css = scrim_css("ink") + """
        /* QC #1: the numeral badge (was top:660, spanning 660-1120) collided with the
           caption band's new position (960-1110). Moved up to clear it; the kicker line
           at 1180 was already clear below the band and is unchanged. */
        .f2-numeral-wrap { top: 400px; left: var(--safe-left); width: 460px; height: 460px;
          background: rgba(19,21,22,0.88); border-radius: 24px;
          display: flex; align-items: center; justify-content: center; }
        .f2-numeral { position: static;
          font-family: var(--font-display); font-size: 320px; font-weight: 600;
          color: var(--aqua); line-height: 1; }
        .f2-kicker { top: 1180px; left: var(--safe-left); width: 858px; bottom: auto;
          font-family: var(--font-mono); font-size: 34px; letter-spacing: 0.06em;
          color: var(--paper); line-height: 1.4; }
"""
f2_body = """
        <div class="clip hero-media" id="f2-hero"><img src="assets/images/promise-hand-dispense.png" alt="" width="781" height="1400" loading="eager" decoding="sync"></div>
        <div class="clip hero-scrim"></div>
        <div class="clip f2-numeral-wrap"><div class="f2-numeral" id="f2-numeral">5</div></div>
        <div class="clip f2-kicker" id="f2-kicker">5 SIMPLE HABITS.<br>NO HOARDING NEEDED.</div>
"""
f2_js = """
        // frame zero is composed: the numeral (and its solid backing capsule) is fully
        // visible from this file's own t=0 -- an earlier version faded it in over 0.2s,
        // which left a blank dark box on-screen for that entire span, caught only by
        // extracting the exact hard-cut frame with ffmpeg (a still compressed to a
        // thumbnail hid it; the full-resolution extract did not). Only the kicker line
        // and the bounded pulse are still authored motion.
        gsap.set("#f2-kicker", { opacity: 0, y: 10 });
        tl.fromTo("#f2-hero img", { scale: 1.08 }, { scale: 1.0, duration: 5.391, ease: "none" }, 0);
        tl.to("#f2-kicker", { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, 0.6);
        // bounded idle pulse -- resolves inside this beat, never infinite (frame.md § Motion)
        tl.to("#f2-numeral", { scale: 1.05, duration: 0.4, ease: "power1.inOut", yoyo: true, repeat: 3 }, 2.0);
"""

# ---------------------------------------------------------------- FRAME 3 --
f3_css = scrim_css("paper") + HABIT_STACK_CSS
f3_stack = habit_stack_html(["active", "pending", "pending", "pending", "pending"], "f3")
f3_body = f"""
        <div class="clip hero-media" id="f3-hero-a"><img src="assets/images/cleanse-balm-melt.png" alt="" width="781" height="1400" loading="eager" decoding="sync"></div>
        <div class="clip hero-media" id="f3-hero-b"><img src="assets/images/hydrate-pour.png" alt="" width="781" height="1400" loading="eager" decoding="sync"></div>
        <div class="clip hero-scrim"></div>
{f3_stack}
"""
f3_js = """
        // habit stack makes its first appearance -- CLEANSE active, everything else pending,
        // already composed at t=0 (not animated in from nothing) since this is a hard-cut
        // boundary and the stack must read correctly the instant the cut lands.
        gsap.set("#f3-hero-b", { opacity: 0 });
        gsap.set("#f3-stack", { opacity: 0, x: -16 });
        tl.fromTo("#f3-hero-a img", { scale: 1.05 }, { scale: 1.0, duration: 3.7, ease: "none" }, 0);
        tl.to("#f3-stack", { opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }, 0.15);

        // Beat B -- "Two: Hydrate" -- hard cut to the toner-pour plate, CLEANSE settles to
        // done, HYDRATE becomes the frame's one aqua accent. attr-based state change via
        // tl.set (never tl.call -- seek does not fire it, per the channel's own caption-skin
        // mechanism note), landing beat pop on both affected rows.
        tl.to("#f3-hero-b", { opacity: 1, duration: 0.08, ease: "power2.out" }, 3.7);
        tl.fromTo("#f3-hero-b img", { scale: 1.05 }, { scale: 1.0, duration: 4.1, ease: "none" }, 3.7);
        tl.set("#f3-row-1", { attr: { "data-state": "done" } }, 3.7);
        tl.set("#f3-row-2", { attr: { "data-state": "active" } }, 3.7);
        tl.to(["#f3-row-1", "#f3-row-2"], { scale: 1.04, duration: 0.16, ease: "power2.out", yoyo: true, repeat: 1 }, 3.7);
"""

# ---------------------------------------------------------------- FRAME 4 --
f4_css = scrim_css("ink") + HABIT_STACK_CSS + """
        /* QC #4 root cause (found, not just patched): .clip sets inset:0, and this rule
           only overrode top/left -- left without an explicit width means the inherited
           right:0 stretched the box to ~1020px wide (a giant slab, not a capsule), with
           the background painting the bottom half of the hero plate and text pinned to
           its top-left corner. bottom/right:auto + width:max-content restores a real
           shrink-to-fit capsule. Also applying the report's own asks on the now-correct
           box: white text (was --paper, measured low-contrast against this dark capsule)
           and 40px (was 22px, under the mobile reading floor) -- moved up from 900 to
           780 to clear the caption band's new position (960-1110, QC #1). */
        .treat-chip { top: 780px; left: var(--safe-left); bottom: auto; right: auto; width: max-content;
          font-family: var(--font-mono); font-size: 40px; font-weight: 600; letter-spacing: 0.08em;
          color: var(--white); background: rgba(19,21,22,0.85); padding: 10px 20px; border-radius: var(--r-2, 6px); }
"""
f4_stack = habit_stack_html(["done", "done", "active", "pending", "pending"], "f4")
f4_body = f"""
        <div class="clip hero-media" id="f4-hero-a"><img src="assets/images/treat-droplet.png" alt="" width="781" height="1400" loading="eager" decoding="sync"></div>
        <div class="clip hero-media" id="f4-hero-b"><img src="assets/images/seal-cream-swirl.png" alt="" width="781" height="1400" loading="eager" decoding="sync"></div>
        <div class="clip hero-scrim"></div>
{f4_stack}
        <div class="clip treat-chip" id="f4-chip">JUST ONE ACTIVE</div>
"""
f4_js = """
        // CLEANSE + HYDRATE already done at this file's own t=0 -- composed directly, not
        // re-animated (those transitions already happened in Frame 3's own timeline).
        gsap.set("#f4-hero-b", { opacity: 0 });
        gsap.set("#f4-chip", { opacity: 0, y: 10 });
        tl.fromTo("#f4-hero-a img", { scale: 1.05 }, { scale: 1.0, duration: 4.3, ease: "none" }, 0);
        // mid-beat content chip -- Beat A (0-4.3s) measured a 3.5s flat stretch on the
        // static-hold check (faceless-video-craft's cadence ceiling for shorts is 2-3s);
        // this isn't decorative filler, it reinforces the VO's actual point ("Pick just
        // one active serum") at the moment that clause lands.
        tl.to("#f4-chip", { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 2.0);
        tl.to("#f4-chip", { opacity: 0, duration: 0.2, ease: "power2.in" }, 4.1);

        // Beat B -- "Four: Seal" -- hard cut to the cream-swirl plate, TREAT settles to
        // done, SEAL becomes the frame's one aqua accent.
        tl.to("#f4-hero-b", { opacity: 1, duration: 0.08, ease: "power2.out" }, 4.3);
        tl.fromTo("#f4-hero-b img", { scale: 1.05 }, { scale: 1.0, duration: 5.0, ease: "none" }, 4.3);
        tl.set("#f4-row-3", { attr: { "data-state": "done" } }, 4.3);
        tl.set("#f4-row-4", { attr: { "data-state": "active" } }, 4.3);
        tl.to(["#f4-row-3", "#f4-row-4"], { scale: 1.04, duration: 0.16, ease: "power2.out", yoyo: true, repeat: 1 }, 4.3);
"""

# ---------------------------------------------------------------- FRAME 5 --
f5_css = scrim_css("paper") + HABIT_STACK_CSS + """
        /* QC #5 root cause (same bug as Frame 4's treat-chip, see its own comment):
           missing explicit width let the inherited right:0 stretch this to a ~1020px
           slab instead of a capsule -- what the reviewer saw as "too small to read" was
           actually 22px text pinned to the corner of an oversized invisible box. Fixed
           box + 40px (not the report's literal 150%, which lands at 33px and still fails
           the mobile reading floor) -- kept at 40px to match Frame 4's chip as one
           component. Moved up from 900 to 780 to clear the caption band (QC #1). */
        .spf-chip { top: 780px; left: var(--safe-left); bottom: auto; right: auto; width: max-content;
          font-family: var(--font-mono); font-size: 40px; letter-spacing: 0.08em; color: var(--ink);
          background: rgba(252,251,249,0.85); padding: 10px 20px; border-radius: var(--r-2, 6px); }
"""
f5_stack = habit_stack_html(["done", "done", "done", "done", "active"], "f5")
f5_body = f"""
        <div class="clip hero-media" id="f5-hero"><img src="assets/images/protect-fingers.png" alt="" width="781" height="1400" loading="eager" decoding="sync"></div>
        <div class="clip hero-scrim"></div>
        <div class="clip spf-chip" id="f5-chip">TWO FINGERS · SPF 50</div>
{f5_stack}
"""
f5_js = """
        // all five rows visible at once for the first time -- the scene's deliberately
        // denser beat (STORYBOARD.md), all four prior habits already settled to done.
        gsap.set("#f5-chip", { opacity: 0, y: 10 });
        tl.fromTo("#f5-hero img", { scale: 1.05 }, { scale: 1.0, duration: 5.05, ease: "none" }, 0);
        tl.to("#f5-chip", { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, 0.4);
"""

# ---------------------------------------------------------------- FRAME 6 --
f6_css = scrim_css("paper") + HABIT_STACK_CSS.replace("top: 170px;", "top: 1160px;") + """
        /* the one structurally different layout: a full-width horizontal product band
           instead of a full-bleed vertical macro plate (faceless-video-craft's
           layout-variety rule). QC #1 moved the caption band from 1360 to 960-1110,
           which landed squarely on this frame's old sub-kicker (940) and habit stack
           (1030-1300) -- the densest layout in the video, and the one QC flagged as a
           "major" collision. Reflowed to split around the new band instead of colliding
           with it: product band, headline, sub-kicker all above it; habit stack and
           brand mark below it. Every block that only sets top (not height) also gets
           bottom:auto -- see Frame 4/5's chip comments for why that inherited inset:0
           bottom/right matters for elements that DO carry a background; these are plain
           centered text with no background, so it's hygiene, not a visible fix. */
        .product-band { top: 150px; left: 0; width: 100%; height: 500px;
          background: var(--paper); display: flex; align-items: center; justify-content: center;
          overflow: hidden; }
        .product-band img { width: 100%; height: 100%; object-fit: contain; display: block; }
        .f6-headline { top: 700px; left: 0; width: 100%; text-align: center; bottom: auto;
          font-family: var(--font-display); font-size: 56px; color: var(--ink); }
        .f6-sub { top: 790px; left: 0; width: 100%; text-align: center; bottom: auto;
          font-family: var(--font-mono); font-size: var(--t-label); letter-spacing: 0.06em;
          color: var(--ink-2); }
        .f6-sub .f6-subscribe-word { color: var(--ink); font-weight: 600; display: inline-block; }
        /* QC #3's fix: the frame's only new on-screen content, not decorative filler --
           it's the burned-in form of the VO's own promise ("because tomorrow we're
           fixing your damaged skin barrier"), timed to land on that clause. It's the
           frame's one aqua accent (every habit row is already done/white by now),
           matching the one-aqua-per-frame law. Same safe pattern as .ghost-kicker
           (full-width wrapper, text-align:center, inline-block pill child) rather than
           a background directly on a .clip-derived block, sidestepping the inset:0 box
           bug entirely instead of needing an explicit-width patch. */
        .f6-next-chip { top: 860px; left: 0; width: 100%; text-align: center; bottom: auto; }
        .f6-next-chip span { display: inline-block; background: rgba(19,21,22,0.85);
          color: var(--aqua); font-family: var(--font-mono); font-size: 28px; font-weight: 600;
          letter-spacing: 0.08em; padding: 14px 28px; border-radius: var(--r-2, 6px); }
        .f6-brand { top: 1480px; left: 0; width: 100%; text-align: center; bottom: auto;
          font-family: var(--font-kr); font-size: 22px; color: var(--ink-2); }
"""
f6_stack = habit_stack_html(["done", "done", "done", "done", "done"], "f6")
f6_body = f"""
        <div class="clip product-band" id="f6-band"><img src="assets/images/cta-five-products.png" alt="" width="1400" height="1024" loading="eager" decoding="sync"></div>
        <div class="clip f6-headline" id="f6-headline">That's it.</div>
        <div class="clip f6-sub" id="f6-sub">5 HABITS. <span class="f6-subscribe-word" id="f6-subscribe-word">HIT SUBSCRIBE.</span></div>
        <div class="clip f6-next-chip" id="f6-next-chip"><span>NEXT: BARRIER REPAIR</span></div>
{f6_stack}
        <div class="clip f6-brand" id="f6-brand-mark">습 SeoulHabit</div>
"""
f6_js = """
        // QC #3: this frame measured 5.0s of frozen imagery (local ~2.06-7.5, PSNR ~70dB
        // between 0.5s samples) against the shorts 2-3s cadence ceiling -- every beat
        // below is new, each landing on a real clause of this scene's own VO (re-timed
        // 2026-08-30 after QC #2 required a fresh take of line 06 -- word times below
        // come from that take's real transcript, not the original).
        //
        // all five habits already settle to done -- the completed ladder, composed
        // directly (the last transition already happened in Frame 5's own timeline).
        gsap.set("#f6-headline", { opacity: 0, y: 10 });
        gsap.set("#f6-sub", { opacity: 0, y: 10 });
        gsap.set("#f6-next-chip", { opacity: 0, y: 10 });
        gsap.set("#f6-brand-mark", { opacity: 0 });

        // continuous Ken Burns across the WHOLE frame (every other scene has this; this
        // was the one that stopped cold at 1.2s, which is most of why the freeze read as
        // static even with the discrete beats below added) -- quick settle first for the
        // hero product shot, then a slow drift for the remainder.
        tl.fromTo("#f6-band img", { scale: 1.03 }, { scale: 1.0, duration: 1.2, ease: "power2.out" }, 0);
        tl.to("#f6-band img", { scale: 1.02, duration: 6.3, ease: "none" }, 1.2);

        tl.to("#f6-headline", { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, 0.2);
        tl.to("#f6-sub", { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, 0.9);

        // habit stack's landing pop on "Five habits." (2.00-3.00) -- the stack is already
        // visible/done from t=0 (frame-zero-composed, not faded in from nothing), this is
        // just the beat that makes the completed ladder register as an event, not wallpaper.
        tl.to("#f6-row-1, #f6-row-2, #f6-row-3, #f6-row-4, #f6-row-5",
          { scale: 1.04, duration: 0.16, ease: "power2.out", yoyo: true, repeat: 1, stagger: 0.09 }, 2.05);

        // finger-tap micro-interaction landing on the real "subscribe" word (3.25-3.68).
        tl.to("#f6-subscribe-word", { scale: 1.08, duration: 0.18, ease: "power2.out", yoyo: true, repeat: 1 }, 3.25);

        // brand mark arrives on "because" (3.68-3.98).
        tl.to("#f6-brand-mark", { opacity: 1, duration: 0.3, ease: "power2.out" }, 3.70);

        // bounded product-band drift on "tomorrow we're fixing your" (4.10-4.99) -- finite,
        // resolves inside its own beat (frame.md § Motion), not an infinite idle.
        tl.fromTo("#f6-band", { x: 0 }, { x: -8, duration: 0.45, ease: "power1.inOut", yoyo: true, repeat: 1 }, 4.10);

        // the next-video handoff chip -- the actual fix for the freeze, not decorative
        // filler: it's the VO's own promise ("...we're fixing your damaged skin barrier")
        // rendered as on-screen text, landing on "damaged" (4.99-5.31) and clearing before
        // the loop-hold settle.
        tl.to("#f6-next-chip", { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 5.00);
        tl.to("#f6-next-chip", { opacity: 0, duration: 0.25, ease: "power2.in" }, 6.30);

        // held, settled through the loop-hold tail -- last frame hands back to Frame 1's
        // cold-open paper ground, same product-photography grammar.
"""

FRAMES = [
    ("01-hook", "7.285", "paper", f1_css, f1_body, f1_js),
    ("02-promise", "6.191", "ink", f2_css, f2_body, f2_js),
    ("03-cleanse-hydrate", "7.800", "paper", f3_css, f3_body, f3_js),
    ("04-treat-seal", "9.400", "ink", f4_css, f4_body, f4_js),
    ("05-protect", "5.850", "paper", f5_css, f5_body, f5_js),
    ("06-cta-endcard", "7.500", "paper", f6_css, f6_body, f6_js),
]

for comp_id, dur, ground, css, body, js in FRAMES:
    content = wrap(comp_id, dur, ground, css, body, js)
    path = os.path.join(OUT, comp_id + ".html")
    with open(path, "w") as f:
        f.write(content)
    print("wrote", path, len(content), "bytes")
