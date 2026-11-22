import re

with open("saibiprint.html", "r", encoding="utf-8") as f:
    html = f.read()

# 既存の @media print ブロックを安全に除去して重複をなくす
def strip_media_print(text):
    out = []
    i = 0
    while i < len(text):
        m = re.search(r'@media\s+print\s*\{', text[i:])
        if not m:
            out.append(text[i:])
            break
        out.append(text[i:i + m.start()])
        brace_start = i + m.end() - 1
        depth = 0
        j = brace_start
        while j < len(text):
            if text[j] == '{': depth += 1
            elif text[j] == '}':
                depth -= 1
                if depth == 0:
                    j += 1
                    break
            j += 1
        i = j
    return "".join(out)

html = strip_media_print(html)

# 1ページ目＝表面、2ページ目＝裏面の全2ページにピタリと収める決定版CSS
master_print_css = """
        @media print {
            @page { size: A4 portrait; margin: 0; }
            html, body {
                margin: 0 !important;
                padding: 0 !important;
                background: #ffffff !important;
            }
            body * {
                visibility: hidden !important;
            }
            #previewContainer, #previewContainer * {
                visibility: visible !important;
            }
            #previewContainer {
                position: absolute !important;
                left: 0 !important;
                top: 0 !important;
                width: 100% !important;
                margin: 0 !important;
                padding: 0 !important;
                display: block !important;
            }
            .a4-sheet {
                margin: 0 !important;
                box-shadow: none !important;
                page-break-after: always !important;
                break-after: page !important;
            }
            .a4-sheet:last-child {
                page-break-after: auto !important;
                break-after: auto !important;
            }
        }
"""

html = html.replace("</style>", master_print_css + "\n    </style>", 1)
with open("saibiprint.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ 1枚目＝表面、2枚目＝裏面（全2ページ構成）への修正が完了しました！")
