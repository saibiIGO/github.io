const CACHE_NAME = "saibiprint-offline-v1";
const ASSETS = ["./", "./manifest.json", "./icon.svg", "./4koma.html", "./igo_generator.html", "./igogenerator.html", "./index (コピー).html", "./index.html", "./kifudepot.html", "./kifunarabe.html", "./kifuprint (コピー).html", "./komonjo.html", "./member.html", "./saibiprint (コピーKaTrain前).html", "./saibiprint.html", "./tozaidenko.html", "./tsumego (コピー).html", "./tsumego (別のコピー).html", "./tsumego.html", "./tumego.html"];

self.addEventListener("install", (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS).catch(() => {}))
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;
  event.respondWith(
    fetch(event.request)
      .then((res) => {
        const copy = res.clone();
        caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy));
        return res;
      })
      .catch(() => caches.match(event.request))
  );
});
