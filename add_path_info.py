with open("saibiprint.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. ステータスバーに読込・保存パスの案内枠を追加
old_status = '<div class="status-bar" id="statusBar">'
new_status = '''<div style="background:#f1f5f9; border-bottom:1px solid #cbd5e1; padding:5px 16px; font-size:12px; color:#334155; display:flex; flex-wrap:wrap; gap:12px; align-items:center;">
    <span>📂 <b>AI解析SGF標準フォルダ：</b><code style="background:#e2e8f0; padding:1px 5px; border-radius:3px;">/home/kazuo/sgfout/</code></span>
    <span>💾 <b>ブラウザ保存先：</b><code style="background:#e2e8f0; padding:1px 5px; border-radius:3px;">/home/kazuo/ダウンロード/</code></span>
    <span id="activeFilePathLabel" style="color:#0369a1; font-weight:bold;"></span>
</div>
<div class="status-bar" id="statusBar">'''

if "activeFilePathLabel" not in html and old_status in html:
    html = html.replace(old_status, new_status, 1)

# 2. 読込時にファイル名・推定パスを表示
old_load = "recalculateAndRender();"
new_load = '''const pathLbl = document.getElementById('activeFilePathLabel');
        if (pathLbl) {
            const guessedDir = fallbackName.startsWith("KaTrain_") ? "/home/kazuo/sgfout/" : "選択フォルダ/";
            pathLbl.textContent = "📄 読込元：" + guessedDir + fallbackName;
        }
        recalculateAndRender();'''

if "activeFilePathLabel" in html and "読込元：" not in html:
    html = html.replace(old_load, new_load, 1)

# 3. 保存時に保存先パスを通知
old_dl = "URL.revokeObjectURL(url);"
new_dl = '''URL.revokeObjectURL(url);
    const savedName = ((currentGame && currentGame.eventName) ? currentGame.eventName : "kifu_data").replace(/[\\\\/:*?"<>|]/g, "_") + ".sgf";
    alert("✅ SGFファイルを保存しました！\\n\\n【保存先パス】\\n/home/kazuo/ダウンロード/" + savedName);'''

if "【保存先パス】" not in html and old_dl in html:
    html = html.replace(old_dl, new_dl, 1)

with open("saibiprint.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ 読込・保存のパス表示機能を追加しました！")
