with open("saibiprint.html", "r", encoding="utf-8") as f:
    html = f.read()

s1 = html.find("function downloadCurrentSgf()")
s2 = html.find("</script>", s1)
if s1 != -1 and s2 != -1:
    new_dl_fn = """async function downloadCurrentSgf() {
    const a = document.getElementById('sgfPasteTextarea');
    const sgf = (a ? a.value.trim() : "") || (currentGame ? currentGame.rawSgf : "");
    if (!sgf) return alert("先にSGF棋譜ファイルを開くか、SGF文字を貼り付けてください。");

    const baseName = ((currentGame && currentGame.eventName) ? currentGame.eventName : "kifu_data").replace(/[\\\\/:*?"<>|]/g, "_");
    const fileName = baseName + ".sgf";

    // 保存先フォルダ（sgfFile 等）を直接選べるダイアログ対応
    if (window.showSaveFilePicker) {
        try {
            const handle = await window.showSaveFilePicker({
                suggestedName: fileName,
                types: [{
                    description: "SGF 囲碁棋譜ファイル",
                    accept: { "application/x-go-sgf": [".sgf"], "text/plain": [".sgf"] }
                }]
            });
            const writable = await handle.createWritable();
            await writable.write(sgf);
            await writable.close();
            alert("✅ 指定したフォルダに「" + handle.name + "」を保存しました！");
            return;
        } catch (err) {
            if (err && err.name === "AbortError") return;
        }
    }

    // 非対応ブラウザ用のフォールバック保存
    const url = URL.createObjectURL(new Blob(Array.of(sgf), { type: "application/octet-stream" }));
    const link = document.createElement("a");
    link.href = url;
    link.download = fileName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    alert("✅ 「" + fileName + "」を保存しました！\\n（※ダウンロードフォルダに入った場合は、ブラウザ設定で「保存場所を毎回確認する」をオンにすると sgfFile を直接選べます）");
}
"""
    html = html[:s1] + new_dl_fn + html[s2:]
    with open("saibiprint.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ 保存先フォルダを直接選べるダイアログ機能を追加しました！")
