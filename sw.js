// Service worker minimal : rend YokusoTD installable comme une appli.
// Réseau d'abord, copie en cache pour jouer hors ligne ; aucune vieille version servie quand le réseau répond.
const CACHE = 'yokusotd';
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', e => e.waitUntil(self.clients.claim()));
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET' || new URL(e.request.url).origin !== location.origin) return;
  e.respondWith(
    fetch(e.request)
      .then(r => { const c = r.clone(); caches.open(CACHE).then(k => k.put(e.request, c)); return r; })
      .catch(() => caches.match(e.request))
  );
});
