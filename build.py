#!/usr/bin/env python3
"""Builds the Product Knowledge site from videos.json.

Add a video:
  1. Make folder NN-slug/ with NN-slug.mp4 (under 100 MB) and poster.jpg.
  2. Add {"slug", "title", "length"} to videos.json.
  3. python3 build.py, then commit and push.
"""
import html, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = "https://dwightrfm.github.io/product-knowledge/"
SITE = "Product Knowledge"
DESC = "Training videos on the plans we use. For licensed professionals only. Not for clients."
FOOT = "Internal training for licensed professionals only. Not for clients. Plans and rates change often; check current details. Not financial advice."

vids = json.loads((ROOT / "videos.json").read_text())
hub_head = (ROOT / "src/hub_head.html").read_text()
page_head = (ROOT / "src/page_head.html").read_text()
e = html.escape


def meta(title, desc, url, img, video=None):
    m = [f'<meta charset="utf-8">', '<meta name="viewport" content="width=device-width,initial-scale=1">',
         '<meta name="robots" content="noindex,nofollow">', f"<title>{e(title)}</title>",
         f'<meta name="description" content="{e(desc)}">',
         f'<meta property="og:type" content="{"video.other" if video else "website"}">',
         f'<meta property="og:title" content="{e(title)}">', f'<meta property="og:description" content="{e(desc)}">',
         f'<meta property="og:url" content="{url}">', f'<meta property="og:image" content="{img}">',
         '<meta property="og:image:width" content="1080"><meta property="og:image:height" content="1920">']
    if video:
        m += [f'<meta property="og:video" content="{video}">', f'<meta property="og:video:secure_url" content="{video}">',
              '<meta property="og:video:type" content="video/mp4">',
              '<meta property="og:video:width" content="1080"><meta property="og:video:height" content="1920">']
    m.append('<meta name="twitter:card" content="summary_large_image">')
    return "\n".join(m)


items = []
for v in vids:
    s, num = v["slug"], v["slug"].split("-")[0]
    url = f"{BASE}{s}/"
    items.append(
        f'<div class="item" id="v{num}">\n'
        f'<button class="vbtn" aria-expanded="false" onclick="toggle(this)"><span class="vnum">{num}</span>'
        f'<span class="vtitle">{e(v["title"])}</span><span class="vlen">{v["length"]}</span>'
        f'<span class="chev" aria-hidden="true"></span></button>\n'
        f'<div class="panel" hidden><video controls playsinline preload="none" poster="{s}/poster.jpg" data-src="{s}/{s}.mp4"></video>\n'
        f'<button class="btn" onclick="copyLink(\'{url}\',this)">Copy link to this video</button></div></div>')

    desc = f"{SITE} #{num}: {v['title']}. {v['length']} long. Licensed professionals only."
    page = (f'<!doctype html><html lang="en"><head>{meta(v["title"] + " | " + SITE, desc, url, url + "poster.jpg", url + s + ".mp4")}\n'
            f'{page_head}</head><body><div class="wrap"><div class="player"><a class="back" href="../">&larr; All videos</a>\n'
            f'<div class="eyebrow"><span class="dot"></span>{SITE} #{num}</div>\n'
            f'<h2>{e(v["title"])}</h2><div class="meta">{v["length"]}</div>\n'
            f'<video controls playsinline preload="metadata" poster="poster.jpg"><source src="{s}.mp4" type="video/mp4"></video>\n'
            f'<div class="row"><button class="btn" onclick="copyLink(\'{url}\',this)">Copy link</button><a class="btn" href="../">All videos</a></div>\n'
            f'<footer>{FOOT}</footer></div></div></body></html>\n')
    (ROOT / s / "index.html").write_text(page)

n = len(vids)
lead = f"{n} training video{'s' if n != 1 else ''} on the plans we use, for licensed professionals. Tap a title to watch it right here."
first = vids[0]["slug"]
hub = (f'<!doctype html><html lang="en"><head>{meta(SITE, DESC, BASE, BASE + first + "/poster.jpg")}\n{hub_head}</head>'
       f'<body><div class="wrap"><div class="eyebrow"><span class="dot"></span>{SITE}</div>\n'
       f'<h1>Product <em>Knowledge</em></h1>\n<p class="lead">{lead}</p>\n'
       f'<div class="list">{chr(10).join(items)}</div>\n<footer>{FOOT}</footer></div></body></html>\n')
(ROOT / "index.html").write_text(hub)
print(f"built {n} video(s)")
