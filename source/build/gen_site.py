"""Generates every Syrax subpage plus the site map artboard from shared parts,
so navigation, footer, type scale and spacing are identical on every page."""
import html, json, os
OUT = "/home/claude/syrax/project"

# ---------- shared tokens (same as build.py) ----------
T = {
    "SEC": "max-width: 1200px; margin: 0 auto; padding: 112px 32px 0",
    "H1": "margin: 0; font-family: 'Inter Tight', Inter, sans-serif; font-weight: 600; font-size: clamp(2.5rem, 4.6vw, 4rem); line-height: 1.04; letter-spacing: -0.03em",
    "H2": "margin: 0; font-family: 'Inter Tight', Inter, sans-serif; font-weight: 600; font-size: clamp(2rem, 3.2vw, 2.75rem); line-height: 1.1; letter-spacing: -0.022em",
    "H3": "margin: 0; font-family: 'Inter Tight', Inter, sans-serif; font-weight: 600; font-size: 20px; line-height: 1.3",
    "LEAD": "font-size: 19px; line-height: 1.6; color: #3E3D39",
    "BODY": "font-size: 16px; line-height: 1.65; color: #55534D",
    "META": "font-size: 13px; line-height: 1.5; color: #6B6A65",
    "HAIR": "border-top: 1px solid #DDD9D0",
    "RULE": "border-top: 1px solid #0B0B0B",
    "BTNG": "text-decoration: none; color: #0B0B0B; background: {{accent}}; font-weight: 600; font-size: 16px; padding: 14px 24px; border-radius: 4px; min-height: 48px; box-sizing: border-box; display: inline-flex; align-items: center",
    "BTN": "text-decoration: none; color: #F7F6F3; background: #0B0B0B; font-weight: 600; font-size: 16px; padding: 14px 24px; border-radius: 4px; min-height: 48px; box-sizing: border-box; display: inline-flex; align-items: center",
    "INPUT": "background: #FFFFFF; border: 1px solid #C9C6BD; border-radius: 4px; padding: 12px 14px; font: inherit; font-size: 16px; font-weight: 400; color: #0B0B0B",
    "LABEL": "display: flex; flex-direction: column; gap: 8px; font-size: 14px; font-weight: 500",
    "NUM": "font-family: 'Inter Tight', Inter, sans-serif; font-weight: 600; letter-spacing: -0.02em; font-variant-numeric: tabular-nums",
}
def t(s):
    for k in sorted(T, key=len, reverse=True):
        s = s.replace("%" + k + "%", T[k])
    return s
e = html.escape

IMG = {
    "detect": "/_blob/c0a15f989bab8aaf166c4b74388dd7e5",
    "flyover": "/_blob/b28f07d833468d60ed20c4549447ecef",
    "dock": "/_blob/ff1b44b7cc7ff10c30dd25a26026ab94",
    "launch": "/_blob/d0bf85568f3e8bf6a923d6d9d3a5913d",
    "farmer": "/_blob/12b4d05099d015bf5d7e1dc8bd1517dd",
    "poster": "/_blob/d6ed1865dfdead58dafbed3bf7429c2e",
}
LOGO = "/_blob/929aeba2faf7c9b2e31c98dcf9054ace"
HELMET = open("/home/claude/syrax/helmet_block.html").read()

NAV = [("CattleCounting.dc.html", "Cattle counting"), ("WaterFeed.dc.html", "Water and feed"),
       ("HowItWorks.dc.html", "How it works"), ("WhoItsFor.dc.html", "Who it's for"),
       ("Resources.dc.html", "Resources"), ("About.dc.html", "About")]

def header(active=None):
    links = "".join(
        f'<a href="{h}" style="text-decoration: none; color: {"#F2F0EA" if h == active else "#CFCAC0"}{"; font-weight: 600" if h == active else ""}"{" aria-current=\"page\"" if h == active else ""}>{e(l)}</a>\n'
        for h, l in NAV)
    return f'''<header style="background: #0B0B0B">
<nav aria-label="Main" style="max-width: 1200px; margin: 0 auto; padding: 20px 32px; display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 16px">
<a href="Main.dc.html" aria-label="Syrax Solutions home" style="display: flex; align-items: center"><img src="{LOGO}" alt="Syrax Solutions" style="height: 38px; width: auto; display: block"></a>
<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 28px; font-size: 15px; font-weight: 500">
{links}<a href="Contact.dc.html" style="text-decoration: none; color: #0B0B0B; background: {{{{accent}}}}; font-weight: 600; padding: 10px 18px; border-radius: 4px; min-height: 44px; box-sizing: border-box; display: inline-flex; align-items: center">Talk to us</a>
</div>
</nav>
</header>'''

FOOT_COLS = [
    ("Product", [("CattleCounting.dc.html", "Cattle counting"), ("WaterFeed.dc.html", "Water and feed monitoring"),
                 ("FenceWelfare.dc.html", "Fence and welfare checks"), ("HowItWorks.dc.html", "How it works")]),
    ("Company", [("About.dc.html", "About"), ("WhoItsFor.dc.html", "Who it's for"), ("Resources.dc.html", "Resources"),
                 ("FAQ.dc.html", "FAQ"), ("Contact.dc.html", "Contact")]),
]
def footer():
    cols = ""
    for title, links in FOOT_COLS:
        items = "".join(f'<li style="padding: 5px 0"><a href="{h}" style="color: #CFCAC0; text-decoration: none">{e(l)}</a></li>' for h, l in links)
        cols += f'<div><p style="margin: 0 0 10px; font-size: 14px; font-weight: 600; color: #F2F0EA">{title}</p><ul style="list-style: none; margin: 0; padding: 0">{items}</ul></div>\n'
    return f'''<footer style="background: #0B0B0B; color: #A9A59B; border-top: 1px solid #222">
<div style="max-width: 1200px; margin: 0 auto; padding: 64px 32px 40px; display: flex; flex-wrap: wrap; justify-content: space-between; gap: 48px; font-size: 15px">
<div style="flex: 1 1 300px; min-width: 0">
<img src="{LOGO}" alt="Syrax Solutions" style="height: 34px; width: auto; display: block">
<p style="margin: 16px 0 0; max-width: 22rem">Every head counted. Every day. Automated herd monitoring for Australian grazing properties.</p>
</div>
<div style="flex: 1 1 400px; min-width: 0; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 32px">
{cols}</div>
</div>
<div style="max-width: 1200px; margin: 0 auto; padding: 20px 32px 32px; border-top: 1px solid #222; font-size: 13px; color: #8F8B82">© 2026 Syrax Solutions · Sydney, Australia</div>
</footer>'''

