with open("saibiprint.html", "r", encoding="utf-8") as f:
    html = f.read()

title_css = """
        .sheet-header { gap: 8px; align-items: flex-end; }
        .sheet-header > div:first-child { min-width: 0; flex: 1; }
        .sheet-title { white-space: nowrap; font-size: 14.5px !important; letter-spacing: -0.02em; }
        .name-box { white-space: nowrap; flex-shrink: 0; }
"""

if ".sheet-title { white-space: nowrap;" not in html and "</style>" in html:
    html = html.replace("</style>", title_css + "\n    </style>", 1)
    with open("saibiprint.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ 一番上のタイトルを美しい1段表示に調整しました！")
