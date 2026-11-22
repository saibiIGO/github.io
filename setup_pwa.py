import os, glob, json

# 1. アプリアイコン (icon.svg) を作成
icon_svg = """<svg xmlns="http://w3.org" viewBox="0 0 512 512">
  <rect width="512" height="512" rx="96" fill="#0f766e"/>
  <rect x="64" y="64" width="384" height="384" rx="32" fill="#f59e0b"/>
  <g stroke="#1e293b" stroke-width="6">
    <line x1="128" y1="128" x2="384" y2="128"/><line x1="128" y1="213" x2="384" y2="213"/>
    <line x1="128" y1="298" x2="384" y2="298"/><line x1="128" y1="384" x2="384" y2="384"/>
    <line x1="128" y1="128" x2="128" y2="384"/><line x1="213" y1="128" x2="213" y2="384"/>
    <line x1="298" y1="128" x2="298" y2="384"/><line x1="384" y1="128" x2="384" y2="384"/>
  </g>
  <circle cx="213" cy="213" r="34" fill="#0f172a"/>
  <circle cx="298" cy="213" r="34" fill="#ffffff" stroke="#0f172a" stroke-width="4"/>
  <circle cx="298" cy="298" r="34" fill="#0f172a"/>
  <circle cx="213" cy="298" r="34" fill="#ffffff" stroke="#0f172a" stroke-width="4"/>
</svg>"""
with open("icon.svg", "w", encoding="utf-8") as f:
    f.write(icon_svg)

# 2. アプリ定義ファイル (manifest.json) を作成
manifest = {
    "name": "才美プリント・囲碁教材システム",
    "short_name": "才美プリント",
    "description": "囲碁棋譜A4両面プリント作成・AI解析表示・詰碁教材アプリ",
    "start_url": "./saibiprint.html",
    "scope": "./",
    "display": "standalone",
    "background_color": "#f8fafc",
    "theme_color": "#0f766e",
    "icons": [
        {"src": "icon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any maskable"}
    ]
}
with open("manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

# 3. オフライン保存エンジン (sw.js) を作成
html_files = sorted(glob.glob("*.html"))
asset_list = ["./", "./manifest.json", "./icon.svg"] + [f"./{h}" for h in html_files]

sw_js = f"""const CACHE_NAME = "saibiprint-offline-v1";
const ASSETS = {json.dumps(asset_list, ensure_ascii=False)};

self.addEventListener("install", (event) => {{
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS).catch(() => {{}}))
  );
}});

self.addEventListener("activate", (event) => {{
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
}});

self.addEventListener("fetch", (event) => {{
  if (event.request.method !== "GET") return;
  event.respondWith(
    fetch(event.request)
      .then((res) => {{
        const copy = res.clone();
        caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy));
        return res;
      }})
      .catch(() => caches.match(event.request))
  );
}});
"""
with open("sw.js", "w", encoding="utf-8") as f:
    f.write(sw_js)

# 4. 全HTMLファイルにアプリ化タグと登録スクリプトを組み込み
pwa_head = """<link rel="manifest" href="manifest.json">
<meta name="theme-color" content="#0f766e">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="才美プリント">
<link rel="apple-touch-icon" href="icon.svg">
<script>
if ("serviceWorker" in navigator && location.protocol.startsWith("http")) {
    window.addEventListener("load", () => navigator.serviceWorker.register("./sw.js").catch(() => {}));
}
</script>
</head>"""

updated = 0
for h in html_files:
    txt = open(h, encoding="utf-8").read()
    if 'rel="manifest"' not in txt and "</head>" in txt:
        txt = txt.replace("</head>", pwa_head, 1)
        open(h, "w", encoding="utf-8").write(txt)
        updated += 1

print(f"✅ オフライン単独アプリ（PWA）化が完了しました！（対象HTML: {updated}ファイル）")
