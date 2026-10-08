// Recibe eventos del navegador (ViewContent, InitiateCheckout) y los reenvia a Meta
// con el mismo event_id que el Pixel, para que Meta los deduplique.
const { sendToMeta } = require("./_meta");

const ALLOWED = new Set(["ViewContent", "InitiateCheckout"]);
const SITE = process.env.SITE_URL || "https://studiolua.netlify.app";

exports.handler = async (event) => {
  if (event.httpMethod !== "POST") return { statusCode: 405, body: "Method not allowed" };

  // Solo acepta llamadas que vienen de este sitio
  const origin = event.headers.origin || event.headers.referer || "";
  const okOrigin = origin.startsWith(SITE) || origin.includes("localhost") || origin.includes("netlify.app");
  if (origin && !okOrigin) return { statusCode: 403, body: "Forbidden" };

  let b;
  try { b = JSON.parse(event.body || "{}"); } catch { return { statusCode: 400, body: "Bad JSON" }; }
  if (!ALLOWED.has(b.event_name) || !b.event_id) return { statusCode: 400, body: "Invalid event" };

  const cd = b.custom_data || {};
  const custom = {
    content_name: String(cd.content_name || "").slice(0, 120),
    content_category: String(cd.content_category || "").slice(0, 60),
  };
  if (Array.isArray(cd.content_ids)) custom.content_ids = cd.content_ids.slice(0, 5).map(String);
  if (typeof cd.value === "number" && cd.value >= 0 && cd.value < 100000) {
    custom.value = cd.value;
    custom.currency = "BOB";
  }
  if (b.ad) custom.ad_code = String(b.ad).slice(0, 80);

  const ev = {
    event_name: b.event_name,
    event_time: Math.floor(Date.now() / 1000),
    event_id: String(b.event_id).slice(0, 64),
    event_source_url: String(b.event_source_url || SITE).slice(0, 500),
    action_source: "website",
    user_data: {
      client_ip_address: event.headers["x-nf-client-connection-ip"] || (event.headers["x-forwarded-for"] || "").split(",")[0].trim(),
      client_user_agent: event.headers["user-agent"],
      fbp: b.fbp || undefined,
      fbc: b.fbc || undefined,
    },
    custom_data: custom,
  };

  const out = await sendToMeta([ev]);
  return { statusCode: 200, headers: { "Content-Type": "application/json" }, body: JSON.stringify({ ok: true, skipped: !!out.skipped }) };
};
