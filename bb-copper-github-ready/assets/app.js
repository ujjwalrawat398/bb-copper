document.querySelector('.menu-toggle')?.addEventListener('click',function(){const open=document.querySelector('.links').classList.toggle('open');this.setAttribute('aria-expanded',String(open));});
const search=document.querySelector('#search'), filter=document.querySelector('#photo-filter');
function applyFilters(){let total=0;document.querySelectorAll('#catalog .product-card').forEach(card=>{const match=card.dataset.search.includes((search?.value||'').trim().toLowerCase())&&(!filter||filter.value==='all'||card.dataset.photo===filter.value);card.hidden=!match;if(match)total++;});if(document.querySelector('#count'))document.querySelector('#count').textContent=total;if(document.querySelector('#empty'))document.querySelector('#empty').hidden=total>0;}
search?.addEventListener('input',applyFilters);filter?.addEventListener('change',applyFilters);
let config;
function getConfig(){return config ||= fetch('/data/site.json').then(r=>{if(!r.ok)throw Error('Configuration could not load');return r.json();}).then(site=>{if(!/^\d{10,15}$/.test(site.whatsapp)||new URL(site.domain).protocol!=='https:')throw Error('Invalid contact configuration');return site;}).catch(error=>{config=null;throw error;});}
document.querySelectorAll('.enquiry').forEach(form=>form.addEventListener('submit',async event=>{event.preventDefault();if(!form.reportValidity())return;const name=form.elements.name.value.trim();if(!name){form.elements.name.setCustomValidity('Please enter your name.');form.elements.name.reportValidity();return;}const button=form.querySelector('button');button.disabled=true;const newWindow=window.open('about:blank','_blank');if(newWindow)newWindow.opener=null;try{const site=await getConfig(),p=JSON.parse(form.dataset.product);const origin=site.domain.replace(/\/$/,'');const text=['Hello BB Copper, I am interested in this product.','','Product: '+p.name,'Item Code: '+p.code,'Category: '+p.categoryName,'Image: '+(p.image?origin+p.image:'Photo not yet available'),'Page: '+origin+location.pathname,'','Name: '+name,'Quantity / Message: '+(form.elements.message.value.trim()||'-')].join('\n');const link='https://wa.me/'+site.whatsapp+'?text='+encodeURIComponent(text);if(newWindow){newWindow.opener=null;newWindow.location.replace(link);}else{location.assign(link);}}catch(error){newWindow?.close();alert('Unable to prepare your enquiry. Please use the WhatsApp contact button.');}finally{button.disabled=false;}}));
document.querySelectorAll('input[name="name"]').forEach(input=>input.addEventListener('input',()=>input.setCustomValidity('')));

document.addEventListener('keydown',event=>{if(event.key==='Escape'){document.querySelector('.links')?.classList.remove('open');document.querySelector('.menu-toggle')?.setAttribute('aria-expanded','false');}});
document.querySelectorAll('.links a').forEach(a=>a.addEventListener('click',()=>{document.querySelector('.links').classList.remove('open');document.querySelector('.menu-toggle').setAttribute('aria-expanded','false');}));
// Native document history is preserved; direct/external entry uses the safe anchor fallback.
document.querySelector('[data-back]')?.addEventListener('click',event=>{
  if(event.button!==0||event.ctrlKey||event.metaKey||event.shiftKey||event.altKey)return;
  let internal=false;
  try{internal=!!document.referrer&&new URL(document.referrer).origin===location.origin;}catch{}
  if(internal&&history.length>1){event.preventDefault();history.back();}
});
// Restore catalogue filters after visiting a product, without adding history entries.
if(search){
 const key='bb-catalogue:'+location.pathname;
 try{const saved=JSON.parse(sessionStorage.getItem(key)||'null');if(saved){search.value=saved.search||'';filter.value=saved.filter==='yes'?'yes':'all';applyFilters();}}catch{}
 const save=()=>{try{sessionStorage.setItem(key,JSON.stringify({search:search.value,filter:filter.value}));}catch{}};
 search.addEventListener('input',save);filter?.addEventListener('change',save);
 window.addEventListener('pageshow',applyFilters);
}
