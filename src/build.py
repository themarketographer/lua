# -*- coding: utf-8 -*-
import os,sys,subprocess,datetime,html,re
HERE=os.path.dirname(os.path.abspath(__file__))
ROOT=os.path.dirname(HERE)+'/'
os.chdir(HERE)
sys.path.insert(0,HERE)
from posts import POSTS
SITE="https://studiolua.netlify.app"
TODAY="2026-10-08"
PIXEL="1559106775456296"
# --- 1) landing
import base64,io
from PIL import Image
def img(p,w=1000,q=72):
    # WebP externo en /assets/img/ (cacheable y sin duplicar la misma foto en el HTML)
    im=Image.open('images/'+p).convert('RGB');im.thumbnail((w,w*2))
    os.makedirs(ROOT+'assets/img',exist_ok=True);n=os.path.splitext(p)[0]+'.webp'
    im.save(ROOT+'assets/img/'+n,'WEBP',quality=q,method=6)
    return '/assets/img/'+n
def font(p): return 'data:font/otf;base64,'+base64.b64encode(open('fonts/'+p,'rb').read()).decode()
def png(p): return 'data:image/png;base64,'+base64.b64encode(open(ROOT+'assets/'+p,'rb').read()).decode()
import json
FAQ_HOME=[
("¿Qué es la onicofagia?","Es el hábito compulsivo de morderse las uñas, muchas veces de forma inconsciente, hasta causar daño visible en las manos."),
("¿Qué lo causa?","La onicofagia suele estar relacionada con la ansiedad, el estrés, el aburrimiento o la necesidad de calmarse en momentos de tensión emocional."),
("¿Cómo puedo tratarlo?","Con uñas diseñadas para proteger mientras sanas el hábito. En LÜA cuidamos tus manos sin juicio."),
("¿Cuánto cuesta una cita en LÜA?","El pintado en gel cuesta desde Bs 70, el soft gel desde Bs 100, la reconstrucción con gel desde Bs 100 y el relleno desde Bs 80. El precio sube según la duración y el nivel de diseño que elijas."),
("¿Cuánto dura una cita?","Dura 2 horas con color entero, 3 horas con diseño sencillo y 4 horas con diseño complejo. En el calendario eliges la duración que corresponde."),
("¿Qué servicio elijo si tengo las uñas mordidas?","Si tus uñas están muy cortas, partidas o dañadas, la reconstrucción con gel las rehace uña por uña. Si tienen algo de largo y quieres cobertura, el soft gel funciona bien. Si solo quieres color sobre tu uña natural, el pintado en gel."),
("¿Qué pasa si ya traigo material puesto?","Si tu cita incluye retiro de material, reserva entre 1 y 1,5 horas extra además del servicio."),
("¿Dónde están y qué horario tienen?","En Av. Papapulo, Edificio Torre Isos, Depto 7C, Cochabamba, de 9:00 a 17:00."),
("¿Cómo reservo?","Eliges tu servicio en la sección de precios, reservas tu horario en el calendario con al menos 24 horas de anticipación y confirmas por WhatsApp."),
]
def faq_ld(items): return {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in items]}
_SV=[("pintado","Pintado en gel","Color en gel sobre tu uña natural.",70,90),("softgel","Soft gel","Uñas diseñadas para proteger mientras sanas el hábito.",100,140),("reconstruccion","Reconstrucción con gel","Reconstruimos uña por uña lo que el hábito dañó.",100,150),("cita-de-relleno-de-sofgel-o-reconstruccion","Relleno","Mantenimiento de un soft gel o una reconstrucción.",80,120)]
HOME_LD=[
 {"@context":"https://schema.org","@type":"HealthAndBeautyBusiness","@id":SITE+"/#negocio","name":"LÜA by Andy Villarroel","description":"Estudio de uñas especializado en onicofagia en Cochabamba, Bolivia.","url":SITE+"/","image":SITE+"/assets/og.jpg","logo":SITE+"/assets/icon-192.png","telephone":"+59178109113","priceRange":"Bs 70 a Bs 150","currenciesAccepted":"BOB","areaServed":{"@type":"City","name":"Cochabamba"},"knowsAbout":["Onicofagia","Uñas en gel","Soft gel","Reconstrucción de uñas"],
  "address":{"@type":"PostalAddress","streetAddress":"Av. Papapulo, Edificio Torre Isos, Depto 7C","addressLocality":"Cochabamba","addressCountry":"BO"},
  "founder":{"@type":"Person","name":"Andy Villarroel"},
  "potentialAction":{"@type":"ReserveAction","target":{"@type":"EntryPoint","urlTemplate":"https://cal.com/lua.nails"},"result":{"@type":"Reservation","name":"Reservar cita"}},
  "hasOfferCatalog":{"@type":"OfferCatalog","name":"Servicios","itemListElement":[{"@type":"Offer","priceCurrency":"BOB","priceSpecification":{"@type":"PriceSpecification","minPrice":lo,"maxPrice":hi,"priceCurrency":"BOB"},"itemOffered":{"@type":"Service","name":n,"description":d,"provider":{"@id":SITE+"/#negocio"}}} for _,n,d,lo,hi in _SV]}},
 {"@context":"https://schema.org","@type":"WebSite","@id":SITE+"/#sitio","name":"LÜA by Andy Villarroel","url":SITE+"/","inLanguage":"es","publisher":{"@id":SITE+"/#negocio"}},
 dict({"@context":"https://schema.org"},**faq_ld(FAQ_HOME)),
]
FAQ_HTML="\n".join(f'      <details class="rv"{(" style=%s--d:%dms%s"%(chr(34),i*80,chr(34))) if i else ""}><summary><span>{html.escape(q)}</span></summary><p>{html.escape(a)}</p></details>' for i,(q,a) in enumerate(FAQ_HOME))
m={'i_statue':img('statue-red-nails.jpg'),'i_bitten':img('bitten-dark.jpg',900),'i_brush':img('gel-brush.jpg'),'i_tools':img('tools-steel.jpg'),'i_nude':img('nails-nude.jpg'),'i_rose':img('nails-rose.jpg'),'i_torn':img('torn-paper-hands.jpg',1400,65),
'f_light':font('QuincyCF-Light.otf'),'f_reg':font('QuincyCF-Regular.otf'),'f_med':font('QuincyCF-Medium.otf'),'f_bold':font('QuincyCF-Bold.otf'),'f_ital':font('QuincyCF-RegularItalic.otf'),'f_text':font('QuincyCFText-Regular.otf'),
'i_logo':png('logo-ivory.png'),'i_logo_nav':png('logo.png'),'BOOK':'https://cal.com/lua.nails','WA':'','pixel_js':open(ROOT+'assets/pixel.js').read(),'ld_home':json.dumps(HOME_LD,ensure_ascii=False),'faq_html':FAQ_HTML}
t=open('tpl.html').read()
for k,v in m.items(): t=t.replace('@'+k+'@',v)
ns={'t':t}
open(ROOT+'index.html','w').write(t)
# --- 2) blog
HEAD="""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<link rel="canonical" href="{url}"><meta name="theme-color" content="#150a0d">
<meta property="og:type" content="{ogtype}"><meta property="og:locale" content="es_BO"><meta property="og:site_name" content="LÜA by Andy Villarroel">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{site}/assets/og.jpg"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title}"><meta name="twitter:description" content="{desc}">{extra}
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300..700;1,6..72,300..700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/blog.css">
{ld}
<script src="/assets/pixel.js"></script>
<script>{evt}</script>
<noscript><img height="1" width="1" style="display:none" alt="" src="https://www.facebook.com/tr?id={pixel}&ev=PageView&noscript=1"></noscript>
</head><body>
<header class="top"><a href="/"><img src="/assets/logo.png" alt="LÜA by Andy Villarroel" width="110" height="38"></a><a class="cta" href="/#precios">Agenda tu sesión</a></header>
"""
FOOT="""<footer>© 2026 LÜA by Andy Villarroel · Av. Papapulo, Edificio Torre Isos, Depto 7C, Cochabamba · De 9:00 a 17:00<br><a href="/privacidad/">Privacidad</a><br><br>Este contenido es informativo. Si tienes dolor, enrojecimiento, hinchazón o pus alrededor de la uña, consulta con un profesional de salud.</footer></body></html>"""
import json
def page(title,desc,url,body,ld,evt,ogtype="article",extra=""):
    return HEAD.format(title=html.escape(title),desc=html.escape(desc),url=url,site=SITE,ld=ld,evt=evt,pixel=PIXEL,ogtype=ogtype,extra=extra)+body+FOOT

