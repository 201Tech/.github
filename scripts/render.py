"""Gera a capa da organização (profile/profile-dark.svg e profile-light.svg).

Uso: python3 scripts/render.py
"""

from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "profile"

THEMES = {
    "dark": {"bg": "#0a0a0a", "panel": "#111111", "line": "#262626", "dot": "#1c1c1c",
             "text": "#f5f5f5", "muted": "#8a8a8a", "logo_bg": "#000000", "logo_fg": "#ffffff"},
    "light": {"bg": "#f5f5f5", "panel": "#ffffff", "line": "#e2e2e2", "dot": "#e4e4e4",
              "text": "#000000", "muted": "#6b6b6b", "logo_bg": "#000000", "logo_fg": "#ffffff"},
}

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
SANS = "ui-sans-serif, -apple-system, Segoe UI, Helvetica, Arial, sans-serif"

WIDTH = 1200
MARGIN = 56
INNER = WIDTH - MARGIN * 2
GAP = 16
SECTION_GAP = 64

TERMINAL = [
    ("$", "whoami", "text"),
    ("", "an independent product studio. we design, build and run software.", "muted"),
    ("$", "while (product.alive) {", "text"),
    ("", "  discover(); design(); build(); ship();", "text"),
    ("", "}", "text"),
]

BUILD = ["mobile apps", "web platforms", "apis &amp; backends",
         "cloud &amp; infra", "ai &amp; automation", "payments &amp; marketplaces"]

LOOP = [
    ("discover", "understand the problem"),
    ("design", "prototype with real users"),
    ("build", "small, senior, tested"),
    ("ship", "to production, then again"),
]

PRINCIPLES = [
    ("we run what we build", "everything we ship lives in production, kept alive by us"),
    ("small and senior", "no layers between the problem and who writes the code"),
    ("code for humans", "readable over clever, config over hardcoded, few deps"),
    ("secure from the first commit", "privacy and security by design, not a final checklist"),
    ("ship small, ship often", "short loops with real users beat long plans"),
    ("yours from day one", "code, infra and docs belong to whoever owns the product"),
]

STACK = ["TypeScript", "Go", "Node.js", "React", "React Native", "PostgreSQL", "Terraform", "Docker"]

FOOTER = "201tech.net  ·  contato@201tech.net"


def text(x, y, content, t, color="text", size=15, weight=400, anchor="start", family=MONO):
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" xml:space="preserve" font-family="{family}" '
            f'font-size="{size}" font-weight="{weight}" fill="{t[color]}">{content}</text>')


def card(x, y, width, height, t, radius=12):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}" rx="{radius}" '
            f'fill="{t["panel"]}" stroke="{t["line"]}"/>')


def heading(y, label, t):
    return text(MARGIN, y, f'<tspan fill="{t["muted"]}">&gt;</tspan> {label}', t, size=17, weight=700)


