with open("saibiprint.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. ヘッダーを「上段：タイトル＋日付名前枠」「下段：全幅の対局者情報1行」に整理
old_header = """<div class="sheet-header"><div><div class="sheet-title">${game.eventName}（全${game.moves.length}手・${div}分割）</div><div class="sheet-meta">⚫黒番：${game.blackName}　⚪白番：${game.whiteName}　${game.dateStr}　${game.komiStr}　${game.resultStr}</div></div><div class="name-box" style="font-size:13px; padding:5px 10px;">　　　年　　月　　日 ／ 名前：　　　　　　　　　</div></div>"""

new_header = """<div class="sheet-header" style="flex-direction:column; align-items:stretch; gap:4px;"><div style="display:flex; justify-content:space-between; align-items:center; gap:8px;"><div class="sheet-title">${game.eventName}（全${game.moves.length}手・${div}分割）</div><div class="name-box" style="font-size:13px; padding:4px 10px;">　　　年　　月　　日 ／ 名前：　　　　　　　　　</div></div><div class="sheet-meta" style="white-space:nowrap; font-size:11.5px; letter-spacing:-0.01em;">⚫黒番：${game.blackName}　⚪白番：${game.whiteName}　${game.dateStr}　${game.komiStr}　${game.resultStr}</div></div>"""

if old_header in html:
    html = html.replace(old_header, new_header, 1)
    with open("saibiprint.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ 対局者・日付・コミ・結果の行を全幅1行レイアウトに改良しました！")
else:
    print("⚠️ 対象行の形式が一部異なるため、CSS補助ルールを追加します。")
    css_add = "\n        .sheet-meta { white-space: nowrap !important; font-size: 11px !important; letter-spacing: -0.02em; }\n"
    html = html.replace("</style>", css_add + "    </style>", 1)
    with open("saibiprint.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ CSSで対局者行の1行固定を適用しました！")