# ---------- blocks ----------
def hero(h1, sub, img=None, pos="center", alt="", crumb=None):
    crumbs = ""
    if crumb:
        crumbs = f'<nav aria-label="Breadcrumb" style="font-size: 14px; color: #8F8B82; margin-bottom: 28px"><a href="Main.dc.html" style="color: #A9A59B; text-decoration: none">Home</a> <span aria-hidden="true">/</span> <span>{e(crumb)}</span></nav>'
    pic = ""
    if img:
        pic = f'<div style="margin-top: 56px; aspect-ratio: 21 / 8; border-radius: 8px; overflow: hidden; background: #2A2620"><img src="{IMG[img]}" alt="{e(alt)}" style="width: 100%; height: 100%; object-fit: cover; object-position: {pos}; display: block"></div>'
    return t(f'''<section style="background: #0B0B0B; color: #F2F0EA">
<div style="max-width: 1200px; margin: 0 auto; padding: 72px 32px 88px">
{crumbs}
<div style="max-width: 820px">
<h1 style="%H1%">{e(h1)}</h1>
<p style="margin: 22px 0 0; max-width: 640px; font-size: 19px; line-height: 1.6; color: #BDB9AE">{e(sub)}</p>
<div style="margin-top: 32px"><a href="Contact.dc.html" style="%BTNG%">Get Syrax on your property</a></div>
</div>
{pic}
</div>
</section>''')

def feature(title, lines, img, pos="center", alt="", reverse=False, intro=None):
    li = "".join(f'<li style="%HAIR%; padding: 14px 0; font-size: 17px; color: #3E3D39">{e(l)}</li>' for l in lines)
    p = f'<p style="margin: 14px 0 0; %BODY%">{e(intro)}</p>' if intro else ""
    return t(f'''<div style="display: flex; flex-wrap: wrap; flex-direction: {"row-reverse" if reverse else "row"}; gap: 64px; align-items: center; margin-top: 80px">
<div style="flex: 1.15 1 460px; min-width: 0; aspect-ratio: 4 / 3; border-radius: 8px; overflow: hidden; background: #3A3426"><img src="{IMG[img]}" alt="{e(alt)}" style="width: 100%; height: 100%; object-fit: cover; object-position: {pos}; display: block"></div>
<div style="flex: 1 1 360px; min-width: 0">
<h3 style="%H2%; font-size: clamp(1.6rem, 2.4vw, 2.1rem)">{e(title)}</h3>
{p}
<ul style="list-style: none; margin: 24px 0 0; padding: 0">{li}</ul>
</div>
</div>''')

def section(inner, bg=None, top=112, bottom=0):
    if bg:
        return t(f'<section style="background: {bg}"><div style="max-width: 1200px; margin: 0 auto; padding: {top}px 32px {bottom or 112}px">{inner}</div></section>')
    return t(f'<section style="max-width: 1200px; margin: 0 auto; padding: {top}px 32px {bottom}px">{inner}</section>')

def h2(text, sub=None, maxw=760):
    s = f'<h2 style="%H2%; max-width: {maxw}px">{e(text)}</h2>'
    if sub: s += f'<p style="margin: 16px 0 0; max-width: 680px; %LEAD%">{e(sub)}</p>'
    return t(s)

def cards(items, cols=3, min_w=260):
    c = "".join(f'<div style="background: #FFFFFF; border: 1px solid #DDD9D0; border-radius: 8px; padding: 24px"><h3 style="%H3%; font-size: 18px">{e(a)}</h3><p style="margin: 8px 0 0; %BODY%">{e(b)}</p></div>' for a, b in items)
    return t(f'<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax({min_w}px, 1fr)); gap: 16px; margin-top: 48px">{c}</div>')

def ruled(items, min_w=250):
    c = "".join(f'<div style="%RULE%; padding: 22px 0 28px"><h3 style="%H3%">{e(a)}</h3><p style="margin: 8px 0 0; %BODY%">{e(b)}</p></div>' for a, b in items)
    return t(f'<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax({min_w}px, 1fr)); gap: 0 40px; margin-top: 48px">{c}</div>')

def steps(items):
    c = "".join(f'<li style="%RULE%; padding-top: 20px"><span style="display: block; %NUM%; font-size: 14px; color: #8A6D12">0{i+1}</span><h3 style="%H3%; margin-top: 10px">{e(a)}</h3><p style="margin: 8px 0 0; %BODY%">{e(b)}</p></li>' for i, (a, b) in enumerate(items))
    return t(f'<ol style="list-style: none; margin: 48px 0 0; padding: 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 40px">{c}</ol>')

def prose(paras, maxw=720):
    return t("".join(f'<p style="margin: 18px 0 0; max-width: {maxw}px; %LEAD%">{e(p)}</p>' for p in paras))

