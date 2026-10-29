/* M Z Smart ICU — Service Worker
   يستقبل الإشعارات من Firebase Cloud Messaging ويعرضها في شريط الإشعارات
   وعلى شاشة القفل حتى لو كان التطبيق مغلقًا، والضغط عليها يفتح المريض المعني. */
const SW_VERSION = 'mz-sw-v1';
const SCOPE = self.registration.scope;

self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', (event) => event.waitUntil(self.clients.claim()));

function abs(path){ try{ return new URL(path || './', SCOPE).href; }catch(e){ return SCOPE; } }

self.addEventListener('push', (event) => {
  let msg = {};
  try{ msg = event.data ? event.data.json() : {}; }
  catch(e){ msg = { data: { title: 'M Z Smart ICU', body: event.data ? event.data.text() : '' } }; }
  const d = Object.assign({}, msg.notification || {}, msg.data || (msg.notification ? {} : msg));
  const urgent = d.urgent === '1' || d.urgent === true;
  const title = d.title || 'M Z Smart ICU';
  const tag = d.id || d.tag || ('mz_' + Date.now());
  const options = {
    body: d.body || '',
    icon: abs(d.icon || 'icons/icon-192.png'),
    badge: abs('icons/badge-96.png'),
    tag,
    renotify: false,
    requireInteraction: urgent,
    silent: false,
    vibrate: urgent ? [500,200,500,200,500,200,500] : [250,100,250],
    timestamp: Number(d.time) || Date.now(),
    dir: 'rtl',
    data: { id: tag, patientId: d.patientId || '', tab: d.tab || '', url: d.url || './' },
    actions: [{ action:'open', title:'فتح' }, { action:'read', title:'تم الاطلاع' }]
  };
  if(d.image) options.image = abs(d.image);

  event.waitUntil((async () => {
    const wins = await self.clients.matchAll({ type:'window', includeUncontrolled:true });
    // إذا التطبيق ظاهر على الشاشة الآن، التنبيه الداخلي (البطاقة + الجرس) يكفي
    if(wins.some(w => w.visibilityState === 'visible')) return;
    try{ if(self.navigator && self.navigator.setAppBadge) await self.navigator.setAppBadge(); }catch(e){}
    await self.registration.showNotification(title, options);
  })());
});

self.addEventListener('notificationclick', (event) => {
  const n = event.notification;
  const d = n.data || {};
  n.close();
  event.waitUntil((async () => {
    const wins = await self.clients.matchAll({ type:'window', includeUncontrolled:true });
    if(event.action === 'read'){
      wins.forEach(w => w.postMessage({ type:'read', id: d.id }));
      return;
    }
    const target = wins.find(w => w.url.startsWith(SCOPE));
    if(target){
      try{ await target.focus(); }catch(e){}
      target.postMessage({ type:'go', patientId: d.patientId, tab: d.tab, id: d.id });
      return;
    }
    await self.clients.openWindow(abs(d.url || './'));
  })());
});
