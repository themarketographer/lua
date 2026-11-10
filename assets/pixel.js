/* LÜA tracking base: Meta Pixel + utilidades. Se usa tal cual en el blog y va inlineado en la landing. */
(function(w,d){
  "use strict";
  var PIXEL_ID="1559106775456296";
  var CAPI_ENDPOINT="/.netlify/functions/capi";
  var CAL_HOST="cal.com";
  var WA_NUMBER="59178109113";
  var WA_CONFIRM="Wuolaa, acabo de agendarte una cita wuuu";

  /* --- snippet oficial de Meta --- */
  if(!w.fbq){
    var n=w.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};
    if(!w._fbq)w._fbq=n;n.push=n;n.loaded=true;n.version="2.0";n.queue=[];
    var t=d.createElement("script");t.async=true;t.src="https://connect.facebook.net/en_US/fbevents.js";
    var s=d.getElementsByTagName("script")[0];s.parentNode.insertBefore(t,s);
  }

  function uid(){return Date.now().toString(36)+Math.random().toString(36).slice(2,10)}
  function ck(k){var m=d.cookie.match(new RegExp("(?:^|; )"+k+"=([^;]*)"));return m?decodeURIComponent(m[1]):""}
  /* localStorage (no sessionStorage): Cal.com abre en otra pestaña y el código de anuncio tiene que sobrevivir hasta la página de gracias.
     shortcut: la atribución dura hasta que llegue un anuncio nuevo; si molesta, guardar con fecha y vencer a los 7 días. */
  function store(k,v){try{if(v!=null)localStorage.setItem(k,v);return localStorage.getItem(k)||""}catch(e){return v||""}}

  /* --- parametros de campaña y fbclid (se conserva toda la sesion) --- */
  var qs=new URLSearchParams(location.search);
  ["utm_source","utm_medium","utm_campaign","utm_content","utm_term"].forEach(function(k){
    if(qs.get(k))store("lua_"+k,qs.get(k));
  });
  var fbclid=qs.get("fbclid");
  if(fbclid&&!ck("_fbc")){
    d.cookie="_fbc=fb.1."+Date.now()+"."+fbclid+";max-age=7776000;path=/;SameSite=Lax";
  }

  fbq("init",PIXEL_ID);

  /* --- envio de eventos: navegador (Pixel) + servidor (CAPI) con el mismo event_id --- */
  function track(name,params,opts){
    opts=opts||{};
    var id=opts.id||uid();
    try{fbq(opts.custom?"trackCustom":"track",name,params||{},{eventID:id})}catch(e){}
    /* todo evento va también por servidor (CAPI), con el mismo event_id. Para no enviarlo: {server:false} */
    if(opts.server!==false){
      try{
        var body=JSON.stringify({
          event_name:name,event_id:id,event_source_url:location.href,
          fbp:ck("_fbp"),fbc:ck("_fbc"),custom_data:params||{},
          ad:store("lua_utm_content")
        });
        if(navigator.sendBeacon)navigator.sendBeacon(CAPI_ENDPOINT,new Blob([body],{type:"application/json"}));
        else fetch(CAPI_ENDPOINT,{method:"POST",body:body,keepalive:true,headers:{"Content-Type":"application/json"}});
      }catch(e){}
    }
    return id;
  }

  /* --- enlaces a Cal.com: agrega UTM, codigo de anuncio y fbp/fbc para que el webhook los lea --- */
  function tag(href,eid){
    try{
      var u=new URL(href);
      if(u.hostname.indexOf(CAL_HOST)<0)return href;
      ["utm_source","utm_medium","utm_campaign","utm_content","utm_term"].forEach(function(k){
        var v=store("lua_"+k);if(v&&!u.searchParams.get(k))u.searchParams.set(k,v);
      });
      if(!u.searchParams.get("utm_source"))u.searchParams.set("utm_source","landing");
      var meta={eid:eid,fbp:ck("_fbp"),fbc:ck("_fbc"),ad:store("lua_utm_content"),src:location.pathname,blog:store("lua_blog")};
      Object.keys(meta).forEach(function(k){if(meta[k])u.searchParams.set("metadata["+k+"]",meta[k])});
      return u.toString();
    }catch(e){return href}
  }

  /* --- enlace a WhatsApp con el codigo de anuncio al final del mensaje: "(A1)" --- */
  function wa(text){
    var ad=(store("lua_utm_content").match(/\bA\d{1,3}\b/)||[])[0];
    return "https://api.whatsapp.com/send?phone="+WA_NUMBER+"&text="+encodeURIComponent((text+(ad?" ("+ad+")":"")).trim());
  }

  track("PageView");
  w.LUA={track:track,tag:tag,uid:uid,wa:wa,store:store,ck:ck,WA_CONFIRM:WA_CONFIRM,PIXEL_ID:PIXEL_ID};
})(window,document);
