"""Catalogue photography and restrained copper visual treatment, before security pass."""
import re

def apply(root):
 def img(name,alt,cls='',eager=False):
  return f'<img class="{cls}" src="/assets/lifestyle/{name}.webp" width="1200" height="900" alt="{alt}" '+('fetchpriority="high" loading="eager"' if eager else 'loading="lazy"')+'>'
 logo='<span class="brand"><img class="official-logo" src="/assets/brand/logo-official.png" width="220" height="143" alt="BB Copper Products"></span>'
 banners={'bottles':('bottles','Copper bottles in three coloured finishes'),'mugs-bar':('mugs','Hammered copper mugs styled with ice and garnish'),'glasses':('glass','Hammered copper drinking glass'),'lota':('lota','Green and copper lota catalogue design'),'religious':('lota','Lota from the BB Copper collection'),'tanks':('matka','Hammered Matka BB-1143'),'jugs':('collection','A selection of BB Copper ware'),'pots-carafes':('collection','BB Copper collection including pots and carafes'),'thali-sets':('collection','Catalogue collection including serving ware'),'bottle-gift-packs':('gift-packs','Bottle and glass gift packs shown together'),'gift-sets':('signature-set','Matching copper bottle and two glasses')}
 for page in root.rglob('index.html'):
  t=page.read_text();t=re.sub(r'<span class="brand">.*?</span></span>',lambda m:logo,t)
  t=t.replace('<link rel="icon" href="/assets/brand/favicon.svg">','<link rel="icon" type="image/png" href="/assets/brand/icon-32.png"><link rel="apple-touch-icon" href="/assets/brand/icon-180.png">')
  if page==root/'index.html':
   t=re.sub(r'<div class="hero-art">.*?<span class="hero-label">.*?</span></div>',lambda m:'<div class="hero-art campaign-art">'+img('signature-set','BB Copper bottle with two matching glasses','',True)+'<span class="hero-label">THE SIGNATURE COPPER COLLECTION</span></div>',t)
   tiles=[('bottles','Copper bottles','34 catalogue designs','bottles'),('mugs-bar','Mugs & bar','8 catalogue designs','mugs'),('tanks','Copper tanks','25 catalogue designs','matka'),('bottle-gift-packs','Gift packs','17 catalogue designs','gift-packs')]
   grid='<div class="category-grid">'+''.join(f'<a class="category-tile photo-tile" href="/categories/{cid}/">'+img(image,title)+f'<div class="tile-copy"><h3>{title}</h3><small>{count}</small><span class="arrow">↗</span></div></a>' for cid,title,count,image in tiles)+'</div>'
   t=re.sub(r'<div class="category-grid">.*?</div></section>',lambda m:grid+'</section>',t,count=1)
   t=re.sub(r'<div class="story-art">.*?<div class="story-year">',lambda m:'<div class="story-art catalogue-story">'+img('bottle-detail','Close-up of copper bottle finishes')+'<div class="story-year">',t,count=1)
   editorial='<section class="container section editorial"><div class="section-head"><div><span class="eyebrow">DETAILS THAT MAKE THE DIFFERENCE</span><h2>More than a beautiful finish.</h2></div><p>Explore textures, colours and forms<br>from the BB Copper catalogue.</p></div><div class="editorial-grid"><a href="/categories/mugs-bar/" class="editorial-card">'+img('mugs','Two hammered copper mugs')+'<div><span class="eyebrow">THE ART OF HOSTING</span><h3>A warmer welcome.</h3><span>Explore mugs & bar ↗</span></div></a><a href="/categories/glasses/" class="editorial-card">'+img('glass','Copper glass with hammered details')+'<div><span class="eyebrow">EVERYDAY DETAILS</span><h3>A ritual of your own.</h3><span>Explore copper glasses ↗</span></div></a></div></section>'
   t=t.replace('<section class="story section">',editorial+'<section class="story section">')
   gallery='<section class="container section catalogue-gallery"><div class="section-head"><div><span class="eyebrow">FROM THE CATALOGUE</span><h2>One material. Many expressions.</h2></div><a class="text-link" href="/products/">Explore all 191 designs ↗</a></div><div class="gallery-grid"><a href="/categories/lota/">'+img('lota','Decorative copper lota')+'<h3>Rooted in tradition.</h3></a><a href="/products/bb-1030/">'+img('black-etching','Detail of the black etching bottle and glasses catalogue photograph')+'<h3>The etching collection.</h3></a><a href="/categories/bottle-gift-packs/">'+img('gift-packs','Three bottle gift pack designs shown together')+'<h3>Made to be gifted.</h3></a></div><a class="collection-panorama" href="/products/">'+img('collection','The BB Copper catalogue collection')+'<span>Discover the complete collection &nbsp; ↗</span></a></section>'
   t=t.replace('</main>',gallery+'</main>')
  if page.parent.parent.name=='categories':
   cid=page.parent.name
   if cid in banners:
    image,alt=banners[cid];t=t.replace('<div class="catalog-layout">','<div class="category-banner">'+img(image,alt)+'<span>CATALOGUE INSPIRATION · '+('ITEM BB-1143' if cid=='tanks' else 'DESIGNS SHOWN FOR COLLECTION CONTEXT')+'</span></div><div class="catalog-layout">')
  if page==root/'products/index.html':t=t.replace('<div class="catalog-layout">','<div class="category-banner wide-banner">'+img('collection','BB Copper full collection')+'<span>EXPLORE THE WORLD OF BB COPPER</span></div><div class="catalog-layout">')
  if page==root/'about/index.html':
   t=re.sub(r'<div class="story-art">.*?</div>',lambda m:'<div class="story-art catalogue-story">'+img('about-detail','Copper bottle details from the company catalogue')+'</div>',t,count=1)
   t=t.replace('</main>','<section class="container section"><span class="eyebrow">OUR APPROACH</span><h2>We innovate by starting with the customer<br>and working backwards.</h2><p>Our catalogue describes a focus on diverse designs shaped around customer preferences.</p><div class="collection-panorama">'+img('collection','BB Copper product range')+'</div></section></main>')
  if page!=root/'index.html':
   route='/'+str(page.relative_to(root).parent)+'/'
   fallback='/products/'
   if route.startswith('/products/bb-'):
    import json
    inventory=json.loads((root/'data/products.json').read_text())
    item=next((p for p in inventory if route=='/products/'+p['code'].lower()+'/'),None)
    if item:fallback='/categories/'+item['category']+'/'
   elif route in ['/products/','/about/','/contact/','/reviews/']:fallback='/'
   t=t.replace('<main id="main" tabindex="-1">','<main id="main" tabindex="-1"><div class="container back-row"><a class="back-link" data-back href="'+fallback+'">← Back</a></div>') if '<main id="main"' in t else t.replace('<main>','<main><div class="container back-row"><a class="back-link" data-back href="'+fallback+'">← Back</a></div>')
  page.write_text(t)
