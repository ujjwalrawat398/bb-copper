"""Run after build.py. Dependency-free structural/security/SEO regression checks."""
from pathlib import Path
from html.parser import HTMLParser
import json,hashlib,base64,xml.etree.ElementTree as ET
root=Path(__file__).parent/'dist';errors=[];titles=[];descriptions=[]
class Page(HTMLParser):
 def __init__(self):super().__init__();self.h1=0;self.meta={};self.title='';self.script=False;self.structured='';self.in_title=False;self.policy=''
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t=='h1':self.h1+=1
  if t=='title':self.in_title=True
  if t=='meta':self.meta[a.get('name',a.get('property',a.get('http-equiv','')))]=a.get('content','')
  if t=='script':
   assert a.get('src') or a.get('type')=='application/ld+json','Inline executable script'
   self.script=a.get('type')=='application/ld+json'
  for k,v in attrs:
   assert not k.startswith('on'),'Inline event handler'
   assert k!='style','Inline styling'
   if k in ('href','src') and v and v.startswith('/'):
    assert (root/v.lstrip('/').split('#')[0]).exists(),f'Missing local link {v}'
  if t=='img':assert a.get('alt') and a.get('width') and a.get('height'),'Image missing alt/dimensions'
  if a.get('target')=='_blank':assert 'noopener' in a.get('rel',''),'Unsafe external window'
 def handle_endtag(self,t):
  if t=='script':self.script=False
  if t=='title':self.in_title=False
 def handle_data(self,d):
  if self.in_title:self.title+=d
  if self.script:self.structured+=d
for f in root.rglob('index.html'):
 try:
  p=Page();p.feed(f.read_text());assert p.h1==1,'Heading count';assert p.meta.get('description'),'Description absent';assert p.meta.get('og:image'),'OG image absent'
  schema=json.loads(p.structured);assert schema['@graph'],'Missing schema graph'
  digest=base64.b64encode(hashlib.sha256(p.structured.encode()).digest()).decode()
  assert "'sha256-"+digest+"'" in p.meta['Content-Security-Policy'],'JSON-LD hash mismatch'
  assert "script-src 'self'" in p.meta['Content-Security-Policy'];assert 'unsafe-inline' not in p.meta['Content-Security-Policy']
  titles.append(p.title);descriptions.append(p.meta['description'])
 except Exception as ex:errors.append(str(f.relative_to(root))+': '+str(ex))
assert len(titles)==len(set(titles)),'Duplicate page titles'
assert len(descriptions)==len(set(descriptions)),'Duplicate meta descriptions'
products=json.loads((root/'data/products.json').read_text());assert {p['code'] for p in products}=={f'BB-{x}' for x in range(1001,1192)}
urls=ET.parse(root/'sitemap.xml').getroot();assert len(urls)==206
assert not (root/'assets/images').exists(),'Original JPEG assets leaked'
result={'pages':len(titles),'product_codes':len(products),'sitemap_urls':len(urls),'unique_titles':len(set(titles)),'unique_descriptions':len(set(descriptions)),'errors':errors,'checks':['local links/assets','image alt/dimensions','JSON-LD parsing','CSP hashes','no inline executable code, event handlers or CSS','noopener','single H1','unique titles and descriptions','sitemap','product inventory']}
(Path(__file__).parent/'structural-results.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));assert not errors
