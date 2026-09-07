#!/usr/bin/env python3
"""retrofit_catalog.py — WO-FVC-007 T2.

Transforms one HyperFrames catalog *component* (per the Gate A ruling,
registry.json blocks are out of scope — components only) from
vendor/hyperframes/registry/components/<name>/ into a token-native,
brand-safe component under videos/_system/catalog/.

Five steps, run in order:
  1. strip_font_links   — remove fonts.googleapis.com/fonts.gstatic.com,
                           inject the design system's 5-face @font-face block
  2. recolour            — classify every colour literal by role and either
                           substitute a design token, alias the item's own
                           custom-property vocabulary to one, or leave it
                           (documented) as structural-neutral / foreign-surface
  3. pin_gsap            — replace any jsdelivr/cdnjs GSAP <script src> with
                           the vendored copy
  4. record_aspect        — components have no native canvas; recorded as
                           "n/a-embeds-in-host" plus the T0b working-set verdict
                           when known
  5. emit_manifest_entry — append to videos/_system/catalog/manifest.json

Usage:
    python3 retrofit_catalog.py <component-name> [item options...]
    python3 retrofit_catalog.py --test    # the 3-item test suite
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

SCRIPT_VERSION = "1.0.0"
REPO_ROOT = Path(__file__).resolve().parents[3]  # videos/_system/catalog/<file> -> repo root
CATALOG_SOURCE_ROOT = REPO_ROOT / "vendor" / "hyperframes"
SYSTEM_ROOT = REPO_ROOT / "videos" / "_system"
OUT_ROOT = SYSTEM_ROOT / "catalog"
MANIFEST_PATH = OUT_ROOT / "manifest.json"

# ---------------------------------------------------------------------------
# Design-system token palette (must match videos/_system/tokens/colors.css)
# ---------------------------------------------------------------------------

# role -> (css var name, hex/rgba string as authored in colors.css, for distance calc)
DESIGN_TOKENS = {
    "surface":        ("--bg",        "#F4EDE3"),
    "surface-raised": ("--bg-lift",   "#FAF3E7"),
    "ink":            ("--ink",       "#26215C"),
    "ink-muted":      ("--muted",     "#26215Cbf"),  # ink at ~0.75 alpha, distance uses base hue
    "accent":         ("--accent",    "#9C3A32"),
    "on-accent":      ("--on-accent", "#F4EDE3"),
    "hairline":       ("--rule",      "#C0A265"),
    "positive":       ("--positive",  "#2F5940"),
    "warning":        ("--warning",   "#7A5A0F"),
    "info":           ("--info",      "#2E5C6E"),
}

# Common local custom-property names catalog items use for a host to supply,
# mapped to the design system's own token. Only names in this table are
# auto-bridged; an unrecognised local var name halts (fail loudly, §T2 step 2).
TOKEN_BRIDGE_MAP = {
    "bg": "var(--bg)",
    "fg": "var(--ink)",
    "surface": "var(--bg-lift)",
    "border": "var(--rule)",
    "muted": "var(--muted)",
    "radius": "12px",  # no design-system radius token exists; a safe literal default
    "font-body": "var(--font-work)",
    "font-display": "var(--font-subject)",
    "font-mono": "var(--font-work)",
    "space-1": "var(--s1)",
    "space-2": "var(--s2)",
    "space-3": "var(--s3)",
}

# Local custom properties confirmed (by reading the source, not guessed) to be
# item-internal computation, not design-bridge candidates — set at runtime by
# the item's own script, unrelated to colour/type/space tokens. Each entry
# names the item it was verified against so a name collision in a future item
# doesn't silently inherit an unrelated exemption.
INTERNAL_VARS = {
    "logical-width": "device-frame-stage: device-geometry px dimension, JS-set via viewport.style.setProperty()",
    "logical-height": "device-frame-stage: device-geometry px dimension, JS-set via viewport.style.setProperty()",
    "screen-scale": "device-frame-stage: computed scale ratio (rect.width / logicalWidth), JS-set at runtime",
}

FONT_FACE_BLOCK = """@font-face{font-family:"DejaVu Serif";font-style:normal;font-weight:400;font-display:block;src:url("../fonts/dejavu-serif-400.woff2") format("woff2")}
@font-face{font-family:"DejaVu Serif";font-style:normal;font-weight:700;font-display:block;src:url("../fonts/dejavu-serif-700.woff2") format("woff2")}
@font-face{font-family:"Archivo";font-style:normal;font-weight:100 900;font-display:block;src:url("../fonts/archivo-variable.woff2") format("woff2-variations")}
@font-face{font-family:"DejaVu Serif";font-style:normal;font-weight:700;font-display:block;unicode-range:U+1100-11FF,U+3130-318F,U+A960-A97F,U+AC00-D7AF,U+D7B0-D7FF;src:url("../fonts/noto-serif-kr-700.woff2") format("woff2")}
@font-face{font-family:"DejaVu Serif";font-style:normal;font-weight:400;font-display:block;unicode-range:U+1100-11FF,U+3130-318F,U+A960-A97F,U+AC00-D7AF,U+D7B0-D7FF;src:url("../fonts/noto-serif-kr-400.woff2") format("woff2")}"""

VENDORED_GSAP = "../vendor/gsap-3.14.2.min.js"

# ---------------------------------------------------------------------------
# Colour parsing / classification
# ---------------------------------------------------------------------------

HEX_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")
RGB_RE = re.compile(r"rgba?\(\s*[\d.]+\s*,\s*[\d.]+\s*,\s*[\d.]+\s*(?:,\s*[\d.]+\s*)?\)")
VAR_FALLBACK_RE = re.compile(r"var\(\s*--([\w-]+)\s*,\s*([^()]*(?:\([^()]*\)[^()]*)*)\)")
VAR_BARE_RE = re.compile(r"var\(\s*--([\w-]+)\s*\)")
SHADOW_PROP_RE = re.compile(r"(box-shadow|text-shadow|filter)\s*:")


def hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) == 8:
        h = h[:6]  # drop alpha for hue comparison
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def rgb_str_to_rgb(s: str) -> tuple[tuple[int, int, int], float]:
    nums = re.findall(r"[\d.]+", s)
    r, g, b = (int(float(x)) for x in nums[:3])
    a = float(nums[3]) if len(nums) > 3 else 1.0
    return (r, g, b), a


def rgb_to_hsl(rgb: tuple[int, int, int]) -> tuple[float, float, float]:
    r, g, b = (c / 255 for c in rgb)
    mx, mn = max(r, g, b), min(r, g, b)
    l = (mx + mn) / 2
    if mx == mn:
        h = s = 0.0
    else:
        d = mx - mn
        s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
        if mx == r:
            h = (g - b) / d + (6 if g < b else 0)
        elif mx == g:
            h = (b - r) / d + 2
        else:
            h = (r - g) / d + 4
        h /= 6
    return h * 360, s, l


def hsl_distance(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    ha, sa, la = rgb_to_hsl(a)
    hb, sb, lb = rgb_to_hsl(b)
    dh = min(abs(ha - hb), 360 - abs(ha - hb)) / 180  # 0..1
    ds = abs(sa - sb)
    dl = abs(la - lb)
    return (dh * 2) ** 2 + ds**2 + dl**2  # hue weighted heaviest


def relative_luminance(rgb: tuple[int, int, int]) -> float:
    def chan(c: int) -> float:
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = rgb
    return 0.2126 * chan(r) + 0.7152 * chan(g) + 0.0722 * chan(b)


def contrast_ratio(rgb1: tuple[int, int, int], rgb2: tuple[int, int, int]) -> float:
    l1, l2 = relative_luminance(rgb1), relative_luminance(rgb2)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def is_structural_neutral(rgb: tuple[int, int, int], alpha: float) -> bool:
    """Near-black or near-white/low-saturation: a depth/shadow cue, not a brand hue."""
    _, s, l = rgb_to_hsl(rgb)
    return s < 0.15 or l < 0.08 or l > 0.94


MATERIAL_MARKER_RE = re.compile(
    r"/\*(?P<comment>(?:(?!\*/).)*?(?:not brand paint|material law|do not (?:swap|recolou?r))(?:(?!\*/).)*?)\*/",
    re.DOTALL | re.IGNORECASE,
)


def find_material_law_properties(html: str) -> set[str]:
    """Custom-property NAMES first declared inside a rule block whose own
    comment documents them as physical/material colour, not brand paint
    (device-frame-stage's own language — this generalises the pattern to any
    future item using the same convention). Every later declaration of the
    same property name anywhere else in the file (e.g. a colour-variant
    override rule) inherits the same protection, since the name — not the
    rule block — carries the documented intent."""
    protected: set[str] = set()
    for m in MATERIAL_MARKER_RE.finditer(html):
        # scan forward from the comment to the next closing brace at this
        # nesting level to find the property declarations it documents
        tail = html[m.end() : m.end() + 2000]
        brace_end = tail.find("}")
        scope = tail[:brace_end] if brace_end != -1 else tail
        protected |= set(re.findall(r"--([\w-]+)\s*:", scope))
    return protected


@dataclass
class ColorFinding:
    raw: str
    property: str
    line_no: int
    role: str | None = None  # None until classified
    reason: str = ""
    replacement: str | None = None


def classify_literal(raw: str, property_name: str) -> ColorFinding:
    if raw.startswith("#"):
        rgb = hex_to_rgb(raw)
        alpha = 1.0
        if len(raw.lstrip("#")) == 8:
            alpha = int(raw.lstrip("#")[6:8], 16) / 255
    else:
        rgb, alpha = rgb_str_to_rgb(raw)

    finding = ColorFinding(raw=raw, property=property_name, line_no=0)

    is_shadow_ctx = property_name in ("box-shadow", "text-shadow", "filter")
    if is_shadow_ctx and is_structural_neutral(rgb, alpha):
        finding.role = "structural-neutral"
        finding.reason = "low-saturation shadow/depth cue, not a brand hue — left as literal"
        finding.replacement = None
        return finding

    # `color:` sets TEXT, never a background — a pure-surface token as a text
    # colour reads as a design smell (text the same tone as the page behind
    # it) and almost always really means "text sitting on the accent fill".
    # Excluding surface/surface-raised here is a property-context tie-break,
    # not a guess: it only changes which of several *already-within-threshold*
    # tokens wins, never turns an otherwise-unclassifiable literal classified.
    excluded_roles = {"surface", "surface-raised"} if property_name == "color" else set()

    best_role, best_dist = None, float("inf")
    for role, (_, token_hex) in DESIGN_TOKENS.items():
        if role in excluded_roles:
            continue
        token_rgb = hex_to_rgb(token_hex[:7])
        d = hsl_distance(rgb, token_rgb)
        if d < best_dist:
            best_role, best_dist = role, d

    THRESHOLD = 0.35
    if best_dist <= THRESHOLD:
        finding.role = best_role
        var_name, _ = DESIGN_TOKENS[best_role]
        if alpha < 0.98:
            finding.replacement = f"color-mix(in srgb, var({var_name}) {round(alpha * 100)}%, transparent)"
        else:
            finding.replacement = f"var({var_name})"
        finding.reason = f"nearest token by HSL distance ({best_dist:.3f} <= {THRESHOLD})"
        return finding

    finding.role = "UNCLASSIFIABLE"
    finding.reason = f"no token within distance threshold (closest: {best_role} at {best_dist:.3f})"
    return finding


# ---------------------------------------------------------------------------
# Font / GSAP steps
# ---------------------------------------------------------------------------

FONT_LINK_RE = re.compile(
    r'<link[^>]*(?:fonts\.googleapis\.com|fonts\.gstatic\.com)[^>]*/?>\s*',
    re.IGNORECASE,
)
GSAP_SCRIPT_RE = re.compile(
    r'<script[^>]*src=["\'][^"\']*(?:jsdelivr\.net/npm/gsap|cdnjs\.cloudflare\.com/ajax/libs/gsap)[^"\']*["\'][^>]*></script>',
    re.IGNORECASE,
)


def strip_font_links(html: str) -> tuple[str, int]:
    new_html, n = FONT_LINK_RE.subn("", html)
    if "<style>" in new_html:
        new_html = new_html.replace("<style>", f"<style>\n{FONT_FACE_BLOCK}\n", 1)
    else:
        new_html = new_html.replace("</head>", f"<style>\n{FONT_FACE_BLOCK}\n</style>\n</head>", 1)
    return new_html, n


def pin_gsap(html: str) -> tuple[str, int]:
    new_html, n = GSAP_SCRIPT_RE.subn(f'<script src="{VENDORED_GSAP}"></script>', html)
    return new_html, n


# ---------------------------------------------------------------------------
# Token bridge (for items using their own local custom-property vocabulary,
# e.g. var(--fg), var(--surface), with no local definition — meant to be
# supplied by whatever host embeds them)
# ---------------------------------------------------------------------------


def find_undefined_local_vars(html: str) -> dict[str, list[str]]:
    """Every --name referenced via var(--name) or var(--name, fallback) that
    is never itself declared with `--name:` somewhere in the file."""
    declared = set(re.findall(r"--([\w-]+)\s*:", html))
    used_bare = set(VAR_BARE_RE.findall(html))
    used_fallback = set(m.group(1) for m in VAR_FALLBACK_RE.finditer(html))
    used = used_bare | used_fallback
    undefined = used - declared
    return {"declared": sorted(declared), "undefined": sorted(undefined)}


# Local var names that are themselves already real design-token names
# (colors.css defines --bg and --muted at top level, not only as an alias).
# Bridging one of these by writing `:root{--bg: var(--bg)}` in a stylesheet
# that loads *after* colors.css is a self-reference — CSS treats a custom
# property whose own definition depends on itself as invalid, and the
# property silently reverts to whatever it would otherwise inherit. Found by
# rendering focus-swap's own retrofit output and checking computed contrast:
# .fs-status (color: var(--muted)) resolved to opaque ink, not the intended
# 0.75-alpha muted tone, because the bridge had just broken --muted. These
# names need no bridge line at all — colors.css already supplies them
# correctly; writing one is actively harmful, not merely redundant.
_REAL_TOKEN_NAMES = {v[0].lstrip("-") for v in DESIGN_TOKENS.values()}


def build_bridge_block(undefined_vars: list[str]) -> tuple[str, list[str], list[str], list[str]]:
    lines = []
    unmapped = []
    skipped_internal = []
    skipped_self_supplied = []
    for name in undefined_vars:
        if name in _REAL_TOKEN_NAMES:
            skipped_self_supplied.append(name)
        elif name in TOKEN_BRIDGE_MAP:
            lines.append(f"  --{name}: {TOKEN_BRIDGE_MAP[name]};")
        elif name in INTERNAL_VARS:
            skipped_internal.append(name)
        else:
            unmapped.append(name)
    return "\n".join(lines), unmapped, skipped_internal, skipped_self_supplied


# ---------------------------------------------------------------------------
# Per-item retrofit
# ---------------------------------------------------------------------------


@dataclass
class RetrofitResult:
    name: str
    classification: str = ""  # recolourable | foreign-surface | reject
    color_map: list[dict] = field(default_factory=list)
    font_links_stripped: int = 0
    gsap_pins: int = 0
    bridged_vars: list[str] = field(default_factory=list)
    unmapped_vars: list[str] = field(default_factory=list)
    unclassifiable: list[dict] = field(default_factory=list)
    output_html_path: str = ""
    output_hash: str = ""
    notes: list[str] = field(default_factory=list)


def find_component_dir(name: str) -> Path:
    d = CATALOG_SOURCE_ROOT / "registry" / "components" / name
    if not d.exists():
        raise SystemExit(f"BLOCKER: no component '{name}' at {d}")
    return d


def retrofit_item(name: str) -> RetrofitResult:
    comp_dir = find_component_dir(name)
    item_json = json.loads((comp_dir / "registry-item.json").read_text())
    if item_json.get("type") != "hyperframes:component":
        raise SystemExit(
            f"BLOCKER: '{name}' is type {item_json.get('type')!r}, not hyperframes:component. "
            "Per the Gate A ruling (reduce registry to components), only components are in scope."
        )

    html_file = None
    for f in item_json.get("files", []):
        if f.get("type") == "hyperframes:snippet" and f["path"].endswith(".html"):
            html_file = comp_dir / f["path"]
            break
    if html_file is None:
        raise SystemExit(f"BLOCKER: no hyperframes:snippet HTML file listed for '{name}'")

    html = html_file.read_text()
    result = RetrofitResult(name=name)

    # Step 1: fonts
    html, n_fonts = strip_font_links(html)
    result.font_links_stripped = n_fonts

    # Step 3: GSAP (numbered to match the WO's own step order; done here so
    # colour classification below sees the final script tag, not that it matters)
    html, n_gsap = pin_gsap(html)
    result.gsap_pins = n_gsap

    # Step 2: recolour
    # 2a. bridge the item's own undefined local custom properties to design tokens
    var_info = find_undefined_local_vars(html)
    bridge_css, unmapped, skipped_internal, skipped_self_supplied = build_bridge_block(var_info["undefined"])
    result.bridged_vars = [v for v in var_info["undefined"] if v in TOKEN_BRIDGE_MAP and v not in _REAL_TOKEN_NAMES]
    result.unmapped_vars = unmapped
    if skipped_internal:
        result.notes.append(
            "item-internal vars, no design-token bridge needed (verified against source, "
            f"see INTERNAL_VARS): {', '.join('--' + v for v in skipped_internal)}"
        )
    if skipped_self_supplied:
        result.notes.append(
            "local var name(s) collide with a real design-token name already defined at :root "
            f"by colors.css — no bridge written (would self-reference): "
            f"{', '.join('--' + v for v in skipped_self_supplied)}"
        )

    if bridge_css:
        # inject right after the first opening <style> tag inside the file
        # (works whether the root is #root, .clip, or similar — scoped globally
        # since :root custom properties cascade to any descendant regardless
        # of the compiler's own selector-scoping of *rules*).
        bridge_block = f":root{{\n{bridge_css}\n}}\n"
        if "<style>" in html:
            html = html.replace("<style>", f"<style>\n{bridge_block}", 1)
        else:
            html = html.replace("</head>", f"<style>\n{bridge_block}</style>\n</head>", 1)
        result.notes.append(
            f"bridged {len(result.bridged_vars)} local custom propert{'y' if len(result.bridged_vars)==1 else 'ies'} "
            f"({', '.join('--' + v for v in result.bridged_vars)}) to design tokens via a :root block — "
            "the item's own CSS is untouched, it inherits real values through the properties it already reads."
        )

    # 2b. classify and substitute literal hex/rgb(a) colours
    material_law_props = find_material_law_properties(html)
    if material_law_props:
        result.notes.append(
            f"{len(material_law_props)} custom propert{'y' if len(material_law_props)==1 else 'ies'} "
            f"documented by the source item as physical/material colour, exempt from token "
            f"substitution wherever declared: {', '.join('--' + p for p in sorted(material_law_props))}"
        )

    style_blocks = re.findall(r"<style[^>]*>(.*?)</style>", html, re.DOTALL)
    all_findings: list[ColorFinding] = []
    for block in style_blocks:
        for m in re.finditer(r"([\w-]+)\s*:\s*[^;{}]*", block):
            decl = m.group(0)
            prop = m.group(1)

            # material-law custom-property declarations: skip entirely,
            # regardless of colour distance — the item's own author already
            # ruled these out of brand-token scope.
            if prop.lstrip("-") in material_law_props:
                for lit_re in (HEX_RE, RGB_RE):
                    for lit_m in lit_re.finditer(decl):
                        all_findings.append(
                            ColorFinding(
                                raw=lit_m.group(0), property=prop, line_no=0,
                                role="foreign-surface",
                                reason=f"declares --{prop.lstrip('-')}, documented material colour by the item's own comment — never substituted",
                            )
                        )
                continue

            # var(--x, LITERAL) fallback where --x is already guaranteed
            # defined (a design token or a bridged local var): the literal
            # fallback can never actually render, so it needs no classification —
            # log it as inert rather than silently dropping it.
            fallback_positions = []
            for fb_m in VAR_FALLBACK_RE.finditer(decl):
                var_name = fb_m.group(1)
                if var_name in TOKEN_BRIDGE_MAP or f"--{var_name}" in {v[0] for v in DESIGN_TOKENS.values()}:
                    fallback_positions.append((fb_m.start(2), fb_m.end(2)))

            for lit_re in (HEX_RE, RGB_RE):
                for lit_m in lit_re.finditer(decl):
                    raw = lit_m.group(0)
                    if any(start <= lit_m.start() < end for start, end in fallback_positions):
                        all_findings.append(
                            ColorFinding(
                                raw=raw, property=prop, line_no=0, role="fallback-inert",
                                reason="fallback value of an already-bridged/token custom property — never rendered",
                            )
                        )
                        continue
                    finding = classify_literal(raw, prop)
                    all_findings.append(finding)

    unclassifiable = [f for f in all_findings if f.role == "UNCLASSIFIABLE"]
    if unclassifiable:
        for f in unclassifiable:
            result.unclassifiable.append({"raw": f.raw, "property": f.property, "reason": f.reason})
        raise SystemExit(
            f"BLOCKER-RETROFIT:{name} — {len(unclassifiable)} colour literal(s) could not be classified:\n"
            + "\n".join(f"  {f.raw} (property: {f.property}) — {f.reason}" for f in unclassifiable)
            + "\nNever guessed. Fix by hand or extend TOKEN classification, then re-run."
        )

    if result.unmapped_vars:
        raise SystemExit(
            f"BLOCKER-RETROFIT:{name} — local custom propert{'y' if len(result.unmapped_vars)==1 else 'ies'} "
            f"with no bridge mapping: {', '.join('--' + v for v in result.unmapped_vars)}. "
            "Add to TOKEN_BRIDGE_MAP with a deliberate choice, or leave undefined only if the "
            "item degrades safely without it (verify, don't assume)."
        )

    # apply substitutions (longest-match-first to avoid partial overlaps, e.g. an
    # 8-digit hex containing a 6-digit prefix). NOTE: this is a literal global
    # string replace, not an AST rewrite — if the identical literal value
    # appears in both a protected and a substitutable context in the same
    # file, both occurrences move together. Not a risk for any of the three
    # test items (checked); flagged as a known limitation for a future item
    # where it might matter, rather than silently assumed safe at scale.
    non_substituting_roles = {"structural-neutral", "foreign-surface", "fallback-inert"}
    for f in sorted(all_findings, key=lambda x: -len(x.raw)):
        if f.role in non_substituting_roles:
            result.color_map.append(
                {"literal": f.raw, "property": f.property, "role": f.role, "action": "kept-as-is", "reason": f.reason}
            )
            continue
        if f.replacement:
            html = html.replace(f.raw, f.replacement)
            result.color_map.append(
                {"literal": f.raw, "property": f.property, "role": f.role, "action": f"-> {f.replacement}", "reason": f.reason}
            )

    # item-level classification (R-13): foreign-surface if any literal was
    # protected as documented material colour; recolourable otherwise. reject
    # is never chosen here — it belongs to the render-time contrast check
    # (§T2 step 2, "render a probe frame ... reject if it fails"), not this
    # static pass.
    if any(f.role == "foreign-surface" for f in all_findings):
        result.classification = "foreign-surface"
    else:
        result.classification = "recolourable"

    # write output
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    out_path = OUT_ROOT / f"{name}.html"
    out_path.write_text(html)
    result.output_html_path = str(out_path.relative_to(REPO_ROOT))
    result.output_hash = hashlib.sha256(html.encode()).hexdigest()

    colormap_path = OUT_ROOT / f"{name}.colormap.json"
    colormap_path.write_text(json.dumps({"item": name, "findings": result.color_map, "bridged_vars": result.bridged_vars}, indent=2))

    return result


def emit_manifest_entry(result: RetrofitResult, source_commit: str, t0b_verdict: str | None) -> None:
    manifest = json.loads(MANIFEST_PATH.read_text()) if MANIFEST_PATH.exists() else {}
    manifest.setdefault("items", [])
    manifest["items"] = [i for i in manifest["items"] if i["name"] != result.name]  # replace if re-run
    manifest["items"].append(
        {
            "name": result.name,
            "upstream_source_commit": source_commit,
            "retrofit_script_version": SCRIPT_VERSION,
            "aspect": "n/a-embeds-in-host",
            "t0b_reframe_verdict": t0b_verdict,
            "classification": result.classification,
            "colormap_file": f"videos/_system/catalog/{result.name}.colormap.json",
            "output_file": result.output_html_path,
            "output_sha256": result.output_hash,
        }
    )
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2))


# ---------------------------------------------------------------------------
# CLI / test suite
# ---------------------------------------------------------------------------

TEST_ITEMS = ["focus-swap", "caption-highlight", "device-frame-stage"]
SOURCE_COMMIT = "0d5d3f3eb3aecd9fd64954d2767d3d64e97e58fc"


def load_t0b_verdict(name: str) -> str | None:
    inv_path = REPO_ROOT / "docs" / "wo" / "007" / "catalog-inventory.json"
    if not inv_path.exists():
        return None
    inv = json.loads(inv_path.read_text())
    for item in inv["items"]:
        if item["name"] == name:
            return item.get("t0b_verdict")
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("name", nargs="?", help="component name to retrofit")
    parser.add_argument("--test", action="store_true", help="run the 3-item test suite")
    args = parser.parse_args()

    if args.test:
        results = []
        for name in TEST_ITEMS:
            print(f"=== retrofitting {name} ===")
            result = retrofit_item(name)
            emit_manifest_entry(result, SOURCE_COMMIT, load_t0b_verdict(name))
            print(f"  classification: {result.classification}")
            print(f"  font links stripped: {result.font_links_stripped}, gsap pins: {result.gsap_pins}")
            print(f"  bridged vars: {result.bridged_vars}")
            print(f"  colour findings: {len(result.color_map)}")
            print(f"  output: {result.output_html_path} ({result.output_hash[:16]}...)")
            results.append(result)
        print("\n=== ALL 3 TEST ITEMS RETROFITTED CLEAN ===")
        return

    if not args.name:
        parser.error("provide a component name or --test")

    result = retrofit_item(args.name)
    emit_manifest_entry(result, SOURCE_COMMIT, load_t0b_verdict(args.name))
    print(json.dumps({"name": result.name, "classification": result.classification, "output": result.output_html_path}, indent=2))


if __name__ == "__main__":
    main()
