with open("saibiprint.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. 「最善手は」の後ろから座標（アルファベット＋数字：例 H15, O16）を確実に取得
s1 = html.find("function parseJapaneseKaTrainComment")
s2 = html.find("function simulateBoardStates")
if s1 != -1 and s2 != -1:
    fixed_fn = """function parseJapaneseKaTrainComment(txt) {
    if (!txt) return null;
    const lines = txt.split(/[\\r\\n]+/).map(s => s.trim()).filter(Boolean);
    let scoreText = "", winText = "", pointsLost = 0, bestText = "", pvText = "", found = false;
    for (const ln of lines) {
        if (ln.startsWith("目差")) { scoreText = ln.replace(/^目差[：:]\\s*/, ""); found = true; }
        else if (ln.startsWith("勝率")) { winText = ln.replace(/^勝率[：:]\\s*/, ""); found = true; }
        else if (ln.startsWith("推定損失目数")) { pointsLost = parseFloat(ln.replace(/^推定損失目数[：:]\\s*/, "")) || 0; found = true; }
        else if (ln.startsWith("最善手は")) {
            const m = ln.match(/([A-HJ-T]\\d{1,2})/i);
            bestText = m ? m.at(1).toUpperCase() : ln.replace(/^最善手は\\s*/, "").split(/\\s+/).at(0);
            found = true;
        }
        else if (ln.startsWith("予想手順")) { pvText = ln.replace(/^予想手順[：:]\\s*/, ""); found = true; }
    }
    return found ? { scoreText, winText, pointsLost, bestText, pvText } : null;
}

"""
    html = html[:s1] + fixed_fn + html[s2:]

# 2. 表示側もそのまま bestText を出力
html = html.replace('item.ai.bestText.split(" ").at(0)', 'item.ai.bestText')

with open("saibiprint.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ 最善手の座標と数字（例：最善:H15）が最後まで表示されるよう修正しました！")