def faq(items, title="Questions", link=True):
    d = "".join(f'''<details style="border-bottom: 1px solid #DDD9D0"><summary style="display: flex; justify-content: space-between; align-items: center; gap: 24px; padding: 22px 0; min-height: 44px; %H3%; font-size: 18px"><span>{e(q)}</span><svg class="syrax-plus" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true" style="flex: 0 0 auto; transition: transform 0.2s"><path d="M12 5v14M5 12h14"></path></svg></summary><p style="margin: 0 0 24px; max-width: 44rem; %BODY%">{e(a)}</p></details>''' for q, a in items)
    more = '<p style="margin: 24px 0 0"><a href="FAQ.dc.html" style="font-weight: 600; text-underline-offset: 4px">See all questions</a></p>' if link else ""
    return t(f'''<div style="display: flex; flex-wrap: wrap; gap: 64px">
<div style="flex: 1 1 280px; min-width: 0"><h2 style="%H2%">{e(title)}</h2></div>
<div style="flex: 2 1 600px; min-width: 0; %RULE%">{d}{more}</div>
</div>''')

def stats_band(stats, caption, source):
    c = "".join(f'<div style="border-top: 1px solid #3A3A3A; padding-top: 16px"><p style="margin: 0; %NUM%; font-size: clamp(2.2rem, 4vw, 3.2rem); line-height: 1; color: {{{{accent}}}}">{e(n)}</p><p style="margin: 10px 0 0; font-size: 16px; line-height: 1.6; color: #A9A59B">{e(b)}</p></div>' for n, b in stats)
    return t(f'''<div style="background: #0B0B0B; color: #F2F0EA; border-radius: 10px; padding: clamp(32px, 5vw, 64px); display: flex; flex-wrap: wrap; gap: 48px; align-items: flex-end; justify-content: space-between">
<div style="flex: 1 1 380px; min-width: 0"><h2 style="%H2%">{e(caption[0])}</h2><p style="margin: 16px 0 0; font-size: 19px; line-height: 1.6; color: #BDB9AE">{e(caption[1])}</p></div>
<div style="flex: 1 1 440px; min-width: 0; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 32px">{c}<p style="grid-column: 1 / -1; margin: 0; font-size: 13px; color: #8F8B82">Source: {e(source)}</p></div>
</div>''')

def callout(text):
    return t(f'<div style="margin-top: 40px; border-left: 3px solid #8A6D12; background: #FFFFFF; padding: 20px 24px; max-width: 760px; %BODY%; color: #3E3D39">{e(text)}</div>')

def cta(title="Get Syrax on your property.", sub="Tell us about your property. We'll come back with a plan and a fixed quote."):
    return t(f'''<section style="max-width: 1200px; margin: 0 auto; padding: 112px 32px 112px">
<div style="background: #0B0B0B; color: #F2F0EA; border-radius: 10px; padding: clamp(32px, 5vw, 64px); display: flex; flex-wrap: wrap; gap: 32px; align-items: center; justify-content: space-between">
<div style="flex: 1 1 480px; min-width: 0"><h2 style="%H2%">{e(title)}</h2><p style="margin: 14px 0 0; font-size: 19px; line-height: 1.6; color: #BDB9AE">{e(sub)}</p></div>
<a href="Contact.dc.html" style="%BTNG%">Talk to us</a>
</div>
</section>''')

def related(items):
    c = "".join(f'<a href="{h}" style="display: block; text-decoration: none; color: #0B0B0B; background: #FFFFFF; border: 1px solid #DDD9D0; border-radius: 8px; padding: 24px"><span style="display: block; %H3%; font-size: 18px">{e(a)}</span><span style="display: block; margin-top: 6px; %BODY%">{e(b)}</span><span style="display: block; margin-top: 14px; font-size: 15px; font-weight: 600; color: #8A6D12">Learn more</span></a>' for h, a, b in items)
    return t(f'<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; margin-top: 40px">{c}</div>')