FAQ_POSTS={
"onicofagia-por-que-me-como-las-unas":[
("¿Qué es la onicofagia?","Es el hábito compulsivo de morderse las uñas, muchas veces de forma inconsciente, hasta causar daño visible en las manos."),
("¿Qué dispara la onicofagia?","Suele estar relacionada con la ansiedad, el estrés, el aburrimiento o la necesidad de calmarse en momentos de tensión emocional."),
("¿Cuándo debo consultar a un profesional de salud?","Si notas dolor, enrojecimiento, hinchazón o pus alrededor de la uña, o si el hábito va acompañado de mucha ansiedad.")],
"como-dejar-de-comerte-las-unas":[
("¿Cómo puedo dejar de comerme las uñas?","Funciona mejor con varios cambios pequeños al mismo tiempo: observar cuándo muerdes, mantener las uñas limadas, darle otra tarea a tus manos, hidratar el contorno, poner una barrera sobre la uña, elegir una meta pequeña y tratarte con respeto."),
("¿Sirve una cobertura de gel para dejar de morderse las uñas?","Sí. Una capa de gel aplicada por una profesional mantiene la uña cubierta y te avisa antes del mordisco mientras el hábito se va aflojando."),
("¿Qué hago si recaigo?","Una recaída pasa y no borra lo avanzado. Si te muerdes la uña un martes, retoma el miércoles.")],
"primera-sesion-pintado-soft-gel-reconstruccion":[
("¿Cuánto cuesta cada servicio en LÜA?","El pintado en gel cuesta desde Bs 70, el soft gel desde Bs 100, la reconstrucción con gel desde Bs 100 y el relleno desde Bs 80."),
("¿Cuánto tiempo debo reservar?","Entre 2 y 4 horas según el diseño: 2 horas color entero, 3 horas diseño sencillo, 4 horas diseño complejo. Si tu sesión incluye retiro de un trabajo anterior, reserva más tiempo."),
("¿Qué servicio elijo para mi primera sesión?","Pintado en gel si tienes algo de largo, soft gel si la uña es muy corta y quieres cobertura y forma, y reconstrucción con gel si hay daño visible que necesita recuperar estructura."),
("¿Dónde y cuándo atienden?","En Av. Papapulo, Edificio Torre Isos, Depto 7C, Cochabamba, de 9:00 a 17:00.")],
}
def faq_block(slug):
    f=FAQ_POSTS[slug]
    return '<div class="faq-post"><h2>Preguntas frecuentes</h2>'+''.join(f'<h3>{html.escape(q)}</h3><p>{html.escape(a)}</p>' for q,a in f)+'</div>'
