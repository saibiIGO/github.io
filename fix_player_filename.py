with open("saibiprint.html", "r", encoding="utf-8") as f:
    html = f.read()

old_line = 'const baseName = ((currentGame && currentGame.eventName) ? currentGame.eventName : "kifu_data").replace(/[\\\\/:*?"<>|]/g, "_");'
new_line = '''let rawBase = "kifu_data";
    if (currentGame) {
        const b = currentGame.blackName || "";
        const w = currentGame.whiteName || "";
        if ((b && b !== "黒番") || (w && w !== "白番")) {
            rawBase = `${b}_vs_${w}`;
        } else if (currentGame.eventName) {
            rawBase = currentGame.eventName;
        }
    }
    const baseName = rawBase.replace(/[\\\\/:*?"<>|]/g, "_");'''

if old_line in html:
    html = html.replace(old_line, new_line, 1)
    with open("saibiprint.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ 保存時のファイル名が「対局者名（黒番_vs_白番）.sgf」になるよう変更しました！")
else:
    print("⚠️ 対象行が見つかりませんでした。")
