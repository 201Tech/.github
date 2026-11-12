"""Gera os SVG da capa (profile/*.svg) em versão clara e escura.

Uso: python3 scripts/render.py
"""

from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "profile"

THEMES = {
    "dark": {"bg": "#0a0a0a", "panel": "#111111", "line": "#262626", "dot": "#1f1f1f",
             "text": "#f5f5f5", "muted": "#8a8a8a", "logo_bg": "#000000", "logo_fg": "#ffffff"},
    "light": {"bg": "#f5f5f5", "panel": "#ffffff", "line": "#e2e2e2", "dot": "#e6e6e6",
              "text": "#000000", "muted": "#6b6b6b", "logo_bg": "#000000", "logo_fg": "#ffffff"},
}

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
SANS = "ui-sans-serif, -apple-system, Segoe UI, Helvetica, Arial, sans-serif"

STACK = ["TypeScript", "Go", "Node.js", "React", "React Native", "PostgreSQL", "Terraform", "Docker"]

LOOP = [
    ("discover", "understand the problem"),
    ("design", "prototype with real users"),
    ("build", "small, senior, tested"),
    ("ship", "to production, then again"),
]


def svg(width: int, height: int, body: str, t: dict) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img">'
        f'<defs><pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">'
        f'<circle cx="2" cy="2" r="1.2" fill="{t["dot"]}"/></pattern></defs>'
        f'<rect width="100%" height="100%" rx="16" fill="{t["bg"]}"/>'
        f'<rect width="100%" height="100%" rx="16" fill="url(#dots)"/>'
        f"{body}</svg>"
    )


def logo(x: int, y: int, size: int, t: dict) -> str:
    scale = size / 100
    return (
        f'<g transform="translate({x} {y}) scale({scale})">'
        f'<rect width="100" height="100" rx="18" fill="{t["logo_bg"]}" stroke="{t["line"]}" stroke-width="2"/>'
        f'<g transform="translate(6 6) scale(0.88)"><g style="isolation:isolate">'
        f'<rect x="33.75" y="11.75" width="57" height="46.5" rx="7" fill="none" stroke="{t["logo_fg"]}" '
        f'stroke-width="7.5" style="mix-blend-mode:difference"/>'
        f'<rect x="23" y="15" width="57.5" height="54" rx="10" fill="{t["logo_fg"]}" style="mix-blend-mode:difference"/></g>'
        f'<rect x="3.25" y="68.25" width="20.5" height="15.5" rx="5" fill="none" stroke="{t["logo_fg"]}" '
        f'stroke-width="2.5"/></g></g>'
    )


def hero(t: dict) -> str:
    lines = [
        ("$", "whoami", t["text"]),
        ("", "an independent product studio. we design, build and run software.", t["muted"]),
        ("$", "while (product.alive) {", t["text"]),
        ("", "  discover(); design(); build(); ship();", t["text"]),
        ("", "}", t["text"]),
    ]
    rows = []
    for index, (prompt, text, color) in enumerate(lines):
        y = 236 + index * 30
        prefix = f'<tspan fill="{t["muted"]}">{prompt} </tspan>' if prompt else ""
        rows.append(
            f'<text x="104" y="{y}" xml:space="preserve" font-family="{MONO}" font-size="19" fill="{color}">'
            f"{prefix}{text}</text>"
        )
    cursor_y = 236 + len(lines) * 30 - 18
    cursor = (
        f'<rect x="104" y="{cursor_y}" width="11" height="22" fill="{t["text"]}">'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" dur="1s" '
        f'repeatCount="indefinite"/></rect>'
    )
    window = (
        f'<rect x="56" y="40" width="1088" height="360" rx="14" fill="{t["panel"]}" stroke="{t["line"]}"/>'
        f'<line x1="56" y1="80" x2="1144" y2="80" stroke="{t["line"]}"/>'
        + "".join(f'<circle cx="{84 + i * 20}" cy="60" r="6" fill="none" stroke="{t["muted"]}"/>' for i in range(3))
        + f'<text x="600" y="65" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{t["muted"]}">~/201tech</text>'
    )
    title = (
        logo(104, 108, 64, t)
        + f'<text x="190" y="152" font-family="{SANS}" font-size="46" font-weight="700" fill="{t["text"]}" letter-spacing="-1">201tech</text>'
        + f'<text x="192" y="178" font-family="{MONO}" font-size="15" fill="{t["muted"]}">we build software that people actually use</text>'
    )
    return svg(1200, 440, window + title + "".join(rows) + cursor, t)


def loop(t: dict) -> str:
    gap, width, top = 270, 210, 70
    start = (1200 - (gap * (len(LOOP) - 1) + width)) // 2
    parts = []
    for index, (name, caption) in enumerate(LOOP):
        x = start + index * gap
        parts.append(
            f'<rect x="{x}" y="{top}" width="{width}" height="86" rx="12" fill="{t["panel"]}" stroke="{t["line"]}"/>'
            f'<text x="{x + width / 2}" y="{top + 38}" text-anchor="middle" font-family="{MONO}" font-size="20" '
            f'font-weight="700" fill="{t["text"]}">{name}()</text>'
            f'<text x="{x + width / 2}" y="{top + 64}" text-anchor="middle" font-family="{MONO}" font-size="13" '
            f'fill="{t["muted"]}">{caption}</text>'
        )
        if index < len(LOOP) - 1:
            ax = x + width + 12
            parts.append(
                f'<path d="M{ax} {top + 43} H{ax + gap - width - 24}" stroke="{t["muted"]}" stroke-width="1.5" '
                f'marker-end="url(#arrow)"/>'
            )
    first_mid = start + width / 2
    last_mid = start + gap * (len(LOOP) - 1) + width / 2
    back = (
        f'<path d="M{last_mid} {top + 86} V{top + 130} H{first_mid} V{top + 98}" fill="none" '
        f'stroke="{t["muted"]}" stroke-width="1.5" stroke-dasharray="5 6" marker-end="url(#arrow)">'
        f'<animate attributeName="stroke-dashoffset" from="0" to="-22" dur="1.2s" repeatCount="indefinite"/></path>'
        f'<text x="600" y="{top + 152}" text-anchor="middle" font-family="{MONO}" font-size="14" '
        f'fill="{t["muted"]}">while (product.alive)</text>'
    )
    marker = (
        f'<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" '
        f'orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{t["muted"]}"/></marker></defs>'
    )
    return svg(1200, 250, marker + "".join(parts) + back, t)


def stack(t: dict) -> str:
    char, pad, gap, size = 9.6, 18, 12, 16
    widths = [len(name) * char + pad * 2 for name in STACK]
    x = (1200 - (sum(widths) + gap * (len(STACK) - 1))) / 2
    pills = []
    for name, width in zip(STACK, widths):
        pills.append(
            f'<rect x="{x:.1f}" y="34" width="{width:.1f}" height="40" rx="20" fill="{t["panel"]}" stroke="{t["line"]}"/>'
            f'<text x="{x + width / 2:.1f}" y="59" text-anchor="middle" font-family="{MONO}" font-size="{size}" '
            f'fill="{t["text"]}">{name}</text>'
        )
        x += width + gap
    return svg(1200, 108, "".join(pills), t)


def main() -> None:
    for name, theme in THEMES.items():
        for part, render in (("hero", hero), ("loop", loop), ("stack", stack)):
            (OUT / f"{part}-{name}.svg").write_text(render(theme), encoding="utf-8")


if __name__ == "__main__":
    main()
