with open("saibiprint.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. 印刷時にパス案内バーとコメント編集枠を完全に隠す（@media print に追加）
if "@media print" in html and "#commentEditorBox" not in html:
    html = html.replace(
        "@media print {",
        "@media print {\n            #pathInfoBar, #commentEditorBox { display: none !important; }",
        1
    )

# パス案内バーに id="pathInfoBar" を付与
html = html.replace(
    '<div style="background:#f1f5f9; border-bottom:1px solid #cbd5e1; padding:5px 16px;',
    '<div id="pathInfoBar" style="background:#f1f5f9; border-bottom:1px solid #cbd5e1; padding:5px 16px;',
    1
)

# 2. 日本語KaTrainのAI諸データ（目差・勝率・推定損失目数・最善手・予想手順）を確実に抽出
s1 = html.find("function parseJapaneseKaTrainComment")
s2 = html.find("function simulateBoardStates")
if s1 != -1 and s2 != -1:
    fixed_parser = """function parseJapaneseKaTrainComment(txt) {
    if (!txt) return null;
    const lines = txt.split(/[\\r\\n]+/).map(s => s.trim()).filter(Boolean);
    let scoreText = "", winText = "", pointsLost = 0, bestText = "", pvText = "", found = false;
    for (const ln of lines) {
        if (ln.startsWith("目差")) { scoreText = ln.replace(/^目差[：:]\\s*/, ""); found = true; }
        else if (ln.startsWith("勝率")) { winText = ln.replace(/^勝率[：:]\\s*/, ""); found = true; }
        else if (ln.startsWith("推定損失目数")) { pointsLost = parseFloat(ln.replace(/^推定損失目数[：:]\\s*/, "")) || 0; found = true; }
        else if (ln.startsWith("最善手は")) { bestText = ln.replace(/^最善手は\\s*/, ""); found = true; }
        else if (ln.startsWith("予想手順")) { pvText = ln.replace(/^予想手順[：:]\\s*/, ""); found = true; }
    }
    return found ? { scoreText, winText, pointsLost, bestText, pvText } : null;
}

"""
    html = html[:s1] + fixed_parser + html[s2:]

with open("saibiprint.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ 印刷時の不要バー非表示 ＆ AIデータ自動抽出の修正が完了しました！")
