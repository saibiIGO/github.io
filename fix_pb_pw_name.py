with open("saibiprint.html", "r", encoding="utf-8") as f:
    html = f.read()

s1 = html.find("let rawBase =")
s2 = html.find("const fileName = baseName + \".sgf\";")
if s1 != -1 and s2 != -1:
    pb_pw_logic = """const pbM = sgf.match(/PB\\[([^\\]]+)\\]/i);
    const pwM = sgf.match(/PW\\[([^\\]]+)\\]/i);
    const pbName = pbM ? pbM.at(1).trim() : "";
    const pwName = pwM ? pwM.at(1).trim() : "";
    let rawBase = "kifu_data";
    if (pbName || pwName) {
        rawBase = `${pbName || "黒番"}_vs_${pwName || "白番"}`;
    } else if (currentGame && currentGame.eventName) {
        rawBase = currentGame.eventName;
    }
    const baseName = rawBase.replace(/[\\\\/:*?"<>|]/g, "_");
    """
    html = html[:s1] + pb_pw_logic + html[s2:]
    with open("saibiprint.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ SGF内の PB[...] と PW[...] から直接ファイル名を生成するよう設定しました！")
