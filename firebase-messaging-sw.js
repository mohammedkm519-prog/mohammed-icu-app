/* Service Worker للإشعارات الخلفية (FCM). يعمل حتى لو التطبيق مغلق أو الشاشة مقفلة. */
importScripts('https://www.gstatic.com/firebasejs/10.12.2/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/10.12.2/firebase-messaging-compat.js');

firebase.initializeApp({
  apiKey: "AIzaSyCEAlqIhbldh9DQFblY-TVjkgeaKM1d4ns",
  authDomain: "m-z-icu.firebaseapp.com",
  projectId: "m-z-icu",
  storageBucket: "m-z-icu.firebasestorage.app",
  messagingSenderId: "419630831547",
  appId: "1:419630831547:web:3794472cf54d4de121969e"
});
const messaging = firebase.messaging();

/* رسائل البيانات فقط: نبني الإشعار بأنفسنا ليظهر بشكل موحّد (أيقونة + عنوان + نص) */
messaging.onBackgroundMessage(function(payload){
  const d = payload.data || {};
  const urgent = d.urgent === '1';
  const opts = {
    body: d.body || '',
    icon: 'icon-192.png',
    badge: 'badge-96.png',
    tag: d.tag || ('mz-' + (d.patientId || 'x') + '-' + (d.tab || '')),
    renotify: true,
    requireInteraction: urgent,
    vibrate: urgent ? [300,120,300,120,300,120,600] : [200,100,200],
    dir: 'auto',
    data: { patientId: d.patientId || '', tab: d.tab || '', url: d.url || './index.html' }
  };
  return self.registration.showNotification(d.title || 'Smart ICU', opts);
});

/* الضغط على الإشعار: يفتح التطبيق مباشرة على المريض والتبويب المطلوب */
self.addEventListener('notificationclick', function(event){
  event.notification.close();
  const data = event.notification.data || {};
  const target = new URL('index.html', self.registration.scope);
  if(data.patientId) target.searchParams.set('p', data.patientId);
  if(data.tab) target.searchParams.set('tab', data.tab);
  event.waitUntil((async () => {
    const all = await clients.matchAll({ type:'window', includeUncontrolled:true });
    for(const c of all){
      if(c.url.startsWith(self.registration.scope)){
        await c.focus();
        c.postMessage({ type:'open-notification', patientId:data.patientId, tab:data.tab });
        return;
      }
    }
    await clients.openWindow(target.href);
  })());
});
