import json

with open("scripts/gen/captions_groups.json") as f:
    data = json.load(f)

GROUPS = data["groups"]
DURATION = data["duration"]
groups_json = json.dumps(GROUPS)

html = f'''<!DOCTYPE html>
<html>
  <head><meta charset="UTF-8"></head>
  <body>
    <template>
      <style>
        @font-face {{ font-family: "Inter"; font-weight: 800; font-style: normal;
          src: url("assets/fonts/inter-800.woff2") format("woff2"); font-display: block; }}
        @font-face {{ font-family: "JetBrains Mono"; font-weight: 100 900; font-style: normal;
          src: url("assets/fonts/jetbrains-mono-500.woff2") format("woff2"); font-display: block; }}

        /*
          Burned-in karaoke captions -- mechanism REUSED VERBATIM from
          videos/snail-mucin-truth/.hyperframes/caption-skin.html (the channel's only
          real caption implementation; see frame.md § Channel audit), re-tokened from
          that project's unrelated "Editorial Forest" preset to THIS project's own
          tokens.css palette. Structure, .is-active/.is-spoken state machine, and the
          gsap.set-not-tl.call discipline are unchanged -- only colors/fonts/position
          differ.

          Accent choice: the "current word" panel uses --highlighter (amber), not
          --aqua -- aqua is already this video's one-per-frame highlight (the habit
          stack's active row); using it again on every spoken word would put two aqua
          accents in the same frame, violating that law. The habit-word underline
          (CLEANSE/HYDRATE/TREAT/SEAL/PROTECT) uses --leaf, the system's
          "evidence/confirm" accent -- reinforcement of the stack's highlight, not a
          duplicate mechanism.
        */
        #root {{
          --paper: #F7F5F0; --ink: #131516; --highlighter: #E0A32B; --leaf: #6F8F72;
          --font-body: "Inter", "Noto Sans KR Video", system-ui, sans-serif;
          position: absolute; inset: 0; pointer-events: none;
        }}
        .caption-stage {{ position: absolute; left: 0; right: 0; top: 1360px; height: 150px;
          display: flex; align-items: center; justify-content: center; }}
        .caption-group {{ position: absolute; inset: 0; display: flex; align-items: center;
          justify-content: center; opacity: 0; }}
        .caption-pill {{ max-width: 88%; padding: 16px 32px; background: rgba(19,21,22,0.80);
          border-radius: 10px; }}
        .caption-line {{ display: flex; flex-wrap: wrap; justify-content: center;
          gap: 0.08em 0.3em; font-family: var(--font-body); font-weight: 700;
          font-size: 38px; line-height: 1.2; }}
        .caption-word {{ display: inline-block; padding: 0 0.05em; color: rgba(247,245,240,0.62); }}
        .caption-word.is-active {{ color: var(--ink); background: var(--highlighter);
          border-radius: 6px; }}
        .caption-word.is-spoken {{ color: var(--paper); background: transparent; }}
        .caption-word.cap-habit {{ text-decoration: underline; text-decoration-thickness: 2px;
          text-decoration-color: var(--leaf); text-underline-offset: 0.14em; }}
      </style>

      <div id="root" data-composition-id="captions" data-start="0" data-duration="{DURATION}" data-width="1080" data-height="1920">
        <div class="caption-stage" id="caption-stage"></div>
      </div>

      <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
      <script>
        var GROUPS = {groups_json};
        var DURATION = {DURATION};

        (function () {{
          var stage = document.getElementById("caption-stage");
          GROUPS.forEach(function (group, g) {{
            var groupEl = document.createElement("div");
            groupEl.className = "caption-group";
            groupEl.id = "caption-group-" + g;
            var pill = document.createElement("div");
            pill.className = "caption-pill";
            var line = document.createElement("div");
            line.className = "caption-line";
            (group.words || []).forEach(function (w, i) {{
              var span = document.createElement("span");
              span.className = "caption-word" + (w.habit ? " cap-habit" : "");
              span.id = "caption-word-" + g + "-" + i;
              span.textContent = String(w.text);
              line.appendChild(span);
            }});
            pill.appendChild(line);
            groupEl.appendChild(pill);
            stage.appendChild(groupEl);
          }});

          window.__timelines = window.__timelines || {{}};
          var tl = gsap.timeline({{ paused: true }});

          GROUPS.forEach(function (group, g) {{
            var groupEl = document.getElementById("caption-group-" + g);
            var words = group.words || [];
            var next = GROUPS[g + 1];
            var isLast = g === GROUPS.length - 1;
            var start = Math.max(0, Number(group.start));
            var end = isLast ? Math.min(DURATION, Number(group.end) + 0.3) : Math.min(Number(next.start), Number(group.end) + 0.3);
            if (end <= start) end = start + 0.01;

            tl.set(groupEl, {{ opacity: 1 }}, start);
            tl.set(groupEl, {{ opacity: 0 }}, end);

            words.forEach(function (w, i) {{
              var el = document.getElementById("caption-word-" + g + "-" + i);
              var at = Math.max(start, Number(w.start));
              var baseClass = "caption-word" + (w.habit ? " cap-habit" : "");
              tl.set(el, {{ className: baseClass }}, start);
              tl.set(el, {{ className: baseClass + " is-active" }}, at);
              tl.fromTo(el, {{ scale: 0.985 }}, {{ scale: 1, duration: 0.18, ease: "power1.out" }}, at);
              if (i + 1 < words.length) {{
                var nextAt = Math.max(start, Number(words[i + 1].start));
                tl.set(el, {{ className: baseClass + " is-spoken" }}, nextAt);
              }}
            }});
            if (words.length) {{
              var lastEl = document.getElementById("caption-word-" + g + "-" + (words.length - 1));
              var lastBaseClass = "caption-word" + (words[words.length - 1].habit ? " cap-habit" : "");
              var lastSpoken = Math.min(end, Number(words[words.length - 1].end) + 0.1);
              tl.set(lastEl, {{ className: lastBaseClass + " is-spoken" }}, lastSpoken);
            }}
          }});

          tl.to({{}}, {{ duration: DURATION }}, 0);
          window.__timelines["captions"] = tl;
        }})();
      </script>
    </template>
  </body>
</html>
'''

with open("compositions/captions.html", "w") as f:
    f.write(html)

print("wrote compositions/captions.html", len(html), "bytes")
