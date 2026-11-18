from pathlib import Path
import json,html,shutil,os
from PIL import Image
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'dist'
if OUT.exists(): shutil.rmtree(OUT)
OUT.mkdir()
P=json.loads((ROOT/'src/data/products.json').read_text()); C=json.loads((ROOT/'src/data/categories.json').read_text()); S=json.loads((ROOT/'src/data/site.json').read_text())
D=S['domain'].rstrip('/')
e=lambda s:html.escape(str(s),quote=True)
wa='https://wa.me/'+S['whatsapp']+'?text=Hello%20BB%20Copper%2C%20I%20would%20like%20to%20know%20more%20about%20your%20products.'
(OUT/'images/products/thumb').mkdir(parents=True)
for p in P:
 if p['image']:
  im=Image.open(ROOT/p['image'].lstrip('/')).convert('RGB'); im.thumbnail((800,800)); im.save(OUT/f"images/products/{p['code'].lower()}.webp",quality=86)
  im.thumbnail((400,400)); im.save(OUT/f"images/products/thumb/{p['code'].lower()}.webp",quality=82)
  p['image']=f"/images/products/{p['code'].lower()}.webp"; p['thumb']=f"/images/products/thumb/{p['code'].lower()}.webp"
 else:p['thumb']=None
shutil.copytree(ROOT/'assets',OUT/'assets')
(OUT/'data').mkdir()
for name,data in [('products',P),('categories',C),('site',S),('reviews',[])]: (OUT/f'data/{name}.json').write_text(json.dumps(data,ensure_ascii=False))

def url(p):return '/products/'+p['code'].lower()+'/'
def brand():return '<span class="brand"><b>BB</b><span>BB COPPER<small>PRODUCTS</small></span></span>'
def photo(p,thumb=False):
 if not p['image']:return '<div class="placeholder"><span>◇</span>Product photo coming soon</div>'
 return f'<img src="{p["thumb"] if thumb else p["image"]}" width="400" height="420" alt="{e(p["name"])} {p["code"]}" loading="lazy">'
