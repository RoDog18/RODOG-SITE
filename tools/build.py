# Builds the RoDog site from plugins.py into the site folder given as argv[1].
import hashlib, html, os, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
from plugins import PLUGINS, SERIES, EFFECTS

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
<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}style.css?v={ver}">
</head>
<body>
<header class="top"><div class="wrap"><nav>
  <a class="logo" href="{up}index.html"><img src="{up}images/rodog-logo.png" alt="RoDog"></a>
  <ul>
    <li><a href="{up}index.html#plugins">Plugins</a></li>
    <li><a href="{up}index.html#download">Download</a></li>
    <li><a class="cart" href="#" aria-disabled="true" title="Shop coming soon">Cart (0)</a></li>
  </ul>
</nav></div></header>
"""

def foot(depth):
    up = "../" * depth
    return f"""<footer><div class="wrap">
  <img src="{up}images/rodog-logo.png" alt="RoDog">
  <span>© 2026 RoDog</span>
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

def card(p):
    return f"""      <a class="pcard" href="plugins/{p['slug']}.html" data-series="{p['series']}">
        <div class="pmedia">{media(p, 0)}</div>
        <div class="pbody">
          <div class="pmeta"><span class="badge s-{p['series']}">{e(series_name[p['series']])}</span><span>{e(p['type'])}</span></div>
          <h3 class="display">{e(p['name'])}</h3>
          <p>{e(p['tag'])}</p>
        </div>
      </a>
"""

def index():
    tabs = '<button class="tab on" data-tab="all">All Plugins</button>' + "".join(
        f'<button class="tab" data-tab="{k}">{e(n)}</button>' for k, n, _ in SERIES)
    blurbs = "".join(f'<p class="blurb" data-blurb="{k}" hidden>{e(d)}</p>' for k, _, d in SERIES)
    by_effect = ""
    for k, n in EFFECTS:
        group = [p for p in PLUGINS if p["effect"] == k]
        if group:
            by_effect += f'    <h3 class="cat">{e(n)}</h3>\n    <div class="pgrid">\n' + "".join(card(p) for p in group) + "    </div>\n"
    by_series = "".join(card(p) for p in PLUGINS)
    return head("RoDog Plugins", 0, "Audio plugins by RoDog. VST3 and AU for macOS and Windows.") + f"""
<main>
  <div class="stage" aria-hidden="true">
    <div class="stage-in wrap">
      <img class="biglogo" src="images/rodog-logo.png" alt="">
      <img class="herodog" src="images/dog-cutout.png" alt="">
    </div>
  </div>
  <section class="hero">
    <div class="wrap">
      <h1 class="sr">RoDog</h1>
      <p class="lead">Audio plugins for producers, mix engineers, sound designers and guitarists. Install and update them all with the RoDog Product Manager.</p>
    </div>
  </section>

  <section id="plugins"><div class="wrap">
    <div class="tabs" role="tablist">{tabs}</div>
    {blurbs}
    <div id="by-effect">
{by_effect}    </div>
    <div id="by-series" class="pgrid" hidden>
{by_series}    </div>
  </div></section>

  <section id="download" class="manager"><div class="wrap">
    <div>
      <h2 class="display">RoDog Product Manager</h2>
      <p class="sub">One app to install, update and remove every RoDog plugin.</p>
      <ol>
        <li>Download the Product Manager for your computer.</li>
        <li>Open it and pick the plugins you want, or install them all.</li>
        <li>Restart your DAW. In Logic, look under Audio Units → RoDog.</li>
      </ol>
      <div class="actions">
        <a class="btn" href="#">Download for Mac</a>
        <a class="btn" href="#">Download for Windows</a>
      </div>
    </div>
  </div></section>
</main>
""" + foot(0)

def plugin_page(p, i):
    up = "../"
    shots = p.get("shots", [])
    gallery_imgs = [f"images/plugins/{p['slug']}/{s}" for s in shots] + [f"images/plugins/{p['slug']}/{a}" for a in p["art"]]
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
            m = '<div class="vslot"><span>Picture coming soon</span></div>'
        feats += f"""    <div class="feature{' flip' if n % 2 else ''}">
      <div class="ftext"><h3 class="display">{e(title)}</h3><p>{e(text)}</p></div>
      <div class="fmedia">{m}</div>
    </div>
"""
    prev_p, next_p = PLUGINS[i - 1], PLUGINS[(i + 1) % len(PLUGINS)]
    same = [q for q in PLUGINS if q["series"] == p["series"] and q is not p][:3]
    related = "".join(card(q).replace('href="plugins/', 'href="').replace('src="images/', 'src="../images/') for q in same)
    return head(f"{p['name']} by RoDog", 1, p["tag"]) + f"""
<main class="product">
  <section class="phero"><div class="wrap">
    <div class="pmain">{media(p, 1, " big")}</div>
    <div class="pinfo">
      <a class="back" href="{up}index.html#plugins">← All plugins</a>
      <div class="pmeta"><span class="badge s-{p['series']}">{e(series_name[p['series']])}</span><span>{e(p['type'])}</span></div>
      <h1 class="display">{e(p['name'])}</h1>
      <p class="lead">{e(p['tag'])}</p>
      <div class="buy">
        <div class="price">Price coming soon</div>
        <button class="btn" disabled>Add to cart</button>
      </div>
      <p class="note">Installs through the <a href="{up}index.html#download">RoDog Product Manager</a>. VST3 &amp; AU, macOS &amp; Windows.</p>
    </div>
  </div></section>

  <section class="overview"><div class="wrap">
    <div class="vslot wide"><span class="play">▶</span><span>{e(p['name'])} walkthrough video coming soon</span></div>
  </div></section>

  <section class="features"><div class="wrap">
    <h2 class="display">Features</h2>
{feats}  </div></section>
""" + (f"""
  <section class="gallery"><div class="wrap">
    <h2 class="display">Pictures</h2>
    <div class="gimgs">{gallery}</div>
  </div></section>
""" if gallery else "") + (f"""
  <section class="related"><div class="wrap">
    <h2 class="display">More from the {e(series_name[p['series']])}</h2>
    <div class="pgrid">
{related}    </div>
  </div></section>
""" if related else "") + f"""
  <nav class="pnav wrap">
    <a href="{prev_p['slug']}.html">← {e(prev_p['name'])}</a>
    <a href="{next_p['slug']}.html">{e(next_p['name'])} →</a>
  </nav>
</main>
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
print("built", len(PLUGINS), "plugin pages")
