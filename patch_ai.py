with open("saibiprint.html", "r", encoding="utf-8") as f:
    html = f.read()

start_marker = "function extractMainLineMoves(sgf, size) {"
end_marker = "function simulateBoardStates(size, setup, moves) {"

s_idx = html.find(start_marker)
e_idx = html.find(end_marker)
if s_idx == -1 or e_idx == -1:
    raise RuntimeError("対象関数が見つかりません")

new_funcs = """function extractMainLineMoves(sgf, size) {
    const moves = new Array();
    const stack = new Array();
    let skipDepth = 0;

    for (let i = 0; i < sgf.length; i++) {
        const ch = sgf.charAt(i);
        if (ch === '(') {
            if (skipDepth > 0) {
                skipDepth++;
            } else {
                const parentHasChild = stack.length > 0 && stack.at(-1).hasChild;
                if (parentHasChild) {
                    skipDepth = 1;
                } else {
                    if (stack.length > 0) stack.at(-1).hasChild = true;
                    stack.push({ hasChild: false });
                }
            }
        } else if (ch === ')') {
            if (skipDepth > 0) {
                skipDepth--;
            } else if (stack.length > 0) {
                stack.pop();
                if (stack.length === 0 && moves.length > 0) break;
            }
        } else if (ch === ';' && skipDepth === 0) {
            let nodeEnd = i + 1, inB = false;
            while (nodeEnd < sgf.length) {
                const c = sgf.charAt(nodeEnd);
                if (c === '\\\\') { nodeEnd += 2; continue; }
                if (c === '[') inB = true;
                else if (c === ']') inB = false;
                else if (!inB && (c === ';' || c === '(' || c === ')')) break;
                nodeEnd++;
            }
            const props = {};
            let p = i + 1;
            while (p < nodeEnd) {
                while (p < nodeEnd && /\\s/.test(sgf.charAt(p))) p++;
                let ks = p;
                while (p < nodeEnd && /[A-Za-z]/.test(sgf.charAt(p))) p++;
                const pk = sgf.slice(ks, p).toUpperCase();
                while (p < nodeEnd && /\\s/.test(sgf.charAt(p))) p++;
                if (pk && sgf.charAt(p) === '[') {
                    const vals = new Array();
                    while (p < nodeEnd && sgf.charAt(p) === '[') {
                        p++; let vs = p;
                        while (p < nodeEnd) {
                            if (sgf.charAt(p) === '\\\\') { p += 2; continue; }
                            if (sgf.charAt(p) === ']') break;
                            p++;
                        }
                        vals.push(sgf.slice(vs, p));
                        if (sgf.charAt(p) === ']') p++;
                        while (p < nodeEnd && /\\s/.test(sgf.charAt(p))) p++;
                    }
                    props[pk] = vals;
                } else { p++; }
            }
            const mc = props.B ? 'B' : (props.W ? 'W' : null);
            if (mc) {
                const coord = (props[mc].at(0) || "").trim().toLowerCase();
                const cTxt = props.C ? props.C.join("\\n").replace(/\\\\([\\]\\\\:])/g, "$1").replace(/[\\u200B-\\u200D\\uFEFF\\u3164]/g, "").trim() : "";
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
    const scoreM = txt.match(/目差[：:]\\s*([^\\r\\n]+)/);
    const winM = txt.match(/勝率[：:]\\s*([^\\r\\n]+)/);
    const lossM = txt.match(/推定損失目数[：:]\\s*([\\d.]+)/);
    const bestM = txt.match(/最善手は\\s*([^\\r\\n]+)/);
    const pvM = txt.match(/予想手順[：:]\\s*([^\\r\\n]+)/);
    if (!scoreM && !winM && !lossM) return null;
    return {
        scoreText: scoreM ? scoreM.at(1).trim() : "",
        winText: winM ? winM.at(1).trim() : "",
        pointsLost: lossM ? parseFloat(lossM.at(1)) : 0,
        bestText: bestM ? bestM.at(1).trim() : "",
        pvText: pvM ? pvM.at(1).trim() : ""
    };
}

"""

with open("saibiprint.html", "w", encoding="utf-8") as f:
    f.write(html[:s_idx] + new_funcs + html[e_idx:])

print("✅ AI解析ハイライトの自動抽出パッチを適用しました！")
