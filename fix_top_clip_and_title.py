import re

with open("saibiprint.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. タイトル文字数に応じてフォントサイズを自動調整し、絶対に2段にならないようにする
old_title_part = '<div class="sheet-title">${game.eventName}（全${game.moves.length}手・${div}分割）</div>'
new_title_part = '<div class="sheet-title" style="font-size:${(game.eventName.length > 26 ? 11 : (game.eventName.length > 18 ? 12.5 : 14))}px !important; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${game.eventName}（全${game.moves.length}手・${div}分割）</div>'

if old_title_part in html:
    html = html.replace(old_title_part, new_title_part)

# 2. 印刷の上端がプリンターの余白で切れないよう、上パディングを 8mm -> 11mm に拡大
html = html.replace(
    'style="padding:8mm ${isF ? om : bm}mm 8mm ${isF ? bm : om}mm;"',
    'style="padding:11mm ${isF ? om : bm}mm 9mm ${isF ? bm : om}mm;"'
)

# 3. 上余白を広げた分、4分割時の盤面サイズを 435 -> 418 に微調整して2ページにピタリと収める
html = html.replace(
    'const svgSize = divisions === 2 ? 880 : (divisions === 4 ? 435 : 298);',
    'const svgSize = divisions === 2 ? 850 : (divisions === 4 ? 418 : 288);'
)

with open("saibiprint.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ 長いタイトルの1段自動調整と、印刷上端の切れ防止が完了しました！")
