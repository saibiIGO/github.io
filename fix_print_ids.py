import re

with open("saibiprint.html", "r", encoding="utf-8") as f:
    html = f.read()

ids = set(re.findall(r'id=["\']([^"\']+)["\']', html))
ids.discard("previewContainer")
id_selectors = ", ".join(f"#{i}" for i in sorted(ids))

force_css = f"""
        @media print {{
            {id_selectors}, header, nav, .toolbar, .status-bar, .no-print {{
                display: none !important;
                height: 0 !important;
                margin: 0 !important;
                padding: 0 !important;
            }}
            html, body {{
                background: #ffffff !important;
                margin: 0 !important;
                padding: 0 !important;
            }}
            #previewContainer {{
                display: block !important;
                margin: 0 !important;
                padding: 0 !important;
            }}
        }}
"""

html = html.replace("</style>", force_css + "\n    </style>", 1)
with open("saibiprint.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ 印刷時にA4シート以外の全要素を完全に非表示にしました！")
