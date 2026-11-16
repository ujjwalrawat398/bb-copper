"""Post-build accessibility, SEO and deployment security improvements."""
from pathlib import Path
import json,re,html,hashlib,base64
from PIL import Image,ImageDraw

def enhance(root,site,products,categories):
 esc=lambda s:html.escape(str(s),quote=True)
 domain=site['domain'].rstrip('/')
 faqs=[('What does BB Copper Products manufacture?','BB Copper Products manufactures, exports and supplies copper ware for household, hospitality and corporate sectors. The catalogue includes bottles, mugs, glasses, pots, lota, religious items, tanks, jugs, thali sets and gift sets.'),('Where is BB Copper Products located?',site['address']+'. Please contact the team to confirm visiting hours and directions.'),('How do I request a product quotation?','Open a product page, enter your name and optionally a quantity or message, then select Get Quote on WhatsApp. Check the prefilled details and press Send in WhatsApp.'),('Are prices, capacities and minimum order quantities available online?','Prices, capacities, dimensions and minimum order quantities are not published in this catalogue. Ask the team to confirm the specifications and quote for the item code you choose.'),('Does the enquiry attach a product photo?','No. WhatsApp click-to-chat prefills text, not photo attachments. The enquiry includes a product image link when a supplied photo is available, and a link to the product page.'),('Does this website collect or store my enquiry?','This static website has no enquiry database. The enquiry fields are used in your browser to prepare a WhatsApp message. When you open WhatsApp, its own privacy terms apply. Hosting providers may process standard access logs.')]
 faq_html='<section class="container section faq" id="questions"><span class="eyebrow">HELPFUL ANSWERS</span><h2>Questions, answered.</h2>'+''.join('<details><summary>'+esc(q)+'</summary><p>'+esc(a)+'</p></details>' for q,a in faqs)+'</section>'
 image=Image.new('RGB',(1200,630),'#faf7f2');draw=ImageDraw.Draw(image);draw.rectangle((0,0,30,630),fill='#985331');draw.text((90,190),'BB COPPER PRODUCTS',fill='#5c2a17',font_size=64);draw.text((90,300),'Discover your Luxury Life',fill='#985331',font_size=40);draw.text((90,390),'Copper ware | Mathura, India | Established 2016',fill='#30251f',font_size=25);image.save(root/'assets/brand/og-default.jpg',quality=90)
 logo=Image.open(root/'assets/brand/logo-official.png').convert('RGBA');logo.thumbnail((280,200));image.paste(logo,(850,80),logo);image.save(root/'assets/brand/og-default.jpg',quality=90)
 styles={}
 for f in root.rglob('*.html'):
  text=f.read_text().replace('<h4>','<h2 class="footer-heading">').replace('</h4>','</h2>').replace('aria-label="BB Copper home"','').replace('aria-label="Chat on WhatsApp"','aria-label="Chat with us on WhatsApp"');path='/'+str(f.relative_to(root).parent).replace('\\','/')+'/'
  if path=='/./' :path='/'
  title=html.unescape(re.search(r'<title>(.*?)</title>',text).group(1)).split(' | ')[0]
  product=next((p for p in products if path=='/products/'+p['code'].lower()+'/'),None)
  description=(f'Enquire about {product["name"]} ({product["code"]}) in {product["categoryName"]} from BB Copper Products, Mathura. Request specifications and a quote on WhatsApp.' if product else f'{title} at BB Copper Products, Mathura. Explore the copper ware catalogue and contact our manufacturing and export team directly on WhatsApp.')
  text=re.sub(r'<meta name="description" content="[^"]*">','<meta name="description" content="'+esc(description)+'">',text)
  text=re.sub(r'<meta property="og:description" content="[^"]*">','<meta property="og:description" content="'+esc(description)+'">',text)
  if 'property="og:image"' not in text:text=text.replace('</head>','<meta property="og:image" content="'+domain+'/assets/brand/og-default.jpg"></head>')
  text=text.replace('</head>','<meta property="og:locale" content="en_IN"><meta property="og:site_name" content="BB Copper Products"><meta name="robots" content="index,follow,max-image-preview:large"></head>')
  text=text.replace('<main>','<main id="main" tabindex="-1">').replace('<body>','<body><a class="skip" href="#main">Skip to content</a>')
  text=text.replace('class="links" aria-label','id="navigation" class="links" aria-label').replace('aria-label="Open menu"','aria-label="Open menu" aria-controls="navigation"')
  text=text.replace('<li><a href="/reviews/">','<li><a href="/#questions">FAQs</a></li><li><a href="/reviews/">')
  if path=='/':text=text.replace('</main>',faq_html+'</main>')
  if path=='/reviews/':text=text.replace('content="index,follow,max-image-preview:large"','content="noindex,follow"')
  schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',text).group(1))
  business={'@type':'LocalBusiness','@id':domain+'/#business','name':site['brand'],'url':domain,'telephone':site['phoneDisplay'],'email':site['email'],'logo':domain+'/assets/brand/logo-official.png','foundingDate':'2016','address':{'@type':'PostalAddress','streetAddress':site['address'],'addressLocality':'Mathura','addressRegion':'Uttar Pradesh','addressCountry':'IN'}}
  graph=[business,{'@type':'WebSite','@id':domain+'/#website','url':domain,'name':site['brand'],'publisher':{'@id':domain+'/#business'}},{'@type':'WebPage','@id':domain+path+'#page','url':domain+path,'name':title,'description':description,'isPartOf':{'@id':domain+'/#website'},'about':{'@id':domain+'/#business'}}]
  crumbs=[('Home','/')]
  if product:
   text=text.replace('<h3>Make it part of your collection.</h3>','<h2 class="enquiry-title">Make it part of your collection.</h2>')
   schema.pop('@context',None);schema['description']=description;schema['manufacturer']={'@id':domain+'/#business'};graph.append(schema)
   crumbs.extend([('Collection','/products/'),(product['categoryName'],'/categories/'+product['category']+'/'),(product['name'],path)])
   # Main product image is above the fold; do not lazy-load it.
   text=text.replace('loading="lazy"','loading="eager" fetchpriority="high"',1)
   facts='<dl class="product-facts"><dt>Item code</dt><dd>'+esc(product['code'])+'</dd><dt>Category</dt><dd>'+esc(product['categoryName'])+'</dd><dt>Specifications & price</dt><dd>Confirm with our team on WhatsApp.</dd></dl>'
   text=text.replace('<form class="enquiry"',facts+'<form class="enquiry"')
   text=text.replace('</form>','<p class="note">Your enquiry is not stored on this site. Continuing opens WhatsApp, subject to its own privacy terms.</p></form>')
  elif path!='/':crumbs.append((title,path))
  if len(crumbs)>1:graph.append({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':i+1,'name':name,'item':domain+link} for i,(name,link) in enumerate(crumbs)]})
  if path=='/':graph.append({'@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in faqs]})
  if path=='/products/' or path.startswith('/categories/'):
   items=[p for p in products if path=='/products/' or path=='/categories/'+p['category']+'/'];items.sort(key=lambda p:not bool(p['image']))
   graph.append({'@type':'ItemList','numberOfItems':len(items),'itemListElement':[{'@type':'ListItem','position':i+1,'url':domain+'/products/'+p['code'].lower()+'/','name':p['name']} for i,p in enumerate(items)]})
  data=json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
  text=re.sub(r'<script type="application/ld\+json">.*?</script>',lambda m:'<script type="application/ld+json">'+data+'</script>',text)
  # Move every template inline style to an external stylesheet.
  def style(m):
   value=m.group(1);key='s'+hashlib.sha256(value.encode()).hexdigest()[:10];styles[key]=value
   return ' data-style="'+key+'"'
  text=re.sub(r' style="([^"]*)"',style,text)
  script_hash=base64.b64encode(hashlib.sha256(data.encode()).digest()).decode()
  policy="default-src 'none'; script-src 'self' 'sha256-"+script_hash+"'; style-src 'self'; img-src 'self'; connect-src 'self'; font-src 'self'; base-uri 'none'; object-src 'none'; form-action 'none'"
  text=text.replace('<meta charset="utf-8">','<meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="'+esc(policy)+'"><meta name="referrer" content="strict-origin-when-cross-origin">')
  f.write_text(text)
 with (root/'assets/style.css').open('a') as css:
  css.write('\n'+''.join('[data-style="'+key+'"]{'+value+'}' for key,value in styles.items()))
 (root/'_headers').write_text('/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=()\n  Content-Security-Policy: frame-ancestors \'none\'; upgrade-insecure-requests\n  X-Frame-Options: DENY\n/assets/*\n  Cache-Control: public, max-age=3600\n/images/*\n  Cache-Control: public, max-age=86400\n')
 # Do not serve original JPEGs or unused temporary logo artwork.
 shutil=__import__('shutil');shutil.rmtree(root/'assets/images',ignore_errors=True);shutil.rmtree(root/'assets/source',ignore_errors=True)
 (root/'assets/brand/logo.svg').unlink(missing_ok=True)
 # Empty reviews page is navigable but not an indexing target.
 sitemap=root/'sitemap.xml';sitemap.write_text(sitemap.read_text().replace('<url><loc>'+domain+'/reviews/</loc></url>',''))
 (root/'404.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Page not found | BB Copper</title><link rel="stylesheet" href="/assets/style.css"><main class="container section"><h1>Page not found.</h1><p>This link may be incorrect or out of date.</p><a class="btn" href="/products/">Explore the collection</a></main></html>')
