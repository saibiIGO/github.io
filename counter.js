(function() {
  const page = (location.pathname.split('/').pop() || 'index.html').replace('.html', '');
  const names = {
    'index': '総合トップ', 'member': '会員教室', 'saibiprint': '才美プリント',
    'tsumego': '詰碁保存庫', 'igogenerator': '問題作成教室', 'komonjo': '古文書教室'
  };
  const label = names[page] || page;
  const today = new Date().toISOString().slice(0, 10);
  const key = 'igoschool_v_' + page + '_' + today;
  const isNew = !localStorage.getItem(key);
  if (isNew) localStorage.setItem(key, '1');

  window.addEventListener('DOMContentLoaded', () => {
    const box = document.createElement('div');
    box.style.cssText = 'text-align:center;margin:2px 0;';
    box.innerHTML = '<span style="display:inline-block;background:#f8fafc;border:1px solid #e2e8f0;color:#64748b;padding:1px 8px;border-radius:999px;font-size:10px;opacity:0.85;">👣 ' + label + ' 訪問: <b id="roomCntVal" style="font-size:10.5px;color:#475569;">...</b>人</span>';
    const h1 = document.querySelector('h1');
    if (h1 && h1.parentNode) h1.parentNode.insertBefore(box, h1.nextSibling);
    else document.body.insertBefore(box, document.body.firstChild);

    fetch('https://counterapi.dev' + page + (isNew ? '/up' : ''))
      .then(r => r.json())
      .then(d => { const el = document.getElementById('roomCntVal'); if (el) el.textContent = (d && typeof d.count === 'number') ? d.count.toLocaleString() : '1'; })
      .catch(() => { const el = document.getElementById('roomCntVal'); if (el) el.textContent = '1'; });
  });
})();