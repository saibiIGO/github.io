with open("saibiprint.html", "r", encoding="utf-8") as f:
    html = f.read()

clean_print_css = """
        @media print {
            body { background: #ffffff !important; margin: 0 !important; padding: 0 !important; }
            body > *:not(.preview-container) { display: none !important; }
            .preview-container { padding: 0 !important; margin: 0 !important; gap: 0 !important; display: block !important; }
            .a4-sheet { box-shadow: none !important; margin: 0 !important; page-break-after: always; break-after: page; }
            .a4-sheet:last-child { page-break-after: auto; break-after: auto; }
        }
"""

if "</style>" in html:
    html = html.replace("</style>", clean_print_css + "\n    </style>", 1)
    with open("saibiprint.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ 印刷時にA4碁盤シート（表面・裏面）のみが綺麗に印刷されるよう設定しました！")
