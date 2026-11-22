import re

with open("saibiprint.html", "r", encoding="utf-8") as f:
    html = f.read()

# visibility: hidden を使った古い印刷ブロックを整理し、シンプルなブロック表示に統一
html = re.sub(r'@media\s+print\s*\{[\s\S]*?\}\s*\n\s*</style>', '''@media print {
            @page { size: A4 portrait; margin: 0; }
            html, body { margin: 0 !important; padding: 0 !important; background: #fff !important; }
            #previewContainer { display: block !important; margin: 0 !important; padding: 0 !important; }
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
    </style>''', html, count=1)

with open("saibiprint.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ 印刷用スタイルをよりシンプルな形式に整理しました！")
