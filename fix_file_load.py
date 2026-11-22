with open("saibiprint.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. ファイル選択の読込処理を確実に1番目のファイル(at(0))を取得するよう修正
html = html.replace("const file = inp.files && inp.files;", "const file = inp.files && inp.files.at(0);")

# 2. 最善手表示の配列取得を修正
html = html.replace('item.ai.bestText.split(" ")', 'item.ai.bestText.split(" ").at(0)')

# 3. 読込時に古い編集メモを確実にリセット
html = html.replace("customDiagramComments = {};", "customDiagramComments = {};\n        const cBox = document.getElementById('commentEditorBox'); if (cBox) cBox.style.display = 'none';")

with open("saibiprint.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ 新しいSGFファイルの確実な読込とコメント切替の修正が完了しました！")
