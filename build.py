#!/usr/bin/env python3
"""Builds the Memorial Cemetery of St. John's Church site (cemetery.stjcsh.org, provisional).
Header, nav and footer live here ONCE so every page gets the same ones.
Run:  python3 build.py   (writes into ./memcem)
Anything wrapped in <mark class="confirm"> is unconfirmed and must be settled before launch."""
import os, html

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = HERE if os.path.isdir(os.path.join(HERE, "assets")) else os.path.join(HERE, "memcem")
BASE = "https://cemetery.stjcsh.org"          # provisional domain
NAME = "The Memorial Cemetery of St. John’s Church"
PHONE = "(516) 692-6748"; TEL = "+15166926748"
EMAIL = "cemetery@stjcsh.org"
ADDR = "1704 NY-25A, Laurel Hollow, NY 11791"
MAPS_LINK = "https://www.google.com/maps/search/?api=1&query=1704+NY-25A+Laurel+Hollow+NY+11791"
CREDIT_PHOTOS = "Photographs by David Almeida and Michael Fairchild, used with permission."
CREDIT_PLANS = ("Plans and drawings from the <em>St. John’s Church Memorial Cemetery Historic Landscape "
                "Management Guide</em> (April 2019) by Heritage Landscapes LLC for the St. John’s Memorial "
                "Cemetery Committee. Historic plans courtesy of the Olmsted Archives, Frederick Law Olmsted "
                "National Historic Site.")

def C(t):  # mark something unconfirmed
    return f'<mark class="confirm">{t}</mark>'

# (path, nav label, title, description)
NAV = [
 ("/history/", "History", None),
 ("/visit/", "Visit", None),
 ("/burial/", "Burial &amp; Memorials", None),
 ("/families/", "For Families", None),
 ("/care/", "Care &amp; Support", None),
 ("/contact/", "Contact", None),
]
HISTORY_SUB = [("/history/", "History of the Cemetery"), ("/olmsted-landscape/", "The Olmsted Landscape"), ("/maps/", "Maps &amp; Plans")]
HISTORY_PATHS = {p for p, _ in HISTORY_SUB}

def nav_html(cur):
    out = ['<nav id="site-nav" aria-label="Main"><ul>']
    for path, label, _ in NAV:
        if path == "/history/":
            out.append('<li class="has-dropdown">')
            hac = ' aria-current="page"' if cur == "/history/" else ""
            out.append(f'<a href="/history/"{hac}>History</a>')
            out.append('<button type="button" class="dropdown-toggle" aria-expanded="false" aria-controls="history-menu" aria-label="Open History submenu"><span aria-hidden="true">&#9662;</span></button>')
            out.append('<ul class="dropdown" id="history-menu">')
            for p, l in HISTORY_SUB:
                ac = ' aria-current="page"' if p == cur else ""
                out.append(f'<li><a href="{p}"{ac}>{l}</a></li>')
            out.append('</ul></li>')
        else:
            ac = ' aria-current="page"' if path == cur else ""
            out.append(f'<li><a href="{path}"{ac}>{label}</a></li>')
    out.append('</ul></nav>')
    return "\n".join(out)

FOOTER = f"""<footer><div class="wrap">
<div class="cols">
<div class="fbrand"><img src="/assets/logo-stacked-white.png" width="550" height="600" alt="{NAME}" loading="lazy">
<p>A historic Episcopal cemetery in Laurel Hollow, New York, founded in 1862 and shaped by the Olmsted Brothers.</p></div>
<div><h4>Explore</h4><ul>
<li><a href="/history/">History</a></li><li><a href="/olmsted-landscape/">The Olmsted Landscape</a></li><li><a href="/maps/">Maps &amp; Plans</a></li>
<li><a href="/visit/">Visit</a></li><li><a href="/burial/">Burial &amp; Memorials</a></li><li><a href="/families/">For Families</a></li><li><a href="/care/">Care &amp; Support</a></li></ul></div>
<div><h4>Contact</h4><p>{ADDR}<br><a href="tel:{TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
<p style="margin-top:1em"><a href="/contact/">Who to call &rarr;</a></p></div>
</div></div>
<div class="family"><div class="wrap">
<div class="row"><span class="lbl">St. John&rsquo;s Family of Websites</span>
<a href="https://stjcsh.org">St. John&rsquo;s Episcopal Church</a>
<a href="https://bluegreentheology.org">BlueGreen Theology</a>
<a href="https://concertsbythepond.org">Concerts by the Pond</a>
<a href="https://save-the-pond.org">Save the Pond</a></div>
<div class="fine"><span>&copy; 2026 The Memorial Cemetery of St. John&rsquo;s Church. {CREDIT_PHOTOS}</span><span>{ADDR}</span></div>
</div></div></footer>"""

