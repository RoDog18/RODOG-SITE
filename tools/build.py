# Builds the RoDog site from plugins.py into the site folder given as argv[1].
import hashlib, html, os, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
import plugins as catalogue
from plugins import PLUGINS, SERIES, EFFECTS
KENNEL = getattr(catalogue, "KENNEL_DOWNLOADS", {})
from legal import PAGES as LEGAL

out = sys.argv[1]
series_name = {k: n for k, n, _ in SERIES}
# a version tag on style.css / site.js so browsers fetch the new files after every change
ver = hashlib.md5(b"".join(open(os.path.join(os.path.dirname(__file__), f), "rb").read() for f in ("style.css", "site.js"))).hexdigest()[:8]
e = html.escape

def head(title, depth, desc):
    up = "../" * depth
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="icon" href="{up}images/rodog-logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600;700&family=Big+Shoulders+Display:wght@800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}style.css?v={ver}">
</head>
<body>
<header class="top"><div class="wrap"><nav class="bar" aria-label="Main">
  <a class="logo" href="{up}index.html"><img src="{up}images/rodog-logo.png" alt="The Dog House by RoDog Audio"></a>
  <ul>
    <li class="plugins-link"><a href="{up}index.html#plugins">Plugins</a></li>
    <li><span class="cart" aria-disabled="true" title="The shop opens at launch">Cart (0)</span></li>
    <li><a class="btn" href="{up}index.html#download">Get The Kennel</a></li>
  </ul>
</nav></div></header>
"""

def foot(depth):
    up = "../" * depth
    return f"""<footer><div class="wrap">
  <img src="{up}images/rodog-logo.png" alt="RoDog Audio">
  <ul class="flinks">""" + "".join(f'<li><a href="{up}{lp["slug"]}.html">{lp["nav"]}</a></li>' for lp in LEGAL) + f"""</ul>
  <span>© 2026 RoDog Audio</span>
</div></footer>
<script src="{up}site.js?v={ver}"></script>
</body>
</html>
"""

def media(p, depth, extra=""):
    """Card / hero picture: a screenshot if there is one, else the display art, else a lettered tile."""
    up = "../" * depth
    shots = p.get("shots", [])
    if shots:
        return f'<img class="shot{extra}" src="{up}images/plugins/{p["slug"]}/{shots[0]}" alt="{e(p["name"])} plugin">'
    if p["art"] and depth:
        return f'<img class="art{extra}" src="{up}images/plugins/{p["slug"]}/{p["art"][0]}" alt="{e(p["name"])} display art">'
    return f'<div class="tile{extra}"><span>{e(p["name"])}</span></div>'

def wname(n):
    """A plug-in name with line-break chances after each hyphen (DAW names like DH-Surgeon-ResonanceSuppressor)."""
    return e(n).replace("-", "-<wbr>")

def kind(p):
    return f'<p class="pkind"><span class="sname">{e(series_name[p["series"]])}</span><span>{e(p["type"])}</span></p>'

def card(p):
    return f"""      <a class="pcard s-{p['series']}" href="plugins/{p['slug']}.html" data-series="{p['series']}">
        <div class="pmedia">{media(p, 0)}</div>
        <div class="pbody">
          <h3>{wname(p['name'])}</h3>
          {kind(p)}
          <p class="ptag">{e(p['tag'])}</p>
        </div>
      </a>
"""

def kennel_buttons():
    out = []
    for key, label in (("mac", "Download for Mac"), ("windows", "Download for Windows")):
        url = KENNEL.get(key, "")
        out.append(f'<a class="btn" href="{e(url)}">{label}</a>' if url else f'<span class="btn" aria-disabled="true">{label}</span>')
    later = "" if all(KENNEL.get(k) for k in ("mac", "windows")) else '\n      <p class="later">The download links go live when The Kennel is released.</p>'
    return '<div class="actions">' + "".join(out) + "</div>" + later

def index():
    tabs = '<button class="tab" role="tab" aria-selected="true" data-tab="all">All Plugins</button>' + "".join(
        f'<button class="tab" role="tab" aria-selected="false" data-tab="{k}">{e(n)}</button>' for k, n, _ in SERIES)
    blurbs = "".join(f'<p class="blurb" data-blurb="{k}" hidden>{e(d)}</p>' for k, _, d in SERIES)
    by_effect = ""
    for k, n in EFFECTS:
        group = [p for p in PLUGINS if p["effect"] == k]
        if group:
            by_effect += f'    <h3 class="cat">{e(n)} <span>{len(group)}</span></h3>\n    <div class="pgrid">\n' + "".join(card(p) for p in group) + "    </div>\n"
    by_series = "".join(card(p) for p in PLUGINS)
    return head("The Dog House | RoDog Audio plugins", 0, "The Dog House: audio plugins by RoDog Audio. VST3 and AU for macOS and Windows.") + f"""