def page(fname, title, desc, active, body, h=3600):
    props = json.dumps({"accent": {"editor": "color", "default": "#D4AF37", "options": ["#D4AF37", "#C9A227", "#B8962E"]}, "$preview": {"width": 1440, "height": h}})
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<script src="./support.js"></script>
</head>
<body>
<x-dc>
{HELMET}
<div style="background: #F7F6F3; color: #0B0B0B; font-family: Inter, system-ui, sans-serif; font-size: 16px; line-height: 1.6; -webkit-font-smoothing: antialiased">
{header(active)}
<main>
{body}
</main>
{footer()}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{props}'>
class Component extends DCLogic {{
  renderVals() {{
    return {{ accent: this.props.accent ?? '#D4AF37' }};
  }}
}}
</script>
</body>
</html>
'''
    open(os.path.join(OUT, fname), "w").write(doc)
    return fname, h

PAGES = []

# ================= Cattle counting =================
PAGES.append(page("CattleCounting.dc.html",
    "Drone Cattle Counting | Daily Automated Head Counts | Syrax",
    "Automated drone cattle counting for Australian grazing properties. A docked drone counts every head by paddock each day and texts you what changed.",
    "CattleCounting.dc.html",
    hero("Drone cattle counting, every day, by paddock.", "A head count you can trust, without mustering, driving or guessing.", "detect", "center", "Aerial image with every animal outlined by a detection box", "Cattle counting")
    + section(h2("How the count works")
        + feature("A count you can check", ["Flown mid-morning, when shadows are short", "Every animal detected and marked on the photo", "Totalled paddock by paddock", "Compared with the previous flight"], "detect", "center", "Detection boxes around cattle in a paddock", intro="The dock launches on schedule and the drone flies the same mapped route every day, so each count compares like with like."))
    + section(h2("Why a daily count matters") + ruled([
        ("Losses found early", "A missing animal shows up in this morning's report, while there's still time to find it."),
        ("Stock on hand, any day", "Know exactly what you're running before a sale, a move or a lender's call."),
        ("Less time and fuel", "No muster and no drive around the property to get a number.")]))
    + section(h2("What's in every count report") + cards([
        ("Total head", "Today's count against what you expect to be running."),
        ("Change by paddock", "Every paddock compared with the previous flight."),
        ("Marked images", "The photo with every animal marked, so you can verify it."),
        ("Last seen", "Where a missing animal was last detected."),
        ("History", "Every count kept, dated and searchable."),
        ("Shareable", "Send a report to an accountant, buyer or lender.")]))
    + section(faq([
        ("Can it count cattle under trees?", "Mid-morning flights and a thermal camera find most animals in cover. Shade can still hide some, which is why every count is checked against yesterday and backed by photos."),
        ("Does it identify individual animals?", "Not yet. Syrax counts head by paddock and flags changes. Individual identification is on our roadmap."),
        ("Can I share counts with my accountant or lender?", "Yes. Every report is dated and photo-backed, and can be shared as a link or download.")]))
    + section(h2("Also on the same flight") + related([
        ("WaterFeed.dc.html", "Water and feed monitoring", "Low troughs and empty bunks flagged."),
        ("FenceWelfare.dc.html", "Fence and welfare checks", "Breaks, open gates and animals that need a look.")]))
    + cta(), 4300))

# ================= Water and feed =================
PAGES.append(page("WaterFeed.dc.html",
    "Remote Water Trough and Feed Bunk Monitoring by Drone | Syrax",
    "Check every water trough and feed bunk from the air each day. Syrax flags low troughs and empty bunks before your cattle go without.",
    "WaterFeed.dc.html",
    hero("Water and feed, checked from the air every day.", "Low troughs and empty bunks flagged before your cattle go without.", "flyover", "center 60%", "The drone flying low over a paddock with cattle beneath it", "Water and feed")
    + section(stats_band([("$120,000", "a year checking and maintaining water"), ("1,200 km", "driven every week to check it")],
        ("The water run is the most expensive check on the place.", "One Queensland station spends this on water alone."), "Beef Central, Isis Downs"))
    + section(feature("Water troughs", ["Every trough on the route photographed", "Low or empty troughs flagged straight away", "Location and photo in the alert"], "flyover", "center 60%", "Drone over a paddock near a trough", intro="A trough can stop filling half an hour after the water run. Syrax checks it every day instead of every week.")
        + feature("Feed bunks", ["Remaining feed estimated from the mapping flight", "Top-up alerts before bunks run empty", "Feed use tracked over time"], "dock", "62% center", "The drone dock beside a paddock with cattle", reverse=True, intro="The mapping flight measures what's left in each bunk, so you know when to top up without driving out."))
    + section(h2("Already using water telemetry?", "Keep it. Telemetry tells you about one tank. Syrax sees every trough the drone passes, plus your cattle, feed and fences, on one flight.", 760))
    + section(faq([
        ("Does Syrax replace tank sensors?", "It complements them. Sensors watch one point continuously. Syrax checks every trough on the route once a day and adds your cattle, feed and fences."),
        ("How accurate are feed estimates?", "Bunk volumes are estimated from mapping imagery. They're designed to tell you when to top up, not to replace a weighbridge.")]))
    + cta(), 4100))

# ================= Fence and welfare =================
PAGES.append(page("FenceWelfare.dc.html",
    "Drone Fence Line Checks and Livestock Welfare Monitoring | Syrax",
    "Find fence breaks, open gates and animals that need attention the same day. Daily drone checks for Australian cattle properties.",
    "FenceWelfare.dc.html",
    hero("Fence breaks and animals that need a look, found the same day.", "Your boundary flown and your herd scanned on every flight.", "launch", "center 45%", "The drone lifting off from its dock beside a paddock fence", "Fences and welfare")
    + section(feature("Fence lines", ["Boundary fences flown on every route", "Breaks and open gates flagged", "Photo and location so you know where to go"], "launch", "55% center", "Drone lifting off beside a fence line", intro="Cattle find a broken fence fast. Syrax finds it first.")
        + feature("Welfare flags", ["Thermal readings that stand out from the herd", "Animals lying apart from the mob", "Last-seen location in the alert"], "flyover", "center 60%", "Drone flying over cattle at sunrise", reverse=True, intro="Flags show you where to look first, so problems don't wait for the next drive past."))
    + section(callout("Welfare flags help you decide where to look. They are not a veterinary diagnosis. Always check the animal and call your vet when needed."), top=56)
    + section(h2("Part of every flight") + related([
        ("CattleCounting.dc.html", "Cattle counting", "Every head, by paddock, every day."),
        ("WaterFeed.dc.html", "Water and feed monitoring", "Troughs and bunks checked from the air.")]))
    + cta(), 3600))

# ================= How it works =================
sys_html = "".join(t(f'<div><div style="aspect-ratio: 4 / 3; border-radius: 8px; overflow: hidden; background: #3A3426"><img src="{IMG[i]}" alt="{e(alt)}" style="width: 100%; height: 100%; object-fit: cover; object-position: {pos}; display: block"></div><h3 style="%H3%; margin-top: 20px">{e(a)}</h3><p style="margin: 6px 0 0; %BODY%">{e(b)}</p></div>') for i, pos, alt, a, b in [
    ("dock", "62% center", "Drone in its weatherproof dock", "The dock", "Lives on your property. Launches, lands and charges the drone, in any season."),
    ("flyover", "center 60%", "Drone flying over a paddock", "The drone", "Visual and thermal cameras. Flies the same mapped route every day."),
    ("farmer", "38% center", "Grazier reading his Syrax report", "The software", "Turns each flight into a count and tells you what changed.")])
PAGES.append(page("HowItWorks.dc.html",
    "How Syrax Works | Automated Drone-in-a-Box for Cattle Properties",
    "A weatherproof dock on your property, a drone on a daily schedule and software that tells you what changed. See how Syrax works.",
    "HowItWorks.dc.html",
    hero("How Syrax works.", "A dock on your property, a drone on a schedule, and software that tells you what changed.", crumb="How it works")
    + section(h2("Three parts. No pilot. No one on site.") + t(f'<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 32px; margin-top: 48px">{sys_html}</div>'))
    + section(h2("From first call to first count") + steps([
        ("Assess", "We check coverage, power and where the dock should go."),
        ("Install", "The dock goes in and every route is mapped."),
        ("Fly and count", "The drone launches on schedule, flies the route and returns to charge."),
        ("Act", "You get a text with what changed and the full report in the app.")]))
    + section(h2("When it flies") + prose([
        "Counting flights run mid-morning. Shadows are short and cattle under trees are easier to see, so that's when a count is most reliable.",
        "The dock waits out unsafe weather and flies when conditions allow. You'll always know when the next flight is due."]))
    + section(h2("What your property needs") + ruled([
        ("Power", "At the dock site. Mains or solar, depending on location."),
        ("Connectivity", "A mobile or satellite internet connection."),
        ("A dock site", "Open ground with a clear view of the sky. We find the best spot.")]))
    + section(h2("Where results arrive") + ruled([
        ("SMS alerts", "When something needs you."), ("Daily summary", "The day's numbers in one text."),
        ("Weekly email", "Trends for your records."), ("Phone and web app", "Reports, photos and a live view.")], 220))
    + cta(), 4400))

# ================= Who it's for =================
def who_block(title, body, lines, img, pos, alt, rev):
    return feature(title, lines, img, pos, alt, reverse=rev, intro=body)
PAGES.append(page("WhoItsFor.dc.html",
    "Who Syrax Is For | Graziers, Station Managers and Agistment Owners",
    "Daily drone herd monitoring for owner-operators, station managers, agistment and absentee owners, and multi-property cattle operations in Australia.",
    "WhoItsFor.dc.html",
    hero("Built for cattle you can't always see.", "For the people responsible for a herd spread across big country.", crumb="Who it's for")
    + section(who_block("Owner-operators", "You know every paddock, but you can't be in all of them every day.", ["Every paddock checked without the drive", "Problems found the same morning", "Time back for the jobs that matter"], "farmer", "38% center", "Grazier reading his phone", False)
        + who_block("Station and farm managers", "Give owners a clear daily picture without adding to anyone's workload.", ["A daily, photo-backed herd report", "Staff sent where they're needed", "History for every paddock"], "detect", "center", "Aerial count image", True)
        + who_block("Agistment and absentee owners", "Cattle on someone else's country, or a property you can't visit often.", ["See your count from anywhere", "Know your cattle have water", "A shared record with the landholder"], "flyover", "center 60%", "Drone flying over cattle", False)
        + who_block("Multi-property operations", "Every property, dock and paddock in one account.", ["Compare herds across properties", "One dashboard for every dock", "Consistent counts on every place"], "dock", "62% center", "Drone dock beside a paddock", True), top=40)
    + section(h2("Stock inventory you can prove", "A dated, photo-verified count every day. Ready when a buyer, accountant or lender asks what's on hand.", 760))
    + cta(), 4800))

# ================= About =================
PAGES.append(page("About.dc.html",
    "About Syrax Solutions | Australian Drone Herd Monitoring",
    "Syrax is a Sydney-based company building software that turns a daily drone flight into answers for Australian graziers.",
    "About.dc.html",
    hero("We turn a drone flight into answers.", "Syrax builds the software that counts your cattle and checks your property, every day.", crumb="About")
    + section(h2("Why we started Syrax") + prose([
        "Counting cattle and checking waters still means hours in the ute on most properties. The technology to do it from the air already exists. What was missing was software that turns the footage into a simple answer a grazier can act on.",
        "Syrax brings together software engineering and drone engineering. We set up the hardware, run the flights and deliver the result to your phone."]))
    + section(h2("What we stand for") + ruled([
        ("Built for Australian country", "Big paddocks, long distances, patchy coverage. Designed around how stations actually run."),
        ("Numbers you can check", "Every count comes with the photo behind it. No black boxes."),
        ("Done for you", "We choose, install and support the hardware. You read the result.")]))
    + section(h2("Based in Sydney, working Australia-wide.", "Talk to us about your property, wherever it is.", 760))
    + cta(), 3200))

# ================= FAQ =================
groups = [
    ("Getting started", [("What does setup involve?", "A property assessment, installing the dock and mapping your routes. We handle all of it."),
                         ("What does my property need?", "Power at the dock site and a mobile or satellite connection. We check both in the assessment."),
                         ("Can I use a drone I already own?", "Syrax is built around the DJI Dock 3. If you already have DJI enterprise equipment, we'll check whether it can be used.")]),
    ("The drone and dock", [("Does anyone need to fly the drone?", "No. The dock launches, lands and charges it on schedule."),
                            ("Do I need a drone licence?", "No. We handle the operating requirements as part of setup."),
                            ("Will the drone stress my cattle?", "It flies well above the herd on the same route every day. Cattle get used to it quickly."),
                            ("What happens in bad weather?", "The dock waits out unsafe conditions and flies when it's safe.")]),
    ("Counting and accuracy", [("Why do flights run mid-morning?", "Short shadows. Cattle under trees are easiest to see, so counts are most reliable."),
                               ("How do I know a count is right?", "Every report shows the photo with every animal marked, and compares it with the previous flight."),
                               ("Does it identify individual animals?", "Not yet. Syrax counts head by paddock and flags changes.")]),
    ("Data and cost", [("Who can see my data?", "Only the people you give access to. Every account uses secure sign-in."),
                       ("What does it cost?", "It depends on your property. You get a fixed quote after the assessment.")]),
]
faq_body = ""
for g, qs in groups:
    faq_body += section(faq(qs, g, link=False), top=80)
PAGES.append(page("FAQ.dc.html",
    "Drone Cattle Monitoring FAQ | Syrax",
    "Answers on setup, drone docks, licences, counting accuracy, data and cost for Syrax automated cattle monitoring.",
    "FAQ.dc.html",
    hero("Frequently asked questions.", "Straight answers on setup, the drone, counting accuracy and cost.", crumb="FAQ") + faq_body + cta("Still have a question?", "Talk to us. We'll answer it straight."), 4200))

# ================= Contact =================
contact_body = t(f'''<section style="max-width: 1200px; margin: 0 auto; padding: 96px 32px 112px; display: flex; flex-wrap: wrap; gap: 64px">
<div style="flex: 1 1 360px; min-width: 0">
<h2 style="%H2%">What happens next</h2>
<ol style="list-style: none; margin: 32px 0 0; padding: 0">
<li style="%HAIR%; padding: 16px 0"><h3 style="%H3%; font-size: 18px">We call you</h3><p style="margin: 4px 0 0; %BODY%">A short chat about your property and herd.</p></li>
<li style="%HAIR%; padding: 16px 0"><h3 style="%H3%; font-size: 18px">We assess your property</h3><p style="margin: 4px 0 0; %BODY%">Coverage, power and dock placement.</p></li>
<li style="%HAIR%; padding: 16px 0"><h3 style="%H3%; font-size: 18px">You get a plan and a fixed quote</h3><p style="margin: 4px 0 0; %BODY%">No surprises, no obligation.</p></li>
</ol>
<p style="margin: 32px 0 0; %BODY%">[YOUR EMAIL]<br>[YOUR PHONE]</p>
</div>
<form style="flex: 1 1 520px; min-width: 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; align-content: start; background: #FFFFFF; border: 1px solid #DDD9D0; border-radius: 10px; padding: 32px">
<label style="%LABEL%">Name<input type="text" name="name" autocomplete="name" style="%INPUT%"></label>
<label style="%LABEL%">Phone<input type="tel" name="phone" autocomplete="tel" style="%INPUT%"></label>
<label style="%LABEL%">Email<input type="email" name="email" autocomplete="email" style="%INPUT%"></label>
<label style="%LABEL%">Property location<input type="text" name="location" style="%INPUT%"></label>
<label style="%LABEL%">Approximate herd size<input type="text" name="herd" style="%INPUT%"></label>
<label style="%LABEL%">I'm interested in<select name="interest" style="%INPUT%"><option>Cattle counting</option><option>Water and feed monitoring</option><option>Fence and welfare checks</option><option>All of it</option></select></label>
<label style="grid-column: 1 / -1; %LABEL%">Anything else we should know?<textarea name="notes" rows="4" style="%INPUT%; resize: vertical"></textarea></label>
<div style="grid-column: 1 / -1"><button type="button" style="%BTN%; border: 0; font-family: inherit; cursor: pointer">Send</button></div>
</form>
</section>''')
PAGES.append(page("Contact.dc.html",
    "Contact Syrax | Get Drone Cattle Monitoring on Your Property",
    "Talk to Syrax about automated drone cattle counting and property checks. Get a property assessment and a fixed quote.",
    None,
    t(f'''<section style="background: #0B0B0B; color: #F2F0EA"><div style="max-width: 1200px; margin: 0 auto; padding: 72px 32px 88px">
