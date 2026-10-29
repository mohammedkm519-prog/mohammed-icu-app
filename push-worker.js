/* M Z Smart ICU — خادم إرسال الإشعارات (Cloudflare Worker مجاني)
   ------------------------------------------------------------------
   وظيفته: يستلم طلب من التطبيق (من مستخدم مسجّل دخول فعلًا)، ويرسل الإشعار
   لأجهزة المستلمين عبر Firebase Cloud Messaging.
   يحتاج متغيرًا سرّيًا واحدًا اسمه SERVICE_ACCOUNT = محتوى ملف JSON
   (Firebase → Project settings → Service accounts → Generate new private key).
   ------------------------------------------------------------------ */
const FIREBASE_API_KEY = 'AIzaSyCEAlqIhbldh9DQFblY-TVjkgeaKM1d4ns'; // نفس مفتاح firebaseConfig بالتطبيق (عام وليس سرّيًا)
const ALLOWED_ORIGINS = ['https://mohammedkm519-prog.github.io'];

let cachedToken = null, cachedTokenExp = 0;

export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin') || '';
    const cors = {
      'Access-Control-Allow-Origin': ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0],
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Vary': 'Origin'
    };
    const json = (obj, status = 200) => new Response(JSON.stringify(obj), { status, headers: { ...cors, 'Content-Type': 'application/json' } });
    if (request.method === 'OPTIONS') return new Response(null, { headers: cors });
    if (request.method !== 'POST') return json({ ok: true, service: 'M Z Smart ICU push relay' });

    try {
      const { idToken, tokens, data } = await request.json();
      if (!idToken || !Array.isArray(tokens) || !tokens.length || !data) return json({ error: 'bad request' }, 400);
      if (!env.SERVICE_ACCOUNT) return json({ error: 'SERVICE_ACCOUNT secret is missing' }, 500);

      // 1) التأكد إن المرسل مستخدم مسجّل دخول بتطبيقنا (حتى ما يقدر أي أحد يستخدم الخادم)
      const lookup = await fetch(`https://identitytoolkit.googleapis.com/v1/accounts:lookup?key=${FIREBASE_API_KEY}`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ idToken })
      });
      if (!lookup.ok) return json({ error: 'unauthorized' }, 401);

      // 2) الإرسال لكل جهاز
      const sa = JSON.parse(env.SERVICE_ACCOUNT);
      const accessToken = await getAccessToken(sa);
      const stringData = {};
      Object.keys(data).forEach(k => { if (data[k] != null) stringData[k] = String(data[k]).slice(0, 1500); });
      const urgent = stringData.urgent === '1';

      const results = await Promise.all(tokens.slice(0, 300).map(async token => {
        const res = await fetch(`https://fcm.googleapis.com/v1/projects/${sa.project_id}/messages:send`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${accessToken}` },
          body: JSON.stringify({ message: {
            token,
            data: stringData,
            webpush: { headers: { Urgency: 'high', TTL: urgent ? '86400' : '43200' } }
          } })
        });
        if (res.ok) return { token, ok: true };
        const err = await res.json().catch(() => ({}));
        const code = JSON.stringify(err);
        const invalid = res.status === 404 || /UNREGISTERED|registration-token-not-registered|INVALID_ARGUMENT/.test(code);
        return { token, ok: false, invalid, status: res.status };
      }));

      return json({
        sent: results.filter(r => r.ok).length,
        failed: results.filter(r => !r.ok).length,
        invalid: results.filter(r => r.invalid).map(r => r.token)
      });
    } catch (e) {
      return json({ error: String(e && e.message || e) }, 500);
    }
  }
};

/* رمز دخول Google من حساب الخدمة (JWT موقّع RS256) — يُخزّن مؤقتًا ساعة */
async function getAccessToken(sa) {
  const now = Math.floor(Date.now() / 1000);
  if (cachedToken && now < cachedTokenExp - 60) return cachedToken;
  const enc = obj => b64url(new TextEncoder().encode(JSON.stringify(obj)));
  const header = enc({ alg: 'RS256', typ: 'JWT' });
  const claims = enc({
    iss: sa.client_email, scope: 'https://www.googleapis.com/auth/firebase.messaging',
    aud: 'https://oauth2.googleapis.com/token', iat: now, exp: now + 3600
  });
  const pem = sa.private_key.replace(/-----[^-]+-----/g, '').replace(/\s+/g, '');
  const der = Uint8Array.from(atob(pem), c => c.charCodeAt(0));
  const key = await crypto.subtle.importKey('pkcs8', der, { name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-256' }, false, ['sign']);
  const sig = await crypto.subtle.sign('RSASSA-PKCS1-v1_5', key, new TextEncoder().encode(`${header}.${claims}`));
  const jwt = `${header}.${claims}.${b64url(new Uint8Array(sig))}`;
  const res = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: `grant_type=${encodeURIComponent('urn:ietf:params:oauth:grant-type:jwt-bearer')}&assertion=${jwt}`
  });
  const out = await res.json();
  if (!out.access_token) throw new Error('Google auth failed: ' + JSON.stringify(out));
  cachedToken = out.access_token; cachedTokenExp = now + (out.expires_in || 3600);
  return cachedToken;
}
function b64url(bytes) {
  let s = ''; bytes.forEach(b => s += String.fromCharCode(b));
  return btoa(s).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}