<main>
  <div class="stage" aria-hidden="true">
    <div class="stage-in wrap">
      <img class="biglogo" src="images/rodog-logo.png" alt="">
      <img class="herodog" src="images/dog-cutout.png" alt="">
    </div>
  </div>
  <section class="hero">
    <div class="wrap">
      <h1>The Dog House</h1>
      <p class="lead">Audio plugins for producers, mix engineers, sound designers and musicians.</p>
      <div class="actions">
        <a class="btn" href="#download">Get The Kennel</a>
        <a class="btn quiet" href="#plugins">Browse the plugins</a>
      </div>
    </div>
  </section>

  <section id="plugins"><div class="wrap">
    <div class="shelfhead"><h2>The plugins</h2><p>{len(PLUGINS)} plugins, all installed and updated through The Kennel.</p></div>
    <div class="tabbar"><div class="tabs" role="tablist" aria-label="Series">{tabs}</div></div>
    {blurbs}
    <div id="by-effect">
{by_effect}    </div>
    <div id="by-series" class="pgrid" hidden>
{by_series}    </div>
  </div></section>

  <section id="download" class="manager"><div class="wrap">
    <img class="sleeppup" src="images/dogs/pup-20210214_104640.png" alt="" aria-hidden="true">
    <img class="kennelpups" src="images/dogs/pup-20210218_090834.png" alt="" aria-hidden="true">
    <div class="kennel">
      <h2>The Kennel</h2>
      <p class="sub">One app to install, update and remove every RoDog plugin.</p>
      <ol class="steps">
        <li>Download The Kennel for your computer.</li>
        <li>Open it and pick the plugins you want, or install them all.</li>
        <li>Restart your DAW. In Logic, look under Audio Units, then RoDog.</li>
      </ol>
      """ + kennel_buttons() + """
    </div>
  </div></section>
""" + peek("pup-20210210_181158.png", 0) + """</main>
""" + foot(0)

# cut-out dog photos (images/dogs) for the inner pages, taken in turn so neighbouring pages differ
STANDING = ["dog-37091.png", "dog-37053.png", "dog-37066.png", "dog-37063.png", "dog-37070.png", "dog-37052.png", "dog-37061.png"]
# Puppy photos: one peeks up over the footer on every page.
PUPS = ["pup-20210210_181146.png", "pup-20210212_121112.png", "pup-20210210_181159.png", "pup-20210212_121116.png",
        "pup-20210210_181221.png", "pup-20210212_121136.png", "pup-20210212_121119.png", "pup-20210210_181149.png",
        "pup-20210212_121124.png", "pup-20210219_161330.png", "pup-20210210_181223.png", "pup-20210212_121126.png",
        "pup-20210214_104746.png", "pup-20210214_104607.png"]
STANDING[2:2] = ["pup-20210214_104607.png"]
STANDING[5:5] = ["pup-20210214_104746.png"]
def peek(src, depth):
    return f'  <img class="peekpup" src="{"../" * depth}images/dogs/{src}" alt="" aria-hidden="true">\n'
LEGAL_DOGS = {"support": "dog-37091.png", "privacy": "dog-37078.png", "licence": "dog-37061.png", "refunds": "dog-37075.png"}

def backdog(src, depth, cls="backdog"):
    wall = '<div class="woodstage" aria-hidden="true"></div>\n' if cls == "sidestage" else ""
    return wall + f'<img class="{cls}" src="{"../" * depth}images/dogs/{src}" alt="" aria-hidden="true">\n'

def plugin_page(p, i):
    up = "../"
    shots = p.get("shots", [])
    gallery_imgs = [f"images/plugins/{p['slug']}/{s}" for s in shots] + [f"images/plugins/{p['slug']}/{a}" for a in p["art"]]
    still = (f"images/plugins/{p['slug']}/{shots[1]}" if len(shots) > 1 else
             f"images/plugins/{p['slug']}/{p['art'][0]}" if p["art"] else None)
    if p.get("video"):
        watch = f'<div class="watch"><video controls preload="metadata" src="{up}{e(p["video"])}"></video></div>'
    elif still:
        watch = f'<div class="watch"><img src="{up}{still}" alt="{e(p["name"])}" loading="lazy"><span class="soon">Walkthrough video coming soon</span></div>'
    else:
        watch = ""
    price = (f'<div class="price">{e(p["price"])}</div><button class="btn" disabled>Add to cart</button>' if p.get("price")
             else '<div class="price">Price<small>Set at launch</small></div><button class="btn" disabled>Add to cart</button>')
    gallery = "".join(f'<img src="{up}{g}" alt="{e(p["name"])} picture {n+1}" loading="lazy">' for n, g in enumerate(gallery_imgs[1:]))
    feats = ""
    for n, f in enumerate(p["features"]):
        title, text = f[0], f[1]
        pics = shots or p["art"]
        pick = f[2] if len(f) > 2 else None
        if not pick and pics:
            # a screenshot whose name shares a word with the feature title (e.g. "advanced"), else take them in turn
            words = [w.lower().strip(",") for w in title.split() if len(w) > 3]
            pick = next((x for x in pics for w in words if w in x.lower()), pics[n % len(pics)])
        if pick:
            m = f'<img class="fpic" src="{up}images/plugins/{p["slug"]}/{pick}" alt="{e(p["name"])}: {e(title)}" loading="lazy">'
        else:
            m = ""
        feats += f"""    <div class="feature{' flip' if n % 2 else ''}">
      <div class="ftext"><h3>{e(title)}</h3><p>{e(text)}</p></div>
      <div class="fmedia">{m}</div>
    </div>
