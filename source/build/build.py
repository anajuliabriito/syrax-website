"""Builds Main.dc.html from a template with one shared set of type and spacing tokens,
so every heading, paragraph and label on the page uses the same scale."""

T = {
    "SEC": "max-width: 1200px; margin: 0 auto; padding: 128px 32px 0",
    "EYEBROW": "margin: 0 0 20px; font-size: 12px; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; color: #8A6D12",
    "EYEBROWD": "margin: 0 0 20px; font-size: 12px; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; color: {{accent}}",
    "H2": "margin: 0; font-family: 'Inter Tight', Inter, sans-serif; font-weight: 600; font-size: clamp(2rem, 3.2vw, 2.75rem); line-height: 1.1; letter-spacing: -0.022em",
    "H3": "margin: 0; font-family: 'Inter Tight', Inter, sans-serif; font-weight: 600; font-size: 20px; line-height: 1.3",
    "LEAD": "font-size: 19px; line-height: 1.6; color: #3E3D39",
    "BODY": "font-size: 16px; line-height: 1.6; color: #55534D",
    "BODYD": "font-size: 16px; line-height: 1.6; color: #A9A59B",
    "META": "font-size: 13px; line-height: 1.5; color: #6B6A65",
    "RULE": "border-top: 1px solid #0B0B0B",
    "HAIR": "border-top: 1px solid #DDD9D0",
    "BTN": "text-decoration: none; color: #F7F6F3; background: #0B0B0B; font-weight: 600; font-size: 16px; padding: 14px 26px; border-radius: 4px; min-height: 48px; box-sizing: border-box; display: inline-flex; align-items: center",
    "BTNG": "text-decoration: none; color: #0B0B0B; background: {{accent}}; font-weight: 600; font-size: 16px; padding: 14px 24px; border-radius: 4px; min-height: 48px; box-sizing: border-box; display: inline-flex; align-items: center",
    "INPUT": "background: #FFFFFF; border: 1px solid #C9C6BD; border-radius: 4px; padding: 12px 14px; font: inherit; font-size: 16px; font-weight: 400; color: #0B0B0B",
    "LABEL": "display: flex; flex-direction: column; gap: 8px; font-size: 14px; font-weight: 500",
    "NUM": "font-family: 'Inter Tight', Inter, sans-serif; font-weight: 600; letter-spacing: -0.02em; font-variant-numeric: tabular-nums",
}

src = open("/home/claude/syrax/template.html").read()
src = src.replace("@@HELMET@@", open("/home/claude/syrax/helmet_block.html").read()).replace("@@VIDEO@@", open("/home/claude/syrax/video_block.html").read()).replace("@@HEADER@@", open("/home/claude/syrax/header_main.html").read()).replace("@@FOOTER@@", open("/home/claude/syrax/footer_shared.html").read())
for k in sorted(T, key=len, reverse=True):
    src = src.replace("%" + k + "%", T[k])
import re
left = re.findall(r"%[A-Z]+%", src)
assert not left, left
open("/home/claude/syrax/project/Main.dc.html", "w").write(src)
print("ok", len(src))