os.makedirs(ROOT+'blog',exist_ok=True)
for p in POSTS:
    url=f"{SITE}/blog/{p['slug']}/"
    others=''.join(f'<a href="/blog/{o["slug"]}/">{html.escape(o["title"])}</a>' for o in POSTS if o['slug']!=p['slug'])
    words=len(re.sub(r'<[^>]+>',' ',p['body']).split())
    art={"@context":"https://schema.org","@type":"Article","headline":p['title'],"description":p['desc'],"datePublished":TODAY,"dateModified":TODAY,"inLanguage":"es","wordCount":words,"articleSection":p['tag'],"mainEntityOfPage":url,"image":{"@type":"ImageObject","url":SITE+"/assets/og.jpg","width":1200,"height":630},"author":{"@type":"Person","name":"Andy Villarroel","url":SITE+"/"},"publisher":{"@type":"Organization","name":"LÜA by Andy Villarroel","logo":{"@type":"ImageObject","url":SITE+"/assets/icon-192.png"}},"about":{"@type":"Thing","name":"Onicofagia"}}
    bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Inicio","item":SITE+"/"},{"@type":"ListItem","position":2,"name":"Blog","item":SITE+"/blog/"},{"@type":"ListItem","position":3,"name":p['title'],"item":url}]}
    fq=dict({"@context":"https://schema.org"},**faq_ld(FAQ_POSTS[p['slug']]))
    ld=''.join('<script type="application/ld+json">'+json.dumps(x,ensure_ascii=False)+'</script>' for x in (art,bc,fq))
    evt='window.addEventListener("load",function(){if(!window.LUA)return;LUA.track("ViewContent",{content_name:%s,content_category:"Blog"},{server:true});LUA.track("BlogView",{post:"%s"},{custom:true});var m=[50,90];addEventListener("scroll",function(){var h=document.documentElement,p=(h.scrollTop+innerHeight)/h.scrollHeight*100;m=m.filter(function(x){if(p>=x){LUA.track("BlogScroll"+x,{post:"%s"},{custom:true});return false}return true})},{passive:true})});document.addEventListener("click",function(e){if(!window.LUA)return;var t=e.target.closest&&e.target.closest("a");if(!t)return;var h=t.getAttribute("href")||"";if(h.indexOf("/#precios")===0)LUA.track("AgendaCTA",{location:"blog",post:"%s"},{custom:true});else if(h.indexOf("/blog/")===0)LUA.track("BlogClick",{post:h.split("/")[2],from:"%s"},{custom:true})},true);'%(json.dumps(p['title'],ensure_ascii=False),p['slug'],p['slug'],p['slug'],p['slug'])
    body=f'''<main><nav class="breadcrumb" aria-label="Ruta"><a href="/">Inicio</a> · <a href="/blog/">Blog</a> · {html.escape(p['title'])}</nav><article><div class="kicker">{p['tag']} · {p['read']} de lectura</div><h1>{html.escape(p['title'])}</h1><div class="meta">Por Andy Villarroel · 8 de octubre de 2026</div>{p['body']}
{faq_block(p['slug'])}
<div class="cta-box"><h2>Tus uñas ya pueden sonreír</h2><p>Reserva tu sesión y elige el servicio que va con tu momento.</p><a class="btn" href="/#precios">Agenda tu sesión</a></div>
<div class="more"><div class="kicker" style="padding-top:20px">Sigue leyendo</div>{others}</div></article></main>'''
    d=ROOT+f'blog/{p["slug"]}';os.makedirs(d,exist_ok=True)
    open(d+'/index.html','w').write(page(p['title']+' | LÜA',p['desc'],url,body,ld,evt,extra=f'<meta property="article:published_time" content="{TODAY}"><meta property="article:author" content="Andy Villarroel"><meta property="article:section" content="{p["tag"]}">'))