"""
    prev_p, next_p = PLUGINS[i - 1], PLUGINS[(i + 1) % len(PLUGINS)]
    same = [q for q in PLUGINS if q["series"] == p["series"] and q is not p][:3]
    related = "".join(card(q).replace('href="plugins/', 'href="').replace('src="images/', 'src="../images/') for q in same)
    return head(f"{p['name']} | The Dog House by RoDog Audio", 1, p["tag"]) + f"""
""" + backdog(STANDING[i % len(STANDING)], 1, "sidestage") + f"""<main class="product">
  <section class="phero"><div class="wrap">
    <div class="pmain">{media(p, 1, " big")}</div>
    <div class="pinfo s-{p['series']}">
      <a class="back" href="{up}index.html#plugins">All plugins</a>
      {kind(p)}
      <h1>{wname(p['name'])}</h1>
      <p class="lead">{e(p['tag'])}</p>
      <div class="buy">{price}</div>
      <p class="note">Installs through <a href="{up}index.html#download">The Kennel</a>. VST3 and AU, for macOS and Windows.</p>
    </div>
  </div></section>

""" + (f"""  <section class="overview"><div class="wrap">
    {watch}
  </div></section>
""" if watch else "") + f"""
  <section class="features"><div class="wrap">
    <h2>Features</h2>
{feats}  </div></section>
""" + (f"""
  <section class="gallery"><div class="wrap">
    <h2>Pictures</h2>
    <div class="gimgs">{gallery}</div>
  </div></section>
""" if gallery else "") + (f"""
  <section class="related"><div class="wrap">
    <h2>More from the {e(series_name[p['series']])}</h2>
    <div class="pgrid">
{related}    </div>
  </div></section>
""" if related else "") + f"""
  <nav class="pnav wrap" aria-label="Other plugins">
    <a href="{prev_p['slug']}.html"><span>Previous</span>{wname(prev_p['name'])}</a>
    <a class="next" href="{next_p['slug']}.html"><span>Next</span>{wname(next_p['name'])}</a>
  </nav>
""" + peek(PUPS[i % len(PUPS)], 1) + """</main>
""" + foot(1)

# screenshots copied in by assemble.sh are named shot-*.png; main view first
for p in PLUGINS:
    d = os.path.join(out, "images", "plugins", p["slug"])
    names = sorted(f for f in os.listdir(d) if f.startswith("shot-")) if os.path.isdir(d) else []
    names.sort(key=lambda f: (not f.endswith("-main.jpg"), f))
    p["shots"] = names

os.makedirs(os.path.join(out, "plugins"), exist_ok=True)
open(os.path.join(out, "index.html"), "w").write(index())
for i, p in enumerate(PLUGINS):
    open(os.path.join(out, "plugins", p["slug"] + ".html"), "w").write(plugin_page(p, i))
def legal_page(lp):
    return head(f"{lp['title']} | The Dog House by RoDog Audio", 0, f"RoDog Audio {lp['title'].lower()}.") + f"""
""" + backdog(LEGAL_DOGS.get(lp["slug"], "dog-37091.png"), 0, "sidestage") + f"""<main class="legal"><div class="wrap">
  <a class="back" href="index.html">Home</a>
  <h1>{e(lp['title'])}</h1>
{lp['body']}
</div>
""" + peek(PUPS[(LEGAL.index(lp) + 5) % len(PUPS)], 0) + """</main>
""" + foot(0)

for lp in LEGAL:
    open(os.path.join(out, lp["slug"] + ".html"), "w").write(legal_page(lp))
print("built", len(PLUGINS), "plugin pages and", len(LEGAL), "policy pages")
