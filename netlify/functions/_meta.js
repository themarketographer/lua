// Utilidades compartidas para la API de conversiones de Meta.
const crypto = require("crypto");

const PIXEL_ID = process.env.META_PIXEL_ID || "1559106775456296";
const API_VERSION = process.env.META_API_VERSION || "v23.0";

const sha = (v) =>
  v ? crypto.createHash("sha256").update(String(v).trim().toLowerCase()).digest("hex") : undefined;

// Bolivia: se deja solo digitos y se antepone 591 si falta
const phone = (v) => {
  if (!v) return undefined;
  let d = String(v).replace(/\D/g, "");
  if (d.length === 8) d = "591" + d;
  return sha(d);
};

async function sendToMeta(events) {
  const token = process.env.META_CAPI_TOKEN;
  if (!token) return { skipped: true, reason: "META_CAPI_TOKEN no configurado" };
  const body = { data: events, access_token: token };
  if (process.env.META_TEST_EVENT_CODE) body.test_event_code = process.env.META_TEST_EVENT_CODE;
  const res = await fetch(`https://graph.facebook.com/${API_VERSION}/${PIXEL_ID}/events`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const json = await res.json().catch(() => ({}));
  if (!res.ok) console.error("Meta CAPI error", res.status, JSON.stringify(json));
  return { status: res.status, json };
}

module.exports = { sha, phone, sendToMeta, PIXEL_ID };
