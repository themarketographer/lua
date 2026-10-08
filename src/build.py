# -*- coding: utf-8 -*-
import os,sys,subprocess,datetime,html
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
    im=Image.open('images/'+p).convert('RGB');im.thumbnail((w,w*2));bb=io.BytesIO();im.save(bb,'JPEG',quality=q,optimize=True,progressive=True)
    return 'data:image/jpeg;base64,'+base64.b64encode(bb.getvalue()).decode()
def font(p): return 'data:font/otf;base64,'+base64.b64encode(open('fonts/'+p,'rb').read()).decode()
def png(p): return 'data:image/png;base64,'+base64.b64encode(open(ROOT+'assets/'+p,'rb').read()).decode()
m={'i_statue':img('statue-red-nails.jpg'),'i_bitten':img('bitten-dark.jpg',900),'i_brush':img('gel-brush.jpg'),'i_tools':img('tools-steel.jpg'),'i_nude':img('nails-nude.jpg'),'i_rose':img('nails-rose.jpg'),'i_torn':img('torn-paper-hands.jpg',1400,65),
'f_light':font('QuincyCF-Light.otf'),'f_reg':font('QuincyCF-Regular.otf'),'f_med':font('QuincyCF-Medium.otf'),'f_bold':font('QuincyCF-Bold.otf'),'f_ital':font('QuincyCF-RegularItalic.otf'),'f_text':font('QuincyCFText-Regular.otf'),
'i_logo':png('logo-ivory.png'),'i_logo_nav':png('logo.png'),'BOOK':'https://cal.com/lua.nails','WA':'','pixel_js':open(ROOT+'assets/pixel.js').read()}
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
<meta property="og:image" content="{site}/assets/og.jpg"><meta name="twitter:card" content="summary_large_image">
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
FOOT="""<footer>© 2026 LÜA by Andy Villarroel · Av. Papapulo, Edificio Torre Isos, Depto 7C, Cochabamba · De 9:00 a 17:00<br><br>Este contenido es informativo. Si tienes dolor, enrojecimiento, hinchazón o pus alrededor de la uña, consulta con un profesional de salud.</footer></body></html>"""
import json
def page(title,desc,url,body,ld,evt,ogtype="article"):
    return HEAD.format(title=html.escape(title),desc=html.escape(desc),url=url,site=SITE,ld=ld,evt=evt,pixel=PIXEL,ogtype=ogtype)+body+FOOT
os.makedirs(ROOT+'blog',exist_ok=True)
for p in POSTS:
    url=f"{SITE}/blog/{p['slug']}/"
    others=''.join(f'<a href="/blog/{o["slug"]}/">{html.escape(o["title"])}</a>' for o in POSTS if o['slug']!=p['slug'])
    ld='<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"Article","headline":p['title'],"description":p['desc'],"datePublished":TODAY,"dateModified":TODAY,"inLanguage":"es","mainEntityOfPage":url,"image":SITE+"/assets/og.jpg","author":{"@type":"Person","name":"Andy Villarroel"},"publisher":{"@type":"Organization","name":"LÜA by Andy Villarroel","logo":{"@type":"ImageObject","url":SITE+"/assets/icon-192.png"}}},ensure_ascii=False)+'</script>'
    evt='window.addEventListener("load",function(){if(window.LUA)LUA.track("ViewContent",{content_name:%s,content_category:"Blog"},{server:true})});document.addEventListener("click",function(e){var a=e.target.closest&&e.target.closest("a[href^=\'/#precios\']");if(a&&window.LUA)LUA.track("AgendaCTA",{location:"blog"},{custom:true})},true);'%json.dumps(p['title'],ensure_ascii=False)
    body=f'''<main><article><div class="kicker">{p['tag']} · {p['read']} de lectura</div><h1>{html.escape(p['title'])}</h1><div class="meta">Por Andy Villarroel · 8 de octubre de 2026</div>{p['body']}
<div class="cta-box"><h2>Tus uñas ya pueden sonreír</h2><p>Reserva tu sesión y elige el servicio que va con tu momento.</p><a class="btn" href="/#precios">Agenda tu sesión</a></div>
<div class="more"><div class="kicker" style="padding-top:20px">Sigue leyendo</div>{others}</div></article></main>'''
    d=ROOT+f'blog/{p["slug"]}';os.makedirs(d,exist_ok=True)
    open(d+'/index.html','w').write(page(p['title']+' | LÜA',p['desc'],url,body,ld,evt))
items=''.join(f'<a class="item" href="/blog/{p["slug"]}/"><div class="kicker">{p["tag"]} · {p["read"]}</div><h2>{html.escape(p["title"])}</h2><p>{html.escape(p["desc"])}</p></a>' for p in POSTS)
body=f'<main><div class="kicker">Blog LÜA</div><h1>Aprende a cuidar tus manos</h1><p class="lede">Artículos sobre onicofagia, hábitos y cuidado de las uñas, escritos por Andy Villarroel.</p><div class="list">{items}</div></main>'
ld='<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"Blog","name":"Blog LÜA","url":SITE+"/blog/","inLanguage":"es"},ensure_ascii=False)+'</script>'
evt='window.addEventListener("load",function(){if(window.LUA)LUA.track("ViewContent",{content_name:"Blog",content_category:"Blog"},{server:true})});'
open(ROOT+'blog/index.html','w').write(page('Blog LÜA | Onicofagia y cuidado de uñas','Artículos sobre onicofagia, hábitos y cuidado de las uñas, por Andy Villarroel en Cochabamba.',SITE+'/blog/',body,ld,evt,"website"))
# sitemap + robots
urls=[SITE+'/',SITE+'/blog/']+[f"{SITE}/blog/{p['slug']}/" for p in POSTS]
open(ROOT+'sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>\n' for u in urls)+'</urlset>\n')
open(ROOT+'robots.txt','w').write(f'User-agent: *\nAllow: /\nDisallow: /.netlify/\nSitemap: {SITE}/sitemap.xml\n')
print('built',len(ns['t'])//1024,'KB landing,',len(POSTS),'posts')
