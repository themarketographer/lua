# LÜA by Andy Villarroel

Landing, blog y API de conversiones de Meta para el estudio de uñas LÜA (Cochabamba, Bolivia). Sitio estático con dos funciones de Netlify.

Sitio: https://studiolua.netlify.app

## Qué incluye

| Ruta | Qué es |
|---|---|
| `index.html` | Landing completa en un solo archivo (fuentes e imágenes embebidas) |
| `blog/` | Índice del blog y 3 artículos |
| `gracias-cita/` | Página a la que Cal.com manda tras reservar: mide `Purchase` y `Contact`, y abre WhatsApp con "Wuolaa, acabo de agendarte una cita wuuu" |
| `ads/` | Misma landing pero los precios abren WhatsApp (sin Cal): mide `InitiateCheckout`, `Lead` y `Contact`. noindex |
| `privacidad/` | Política de privacidad (exigida por Meta) |
| `llms.txt`, `ai.txt`, `robots.txt`, `sitemap.xml` | SEO y GEO (robots abre los rastreadores de IA y cierra las páginas de gracias y la de anuncios) |
| `assets/` | Favicon, imagen para redes (`og.jpg`), `pixel.js`, estilos del blog |
| `netlify/functions/capi.js` | Reenvía a Meta los eventos del navegador (API de conversiones) |
| `netlify/functions/cal-webhook.js` | Recibe las reservas de Cal.com y envía `Schedule` a Meta |
| `src/` | Plantilla, artículos y script para regenerar el sitio |
| `.env.example` | Nombres de las variables de entorno (sin valores) |

## Eventos que se miden

Pixel `1559106775456296`, con el mismo `event_id` en navegador y servidor para que Meta deduplique.

### Flujo A: landing → Cal.com → gracias → WhatsApp

| Paso | Evento | Cuándo | Origen |
|---|---|---|---|
| Llega | `PageView` | Cada página | Navegador |
| Ve precios | `ViewContent` | Llega a la sección de precios (y al abrir un artículo) | Navegador y servidor |
| Pregunta antes de reservar | `Contact` | Toca el botón de WhatsApp del header o de la barra de abajo | Navegador y servidor |
| Elige servicio | `InitiateCheckout` | Toca un precio (valor en BOB); sale hacia Cal.com | Navegador y servidor |
| Reserva confirmada | `Schedule` | Cal.com confirma (webhook, valor según servicio y duración). Fuente de verdad | Servidor |
| Gracias | `Purchase` | Carga `/gracias-cita/` (monto reservado, no cobrado) | Navegador y servidor |
| Confirma por WhatsApp | `ConfirmoPorWhatsApp` (personalizado) | Toca o se abre WhatsApp desde la página de gracias | Navegador y servidor |

### Flujo B: `/ads/` → WhatsApp directo (sin Cal)

| Paso | Evento | Cuándo |
|---|---|---|
| Llega y ve precios | `PageView`, `ViewContent` | Igual que A |
| Consulta general | `Contact` | Botón de WhatsApp del header o la barra |
| Quiere un servicio | `InitiateCheckout` + `Lead` | Toca un precio; se abre WhatsApp con ese servicio. **`Lead` es el evento para optimizar** |

### Interacciones (personalizados, navegador)
`AgendaCTA`, `Scroll50`, `Scroll90`, `BlogClick`, `BlogView`, `BlogScroll50`, `BlogScroll90`, `LlegoDesdeBlog` (el post viaja hasta Cal.com y vuelve en `Schedule` como `blog_post`).

Optimiza la campaña por un solo evento: `Lead` (flujo B) o `Schedule` (flujo A, cuando haya unas 50 reservas por semana).

Código de anuncio: si el enlace del anuncio trae `utm_content=A1`, ese código viaja hasta Cal.com y vuelve en el evento `Schedule` como `ad_code`. Parámetros de URL recomendados en cada anuncio:

```
utm_source=meta&utm_medium=paid&utm_campaign={{campaign.name}}&utm_content={{ad.name}}
```

## Dos caminos para los anuncios

- **A. Landing principal → Cal.com → `/gracias-cita/` → WhatsApp.** En cada tipo de evento de Cal.com, "Redirigir al reservar" debe apuntar a `https://studiolua.netlify.app/gracias-cita/` (con "reenviar parámetros" activo). Hacerlo solo después de publicar esta rama.
- **B. `/ads/` → WhatsApp directo.** Para probar el pixel sin depender de Cal. El mensaje termina con el código del anuncio, por ejemplo `(A1)`.

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

Los precios y los enlaces de Cal.com están en `src/tpl.html` (tarjetas de precios) y en `netlify/functions/cal-webhook.js` (tabla `PRICES`) y en `src/build.py` (tabla `PRICES`, para `gracias-cita`). Si cambias un precio, cámbialo en los tres lugares.

## Pendientes

- Confirmar el precio de "Soft gel, diseño sencillo" (hoy 120).
- Confirmar el número de WhatsApp correcto (Canva y Cal.com muestran números distintos).
- Reemplazar la tipografía Quincy CF (versión demo) por la licencia completa.
- Verificar el dominio en Meta Business Manager cuando haya dominio propio.
- Revisar los artículos del blog con Andy antes de promocionarlos.
