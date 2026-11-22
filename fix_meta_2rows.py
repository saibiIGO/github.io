import re

with open("saibiprint.html", "r", encoding="utf-8") as f:
    html = f.read()

new_meta = '<div class="sheet-meta" style="line-height:1.45; margin-top:2px;"><div>⚫黒番：${game.blackName}　⚪白番：${game.whiteName}</div><div>${game.dateStr}　${game.komiStr}　${game.resultStr}</div></div>'

html, count = re.subn(r'<div class="sheet-meta"[^>]*>.*?</div>', new_meta, html, count=1)

# 前回追加した1行強制CSSがあれば解除して自然な2段表示にする
html = html.replace(".sheet-meta { white-space: nowrap !important; font-size: 11px !important; letter-spacing: -0.02em; }", "")

with open("saibiprint.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ 対局者行と日付・コミ・結果行の2段構成への変更が完了しました！（置換数: {count}）")
