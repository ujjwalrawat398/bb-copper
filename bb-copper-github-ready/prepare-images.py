from pathlib import Path
from PIL import Image
import json
root=Path(__file__).parent
source=root/'assets/source/catalogue'
def crop(name,out,box=None,width=1400):
 im=Image.open(source/name).convert('RGB')
 if box:im=im.crop(tuple(round(v*s) for v,s in zip(box,(im.width,im.height,im.width,im.height))))
 im.thumbnail((width,1600));im.save(root/'assets/lifestyle'/out,'WEBP',quality=84)
for name,out,box in [
('page-01-cover.jpg','signature-set.webp',(0,.29,1,.89)),
('page-03-hero-copper-bottles.jpg','bottles.webp',(0,.235,1,1)),
('page-06-hero-amazing-experience.jpg','bottle-detail.webp',(0,.04,.625,.96)),
('page-07-feature-black-etching-bottle-BB-1030.jpg','black-etching.webp',(.065,.575,.94,.98)),
('page-08-hero-copper-mugs.jpg','mugs.webp',(.008,.265,1,.93)),
('page-09-hero-hammered-glass.jpg','glass.webp',(0,.25,1,1)),
('page-13-hero-handcrafted-lota.jpg','lota.webp',(.025,.415,.97,1)),
('page-17-hero-hammered-matka-BB-1143.jpg','matka.webp',(0,.015,.95,.99)),
('page-21-hero-gift-packs-group.jpg','gift-packs.webp',(.01,.19,.95,.98)),
('page-24-back-cover-all-products.jpg','collection.webp',(.07,.285,.92,.72)),
('page-02-about.jpg','about-detail.webp',(0,.56,.405,.975))]:crop(name,out,box)
im=Image.open(source/'page-07-feature-black-etching-bottle-BB-1030.jpg').convert('RGBA')
w,h=im.size;im=im.crop((round(w*.382),round(h*.058),round(w*.617),round(h*.202)))
pixels=[]
for r,g,b,a in im.getdata():
 # Remove neutral white only, retaining copper gradients and black lettering.
 if min(r,g,b)>235:a=round(255*(255-min(r,g,b))/20)
 pixels.append((r,g,b,a))
im.putdata(pixels);im.save(root/'assets/brand/logo-official.png')
mark=im.crop((45,0,im.width-45,round(im.height*.64)))
for size in (32,180,512):
 canvas=Image.new('RGBA',(size,size),(250,247,242,255));m=mark.copy();m.thumbnail((int(size*.9),int(size*.9)));canvas.alpha_composite(m,((size-m.width)//2,(size-m.height)//2));canvas.save(root/f'assets/brand/icon-{size}.png')
p=root/'src/data/products.json';data=json.loads(p.read_text())
for item in data:
 if item['code']=='BB-1143':item['image']='/assets/lifestyle/matka.webp';item['note']='Catalogue lifestyle photograph for item BB-1143.'
p.write_text(json.dumps(data,indent=2,ensure_ascii=False))
