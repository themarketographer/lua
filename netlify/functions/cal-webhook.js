// Webhook de Cal.com. Cuando alguien completa una reserva (BOOKING_CREATED),
// envia el evento Schedule a Meta con valor en bolivianos y datos del cliente (hasheados).
const crypto = require("crypto");
const { sha, phone, sendToMeta } = require("./_meta");

// Precios de la landing por servicio (slug de Cal.com) y duracion en minutos
const PRICES = {
  "pintado": { 120: 70, 180: 80, 240: 90 },
  "softgel": { 120: 100, 180: 120, 240: 140 },
  "reconstruccion": { 120: 100, 180: 120, 240: 150 },
  "cita-de-relleno-de-sofgel-o-reconstruccion": { 120: 80, 180: 100, 240: 120 },
};
const NAMES = {
  "pintado": "Pintado en gel",
  "softgel": "Soft gel",
  "reconstruccion": "Reconstrucción con gel",
  "cita-de-relleno-de-sofgel-o-reconstruccion": "Relleno",
};

function validSignature(raw, header) {
  const secret = process.env.CAL_WEBHOOK_SECRET;
  if (!secret) return false;
  const expected = crypto.createHmac("sha256", secret).update(raw).digest("hex");
  const a = Buffer.from(expected), b = Buffer.from(String(header || ""));
  return a.length === b.length && crypto.timingSafeEqual(a, b);
}

exports.handler = async (event) => {
  if (event.httpMethod !== "POST") return { statusCode: 405, body: "Method not allowed" };
  const raw = event.isBase64Encoded ? Buffer.from(event.body, "base64").toString("utf8") : event.body || "";

  if (!validSignature(raw, event.headers["x-cal-signature-256"])) {
    return { statusCode: 401, body: "Invalid signature" };
  }

  let msg;
  try { msg = JSON.parse(raw); } catch { return { statusCode: 400, body: "Bad JSON" }; }
  if (msg.triggerEvent !== "BOOKING_CREATED") return { statusCode: 200, body: "ignored" };

  const p = msg.payload || {};
  const slug = String(p.type || p.eventType?.slug || "");
  const minutes = Number(p.length || p.eventType?.length || 0);
  const value = (PRICES[slug] || {})[minutes];
  const att = (p.attendees || [])[0] || {};
  const resp = p.responses || {};
  const meta = p.metadata || {};
  const phoneRaw = att.phoneNumber || resp.attendeePhoneNumber?.value || resp.phone?.value;
  const fullName = (att.name || resp.name?.value || "").trim().split(/\s+/);

  const ev = {
    event_name: "Schedule",
    event_time: Math.floor(Date.now() / 1000),
    event_id: meta.eid ? `${meta.eid}-sch` : `cal-${p.uid}`,
    event_source_url: process.env.SITE_URL || "https://studiolua.netlify.app",
    action_source: "website",
    user_data: {
      em: sha(att.email),
      ph: phone(phoneRaw),
      fn: sha(fullName[0]),
      ln: sha(fullName.length > 1 ? fullName[fullName.length - 1] : ""),
      country: sha("bo"),
      ct: sha("cochabamba"),
      fbp: meta.fbp || undefined,
      fbc: meta.fbc || undefined,
    },
    custom_data: {
      content_name: NAMES[slug] || slug,
      content_category: "Servicios",
      content_ids: [slug],
      currency: "BOB",
      ...(value ? { value } : {}),
      ...(meta.ad ? { ad_code: meta.ad } : {}),
    },
  };
  Object.keys(ev.user_data).forEach((k) => ev.user_data[k] === undefined && delete ev.user_data[k]);

  const out = await sendToMeta([ev]);
  console.log("Schedule", slug, minutes, value, JSON.stringify(out));
  return { statusCode: 200, body: JSON.stringify({ ok: true, skipped: !!out.skipped }) };
};
