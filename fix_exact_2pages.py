with open("saibiprint.html", "r", encoding="utf-8") as f:
    html = f.read()

js_hook = """
window.addEventListener('beforeprint', () => {
    document.querySelectorAll('body > *').forEach(el => {
        if (el.id !== 'previewContainer') {
            el.dataset.prevDisplay = el.style.display || '';
            el.style.setProperty('display', 'none', 'important');
        }
    });
});
window.addEventListener('afterprint', () => {
    document.querySelectorAll('body > *').forEach(el => {
        if (el.id !== 'previewContainer') {
            el.style.display = el.dataset.prevDisplay || '';
        }
    });
});
"""

if "beforeprint" not in html:
    html = html.replace("</script>", js_hook + "\n</script>", 1)

with open("saibiprint.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ 印刷直前にトップ画面・ボタンを物理消去する処理を追加しました！")
