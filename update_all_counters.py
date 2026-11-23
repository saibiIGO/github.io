js = open("counter.js", encoding="utf-8").read()
js = js.replace("'kifunarabe': '棋譜並べ教室'", "'kifunarabe': '棋譜並べ教室',\n    'igogenerator': '囲碁問題作成教室',\n    'komonjo': '古文書・古典棋譜教室'")
js = js.replace(
    "background:#f0fdf4;border:1px solid #86efac;color:#166534;padding:4px 12px;border-radius:999px;font-size:12px;font-weight:bold;margin:4px auto;",
    "background:#f8fafc;border:1px solid #e2e8f0;color:#64748b;padding:2px 8px;border-radius:999px;font-size:10px;font-weight:normal;margin:2px auto;opacity:0.85;"
)
js = js.replace("font-size:14px;color:#15803d;", "font-size:10.5px;color:#475569;font-weight:bold;")
open("counter.js", "w", encoding="utf-8").write(js)

for fn in ["index.html", "member.html", "saibiprint.html", "tsumego.html", "igogenerator.html", "komonjo.html"]:
    s = open(fn, encoding="utf-8").read()
    tag = '<script src="counter.js"></script>'
    if tag not in s and "</body>" in s:
        s = s.replace("</body>", tag + "\n</body>", 1)
        open(fn, "w", encoding="utf-8").write(s)
        print("✅ 追加完了:", fn)
print("✅ 全6教室のカウンター設置と控えめサイズ調整が完了しました！")