items=''.join(f'<a class="item" href="/blog/{p["slug"]}/"><div class="kicker">{p["tag"]} · {p["read"]}</div><h2>{html.escape(p["title"])}</h2><p>{html.escape(p["desc"])}</p></a>' for p in POSTS)
body=f'<main><div class="kicker">Blog LÜA</div><h1>Aprende a cuidar tus manos</h1><p class="lede">Artículos sobre onicofagia, hábitos y cuidado de las uñas, escritos por Andy Villarroel.</p><div class="list">{items}</div></main>'
bl={"@context":"https://schema.org","@type":"Blog","name":"Blog LÜA","url":SITE+"/blog/","inLanguage":"es","publisher":{"@type":"Organization","name":"LÜA by Andy Villarroel"},"blogPost":[{"@type":"BlogPosting","headline":p['title'],"url":f"{SITE}/blog/{p['slug']}/","description":p['desc']} for p in POSTS]}
il={"@context":"https://schema.org","@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"url":f"{SITE}/blog/{p['slug']}/","name":p['title']} for i,p in enumerate(POSTS)]}
bcl={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Inicio","item":SITE+"/"},{"@type":"ListItem","position":2,"name":"Blog","item":SITE+"/blog/"}]}
ld=''.join('<script type="application/ld+json">'+json.dumps(x,ensure_ascii=False)+'</script>' for x in (bl,il,bcl))
evt='window.addEventListener("load",function(){if(window.LUA)LUA.track("ViewContent",{content_name:"Blog",content_category:"Blog"},{server:true})});document.addEventListener("click",function(e){var t=e.target.closest&&e.target.closest("a.item");if(t&&window.LUA)LUA.track("BlogClick",{post:t.getAttribute("href").split("/")[2],from:"indice"},{custom:true})},true);'
open(ROOT+'blog/index.html','w').write(page('Blog LÜA | Onicofagia y cuidado de uñas','Artículos sobre onicofagia, hábitos y cuidado de las uñas, por Andy Villarroel en Cochabamba.',SITE+'/blog/',body,ld,evt,"website"))
# --- 3) paginas extra: gracias, privacidad, camino sin Cal
import re,urllib.parse
WA_NUM="59178109113"
NAMES={"pintado":"Pintado en gel","softgel":"Soft gel","reconstruccion":"Reconstrucción con gel","cita-de-relleno-de-sofgel-o-reconstruccion":"Relleno"}
PRICES={"pintado":{120:70,180:80,240:90},"softgel":{120:100,180:120,240:140},"reconstruccion":{120:100,180:120,240:150},"cita-de-relleno-de-sofgel-o-reconstruccion":{120:80,180:100,240:120}}
def noidx(h): return h.replace('<meta charset="utf-8">','<meta charset="utf-8"><meta name="robots" content="noindex,nofollow">',1)

# 3a) /ads/: misma landing, pero los precios abren WhatsApp (sin Cal) y miden Lead + Contact
def to_wa(m):
    slug,dur=m.group(3),m.group(5)
    txt=f"Hola, quiero reservar mi cita de {NAMES[slug]}"+(f" ({int(dur)//60} h)" if dur else "")
    url=f"https://api.whatsapp.com/send?phone={WA_NUM}&text="+urllib.parse.quote(txt)
    return f'<a {m.group(1) or ""}href="{url}" data-wa="{html.escape(txt)}" data-svc="{slug}" data-min="{m.group(6)}"'
ads=re.sub(r'<a (class="btn cta" )?href="(https://cal\.com/lua\.nails/([a-z\-]+))(\?duration=(\d+))?" data-svc="[a-z\-]+" data-min="(\d+)"',to_wa,t)
ads=ads.replace('<script>/* LÜA tracking base','<script>window.LUA_MODE="wa";</script><script>/* LÜA tracking base',1)
assert 'LUA_MODE="wa"' in ads and 'cal.com/lua.nails/pintado' not in ads, 'camino WhatsApp mal generado'
os.makedirs(ROOT+'ads',exist_ok=True)
open(ROOT+'ads/index.html','w').write(noidx(ads))

# 3b) /gracias-cita/: a donde manda Cal.com despues de reservar. Mide Purchase y Contact, y abre WhatsApp.
GRJS='''document.addEventListener("DOMContentLoaded",function(){
var q=new URLSearchParams(location.search),PR=%s,NM=%s;
var slug=q.get("eventTypeSlug")||"",start=q.get("startTime")||"",end=q.get("endTime")||"";
var mins=start&&end?Math.round((new Date(end)-new Date(start))/60000):0;
var val=(PR[slug]||{})[mins]||0,name=NM[slug]||q.get("title")||"tu cita";
var eid=q.get("metadata[eid]")||LUA.uid();
var r=document.getElementById("resumen");
if(start){try{r.textContent=name+" · "+new Date(start).toLocaleString("es-BO",{timeZone:"America/La_Paz",dateStyle:"full",timeStyle:"short"})}catch(e){}}
var a=document.getElementById("wa"),cd=document.getElementById("cd"),sent=0,timer;
a.href=LUA.wa(LUA.WA_CONFIRM);
function contact(){if(!sent){sent=1;LUA.track("Contact",{content_name:name,content_category:"Servicios"},{id:eid+"-ct",server:true})}}
a.addEventListener("click",function(){clearTimeout(timer);cd.textContent="";contact()});
/* sin startTime = alguien entro directo, no una reserva: no se mide ni se redirige */
if(!start)return;
var key="lua_pur_"+slug+start; /* evita contar de nuevo si recarga la pagina */
if(!LUA.store(key)){LUA.store(key,"1");LUA.track("Purchase",{content_name:name,content_category:"Servicios",content_ids:[slug],value:val,currency:"BOB"},{id:eid+"-pur",server:true})}
cd.textContent="Te llevamos a WhatsApp en unos segundos…";
timer=setTimeout(function(){contact();location.href=a.href},4000);
});'''%(json.dumps(PRICES),json.dumps(NAMES,ensure_ascii=False))
os.makedirs(ROOT+'gracias-cita',exist_ok=True)
# la pagina de gracias reusa la cabecera (CSS, fuentes, pixel), el nav y el footer de la landing
head=t[:t.index('<body>')]
head=re.sub(r'<script type="application/ld\+json">.*?</script>\n?','',head,flags=re.S)
head=head.replace('<title>LÜA · Uñas con onicofagia en Cochabamba</title>','<title>¡Cita agendada! | LÜA</title>')
head=head.replace('<link rel="canonical" href="https://studiolua.netlify.app/">','<link rel="canonical" href="https://studiolua.netlify.app/gracias-cita/">')
nav=t[t.index('<nav class="top glass"'):t.index('</nav>')+6].replace('href="#top"','href="/"').replace('href="#precios" data-cta>Agenda tu sesión','href="/">Volver al inicio')
foot=t[t.index('<footer class="foot'):t.index('</footer>')+9]
GR=f'''<body>
{nav}
<main id="top">
<section class="wine grain final" data-spot>
  <div class="spot"></div>
  <div class="photo"><img src="/assets/img/torn-paper-hands.webp" alt="" aria-hidden="true" width="1400" height="933"></div>
  <i class="orb" style="width:520px;height:520px;left:-120px;top:-160px;background:radial-gradient(circle at 35% 30%,rgba(179,143,111,.45),transparent 70%)"></i>
  <div class="wrap" style="position:relative;z-index:2">
    <div class="big eyes" aria-hidden="true"><i class="eye"></i><i class="eye"></i></div>
    <h1>Tu cita quedó <em>agendada</em></h1>
    <p class="lead" id="resumen">Recibirás la confirmación en tu correo.</p>
    <div class="cta-row"><a class="btn" id="wa" href="#">Confirmar por WhatsApp <span class="eyes" aria-hidden="true"><i class="eye"></i><i class="eye"></i></span></a></div>
    <p id="cd" style="margin-top:22px;font-size:16px;opacity:.7"></p>
    <p style="margin-top:10px;font-size:16px;opacity:.6">Si necesitas mover tu cita, usa el enlace del correo de confirmación.</p>
  </div>
</section>
</main>
{foot}
<script>{GRJS}</script>
</body></html>'''
os.makedirs(ROOT+'gracias-cita',exist_ok=True)
open(ROOT+'gracias-cita/index.html','w').write(noidx(head+GR))

# 3b2) 404.html: Netlify la sirve sola cuando una ruta no existe. Rutas absolutas porque se muestra en cualquier URL.
h404=head.replace('<title>¡Cita agendada! | LÜA</title>','<title>Página no encontrada | LÜA</title>').replace('/gracias-cita/">','/">')
NF=f'''<body>
{nav}
<main id="top">
<section class="wine grain final" data-spot>
  <div class="spot"></div>
  <div class="photo"><img src="/assets/img/torn-paper-hands.webp" alt="" aria-hidden="true" width="1400" height="933"></div>
  <i class="orb" style="width:520px;height:520px;left:-120px;top:-160px;background:radial-gradient(circle at 35% 30%,rgba(179,143,111,.45),transparent 70%)"></i>
  <div class="wrap" style="position:relative;z-index:2">
    <div class="big eyes" aria-hidden="true"><i class="eye"></i><i class="eye"></i></div>
    <h1>Esta página <em>no existe</em></h1>
    <p class="lead">Pero tus uñas sí pueden tener arreglo.</p>
    <div class="cta-row"><a class="btn" href="/">Volver al inicio <span class="eyes" aria-hidden="true"><i class="eye"></i><i class="eye"></i></span></a><a class="btn btn--ghost" href="/blog/">Leer el blog</a></div>
  </div>
</section>
</main>
{foot}
</body></html>'''
open(ROOT+'404.html','w').write(noidx(h404+NF))

# 3c) /privacidad/ (Meta lo exige si hay Pixel)
PV='''<main><div class="kicker">Legal</div><h1>Política de privacidad</h1><div class="meta">Última actualización: 10 de noviembre de 2026</div>
<p>Este sitio es de LÜA by Andy Villarroel, Av. Papapulo, Edificio Torre Isos, Depto 7C, Cochabamba, Bolivia.</p>
<h2>Qué datos recogemos</h2><p>Datos de navegación (páginas que visitas, botones que tocas, de qué anuncio llegas) mediante el Pixel de Meta y su API de conversiones. Cuando reservas, Cal.com nos entrega tu nombre, correo y teléfono, que tú escribes voluntariamente.</p>
<h2>Para qué los usamos</h2><p>Para agendar tu cita, responderte por WhatsApp, medir qué anuncios funcionan y mostrarte publicidad relevante en Facebook e Instagram.</p>
<h2>Con quién se comparten</h2><p>Con Meta (datos de navegación y, cifrados, los de tu reserva) y con Cal.com (agenda). No vendemos tus datos.</p>
<h2>Cómo desactivar el seguimiento</h2><p>Puedes bloquear cookies desde tu navegador o desactivar anuncios personalizados en la configuración de tu cuenta de Facebook o Instagram.</p>
<h2>Cómo pedir que borremos tus datos</h2><p>Escríbenos por WhatsApp al +591 78109113 y los eliminamos.</p></main>'''
os.makedirs(ROOT+'privacidad',exist_ok=True)
open(ROOT+'privacidad/index.html','w').write(page('Política de privacidad | LÜA','Qué datos recoge LÜA by Andy Villarroel, para qué los usa y cómo pedir que se borren.',SITE+'/privacidad/',PV,'','',"website"))

# sitemap, robots, llms.txt, ai.txt
urls=[SITE+'/',SITE+'/blog/']+[f"{SITE}/blog/{p['slug']}/" for p in POSTS]+[SITE+'/privacidad/']
open(ROOT+'sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>\n' for u in urls)+'</urlset>\n')
bots=''.join(f'User-agent: {b}\nAllow: /\n\n' for b in ['GPTBot','ChatGPT-User','OAI-SearchBot','ClaudeBot','Claude-Web','PerplexityBot','Google-Extended','Applebot-Extended'])
open(ROOT+'robots.txt','w').write(f'User-agent: *\nAllow: /\nDisallow: /.netlify/\nDisallow: /gracias-cita\nDisallow: /ads\n\n{bots}Sitemap: {SITE}/sitemap.xml\n')
posts_md=''.join(f"  - [{p['title']}]({SITE}/blog/{p['slug']}/): {p['desc']}\n" for p in POSTS)
open(ROOT+'llms.txt','w').write(f"""# LÜA by Andy Villarroel

> Estudio de uñas en Cochabamba, Bolivia, especializado en onicofagia (el hábito de morderse las uñas). Pintado en gel, soft gel, reconstrucción con gel y relleno, desde Bs 70, con reserva online.

LÜA trabaja uñas mordidas, cortas o dañadas con técnicas seguras que cuidan la uña natural. Atiende Andy Villarroel en Av. Papapulo, Edificio Torre Isos, Depto 7C, Cochabamba, de 9:00 a 17:00.

## Páginas principales

- [Inicio]({SITE}/): servicios, precios en bolivianos y reserva.
- [Blog]({SITE}/blog/): artículos sobre onicofagia y cuidado de las uñas.
{posts_md}- [Privacidad]({SITE}/privacidad/): qué datos recoge el sitio.

## Contacto

Reservas: https://cal.com/lua.nails
WhatsApp: https://api.whatsapp.com/send?phone={WA_NUM}
""")
open(ROOT+'ai.txt','w').write('User-agent: *\nAllow: /\nPurpose: training, search, citation\n')
print('built',len(ns['t'])//1024,'KB landing,',len(POSTS),'posts')