def grid(items, columns, y, height, t, draw):
    width = (INNER - GAP * (columns - 1)) / columns
    parts = []
    for index, item in enumerate(items):
        x = MARGIN + (index % columns) * (width + GAP)
        top = y + (index // columns) * (height + GAP)
        parts.append(card(x, top, width, height, t) + draw(item, x, top, t))
    rows = (len(items) + columns - 1) // columns
    return "".join(parts), y + rows * height + (rows - 1) * GAP


def logo(x, y, size, t):
    return (
        f'<g transform="translate({x} {y}) scale({size / 100})">'
        f'<rect width="100" height="100" rx="18" fill="{t["logo_bg"]}" stroke="{t["line"]}" stroke-width="2"/>'
        f'<g transform="translate(6 6) scale(0.88)"><g style="isolation:isolate">'
        f'<rect x="33.75" y="11.75" width="57" height="46.5" rx="7" fill="none" stroke="{t["logo_fg"]}" '
        f'stroke-width="7.5" style="mix-blend-mode:difference"/>'
        f'<rect x="23" y="15" width="57.5" height="54" rx="10" fill="{t["logo_fg"]}" style="mix-blend-mode:difference"/></g>'
        f'<rect x="3.25" y="68.25" width="20.5" height="15.5" rx="5" fill="none" stroke="{t["logo_fg"]}" '
        f'stroke-width="2.5"/></g></g>'
    )


def hero(y, t):
    line_height, first_line = 30, y + 196
    height = first_line - y + len(TERMINAL) * line_height + 24
    parts = [
        card(MARGIN, y, INNER, height, t, radius=14),
        f'<line x1="{MARGIN}" y1="{y + 40}" x2="{MARGIN + INNER}" y2="{y + 40}" stroke="{t["line"]}"/>',
        *(f'<circle cx="{MARGIN + 28 + i * 20}" cy="{y + 20}" r="6" fill="none" stroke="{t["muted"]}"/>' for i in range(3)),
        text(WIDTH / 2, y + 25, "~/201tech", t, "muted", 14, anchor="middle"),
        logo(MARGIN + 48, y + 68, 64, t),
        text(MARGIN + 134, y + 112, "201tech", t, size=46, weight=700, family=SANS),
        text(MARGIN + 136, y + 138, "we build software that people actually use", t, "muted"),
    ]
    for index, (prompt, content, color) in enumerate(TERMINAL):
        prefix = f'<tspan fill="{t["muted"]}">{prompt} </tspan>' if prompt else ""
        parts.append(text(MARGIN + 48, first_line + index * line_height, prefix + content, t, color, 19))
    cursor_y = first_line + len(TERMINAL) * line_height - 18
    parts.append(
        f'<rect x="{MARGIN + 48}" y="{cursor_y}" width="11" height="22" fill="{t["text"]}">'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" dur="1s" repeatCount="indefinite"/></rect>'
    )
    return "".join(parts), y + height


def what_we_build(y, t):
    def draw(label, x, top, t):
        return text(x + 24, top + 35, f'<tspan fill="{t["muted"]}">~ </tspan>{label}', t, size=16)

    body, end = grid(BUILD, 3, y + 24, 56, t, draw)
    return heading(y, "what we build", t) + body, end


def how_we_build(y, t):
    box_width, box_height, top = (INNER - GAP * 3) / 4, 86, y + 24
    parts = [heading(y, "how we build", t),
             f'<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" '
             f'orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{t["muted"]}"/></marker></defs>']
    for index, (name, caption) in enumerate(LOOP):
        x = MARGIN + index * (box_width + GAP)
        parts += [card(x, top, box_width, box_height, t),
                  text(x + box_width / 2, top + 38, f"{name}()", t, size=20, weight=700, anchor="middle"),
                  text(x + box_width / 2, top + 64, caption, t, "muted", 13, anchor="middle")]

    first_mid = MARGIN + box_width / 2
    last_mid = MARGIN + 3 * (box_width + GAP) + box_width / 2
    loop_y = top + box_height + 34
    parts.append(
        f'<path d="M{last_mid:.1f} {top + box_height} V{loop_y} H{first_mid:.1f} V{top + box_height + 10}" fill="none" '
        f'stroke="{t["muted"]}" stroke-width="1.5" stroke-dasharray="5 6" marker-end="url(#arrow)">'
        f'<animate attributeName="stroke-dashoffset" from="0" to="-22" dur="1.2s" repeatCount="indefinite"/></path>'
    )
    parts.append(text(WIDTH / 2, loop_y - 8, "while (product.alive)", t, "muted", 14, anchor="middle"))

    def draw(item, x, top, t):
        title, description = item
        return text(x + 24, top + 30, title, t, size=16, weight=700) + text(x + 24, top + 52, description, t, "muted", 13)

    body, end = grid(PRINCIPLES, 2, loop_y + 28, 70, t, draw)
    return "".join(parts) + body, end


def stack(y, t):
    char, pad = 9.6, 18
    widths = [len(name) * char + pad * 2 for name in STACK]
    x = MARGIN + (INNER - (sum(widths) + GAP * (len(STACK) - 1))) / 2
    parts = [heading(y, "stack", t)]
    for name, width in zip(STACK, widths):
        parts += [card(x, y + 24, width, 40, t, radius=20),
                  text(x + width / 2, y + 49, name, t, size=16, anchor="middle")]
        x += width + GAP
    return "".join(parts), y + 64


def page(t):
    parts, y = [], 40
    for section in (hero, what_we_build, how_we_build, stack):
        body, end = section(y if section is hero else y + 24, t)
        parts.append(body)
        y = end + SECTION_GAP - 24
    parts.append(text(WIDTH / 2, y + 30, FOOTER, t, "muted", 15, anchor="middle"))
    height = y + 70
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height:.0f}" '
        f'viewBox="0 0 {WIDTH} {height:.0f}" role="img" aria-label="201tech">'
        f'<defs><pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">'
        f'<circle cx="2" cy="2" r="1.2" fill="{t["dot"]}"/></pattern></defs>'
        f'<rect width="100%" height="100%" rx="16" fill="{t["bg"]}"/>'
        f'<rect width="100%" height="100%" rx="16" fill="url(#dots)"/>'
        + "".join(parts) + "</svg>"
    )


def main():
    for name, theme in THEMES.items():
        (OUT / f"profile-{name}.svg").write_text(page(theme), encoding="utf-8")


if __name__ == "__main__":
    main()