<nav aria-label="Breadcrumb" style="font-size: 14px; color: #8F8B82; margin-bottom: 28px"><a href="Main.dc.html" style="color: #A9A59B; text-decoration: none">Home</a> <span aria-hidden="true">/</span> <span>Contact</span></nav>
<h1 style="%H1%">Talk to us.</h1>
<p style="margin: 22px 0 0; max-width: 640px; font-size: 19px; line-height: 1.6; color: #BDB9AE">Tell us about your property. We'll come back with a plan and a fixed quote.</p>
</div></section>''') + contact_body, 2400))

# ================= Resources + articles =================
ARTICLES = [
    ("ArticleMidMorning.dc.html", "Why mid-morning flights give the most accurate cattle counts", "Counting", "detect", "center",
     "Why Mid-Morning Drone Flights Give the Most Accurate Cattle Counts | Syrax",
     "Long shadows hide cattle. Here's why Syrax schedules counting flights mid-morning, and how timing affects drone cattle counts.",
     ["When you count cattle from the air, light matters as much as the camera. Early and late in the day, the sun sits low and trees throw long shadows across the paddock. Cattle resting in that shade are hard to see, and a count taken then will often come up short.",
      "By mid-morning, the sun is higher and shadows are shorter. More of the paddock is in clear light, and animals under trees are easier to pick out. That's why Syrax schedules counting flights for mid-morning by default.",
      "Timing is only part of it. Flying the same route at the same time every day means each count is taken in similar conditions, so today's number compares like with like against yesterday's. When a paddock comes up short, you know it's worth a look rather than a quirk of the light.",
      "Every report also includes the photo with every animal marked. If a count looks off, you can check it yourself before anyone gets in the ute."]),
    ("ArticleCountCost.dc.html", "Drone counts vs mustering: what a stock count really costs", "Costs", "flyover", "center 60%",
     "Drone Cattle Counts vs Mustering: The Real Cost of a Stock Count | Syrax",
     "A traditional stock count takes people, fuel and days. Here's how drone counting changes the cost of knowing what's on hand.",
     ["A traditional stock count means mustering, yarding and counting through a race, or driving every paddock and estimating. Either way it takes people, fuel and days, and the number is out of date the moment you finish.",
      "Researchers have measured the difference. In a study of drone-supported livestock audits, drones and counting software cut the time to take inventory at one ranch from 631 hours to 19 (University of Georgia, Terry College of Business).",
      "There's also the cost you don't see. Mustering takes cattle off feed and puts stress on the herd. A count from the air leaves the herd where it is.",
      "And because a docked drone counts every day, you're not paying for one big count a year. You have a current number whenever a buyer, accountant or lender asks."]),
    ("ArticleDroneInABox.dc.html", "How a drone-in-a-box works on a cattle property", "Technology", "dock", "62% center",
     "How a Drone-in-a-Box Works on a Cattle Property | Syrax",
     "A plain-English guide to drone docks for graziers: what the dock does, how flights are scheduled and what your property needs.",
     ["A drone-in-a-box is exactly what it sounds like: a weatherproof dock that lives on your property and houses a drone. The dock opens, launches the drone, lands it again and charges it, all without anyone on site.",
      "Flights are scheduled. You set a time once and the drone flies a mapped route on its own, covering paddocks, troughs, bunks and fence lines, then returns to the dock to charge.",
      "The dock needs power and an internet connection, either mobile or satellite. It also needs a spot with open ground and a clear view of the sky. Finding that spot is the first thing we do in a property assessment.",
      "The hardware collects the images. Syrax is the part that turns them into answers: a head count by paddock, the troughs that are low, the fence that's down, sent to your phone."]),
]
res_cards = "".join(t(f'''<a href="{f}" style="display: block; text-decoration: none; color: #0B0B0B; background: #FFFFFF; border: 1px solid #DDD9D0; border-radius: 8px; overflow: hidden">
<div style="aspect-ratio: 16 / 9; background: #3A3426"><img src="{IMG[img]}" alt="" style="width: 100%; height: 100%; object-fit: cover; object-position: {pos}; display: block"></div>
<div style="padding: 24px"><span style="font-size: 13px; font-weight: 600; color: #8A6D12">{e(cat)}</span><span style="display: block; margin-top: 8px; %H3%">{e(title)}</span><span style="display: block; margin-top: 16px; font-size: 15px; font-weight: 600">Read article</span></div>
</a>''') for f, title, cat, img, pos, *_ in ARTICLES)
PAGES.append(page("Resources.dc.html",
    "Resources | Drone Cattle Monitoring Guides for Australian Graziers | Syrax",
    "Practical guides on drone cattle counting, drone docks and remote property checks for Australian graziers.",
    "Resources.dc.html",
    hero("Resources.", "Practical guides on drone monitoring for Australian graziers.", crumb="Resources")
    + section(t(f'<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px">{res_cards}</div>'), top=80)
    + cta(), 2600))

for f, title, cat, img, pos, ttag, desc, paras in ARTICLES:
    others = [(a[0], a[1], a[2]) for a in ARTICLES if a[0] != f]
    body = t(f'''<article>
