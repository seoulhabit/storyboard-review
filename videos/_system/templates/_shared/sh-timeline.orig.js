/* SeoulHabit scene timeline builder.
   Every template's scenes carry data-scene / data-start / data-dur / data-anchor.
   This reads them and builds ONE paused GSAP timeline registered as
   window.__timelines["main"], per the determinism rules: no Date.now, no
   Math.random, no timers, no rAF, no repeat:-1, built synchronously.
   If GSAP is absent (Claude Design preview), it exits quietly and the scenes
   just sit there as a static contact sheet. */
(() => {
  const build = () => {
    const g = window.gsap;
    if (!g) return;
    const scenes = [...document.querySelectorAll('[data-scene]')].map((el) => ({
      el,
      start: parseFloat(el.dataset.start || '0'),
      dur: parseFloat(el.dataset.dur || '2'),
      anchor: el.dataset.anchor === 'true'
    })).sort((a, b) => a.start - b.start);
    if (!scenes.length) return;

    const tl = g.timeline({ paused: true });

    scenes.forEach((s, i) => {
      // anchors: opacity 0, no autoAlpha, first shown by an explicit set
      if (s.anchor) {
        g.set(s.el, { opacity: 0 });
        tl.set(s.el, { opacity: 1 }, s.start);
        if (i < scenes.length - 1) tl.set(s.el, { opacity: 0 }, s.start + s.dur);
      } else {
        g.set(s.el, { visibility: 'hidden', autoAlpha: 0 });
        tl.set(s.el, { autoAlpha: 1 }, s.start);
        tl.set(s.el, { autoAlpha: 0 }, s.start + s.dur);
      }

      // one entrance per element, 0.35s power3.out, offset 0.1-0.3s into the scene
      const kids = s.el.querySelectorAll('[data-enter]');
      if (kids.length) {
        tl.from(kids, {
          opacity: 0, y: 40, duration: 0.35, ease: 'power3.out',
          stagger: kids[0].dataset.enter === 'row' ? 0.8 : 0.12
        }, s.start + 0.15);
      }

      // continuous patterns: breathing hairlines, clay sweep
      const floats = s.el.querySelectorAll('[data-float]');
      if (floats.length) tl.to(floats, { y: -6, duration: s.dur / 2, yoyo: true, repeat: 1, ease: 'sine.inOut' }, s.start);
      const sweeps = s.el.querySelectorAll('[data-sweep]');
      if (sweeps.length) tl.fromTo(sweeps, { scaleX: 0 }, { scaleX: 1, transformOrigin: 'left center', duration: 0.6, ease: 'power2.out' }, s.start + 0.4);
      const counts = s.el.querySelectorAll('[data-sh-count]');
      counts.forEach((c) => {
        const target = parseFloat(c.dataset.to || c.textContent);
        const suffix = c.dataset.suffix || '';
        const o = { v: 0 };
        tl.to(o, {
          v: target, duration: Math.min(1.2, s.dur * 0.6), ease: 'power2.out',
          onUpdate: () => { c.textContent = o.v.toFixed(c.dataset.decimals ? +c.dataset.decimals : 0) + suffix; }
        }, s.start + 0.2);
      });
      const strikes = s.el.querySelectorAll('[data-sh-strike]');
      if (strikes.length) tl.fromTo(strikes, { scaleX: 0 }, { scaleX: 1, transformOrigin: 'left center', duration: 0.4, ease: 'power2.out' }, s.start + 0.5);
    });

    // fade only, final scene only
    const last = scenes[scenes.length - 1];
    tl.to(last.el, { opacity: 0, duration: 0.25 }, last.start + last.dur - 0.25);

    window.__timelines = window.__timelines || {};
    window.__timelines['main'] = tl;
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', build);
  else build();
})();
