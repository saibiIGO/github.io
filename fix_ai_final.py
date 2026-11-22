with open("saibiprint.html", "r", encoding="utf-8") as f:
    html = f.read()

s1 = html.find("function extractMainLineMoves")
s2 = html.find("function simulateBoardStates")
if s1 != -1 and s2 != -1:
    clean_extract = r'''function extractMainLineMoves(sgf, size) {
    const moves = new Array();
    const stack = new Array();
    let skipDepth = 0;
    for (let i = 0; i < sgf.length; i++) {
        const ch = sgf.charAt(i);
        if (ch === '(') {
            if (skipDepth > 0) { skipDepth++; }
            else {
                const hasC = stack.length > 0 && stack.at(-1).hasChild;
                if (hasC) { skipDepth = 1; }
                else {
                    if (stack.length > 0) stack.at(-1).hasChild = true;
                    stack.push({ hasChild: false });
                }
            }
        } else if (ch === ')') {
            if (skipDepth > 0) { skipDepth--; }
            else if (stack.length > 0) {
                stack.pop();
                if (stack.length === 0 && moves.length > 0) break;
            }
        } else if (ch === ';' && skipDepth === 0) {
            let nodeEnd = i + 1, inB = false;
            while (nodeEnd < sgf.length) {
                const c = sgf.charAt(nodeEnd);
                if (c === '\\') { nodeEnd += 2; continue; }
                if (c === '[') inB = true;
                else if (c === ']') inB = false;
                else if (!inB && (c === ';' || c === '(' || c === ')')) break;
                nodeEnd++;
            }
            const props = {};
            let p = i + 1;
            while (p < nodeEnd) {
                while (p < nodeEnd && /\s/.test(sgf.charAt(p))) p++;
                let ks = p;
                while (p < nodeEnd && /[A-Za-z]/.test(sgf.charAt(p))) p++;
                const pk = sgf.slice(ks, p).toUpperCase();
                while (p < nodeEnd && /\s/.test(sgf.charAt(p))) p++;
                if (pk && sgf.charAt(p) === '[') {
                    const vals = new Array();
                    while (p < nodeEnd && sgf.charAt(p) === '[') {
                        p++; let vs = p;
                        while (p < nodeEnd) {
                            if (sgf.charAt(p) === '\\') { p += 2; continue; }
                            if (sgf.charAt(p) === ']') break;
                            p++;
                        }
                        vals.push(sgf.slice(vs, p));
                        if (sgf.charAt(p) === ']') p++;
                        while (p < nodeEnd && /\s/.test(sgf.charAt(p))) p++;
                    }
                    props[pk] = vals;
                } else { p++; }
            }
            const mc = props.B ? 'B' : (props.W ? 'W' : null);
            if (mc) {
                const coord = (props[mc].at(0) || "").trim().toLowerCase();
                const rawC = props.C ? props.C.join(" ") : "";
                const cTxt = rawC.replace(/\\([\]\\:])/g, "$1").replace(/[\u200B-\u200D\uFEFF\u3164]/g, "").trim();
                const aiInfo = parseJapaneseKaTrainComment(cTxt);
                if (coord.length === 2) {
                    const x = SGF_CHARS.indexOf(coord.charAt(0));
                    const y = SGF_CHARS.indexOf(coord.charAt(1));
                    if (x >= 0 && y >= 0 && x < size && y < size) {
                        moves.push({ x, y, color: mc, comment: cTxt, ai: aiInfo });
                    }
                }
            }
            i = nodeEnd - 1;
        }
    }
    return moves;
}

function parseJapaneseKaTrainComment(txt) {
    if (!txt) return null;
    const scoreM = txt.match(/目差[：:]\s*([^\s\r\n]+)/);
    const winM = txt.match(/勝率[：:]\s*([黒白]\s*[\d.]+%)/);
    const lossM = txt.match(/推定損失目数[：:]\s*([\d.]+)/);
    const bestM = txt.match(/最善手は\s*([A-T]\d{1,2}(?:\s*\([^)]+\))?)/);
    const pvM = txt.match(/予想手順[：:]\s*([BW]?[A-T]\d{1,2}(?:\s+[BW]?[A-T]\d{1,2})*)/);
    if (!scoreM && !winM && !lossM) return null;
    return {
        scoreText: scoreM ? scoreM.at(1).trim() : "",
        winText: winM ? winM.at(1).trim() : "",
        pointsLost: lossM ? parseFloat(lossM.at(1)) : 0,
        bestText: bestM ? bestM.at(1).trim() : "",
        pvText: pvM ? pvM.at(1).trim() : ""
    };
}

'''
    html = html[:s1] + clean_extract + html[s2:]

# 8分割でも右側AIコメントが省略されないように統一
old_div8 = "if (div === 8) return `<div class=\"diagram-card\"><div class=\"diagram-label\"><span><span class=\"diagram-badge\">第${r.figNum}譜</span> ${rt}</span><span style=\"font-size:10px;color:#475569;\">${sb}</span></div><div class=\"diagram-board-wrap\">${res.svg}</div><div class=\"diagram-note\">${nHtml}</div></div>`;"
if old_div8 in html:
    html = html.replace(old_div8, "")

with open("saibiprint.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ 修正完了！2分割・4分割・8分割すべてでAI解析が表示されます！")
