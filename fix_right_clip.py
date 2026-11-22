with open("saibiprint.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. 右側欄がはみ出して右端が切れるのを防止（min-width: 0 と box-sizing）
html = html.replace(
    ".diagram-side-info { overflow: hidden; display: flex; flex-direction: column; justify-content: flex-start; }",
    ".diagram-side-info { min-width: 0; flex: 1; box-sizing: border-box; overflow: hidden; display: flex; flex-direction: column; justify-content: flex-start; }"
)

# 2. 読みやすい大きさを保ちつつ右端まで余裕をもって収めるサイズ調整
html = html.replace(
    "margin-top: 4px; padding: 4px 6px; background: #f8fafc;",
    "margin-top: 4px; padding: 4px 5px; box-sizing: border-box; width: 100%; background: #f8fafc;"
)
html = html.replace(
    "font-size: 11.5px; line-height: 1.48; letter-spacing: -0.02em;",
    "font-size: 11px; line-height: 1.45; letter-spacing: -0.03em;"
)

# 3. 区切り記号の無駄な余白を詰めて1行の中に右端まで完全に収める
html = html.replace('sub.join(" / ")', 'sub.join(" ")')

with open("saibiprint.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ コメント右端の文字欠落を解消し、1行に美しく収めました！")
