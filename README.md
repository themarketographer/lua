# LÜA by Andy Villarroel

Landing, blog y API de conversiones de Meta para el estudio de uñas LÜA (Cochabamba, Bolivia). Sitio estático con dos funciones de Netlify.

Sitio: https://studiolua.netlify.app

## Qué incluye

| Ruta | Qué es |
|---|---|
| `index.html` | Landing completa en un solo archivo (fuentes e imágenes embebidas) |
| `blog/` | Índice del blog y 3 artículos |
| `assets/` | Favicon, imagen para redes (`og.jpg`), `pixel.js`, estilos del blog |
| `netlify/functions/capi.js` | Reenvía a Meta los eventos del navegador (API de conversiones) |
| `netlify/functions/cal-webhook.js` | Recibe las reservas de Cal.com y envía `Schedule` a Meta |
| `src/` | Plantilla, artículos y script para regenerar el sitio |
| `.env.example` | Nombres de las variables de entorno (sin valores) |

## Eventos que se miden

Pixel `1559106775456296`, con el mismo `event_id` en navegador y servidor para que Meta deduplique.

| Evento | Cuándo | Origen |
|---|---|---|
| `PageView` | Cada página | Navegador |
| `ViewContent` | Al llegar a precios, y al abrir un artículo | Navegador y servidor |
| `InitiateCheckout` | Clic en un precio (valor en BOB, nombre del servicio) | Navegador y servidor |
| `Schedule` | Reserva confirmada en Cal.com (valor según servicio y duración) | Servidor |
| `AgendaCTA`, `BlogClick`, `Scroll50`, `Scroll90` | Interacciones | Navegador (personalizados) |

Código de anuncio: si el enlace del anuncio trae `utm_content=A1`, ese código viaja hasta Cal.com y vuelve en el evento `Schedule` como `ad_code`. Parámetros de URL recomendados en cada anuncio:

```
utm_source=meta&utm_medium=paid&utm_campaign={{campaign.name}}&utm_content={{ad.name}}
```

## Puesta en marcha

### 1. GitHub
Crea un repositorio vacío y sube el contenido de esta carpeta (el archivo `.env` nunca se sube).

### 2. Netlify
1. Netlify, Add new project, Import from Git, elige el repositorio.
2. Build command vacío. Publish directory: `.`
3. Project configuration, Environment variables, crea estas dos:
   - `META_CAPI_TOKEN`: en Events Manager, tu pixel, Configuración, API de conversiones, Generar token de acceso.
   - `CAL_WEBHOOK_SECRET`: una frase larga que inventas tú (mínimo 20 caracteres).
4. Redeploy para que las variables se apliquen.

### 3. Webhook en Cal.com
1. Cal.com, Settings, Developer, Webhooks, New.
2. Subscriber URL: `https://studiolua.netlify.app/.netlify/functions/cal-webhook`
3. Trigger: `Booking Created`.
4. Secret: el mismo valor de `CAL_WEBHOOK_SECRET`.

### 4. Probar
1. Events Manager, Probar eventos, copia el código de prueba y ponlo en `META_TEST_EVENT_CODE` (Netlify). Redeploy.
2. Abre el sitio, baja a precios, toca un precio. Debes ver `ViewContent` e `InitiateCheckout` con origen Navegador y Servidor.
3. Haz una reserva de prueba en Cal.com. Debe aparecer `Schedule` con origen Servidor.
4. Borra `META_TEST_EVENT_CODE` al terminar.

## Editar el sitio

Los textos de la landing están en `src/tpl.html` y los artículos en `src/posts.py`. Para regenerar `index.html`, `blog/`, `sitemap.xml` y `robots.txt`:

```
pip install pillow
python3 src/build.py
```

Los precios y los enlaces de Cal.com están en `src/tpl.html` (tarjetas de precios) y en `netlify/functions/cal-webhook.js` (tabla `PRICES`). Si cambias un precio, cámbialo en los dos lugares.

## Pendientes

- Confirmar el precio de "Soft gel, diseño sencillo" (hoy 120).
- Confirmar el número de WhatsApp correcto (Canva y Cal.com muestran números distintos).
- Reemplazar la tipografía Quincy CF (versión demo) por la licencia completa.
- Verificar el dominio en Meta Business Manager cuando haya dominio propio.
- Revisar los artículos del blog con Andy antes de promocionarlos.