def page(path, title, desc, body, hero=None, hero_h1=None, motto=None, og=None, jsonld=None, home=False):
    full_title = html.escape(f"{title} — {NAME}" if not home else NAME, quote=False)
    url = BASE + path
    ogimg = BASE + (og or "/assets/og-image.jpg")
    cur = path
    if hero:
        cls = "hero" if home else "hero subhero"
        h1 = hero_h1 or title
        if home:
            herohtml = (f'<div class="{cls}" style="background-image:url({hero})"><div class="wrap"><div class="hero-block">'
                '<p class="eyebrow">Laurel Hollow, New York &middot; Founded 1862</p>'
                '<h1>The Memorial Cemetery <em>of St.&nbsp;John&rsquo;s Church</em></h1>'
                f'<p class="motto">{motto}</p>'
                '<p class="hero-lede">A quiet, wooded burial ground, shaped by the Olmsted Brothers and cared for by the people of St.&nbsp;John&rsquo;s Episcopal Church.</p>'
                '<div class="hero-actions"><a class="pill solid" href="/visit/">Plan a Visit</a><a class="pill ghost" href="/history/">Our History</a></div>'
                '</div></div></div>')
        else:
            herohtml = f'<div class="{cls}" style="background-image:url({hero})"><div class="wrap"><h1>{h1}</h1></div></div>'
    else:
        herohtml = ""
    ld = f'<script type="application/ld+json">\n{jsonld}\n</script>' if jsonld else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{html.escape(desc, quote=True)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{html.escape(desc, quote=True)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{ogimg}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/assets/favicon-16.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta name="theme-color" content="#004687">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600&family=PT+Sans:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="siteheader{' solid' if not hero else ''}"><div class="masthead"><div class="wrap">
<a class="brand" href="/"><img src="/assets/logo-white.png" width="1632" height="441" alt="{NAME}, Laurel Hollow, New York"></a>
<button type="button" class="menu-toggle" aria-expanded="false" aria-controls="site-nav">Menu</button>
{nav_html(cur)}
</div></div></header>
{herohtml}
<main id="main">
{body}
</main>
{FOOTER}
<script src="/assets/nav.js"></script>
</body>
</html>
"""

def write(path, content):
    d = os.path.join(OUT, path.strip("/")) if path != "/" else OUT
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(content)

PAGES = []  # (path) for sitemap

# ------------------------------------------------------------------ HOME
jsonld = f"""{{
  "@context": "https://schema.org",
  "@type": "Cemetery",
  "name": "Memorial Cemetery of St. John's Church",
  "description": "A historic Episcopal cemetery in Laurel Hollow, New York, founded in 1862 and shaped by the Olmsted Brothers.",
  "url": "{BASE}/",
  "telephone": "+1-516-692-6748",
  "address": {{"@type": "PostalAddress", "streetAddress": "1704 NY-25A", "addressLocality": "Laurel Hollow", "addressRegion": "NY", "postalCode": "11791", "addressCountry": "US"}}
}}"""

home = f"""
<section><div class="wrap"><div class="split">
<div class="prose">
<p>The Memorial Cemetery of St. John&rsquo;s Church lies on a hill and valley of old trees, stone walls, and winding drives. In the early twentieth century the church asked the Olmsted Brothers, landscape architects from the family that designed Central Park, to shape its grounds, and many of the quiet family &ldquo;rooms&rdquo; they designed are still here today.</p>
<p>The cemetery is open to all visitors, whether you have come to remember someone you love or to learn about the history and the landscape. Burial plots are made available to members of St.&nbsp;John&rsquo;s Church and to the children of those already buried here.</p>
</div>
<figure><img src="/assets/img/olmsted-room-drive.jpg" alt="A winding drive and stone-edged room designed by the Olmsted Brothers" loading="lazy"><figcaption>A drive and room shaped by the Olmsted Brothers.</figcaption></figure>
</div></div></section>

<section class="warm"><div class="wrap">
<h2>Explore</h2>
<div class="grid">
<div class="card"><a class="card-link" href="/history/"><img src="/assets/img/jones-monuments.jpg" alt="Jones family monuments beneath a flowering dogwood" loading="lazy"><p class="k">History</p><p>From John Divine Jones&rsquo;s family burial ground in 1862 to the Olmsted plans of 1921.</p></a></div>
<div class="card"><a class="card-link" href="/olmsted-landscape/"><img src="/assets/img/bench-room.jpg" alt="A stone-walled Olmsted room with a bench and slate markers" loading="lazy"><p class="k">The Olmsted Landscape</p><p>Woodland &ldquo;rooms,&rdquo; stone steps, and a design meant to feel as if it had always been there.</p></a></div>
<div class="card"><a class="card-link" href="/maps/"><img src="/assets/maps/zones-olmsted-rooms.jpg" alt="Plan of the cemetery showing its eleven zones and Olmsted rooms" loading="lazy" style="object-position:25% 85%"><p class="k">Maps &amp; Plans</p><p>Historic plans, aerial photographs, and the layout of the grounds today.</p></a></div>
</div></div></section>

<section><div class="wrap">
<div class="split">
<div>
<h2>Visiting</h2>
<dl class="facts">
<dt>Address</dt><dd>{ADDR}</dd>
<dt>Telephone</dt><dd><a href="tel:{TEL}">{PHONE}</a></dd>
<dt>The grounds</dt><dd>Open during daylight hours, seven days a week.</dd>
<dt>Office</dt><dd>Monday&ndash;Friday 8:00&ndash;4:00; Saturday 8:00&ndash;12:00</dd>
</dl>
<p style="margin-top:1.4em"><a class="button" href="/visit/">Plan your visit</a></p>
</div>
<figure><img src="/assets/img/chapel.jpg" alt="The cemetery chapel among flowering dogwoods" loading="lazy"><figcaption>The cemetery chapel, near the entrance.</figcaption></figure>
</div></div></section>

<section class="warm"><div class="wrap">
<div class="prose">
<h2>If you are here because someone has died</h2>
<p>We are so sorry for your loss. Please call the cemetery office at <a href="tel:{TEL}">{PHONE}</a>. We will help you with the arrangements, and we are glad to help you reach the clergy of St.&nbsp;John&rsquo;s as well. More about <a href="/burial/">burial and memorials</a>.</p>
</div></div></section>
"""
write("/", page("/", NAME, "A historic Episcopal cemetery in Laurel Hollow, New York, founded in 1862, with landscape design by the Olmsted Brothers. Visiting, history, maps, and burial information.",
    home, hero="/assets/img/gate.jpg", hero_h1=NAME, motto="Et Audierent Qui Vivent", jsonld=jsonld, home=True)); PAGES.append("/")

# ------------------------------------------------------------------ HISTORY
history = f"""
<section><div class="wrap"><div class="prose">
<p class="lede" style="max-width:none">A family burial ground that became a parish cemetery, and then a landscape worth preserving.</p>
</div></div></section>

<section><div class="wrap">
<h2>A timeline</h2>
<ul class="timeline">
<li><span class="yr">1862</span><div>John Divine Jones founded the cemetery on wooded, steep-sided land. He had meant it as a burial ground for his family; it became the cemetery for the people of St.&nbsp;John&rsquo;s Episcopal Church, replacing an earlier burying ground above the church. The first graves lay on the high ground in the northeast, near where the Jones family plot stands today.</div></li>
<li><span class="yr">By 1890</span><div>A small chapel stood near the Jones graves by the entrance.</div></li>
<li><span class="yr">1912</span><div>Robert and Henry De Forest bought about ten acres to the west, the parcel to the west that was later added to the cemetery.</div></li>
<li><span class="yr">1918</span><div>After fifty-six years of burials, St.&nbsp;John&rsquo;s turned to the Olmsted Brothers, the Brookline, Massachusetts landscape architects, for advice. A civil engineer, H.&thinsp;C. Harrington, first surveyed the grounds, about 34 acres at that time.</div></li>
<li><span class="yr">1921</span><div>The Olmsted Brothers&rsquo; Preliminary Plan set out the drives, paths, parks, and wooded edges that still shape the cemetery. Over the following decades the firm also designed individual plots for families.</div></li>
<li><span class="yr">1947&ndash;58</span><div>New sections were laid out on the slopes. The plots here are smaller, a change from the large family rooms of earlier years.</div></li>
<li><span class="yr">2018&ndash;19</span><div>The cemetery committee commissioned Heritage Landscapes, preservation landscape architects, to study the Olmsted record and recommend how to care for the grounds. They found the cemetery to be a significant historic landscape, potentially eligible for the National Register of Historic Places.</div></li>
</ul>
<p class="note" style="margin-top:1.6em"><strong>A note on dates.</strong> Historical sources differ slightly on some details, such as the exact years of the Olmsted firm&rsquo;s early work and the size of the grounds. We have given the dates we are most sure of and will refine them as our research continues.</p>
</div></section>

<section class="warm"><div class="wrap"><div class="split">
<div class="prose">
<h2>The Chapel and the Jones plot</h2>
<p>Near the entrance, the chapel and the Jones family graves are the oldest part of the cemetery. The Olmsted plan kept this area as a green, open setting for the chapel, bordered by the Jones lot, which is why the first sight of the cemetery is a clearing rather than a row of stones.</p>
<p>The people of St.&nbsp;John&rsquo;s still gather here to bury their dead, as they have for more than a century and a half.</p>
</div>
<figure><img src="/assets/img/jones-monuments.jpg" alt="The Jones family plot, with the large JONES monument and older upright stones" loading="lazy"><figcaption>The Jones family plot near the chapel.</figcaption></figure>
</div></div></section>

<section><div class="wrap"><div class="split">
<figure><img src="/assets/img/slate-markers.jpg" alt="Flat slate markers in a curved, stone-walled hollow in the woods" loading="lazy"><figcaption>Flat slate markers in a stone-walled hollow.</figcaption></figure>
<div class="prose">
<h2>How the cemetery grew</h2>
<p>The earliest graves were laid out in lines on the high plateau. When the Olmsted Brothers arrived, they followed the land instead. Drives bend with the hillside, paths follow the contours, and families could commission quiet, wooded plots set apart from their neighbors.</p>
<p>In the late 1940s and 1950s the cemetery added new sections with smaller plots. The mix you see today, grand family rooms beside simple rows of single graves, is part of its character.</p>
<p><a href="/olmsted-landscape/">Read about the Olmsted landscape &rarr;</a> &nbsp; <a href="/maps/">See the maps &rarr;</a></p>
</div></div></div></section>

<section class="warm"><div class="wrap"><div class="prose">
<h2>Further reading</h2>
<p>The Cultural Landscape Foundation has a page on the cemetery, with photographs: <a href="https://www.tclf.org/landscapes/memorial-cemetery">tclf.org/landscapes/memorial-cemetery</a>.</p>
</div></div></section>
"""
write("/history/", page("/history/", "History", "The history of the Memorial Cemetery of St. John's Church in Laurel Hollow, from its founding in 1862 by John Divine Jones to the Olmsted Brothers' plans of 1921.",
    history, hero="/assets/img/chapel.jpg", hero_h1="History")); PAGES.append("/history/")

# ------------------------------------------------------------------ OLMSTED LANDSCAPE
rooms = [
 ("Alfred P. Sloan Jr.", "1875&ndash;1966"), ("Otto Kahn", "1867&ndash;1934"), ("Walter Burr Jennings", "1858&ndash;1933"),
 ("Col. Henry Stimson", "1867&ndash;1950"), ("Benjamin Moore", "1886&ndash;1938"), ("Henry and Robert De Forest", ""),
 ("Mai (Mary) Rogers Coe, Coe Mausoleum", "1875&ndash;1924"), ("William John Matheson", "1856&ndash;1930"),
 ("Paul E. Gardner", "1888&ndash;1938"), ("John A. Garver", ""), ("F.&thinsp;H. Kalbfleisch", ""), ("Ray Morris", ""),
 ("James C. Ayer", ""), ("Oliver Campbell", ""), ("James A. Blair", ""), ("Fred A. Snow", ""), ("William Kennedy", ""),
 ("H.&thinsp;U. Harris", ""), ("Trawbridge", ""), ("Dr. James", ""), ("Nichols", ""), ("McKelvey", ""),
]
roomli = "\n".join(f"<li>{n}{' (' + d + ')' if d else ''}</li>" for n, d in rooms)
olmsted = f"""
<section><div class="wrap"><div class="split">
<div class="prose">
<p class="lede" style="max-width:none">A landscape designed to feel as though it had always been here.</p>
<p style="margin-top:1.2em">Frederick Law Olmsted co-designed Central Park; his sons and successors, the Olmsted Brothers, carried the family&rsquo;s idea of the <em>naturalistic</em> landscape into the twentieth century. For St.&nbsp;John&rsquo;s they drew a cemetery of curving drives, wooded edges, open lawns, and, for families who wanted them, private garden &ldquo;rooms.&rdquo;</p>
<p>The result is a place where one walks, rather than marches, from one quiet space to the next.</p>
</div>
<figure><img src="/assets/img/coe-mausoleum.jpg" alt="The Coe Mausoleum, a small white marble temple standing in a lawn clearing among rhododendrons and tall trees" loading="lazy"><figcaption>The Coe Mausoleum in its clearing.</figcaption></figure>
</div></div></section>

<section class="warm"><div class="wrap"><div class="split">
<figure><img src="/assets/img/bench-room.jpg" alt="An Olmsted room: a stone-walled garden space with a bench, slate markers, and a groundcover of periwinkle" loading="lazy"><figcaption>An Olmsted room, with its stone wall, bench, and groundcover.</figcaption></figure>
<div class="prose">
<h2>What is an &ldquo;Olmsted room&rdquo;?</h2>
<p>An Olmsted room is a family plot designed for its owners by the Olmsted firm. Each is set apart from its neighbors by a bank of evergreens and flowering shrubs, a low stone wall, or a change in grade, and each has its own steps, paths, and plantings: red cedar, white pine and hemlock; dogwoods; azaleas, rhododendrons, and mountain laurel; moss and low groundcover beneath. Some of the plants were moved from the families&rsquo; own estates.</p>
<p>More than twenty of these rooms were designed. Each of them is private to the family who owns it, and each belongs to the whole cemetery&rsquo;s character.</p>
</div></div></div></section>

<section><div class="wrap">
<h2>Four kinds of landscape</h2>
<p class="prose" style="max-width:64ch;margin-bottom:1.6em">The 2019 landscape guide describes the cemetery as four kinds of area. Each is cared for a little differently.</p>
<div class="areas">
<div class="area a1"><h3>Parks, reservations &amp; open space</h3><p>Wooded margins, the open lawn at the chapel, and the green valley. The Olmsted plan set these aside to screen the cemetery from the road and give visitors room to breathe. The cemetery staff care for them.</p></div>
<div class="area a2"><h3>Olmsted rooms</h3><p>The large family plots designed by the Olmsted firm. The families chose their designs; the cemetery cares for the grounds around them.</p></div>
<div class="area a3"><h3>Scatter gardens &amp; columbaria</h3><p>Places for cremated remains: a columbarium near the chapel and a scatter garden near East and Valley Avenues, designed to feel part of the landscape rather than apart from it.</p></div>
<div class="area a4"><h3>Small plot areas</h3><p>Rows of single and smaller family plots, arranged along curving paths and aisles.</p></div>
</div>
<p style="margin-top:1.6em"><a href="/maps/">See these areas on the map &rarr;</a></p>
</div></section>

<section class="warm"><div class="wrap">
<h2>The Olmsted rooms</h2>
<p class="prose" style="max-width:64ch">The 2019 guide lists the following families among the Olmsted rooms. Names and dates are as the guide gives them.</p>
<ul class="rooms">
{roomli}
</ul>
</div></section>
"""
write("/olmsted-landscape/", page("/olmsted-landscape/", "The Olmsted Landscape", "How the Olmsted Brothers shaped the Memorial Cemetery of St. John's Church: naturalistic design, family garden rooms, and the four kinds of landscape on the grounds.",
    olmsted, hero="/assets/img/olmsted-room-drive.jpg", hero_h1="The Olmsted Landscape")); PAGES.append("/olmsted-landscape/")

# ------------------------------------------------------------------ MAPS
maps = [
 ("zones-olmsted-rooms", "Zones and Olmsted rooms", "The cemetery&rsquo;s eleven numbered sections, with the family plots designed by the Olmsted firm shown in gold."),
 ("1921-olmsted-plan", "The Olmsted Preliminary Plan, 1921", "The plan that set out the drives, paths, parks, and wooded edges."),
 ("1921-plan-overlay", "The 1921 plan, in colour", "Parks and reservations in green, drives and paths in peach and gold, small plots in gray."),
 ("1918-topographic-plan", "Survey of the grounds, 1918", "H.&thinsp;C. Harrington&rsquo;s topographic survey, made before the Olmsted designs."),
 ("1953-aerial", "Aerial photograph, 1953", "The grounds in the mid-twentieth century, with the Olmsted rooms in the west already under heavy canopy."),
 ("2018-aerial", "Aerial photograph, 2018", "The cemetery today, under its canopy of mature trees."),
 ("circulation-comparison", "How the roads and paths changed", "The drives and paths of the 1918 survey, the Olmsted plans, and the 1975&ndash;95 survey, drawn on top of one another."),
 ("parks-and-reservations", "Parks, reservations &amp; open space", "The green margins and open lawns that frame the cemetery."),
 ("olmsted-rooms", "Olmsted rooms and large plots", "The larger family plots, in gold."),
 ("scatter-gardens-columbaria", "Scatter gardens &amp; columbaria", "Places for cremated remains, in light green."),
 ("small-plot-areas", "Small plot areas", "Single and small family plots, in lavender."),
 ("landscape-areas-composite", "All four areas together", "The four landscape areas on one plan."),
]
cards = "\n".join(f'<figure><a href="/assets/maps/{f}.jpg"><img src="/assets/maps/{f}.jpg" alt="{t}" loading="lazy"></a><figcaption><strong>{t}.</strong> {d}</figcaption></figure>' for f, t, d in maps)
mapspage = f"""
<section><div class="wrap">
<div class="prose"><p class="lede" style="max-width:none">A century of plans and photographs, from the first survey to the cemetery today.</p></div>
</div></section>
<section class="warm"><div class="wrap">
<p class="prose" style="max-width:64ch;margin-bottom:1.6em">Select any map to see it full size. They were prepared in 2019 for the cemetery&rsquo;s landscape guide, and the oldest drawings are the Olmsted Brothers&rsquo; own.</p>
<div class="mapgrid">
{cards}
</div>
<p class="note" style="margin-top:2em"><strong>Credits.</strong> {CREDIT_PLANS}</p>
</div></section>
"""
# The lede above should not say 'two hundred acres'; keep it truthful:
write("/maps/", page("/maps/", "Maps & Plans", "Historic plans, aerial photographs, and landscape maps of the Memorial Cemetery of St. John's Church, including the Olmsted Brothers' 1921 plan.",
    mapspage, hero="/assets/img/coe-mausoleum.jpg", hero_h1="Maps &amp; Plans")); PAGES.append("/maps/")

# ------------------------------------------------------------------ VISIT
visit = f"""
<section><div class="wrap"><div class="split">
<div>
<h2>Plan your visit</h2>
<dl class="facts">
<dt>Address</dt><dd>{ADDR}<br><a href="{MAPS_LINK}">Open in Google Maps</a></dd>
<dt>Telephone</dt><dd><a href="tel:{TEL}">{PHONE}</a></dd>
<dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd>
<dt>The grounds</dt><dd>Open during daylight hours, seven days a week.</dd>
<dt>Cemetery office</dt><dd>Monday&ndash;Friday 8:00&ndash;4:00; Saturday 8:00&ndash;12:00</dd>
<dt>Mailing address</dt><dd>P.O. Box 114, Cold Spring Harbor, NY 11724</dd>
</dl>
<p style="margin-top:1.4em;max-width:46ch">The cemetery is about a mile west of St.&nbsp;John&rsquo;s Church on Route&nbsp;25A. The entrance is off Route&nbsp;25A; look for the stone gateposts and the sign. Parking is available near the cemetery office.</p>
</div>
<figure><img src="/assets/img/entrance-sign.jpg" alt="The entrance sign: 1704, Memorial Cemetery of St. John's Church, between two stone piers" loading="lazy"><figcaption>The entrance on Route 25A. Photo: Gideon Pollach.</figcaption></figure>
</div></div></section>

<section class="warm"><div class="wrap"><div class="split">
<div class="prose">
<h2>Finding someone you love</h2>
<p>Everyone is welcome to visit the cemetery.</p>
<p>If you know the family name, section, and plot, the <a href="/maps/">map of zones and Olmsted rooms</a> will help you find the right part of the grounds. If you are not sure where someone is buried, step into the cemetery office, near the parking area, or call and we will help you find them.</p>
<p>Many families also search <a href="https://www.findagrave.com/">Find a Grave</a> for the Memorial Cemetery of St. John&rsquo;s Church.</p>
</div>
<figure><img src="/assets/img/dogwood-stones.jpg" alt="Gravestones in the sun beneath a flowering dogwood" loading="lazy"></figure>
</div></div></section>

<section><div class="wrap"><div class="prose">
<h2>While you are here</h2>
<p>This is a place of quiet, and a living landscape that many people share. Please stay on the drives and paths when you can, and treat the monuments gently. If you would like to leave flowers or a remembrance, our <a href="/families/">guide for families</a> explains what works best in the cemetery.</p>
<p>The gates close at dusk, and we ask visitors to be out of the grounds by then.</p>
</div></div></section>
"""
write("/visit/", page("/visit/", "Visit", "Address, hours, and visiting information for the Memorial Cemetery of St. John's Church, 1704 NY-25A, Laurel Hollow, NY.",
    visit, hero="/assets/img/dogwood-road.jpg", hero_h1="Visit")); PAGES.append("/visit/")

# ------------------------------------------------------------------ BURIAL
burial = f"""
<section><div class="wrap"><div class="prose">
<p class="lede" style="max-width:none">We are glad to help you think through what you need, at whatever pace you need.</p>
<p style="margin-top:1.2em">The cemetery offers more than one way to be laid to rest here, and choosing ahead of time is a kindness to those who come after. If someone has just died, please call the cemetery office at <a href="tel:{TEL}">{PHONE}</a>.</p>
</div></div></section>

<section class="warm"><div class="wrap"><div class="prose">
<h2>Plots and who they are for</h2>
<p>Everyone is welcome to walk the grounds. Burial plots are made available to members of St.&nbsp;John&rsquo;s Church and to the children of those already buried here.</p>
</div></div></section>

<section><div class="wrap">
<h2>What the cemetery offers</h2>
<div class="areas">
<div class="area a4"><h3>Burial plots</h3><p>Traditional in-ground burial, in single and family plots across the older and newer sections of the cemetery.</p></div>
<div class="area a3"><h3>Columbarium</h3><p>A columbarium near the chapel holds the cremated remains of those who have died.</p></div>
<div class="area a3"><h3>Scatter garden</h3><p>A garden near East and Valley Avenues where cremated remains may be scattered in a landscape designed for the purpose.</p></div>
</div>
<p class="prose" style="margin-top:1.6em;max-width:64ch">The cemetery&rsquo;s long-term landscape plan includes additional space for cremated remains.</p>
</div></section>

<section class="warm"><div class="wrap"><div class="split">
<div class="prose">
<h2>How to begin</h2>
<p>Call the cemetery office at <a href="tel:{TEL}">{PHONE}</a>, or write to <a href="mailto:{EMAIL}">{EMAIL}</a>. Our Cemetery Superintendent, Brian Pierce, will be glad to talk with you about what is available, the cost, and the next steps.</p>
<p>If you would like a funeral or committal service led by the clergy of St.&nbsp;John&rsquo;s, you can read about <a href="https://stjcsh.org/worship/funeral-services/">funeral services at St. John&rsquo;s</a>, or ask when you call.</p>
</div>
<figure><img src="/assets/img/chapel.jpg" alt="The cemetery chapel among flowering dogwoods" loading="lazy"></figure>
</div></div></section>
"""
write("/burial/", page("/burial/", "Burial & Memorials", "Burial plots, the columbarium, and the scatter garden at the Memorial Cemetery of St. John's Church, and how to begin.",
    burial, hero="/assets/img/slate-markers.jpg", hero_h1="Burial &amp; Memorials")); PAGES.append("/burial/")

# ------------------------------------------------------------------ FAMILIES
families = f"""
<section><div class="wrap"><div class="prose">
<p class="lede" style="max-width:none">The cemetery is a shared garden. This is how we care for it together.</p>
<p style="margin-top:1.2em">Remembering someone you love at their grave is welcome here. These guidelines help keep the whole cemetery serene and respectful through the seasons, and they make it easier for our grounds crew to care for it.</p>
</div></div></section>

<section class="warm"><div class="wrap"><div class="prose">
<h2>Flowers and remembrances</h2>
<h3>Flowers</h3>
<p>Cut flowers and small potted plants in fiber pots of natural material may be placed at the base of a headstone. Please plan to remove them when they fade; any left behind are gathered and composted by our staff each month. Because annuals need constant watering, we ask that they not be planted.</p>
<h3>Holidays</h3>
<p>For Veterans Day, Thanksgiving, Christmas, Easter, Memorial Day, Independence Day, and Labor Day, you may place boughs, wreaths, or sprays of evergreen, or dried plant material tied with natural twine or ribbon. Everything should be natural and compostable. Please avoid wire, plastic, laminated items, and signs. Holiday tributes stay for about four weeks.</p>
<h3>Lights</h3>
<p>Because the cemetery closes at dusk, lighting is not needed, and it adds clutter to the landscape.</p>
</div></div></section>

<section><div class="wrap"><div class="prose">
<h2>Stones and plantings</h2>
<h3>Headstones</h3>
<p>Markers are granite or slate, in soft grays, blue-grays, and green-grays. Bright colors and highly polished surfaces are not used. Upright stones are up to 32 inches tall; widths run up to 30 inches for a single grave, 42 for two, and 60 for three. Proposed monuments are reviewed by the Cemetery Committee before they are made.</p>
<h3>Plantings</h3>
<p>Families may plant low groundcovers, bulbs, and perennials from the cemetery&rsquo;s approved plant list, with white as the leading flower color, within two feet of the stone, after a planting plan is approved. Clipped hedges around individual plots are no longer permitted. Existing hedges will be removed over time as they decline, in keeping with the Olmsted design.</p>
<p>If you would like to plant something, or to ask about a stone, please call the cemetery office at <a href="tel:{TEL}">{PHONE}</a> first. We are happy to help.</p>
</div></div></section>
"""
write("/families/", page("/families/", "For Families", "Guidance for families caring for graves at the Memorial Cemetery of St. John's Church: flowers, holiday tributes, headstones, and plantings.",
    families, hero="/assets/img/dogwood-stones.jpg", hero_h1="For Families")); PAGES.append("/families/")

# ------------------------------------------------------------------ CARE
care = f"""
<section><div class="wrap"><div class="split">
<div class="prose">
<p class="lede" style="max-width:none">An Olmsted landscape is a living work of art, and it needs tending.</p>
<p style="margin-top:1.2em">The cemetery&rsquo;s grounds crew and superintendent care for the roads, the trees, the lawns, and the common areas, guided by the Cemetery Committee of St.&nbsp;John&rsquo;s. Families and friends care for the plots that belong to them. In a cemetery this old and this large, there is always more to do.</p>
</div>
<figure><img src="/assets/img/olmsted-room-drive.jpg" alt="A moss-covered Olmsted room with stone steps beside a cemetery drive" loading="lazy"></figure>
</div></div></section>

<section class="warm"><div class="wrap"><div class="prose">
<h2>Our preservation plan</h2>
<p>In 2018 and 2019 the cemetery committee and the wider St.&nbsp;John&rsquo;s community worked with Heritage Landscapes, preservation landscape architects, to study the Olmsted record and decide how to care for the cemetery in the years ahead. The committee agreed to:</p>
<ul>
<li>preserve and restore the Olmsted rooms;</li>
<li>work toward a more unified landscape across the cemetery;</li>
<li>replace clipped hedges with low plantings, trees, and bulbs, and add stone paths in the small-plot areas;</li>
<li>plant flowering trees and shrubs where there is room;</li>
<li>restore the Olmsted-style wooded edges around the perimeter; and</li>
<li>guide the materials, color, and size of gravestones.</li>
</ul>
<p>The study also found that the cemetery is potentially eligible for the National Register of Historic Places, which would recognize it as the work of master landscape architects.</p>
</div></div></section>

<section><div class="wrap"><div class="prose">
<h2>Supporting the cemetery</h2>
<p>Gifts of any size help us tend the trees, repair the walls and steps, and carry out the preservation plan. Gifts are made through St.&nbsp;John&rsquo;s Church: you can <a href="https://stjcsh.org/give/">give online</a>, or send a check to St.&nbsp;John&rsquo;s Episcopal Church, 1670 Route&nbsp;25A, Cold Spring Harbor, NY&nbsp;11724. Please note &ldquo;Memorial Cemetery&rdquo; on your gift.</p>
<p>To talk about a gift, a memorial tree, or volunteering, please call <a href="tel:{TEL}">{PHONE}</a> or <a href="/contact/">contact us</a>. Our thanks, always, to our grounds crew, who care for this place every day.</p>
</div></div></section>
"""
write("/care/", page("/care/", "Care & Support", "How the Olmsted landscape of the Memorial Cemetery of St. John's Church is cared for, the preservation plan, and how to support the work.",
    care, hero="/assets/img/bench-room.jpg", hero_h1="Care &amp; Support")); PAGES.append("/care/")

# ------------------------------------------------------------------ CONTACT
contact = f"""
<section><div class="wrap"><div class="split">
<div>
<h2>Cemetery office</h2>
<dl class="facts">
<dt>Telephone</dt><dd><a href="tel:{TEL}">{PHONE}</a></dd>
<dt>Fax</dt><dd>(516) 692-7024</dd>
<dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd>
<dt>Address</dt><dd>{ADDR}</dd>
<dt>Mail</dt><dd>P.O. Box 114, Cold Spring Harbor, NY 11724</dd>
<dt>Office hours</dt><dd>Monday&ndash;Friday 8:00&ndash;4:00; Saturday 8:00&ndash;12:00</dd>
</dl>
</div>
<figure><img src="/assets/img/chapel.jpg" alt="The cemetery chapel among flowering dogwoods" loading="lazy"></figure>
</div></div></section>

<section class="warm"><div class="wrap">
<h2>Who we are</h2>
<ul class="people">
<li><span class="nm">Brian Pierce</span><br><span class="rl">Cemetery Superintendent</span></li>
<li><span class="nm">Monica Pierce</span><br><span class="rl">Administrator</span></li>
<li><span class="nm">Joe Bonventre</span><br><span class="rl">Chair, Cemetery Committee</span></li>
<li><span class="nm">The Very Rev. Gideon L.&nbsp;K. Pollach</span><br><span class="rl">Rector, St. John&rsquo;s Episcopal Church</span></li>
</ul>
<p class="prose" style="margin-top:1.8em;max-width:64ch">The cemetery is overseen by the board of St.&nbsp;John&rsquo;s Episcopal Church: Gideon Pollach, Billy Wresch, Lindsay Kamdar, and Jon Hatch, Treasurer. It is cared for every day by our grounds crew.</p>
</div></section>
"""
write("/contact/", page("/contact/", "Contact", "Contact the Memorial Cemetery of St. John's Church: telephone, address, and the people who care for the cemetery.",
    contact, hero="/assets/img/gate.jpg", hero_h1="Contact")); PAGES.append("/contact/")

# ------------------------------------------------------------------ 404, robots, sitemap
nf = page("/404.html", "Page not found", "That page could not be found.",
    '<section><div class="wrap"><div class="prose"><h2>Page not found</h2><p>We could not find that page. You may be looking for the <a href="/">home page</a>, the <a href="/visit/">visiting information</a>, or the <a href="/contact/">contact page</a>.</p></div></div></section>')
with open(os.path.join(OUT, "404.html"), "w", encoding="utf-8") as f: f.write(nf)
with open(os.path.join(OUT, "robots.txt"), "w") as f: f.write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
            "".join(f"<url><loc>{BASE}{p}</loc></url>\n" for p in PAGES) + "</urlset>\n")
print("built", len(PAGES), "pages")