def card(p):return f'''<article class="product-card" data-search="{e((p['name']+' '+p['code']+' '+p['categoryName']).lower())}" data-photo="{'yes' if p['image'] else 'no'}"><a class="product-image" href="{url(p)}"><span class="badge">{p['code']}</span>{photo(p,True)}</a><h3><a href="{url(p)}">{e(p['name'])}</a></h3><div class="product-meta"><span>{e(p['categoryName'].replace('Copper ',''))}</span><a href="{url(p)}">Enquire ↗</a></div></article>'''
def get(code):return next(p for p in P if p['code']==code)
def shell(path,title,body,description='',product=None):
 canonical=D+path
 schema={'@context':'https://schema.org','@type':'LocalBusiness','name':S['brand'],'telephone':S['phoneDisplay'],'email':S['email'],'url':D,'address':{'@type':'PostalAddress','streetAddress':S['address'],'addressLocality':'Mathura','addressRegion':'Uttar Pradesh','addressCountry':'IN'}}
 if product:
  schema={'@context':'https://schema.org','@type':'Product','name':product['name'],'sku':product['code'],'brand':{'@type':'Brand','name':S['brand']},'url':canonical}
  if product['image']:schema['image']=D+product['image']
 og=f'<meta property="og:image" content="{D+product["image"]}">' if product and product['image'] else ''
 desc=description or 'Explore copper ware from BB Copper Products, manufacturer, exporter and supplier in Mathura. Enquire directly on WhatsApp.'
 content=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} | BB Copper Products</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{canonical}"><meta property="og:title" content="{e(title)} | BB Copper"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{canonical}"><meta property="og:type" content="website">{og}<meta name="twitter:card" content="summary_large_image"><link rel="icon" href="/assets/brand/favicon.svg"><link rel="stylesheet" href="/assets/style.css"><script type="application/ld+json">{json.dumps(schema)}</script><script defer src="/assets/app.js"></script></head><body><div class="topbar">MANUFACTURER & EXPORTER OF COPPER WARE · MATHURA, INDIA</div><header class="header"><div class="container nav"><a href="/" aria-label="BB Copper home">{brand()}</a><button class="menu-toggle" aria-label="Open menu" aria-expanded="false">☰</button><nav class="links" aria-label="Main navigation"><a href="/">Home</a><a href="/products/">Our collection ▾</a><a href="/about/">Our story</a><a href="/contact/">Contact</a><a class="btn" href="{wa}" target="_blank" rel="noopener">WhatsApp us ↗</a></nav></div></header><main>{body}</main><footer class="footer"><div class="container"><div class="footer-grid"><div><a href="/">{brand()}</a><p>Discover your Luxury Life.<br>Copper ware for everyday rituals,<br>thoughtful homes and meaningful gifts.</p><a href="{wa}" target="_blank" rel="noopener">Chat on WhatsApp ↗</a></div><div><h4>EXPLORE</h4><ul><li><a href="/products/">Our collection</a></li><li><a href="/about/">Our story</a></li><li><a href="/reviews/">Reviews</a></li><li><a href="/contact/">Contact us</a></li></ul></div><div><h4>OUR COLLECTIONS</h4><ul>{''.join(f'<li><a href="/categories/{c["id"]}/">{e(c["name"])}</a></li>' for c in [C[0],C[6],C[9],C[10]])}</ul></div><div><h4>COME SAY HELLO</h4><p>{e(S['address'])}</p><a href="tel:+{S['whatsapp']}">{e(S['phoneDisplay'])}</a><br><a href="mailto:{e(S['email'])}">{e(S['email'])}</a></div></div><div class="copyright"><span>© {__import__('datetime').date.today().year} {e(S['legalName'])}. All rights reserved.</span><span>Made for homes. Crafted for generations.</span></div></div></footer><a class="floating" href="{wa}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">◉ &nbsp; Chat with us</a></body></html>'''
 target=OUT/path.lstrip('/')/'index.html' if path!='/' else OUT/'index.html'
 target.parent.mkdir(parents=True,exist_ok=True);target.write_text(content)
 return path
paths=[]
category_images=[('bottle-gift-packs','BB-1177','Bottle gift packs',17),('gift-sets','BB-1185','Jugs & gift sets',11),('tanks','BB-1131','Copper tanks',25),('gift-sets','BB-1191','Pots & carafe sets',11)]
category_tiles=''.join(f'<a class="category-tile" href="/categories/{cid}/"><img src="{get(code)["image"]}" width="260" height="230" alt="{e(title)}" loading="lazy"><h3>{title}</h3><small>{count} catalogue designs</small><span class="arrow">↗</span></a>' for cid,code,title,count in category_images)
featured=[get(x) for x in ['BB-1185','BB-1177','BB-1191','BB-1130']]
body=f'''<div class="container hero"><div><span class="eyebrow">A little tradition. A lasting impression.</span><h1>The warmth of copper.<br>The art of<br><em>everyday living.</em></h1><p>Discover thoughtfully designed copper ware that brings timeless beauty to your home, your table and your everyday rituals.</p><div class="hero-actions"><a class="btn" href="/products/">Explore the collection &nbsp; ↗</a><a class="btn outline" href="/about/">Our story</a></div><div class="hero-foot">EST. 2016 &nbsp; — &nbsp; ROOTED IN MATHURA, INDIA</div></div><div class="hero-art"><img src="{get('BB-1185')['image']}" alt="Luxury copper jug and two matching glasses, BB-1185" width="530" height="480" fetchpriority="high"><div class="hero-stamp"><strong>BB</strong>COPPER WARE<br>SINCE 2016</div><span class="hero-label">TIMELESS MATERIAL. EVERYDAY BEAUTY.</span></div></div><div class="benefits"><div class="container"><div class="benefit"><i>◇</i><div>Made by manufacturers<small>Direct from BB Copper</small></div></div><div class="benefit"><i>♧</i><div>Rooted in tradition<small>Designed for modern living</small></div></div><div class="benefit"><i>□</i><div>Gifting, thoughtfully done<small>Explore our matching sets</small></div></div><div class="benefit"><i>↗</i><div>From Mathura, to the world<small>Manufacturer & exporter</small></div></div></div></div><section class="container section"><div class="section-head"><div><span class="eyebrow">Find your everyday favourite</span><h2>A collection for every ritual.</h2></div><a class="text-link" href="/products/">View all collections ↗</a></div><div class="category-grid">{category_tiles}</div></section><section class="container section" style="padding-top:10px"><div class="section-head"><div><span class="eyebrow">A closer look</span><h2>Distinctive by design.</h2></div><a class="text-link" href="/products/">Browse all products ↗</a></div><div class="tabs"><a href="/products/">Selected designs</a><a href="/categories/gift-sets/">Gift sets</a><a href="/categories/bottle-gift-packs/">Bottle gift packs</a><a href="/categories/tanks/">Copper tanks</a></div><div class="product-grid">{''.join(map(card,featured))}</div></section><section class="story section"><div class="container story-grid"><div class="story-art"><img src="{get('BB-1191')['image']}" width="390" height="350" alt="Antique finish apple liner copper set" loading="lazy"><div class="story-year">2016<small>OUR JOURNEY BEGAN</small></div></div><div><span class="eyebrow">Our roots. Our craft.</span><h2>From the heart of Mathura,<br>with a love for copper.</h2><p>Established in 2016 and founded by CEO Vikas, BB Copper Products manufactures, exports and supplies copper products for household, hospitality and corporate sectors.</p><p>From simple everyday pieces to ornate gifting collections, our catalogue brings a variety of forms and finishes together in one place.</p><div class="story-facts"><div><b>191</b><small>CATALOGUE DESIGNS</small></div><div><b>11</b><small>COLLECTIONS</small></div><div><b>2016</b><small>ESTABLISHED</small></div></div><a class="text-link" href="/about/">Get to know BB Copper ↗</a></div></div></section><div class="container"><section class="bulk"><div><span class="eyebrow" style="color:#d4ad8d">FOR BUSINESSES & THOUGHTFUL GIVERS</span><h2>Something special in mind?</h2><p>Talk to us about product availability, business enquiries and gifting requirements.</p></div><a class="btn" href="{wa}" target="_blank" rel="noopener">Let’s talk on WhatsApp ↗</a></section></div>'''
paths.append(shell('/','Copper ware for everyday living',body))
def listing(category=None):
 if category:
  items=[get(code) for code in category.get('showcase',[])]
  count_html=f'<span id="count">{len(items)}</span> featured designs · Full range of {category["count"]} designs in the catalogue below ↓'
  download_top='<div class="page-head-actions"><a class="btn btn-red" href="/assets/BB-Copper-Catalogue.pdf" download>Download Catalogue ↓</a></div>'
  download_cta=f'''<div class="catalogue-cta"><h2>Looking for the full range?</h2><p>These are 5 featured designs from {e(category["name"])}. The complete catalogue has all {category["count"]} designs in this collection — and all 191 across BB Copper.</p><a class="btn btn-red" href="/assets/BB-Copper-Catalogue.pdf" download>Download Full Catalogue (PDF) ↓</a></div>'''
 else:
  items=[p for p in P]
  items.sort(key=lambda p:not bool(p['image']))
  count_html=f'<span id="count">{len(items)}</span> products · Enquire for availability and specifications'
  download_top=''
  download_cta=''
 title=category['name'] if category else 'The copper collection'
 filters=''.join(f'<a class="{"active" if category and category["id"]==c["id"] else ""}" href="/categories/{c["id"]}/">{e(c["name"].replace("Copper ",""))} <span>{c["count"]}</span></a>' for c in C)
 b=f'''<div class="container"><div class="page-head"><span class="eyebrow">BB COPPER · PRODUCT CATALOGUE</span><h1>{e(title)}</h1><p>Traditional forms. Distinctive finishes. Find a piece for your everyday ritual, then ask us for a quote directly on WhatsApp.</p>{download_top}</div><div class="catalog-layout"><aside class="filters"><h3>COLLECTIONS</h3><a href="/products/">All products <span>191</span></a>{filters}</aside><section><div class="tools"><input id="search" type="search" placeholder="Search product name or item code…" aria-label="Search products"><select id="photo-filter" aria-label="Photo availability"><option value="all">All catalogue entries</option><option value="yes">With supplied photos</option></select></div><div class="result-count" aria-live="polite">{count_html}</div><div class="product-grid" id="catalog">{''.join(map(card,items))}</div>{download_cta}<p class="empty" id="empty" hidden>No matching products. Try a name or item code.</p></section></div></div>'''
 return shell('/categories/'+category['id']+'/' if category else '/products/',title,b)
paths.append(listing())
for c in C:paths.append(listing(c))
for p in P:
 variants=f'<p>Variants: {e(", ".join(p["variants"]))}. Please confirm availability.</p>' if p['variants'] else ''
 b=f'''<div class="container"><div class="breadcrumb"><a href="/products/">Collection</a> / <a href="/categories/{p['category']}/">{e(p['categoryName'])}</a> / {p['code']}</div><div class="detail"><div class="product-image">{photo(p)}</div><div><span class="eyebrow">{e(p['categoryName'])}</span><h1>{e(p['name'])}</h1><div class="code">ITEM CODE · {p['code']}</div><p>A design from the BB Copper catalogue. Contact our team to confirm material composition, dimensions, capacity, finish options and order requirements.</p>{variants}<form class="enquiry" data-product="{e(json.dumps(p))}"><h3>Make it part of your collection.</h3><p>Tell us your name. We’ll take it from here on WhatsApp.</p><label>Your name *<input name="name" required maxlength="100" autocomplete="name" placeholder="Enter your name"></label><label>Quantity / message <span style="color:#685b50">(optional)</span><textarea name="message" rows="3" maxlength="1500" placeholder="Tell us what you have in mind"></textarea></label><button class="btn" type="submit">Get Quote on WhatsApp &nbsp; ↗</button><p class="note">Opens WhatsApp with your enquiry prefilled. Review it and press Send. Image links are included when a product photo is available; photos are not attached.</p></form></div></div><div class="section-head"><h2>Explore the collection</h2><a class="text-link" href="/categories/{p['category']}/">More in this collection ↗</a></div><div class="product-grid" style="padding-bottom:65px">{''.join(card(q) for q in sorted([q for q in P if q['category']==p['category'] and q!=p],key=lambda q:not bool(q['image']))[:4])}</div></div>'''
 paths.append(shell(url(p),p['name']+' '+p['code'],b,product=p))
paths.append(shell('/about/','Our story',f'''<div class="container section"><span class="eyebrow">ROOTED IN MATHURA · ESTABLISHED 2016</span><h1>A timeless material.<br>A story of our own.</h1><div class="story-grid"><div><h2>Discover your Luxury Life.</h2><p>BB Copper Products is a manufacturer, exporter and supplier of copper products in India, serving household, hospitality and corporate sectors. Founded by CEO Vikas in 2016, our business is based in Mathura, Uttar Pradesh.</p><p>Our catalogue spans bottles, glasses, pots, jugs, religious ware, tanks and gift sets. Explore understated matt and hammered finishes alongside decorative printed and antique etching designs.</p><p>For questions about products, specifications or order requirements, speak directly with our team.</p><a class="btn" href="{wa}">Talk to BB Copper ↗</a></div><div class="story-art"><img src="{get('BB-1181')['image']}" alt="Hammered copper jug set" width="400" height="380"></div></div></div>'''))
paths.append(shell('/reviews/','Customer reviews','''<div class="container section"><span class="eyebrow">CUSTOMER VOICES</span><h1>Real experiences. Only.</h1><div class="review-box"><h2>Authenticity comes first.</h2><p>We publish customer reviews only when the original review text and source have been verified. No testimonials are published here yet.</p><a class="btn outline" href="/contact/">Get in touch with our team ↗</a></div></div>'''))
paths.append(shell('/contact/','Contact BB Copper Mathura',f'''<div class="container"><div class="page-head"><span class="eyebrow">WE’D LOVE TO HEAR FROM YOU</span><h1>Let’s talk copper.</h1><p>Product questions, gifting requirements or business enquiries — our team is a message away.</p></div><div class="contact-grid"><div class="contact-card"><h3>Visit us in Mathura</h3><p>{e(S['address'])}</p><h3>Call or WhatsApp</h3><a href="tel:+{S['whatsapp']}">{e(S['phoneDisplay'])}</a><h3>Email us</h3><a href="mailto:{S['email']}">{e(S['email'])}</a><p style="margin-top:25px">Please call ahead to confirm visiting hours.</p><a class="btn" href="{wa}" target="_blank" rel="noopener">Chat on WhatsApp ↗</a></div><div class="map-panel"><span class="eyebrow">FIND US</span><h2>Mathura,<br>Uttar Pradesh.</h2><p>Goverdhan Road · Surya Nagar</p><a class="btn outline" href="{S['googleMapsSearch']}" target="_blank" rel="noopener">Search on Google Maps ↗</a><p class="note">Opens a Maps search. Please confirm the location before travelling.</p></div></div></div>'''))
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+D+x+'</loc></url>' for x in paths)+'</urlset>')
(OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+D+'/sitemap.xml\n')
cats='\n'.join(f"- [{c['name']}]("+D+f"/categories/{c['id']}/): {c['count']} catalogue designs" for c in C)
feat='\n'.join(f"- [{p['name']} ({p['code']})]("+D+url(p)+")" for p in [get(x) for x in ['BB-1185','BB-1177','BB-1191','BB-1130']])
(OUT/'llms.txt').write_text(f'''# BB Copper Products

