with open("saibiprint.html", "r", encoding="utf-8") as f:
    html = f.read()

# 古い beforeprint / afterprint 処理があれば削除
idx_bp = html.find("window.addEventListener('beforeprint'")
if idx_bp != -1:
    idx_end = html.find("</script>", idx_bp)
    html = html[:idx_bp] + html[idx_end:]

strict_js = """
function prepareCleanPrint() {
    const target = document.getElementById('previewContainer');
    if (!target) return;
    window._hiddenPrintEls = [];
    let cur = target;
    while (cur && cur !== document.body) {
        const parent = cur.parentElement;
        if (parent) {
            Array.from(parent.children).forEach(sib => {
                if (sib !== cur && sib.tagName !== 'SCRIPT' && sib.tagName !== 'STYLE') {
                    window._hiddenPrintEls.push({ el: sib, prev: sib.style.display });
                    sib.style.setProperty('display', 'none', 'important');
                }
            });
            window._hiddenPrintEls.push({ el: parent, prevPad: parent.style.padding, prevMar: parent.style.margin });
            parent.style.setProperty('padding', '0', 'important');
            parent.style.setProperty('margin', '0', 'important');
        }
        cur = parent;
    }
    document.querySelectorAll('.a4-sheet').forEach(sheet => {
        sheet.style.setProperty('height', '295mm', 'important');
        sheet.style.setProperty('min-height', '295mm', 'important');
        sheet.style.setProperty('max-height', '295mm', 'important');
        sheet.style.setProperty('overflow', 'hidden', 'important');
    });
}

function restoreAfterPrint() {
    if (!window._hiddenPrintEls) return;
    window._hiddenPrintEls.forEach(item => {
        if ('prev' in item) item.el.style.display = item.prev || '';
        if ('prevPad' in item) {
            item.el.style.padding = item.prevPad || '';
            item.el.style.margin = item.prevMar || '';
        }
    });
    window._hiddenPrintEls = [];
}

window.addEventListener('beforeprint', prepareCleanPrint);
window.addEventListener('afterprint', restoreAfterPrint);
"""

html = html.replace("</script>", strict_js + "\n</script>", 1)
with open("saibiprint.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ 階層をさかのぼって不要要素を完全消去し、全2ページに収める処理を設定しました！")