<section style="background: #0B0B0B; color: #F2F0EA"><div style="max-width: 820px; margin: 0 auto; padding: 72px 32px 72px">
<nav aria-label="Breadcrumb" style="font-size: 14px; color: #8F8B82; margin-bottom: 28px"><a href="Main.dc.html" style="color: #A9A59B; text-decoration: none">Home</a> <span aria-hidden="true">/</span> <a href="Resources.dc.html" style="color: #A9A59B; text-decoration: none">Resources</a></nav>
<span style="font-size: 14px; font-weight: 600; color: {{{{accent}}}}">{e(cat)}</span>
<h1 style="%H1%; font-size: clamp(2.2rem, 4vw, 3.4rem); margin-top: 12px">{e(title)}</h1>
</div></section>
<div style="max-width: 1000px; margin: -1px auto 0; padding: 0 32px"><div style="aspect-ratio: 16 / 8; border-radius: 0 0 8px 8px; overflow: hidden; background: #3A3426"><img src="{IMG[img]}" alt="" style="width: 100%; height: 100%; object-fit: cover; object-position: {pos}; display: block"></div></div>
<div style="max-width: 720px; margin: 0 auto; padding: 48px 32px 0">
{"".join(f'<p style="margin: 0 0 22px; font-size: 18px; line-height: 1.75; color: #2E2D2A">{e(p)}</p>' for p in paras)}
</div>
</article>''')
    rel = "".join(t(f'<a href="{h}" style="display: block; text-decoration: none; color: #0B0B0B; background: #FFFFFF; border: 1px solid #DDD9D0; border-radius: 8px; padding: 24px"><span style="font-size: 13px; font-weight: 600; color: #8A6D12">{e(c)}</span><span style="display: block; margin-top: 6px; %H3%; font-size: 18px">{e(tt)}</span></a>') for h, tt, c in others)
    body += section(h2("Keep reading") + t(f'<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-top: 32px">{rel}</div>'), top=64)
    body += cta()
    PAGES.append(page(f, ttag, desc, "Resources.dc.html", body, 2900))

# ================= Site map artboard (planning, not a web page) =================
SEO = [
    ("Home", "/", "Main.dc.html", "Syrax | Automated Drone Cattle Counting for Australian Properties", "drone cattle counting Australia"),
    ("Cattle counting", "/cattle-counting", "CattleCounting.dc.html", "Drone Cattle Counting | Daily Automated Head Counts | Syrax", "drone cattle counting, automated head count"),
    ("Water and feed", "/water-and-feed-monitoring", "WaterFeed.dc.html", "Remote Water Trough and Feed Bunk Monitoring by Drone | Syrax", "water trough monitoring, feed bunk monitoring"),
    ("Fences and welfare", "/fence-and-welfare-checks", "FenceWelfare.dc.html", "Drone Fence Line Checks and Livestock Welfare Monitoring | Syrax", "drone fence checks, livestock welfare monitoring"),
    ("How it works", "/how-it-works", "HowItWorks.dc.html", "How Syrax Works | Automated Drone-in-a-Box for Cattle Properties", "drone in a box farm, drone dock cattle"),
    ("Who it's for", "/who-its-for", "WhoItsFor.dc.html", "Who Syrax Is For | Graziers, Station Managers and Agistment Owners", "remote livestock monitoring, agistment stock check"),
    ("About", "/about", "About.dc.html", "About Syrax Solutions | Australian Drone Herd Monitoring", "Syrax Solutions"),
    ("FAQ", "/faq", "FAQ.dc.html", "Drone Cattle Monitoring FAQ | Syrax", "drone cattle monitoring questions"),
    ("Contact", "/contact", "Contact.dc.html", "Contact Syrax | Get Drone Cattle Monitoring on Your Property", "drone cattle monitoring quote"),
    ("Resources", "/resources", "Resources.dc.html", "Resources | Drone Cattle Monitoring Guides | Syrax", "cattle monitoring guides"),
    ("Article", "/resources/mid-morning-cattle-counts", "ArticleMidMorning.dc.html", "Why Mid-Morning Drone Flights Give the Most Accurate Cattle Counts", "best time to count cattle with a drone"),
    ("Article", "/resources/drone-count-vs-mustering", "ArticleCountCost.dc.html", "Drone Cattle Counts vs Mustering: The Real Cost of a Stock Count", "cost of mustering, stock count cost"),
    ("Article", "/resources/drone-in-a-box-cattle", "ArticleDroneInABox.dc.html", "How a Drone-in-a-Box Works on a Cattle Property", "drone in a box agriculture"),
]
rows = "".join(f'<tr><td style="padding: 12px 16px 12px 0; border-bottom: 1px solid #ECEAE4; font-weight: 600"><a href="{f}">{e(n)}</a></td><td style="padding: 12px 16px 12px 0; border-bottom: 1px solid #ECEAE4; font-family: ui-monospace, Menlo, monospace; font-size: 14px">{e(u)}</td><td style="padding: 12px 16px 12px 0; border-bottom: 1px solid #ECEAE4">{e(ti)}</td><td style="padding: 12px 0; border-bottom: 1px solid #ECEAE4; color: #55534D">{e(k)}</td></tr>' for n, u, f, ti, k in SEO)
tree = t('''<div style="display: flex; flex-direction: column; align-items: center; gap: 0">
<div style="background: #0B0B0B; color: #F2F0EA; border-radius: 8px; padding: 14px 28px; font-weight: 600">Home</div>
<div style="width: 1px; height: 28px; background: #0B0B0B"></div>
<div style="width: 92%; border-top: 1px solid #0B0B0B"></div>
<div style="display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 16px; width: 100%; margin-top: 0">
''' + "".join(f'<div style="display: flex; flex-direction: column; align-items: center"><div style="width: 1px; height: 24px; background: #0B0B0B"></div><div style="background: #FFFFFF; border: 1px solid #0B0B0B; border-radius: 8px; padding: 14px 16px; width: 100%; box-sizing: border-box"><p style="margin: 0; font-weight: 600">{e(g)}</p>' + "".join(f'<p style="margin: 6px 0 0; font-size: 14px; color: #55534D">{e(x)}</p>' for x in items) + '</div></div>' for g, items in [
    ("Product", ["Cattle counting", "Water and feed", "Fences and welfare"]),
    ("How it works", ["Dock, drone, software", "Setup steps"]),
    ("Who it's for", ["Owner-operators", "Managers", "Agistment", "Multi-property"]),
    ("Resources", ["Mid-morning counts", "Drone vs mustering", "Drone-in-a-box"]),
    ("Company", ["About", "FAQ", "Contact"])]) + '</div></div>')
sitemap = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Syrax site map and SEO plan</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
{HELMET}
<div style="width: 1440px; min-height: 1500px; box-sizing: border-box; padding: 72px 80px; background: #F7F6F3; color: #0B0B0B; font-family: Inter, system-ui, sans-serif">
<h1 style="margin: 0; font-family: 'Inter Tight', Inter, sans-serif; font-weight: 600; font-size: 44px; letter-spacing: -0.02em">Syrax site map and SEO plan</h1>
<p style="margin: 12px 0 48px; font-size: 18px; color: #55534D">13 pages. Every page links to the contact page. Product pages cross-link to each other.</p>
{tree}
<h2 style="margin: 64px 0 16px; font-family: 'Inter Tight', Inter, sans-serif; font-weight: 600; font-size: 28px">Pages, URLs and target searches</h2>
<table style="width: 100%; border-collapse: collapse; font-size: 15px; text-align: left">
<thead><tr><th scope="col" style="padding: 10px 16px 10px 0; border-bottom: 1px solid #0B0B0B">Page</th><th scope="col" style="padding: 10px 16px 10px 0; border-bottom: 1px solid #0B0B0B">URL</th><th scope="col" style="padding: 10px 16px 10px 0; border-bottom: 1px solid #0B0B0B">Title tag</th><th scope="col" style="padding: 10px 0; border-bottom: 1px solid #0B0B0B">Target search</th></tr></thead>
<tbody>{rows}</tbody>
</table>
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":1440,"height":1500}}}}'>
class Component extends DCLogic {{
  renderVals() {{ return {{}}; }}
}}
</script>
</body>
</html>
'''
open(os.path.join(OUT, "SiteMap.dc.html"), "w").write(sitemap)

json.dump(PAGES, open("/home/claude/syrax/pages.json", "w"))
print(len(PAGES), "pages")

# shared chrome for the home page build
open("/home/claude/syrax/header_main.html", "w").write(header("Main.dc.html"))
open("/home/claude/syrax/footer_shared.html", "w").write(footer())