> BB Copper Products (Divy Enterprises) is a copper-ware manufacturer, exporter and supplier based in Mathura, Uttar Pradesh, India. Established in 2016. The catalogue lists 191 copper designs across 11 collections for household, hospitality and corporate buyers. Prices, capacities, dimensions and minimum order quantities are not published online; ask the team for a quote on WhatsApp.

## Key pages

- [Home]({D}/): Copper ware for everyday living, featured collections and company story.
- [The copper collection]({D}/products/): All 191 catalogue designs with photos, search and collection filters.
- [Our story]({D}/about/): Manufacturer and exporter in Mathura since 2016, founded by CEO Vikas.
- [Contact]({D}/contact/): Address, phone, WhatsApp and email for product and business enquiries.
- [Customer reviews]({D}/reviews/): Verified customer reviews (none published yet).

## Collections

{cats}

## Featured products

{feat}

## Common questions

- What does BB Copper Products manufacture? BB Copper Products manufactures, exports and supplies copper ware for household, hospitality and corporate sectors. The catalogue includes bottles, mugs, glasses, pots, lota, religious items, tanks, jugs, thali sets and gift sets.
- Where is BB Copper Products located? {S['address']}. Please contact the team to confirm visiting hours and directions.
- How do I request a product quotation? Open a product page, enter your name and optionally a quantity or message, then select Get Quote on WhatsApp. Check the prefilled details and press Send in WhatsApp.
- Are prices, capacities and minimum order quantities available online? Prices, capacities, dimensions and minimum order quantities are not published in this catalogue. Ask the team to confirm the specifications and quote for the item code you choose.
- Does the enquiry attach a product photo? No. WhatsApp click-to-chat prefills text, not photo attachments. The enquiry includes a product image link when a supplied photo is available, and a link to the product page.
- Does this website collect or store my enquiry? This static website has no enquiry database. The enquiry fields are used in your browser to prepare a WhatsApp message. When you open WhatsApp, its own privacy terms apply. Hosting providers may process standard access logs.

## Contact

- Visit: {S['address']}
- WhatsApp / phone: {S['phoneDisplay']}
- Email: {S['email']}
- Enquiries: open any product page and use Get Quote on WhatsApp. No prices are listed online.
''')
print(f'Built {len(paths)} pages; {len(P)} products; {sum(bool(p["image"]) for p in P)} photos.')
from visual import apply
apply(OUT)
from harden import enhance
enhance(OUT,S,P,C)
