with open("saibiprint.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. 「最善手は」の後ろから座標と数字（例：H15, O16）を確実に抽出
s1 = html.find("function parseJapaneseKaTrainComment")
s2 = html.find("function simulateBoardStates")
if s1 != -1 and s2 != -1:
    fixed_fn = r'''function parseJapaneseKaTrainComment(txt) {
    if (!txt) return null;
    const lines = txt.split(/[\r\n]+/).map(s => s.trim()).filter(Boolean);
    let scoreText = "", winText = "", pointsLost = 0, bestText = "", pvText = "", found = false;
    for (const ln of lines) {
        if (ln.startsWith("目差")) { scoreText = ln.replace(/^目差[：:]\s*/, ""); found = true; }
        else if (ln.startsWith("勝率")) { winText = ln.replace(/^勝率[：:]\s*/, ""); found = true; }
        else if (ln.startsWith("推定損失目数")) { pointsLost = parseFloat(ln.replace(/^推定損失目数[：:]\s*/, "")) || 0; found = true; }
        else if (ln.startsWith("最善手は")) {
            const m = ln.match(/([A-HJ-T][0-9]{1,2})/i);
            bestText = m ? m.at(1).toUpperCase() : ln.replace(/^最善手は\s*/, "").split(/\s+/).at(0);
            found = true;
        }
        else if (ln.startsWith("予想手順")) { pvText = ln.replace(/^予想手順[：:]\s*/, ""); found = true; }
    }
    return found ? { scoreText, winText, pointsLost, bestText, pvText } : null;
}

'''
    html = html[:s1] + fixed_fn + html[s2:]

# 2. 碁盤の上辺（A〜T）と左辺（19〜1）に座標目盛りを描画するよう強化
r1 = html.find("function renderDiagramSvg")
r2 = html.find("function toggleCommentEditorBox")
if r1 != -1 and r2 != -1:
    coord_svg_fn = r'''function renderDiagramSvg(game, snapshots, range, divisions, numberMode) {
    const sz = game.size;
    const svgSize = divisions === 2 ? 880 : (divisions === 4 ? 435 : 298);
    const margin = Math.round(svgSize / (sz * 1.48));
    const step = (svgSize - margin * 2) / (sz - 1);
    const stoneR = step * 0.47;
    const ink = document.getElementById('inkShadeSelect')?.value || "#0f172a";
    const colLabels = "ABCDEFGHJKLMNOPQRST";
    const coordFont = Math.max(7.5, Math.round(step * 0.43 * 10) / 10);

    let svg = `<svg width="${svgSize}" height="${svgSize}" viewBox="0 0 ${svgSize} ${svgSize}" xmlns="http://w3.org" style="background:#fff;display:block;">`;

    // 上辺(A〜T)と左辺(19〜1)の座標目盛り
    for (let i = 0; i < sz; i++) {
        const pos = margin + i * step;
        const cLabel = colLabels.charAt(i) || "";
        const rLabel = String(sz - i);
        svg += `<text x="${pos}" y="${margin * 0.42}" fill="#475569" font-size="${coordFont}" font-weight="bold" text-anchor="middle" dominant-baseline="central" font-family="sans-serif">${cLabel}</text>`;
        svg += `<text x="${margin * 0.42}" y="${pos}" fill="#475569" font-size="${coordFont}" font-weight="bold" text-anchor="middle" dominant-baseline="central" font-family="sans-serif">${rLabel}</text>`;
    }

    // 碁盤の線
    for (let i = 0; i < sz; i++) {
        const pos = margin + i * step;
        const sw = (i === 0 || i === sz - 1) ? 1.6 : 0.8;
        svg += `<line x1="${margin}" y1="${pos}" x2="${svgSize - margin}" y2="${pos}" stroke="${ink}" stroke-width="${sw}"/>`;
        svg += `<line x1="${pos}" y1="${margin}" x2="${pos}" y2="${svgSize - margin}" stroke="${ink}" stroke-width="${sw}"/>`;
    }

    const stars = sz === 19 ? Array.of(3,9,15) : (sz === 13 ? Array.of(3,6,9) : (sz === 9 ? Array.of(2,4,6) : new Array()));
    stars.forEach(sx => stars.forEach(sy => {
        svg += `<circle cx="${margin + sx * step}" cy="${margin + sy * step}" r="${Math.max(2.2, step * 0.11)}" fill="${ink}"/>`;
    }));

    if (!range.start) {
        return { svg: svg + `<text x="${svgSize/2}" y="${svgSize/2}" fill="#94a3b8" font-size="14" text-anchor="middle" dominant-baseline="central">（終局済み・余白）</text></svg>`, notes: new Array() };
    }

    const base = snapshots.at(range.start - 1), numMap = new Map(), notes = new Array();
    for (let m = range.start - 1; m < range.end; m++) {
        const mv = game.moves.at(m), no = m + 1, dNo = (numberMode === "RESET") ? (no - range.start + 1) : no, k = `${mv.x},${mv.y}`;
        if (!numMap.has(k)) numMap.set(k, { num: dNo, origNo: no, color: mv.color });
        else {
            const p = numMap.get(k);
            notes.push(`${dNo}は${numberMode === "RESET" ? (p.origNo - range.start + 1) : p.origNo}の所`);
        }
    }
    for (let y = 0; y < sz; y++) {
        for (let x = 0; x < sz; x++) {
            const c = base.at(y).at(x);
            if (c && !numMap.has(`${x},${y}`)) {
                svg += `<circle cx="${margin + x * step}" cy="${margin + y * step}" r="${stoneR}" fill="${c === 'B' ? ink : '#fff'}" stroke="${ink}" stroke-width="1"/>`;
            }
        }
    }
    numMap.forEach((info, k) => {
        const pts = k.split(',').map(Number), cx = margin + pts.at(0) * step, cy = margin + pts.at(1) * step, isB = info.color === 'B';
        const d = String(info.num).length, fs = d >= 3 ? stoneR * 0.85 : (d === 2 ? stoneR * 1.05 : stoneR * 1.25);
        svg += `<circle cx="${cx}" cy="${cy}" r="${stoneR}" fill="${isB ? ink : '#fff'}" stroke="${ink}" stroke-width="1"/>`;
        svg += `<text x="${cx}" y="${cy}" fill="${isB ? '#fff' : ink}" font-size="${fs}" font-weight="bold" text-anchor="middle" dominant-baseline="central" font-family="sans-serif">${info.num}</text>`;
    });
    return { svg: svg + '</svg>', notes };
}

'''
    html = html[:r1] + coord_svg_fn + html[r2:]

with open("saibiprint.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ 最善手の数字（H15等）と、碁盤の座標目盛り（A〜T / 19〜1）の追加が完了しました！")
