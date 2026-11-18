/* fig-extension.js — Figure 6, "Later coaches did not build better players".
   x = the generation the coach was picked at (0 / 12 / 20 / 40, proportional spacing),
   or the cumulative coach tokens along the picked coach's lineage in its source run.
   One line per seed 0–3 (seed i = source_s{i+1}); grey dots = runs outside those lines
   (the six I₀ runs at gen 0, the I_g runs from s5 and s6 at gen 12). Each generation
   column carries its mean and 95% interval (generation mode only). B0 band and the
   xhigh line are reference marks. Repeated coach picks are ringed; s4's gen-20 run,
   whose final player was the unedited A₀, is drawn hollow.
   Data: summary.json (extension, B0, xhigh, final_runs), trees.json (coach_origin).
   Emits: select-run {run} (a point) and select-run {source_sN} (a seed row).
   Listens: select-run (pins that point / seed, quietly).
   Hash: #extension?run=…   (written only on a user pin). */
(function(){
  'use strict';

  var CSS = [
    '.fx-extension{position:relative}',
    '.fx-extension .fxe-controls{display:flex;flex-wrap:wrap;align-items:center;gap:10px 18px;margin:0 0 10px}',
    '.fx-extension .fxe-body{display:grid;grid-template-columns:minmax(0,1fr) 290px;gap:28px;align-items:start}',
    '.fx-extension.narrow .fxe-body{grid-template-columns:minmax(0,1fr);gap:18px}',
    '.fx-extension .fxe-main{min-width:0}',
    '.fx-extension .fxe-note{font-size:13.5px;line-height:1.5;color:var(--ink-2);margin:0 0 6px;min-height:3em}',
    '.fx-extension svg.fxe-plot{display:block;width:100%;height:auto;overflow:visible;font-variant-numeric:tabular-nums}',
    '.fx-extension .fxe-ax-title{fill:var(--ink-muted);font-family:var(--font-mono);font-size:11.5px}',
    '.fx-extension .fxe-ax-sub{fill:var(--ink-muted);font-family:var(--font-mono);font-size:11px}',
    '.fx-extension .fxe-ref-xh{stroke:var(--ink-muted);stroke-width:1.2}',
    '.fx-extension .fxe-ref-lbl{fill:var(--ink-2);font-size:12.5px}',
    '.fx-extension .fxe-ref-lbl tspan.v{font-family:var(--font-mono);font-size:12px}',
    '.fx-extension .fxe-mean-lbl{fill:var(--ink);font-family:var(--font-mono);font-size:11.5px}',
    '.fx-extension .fxe-seed-line{stroke:var(--ink-2);stroke-width:1.3;fill:none;transition:stroke var(--dur),stroke-width var(--dur)}',
    '.fx-extension .fxe-seed-hit{stroke:transparent;stroke-width:16;fill:none;cursor:pointer;pointer-events:stroke}',
    '.fx-extension .fxe-seed-lbl{fill:var(--ink-2);font-family:var(--font-mono);font-size:12px;cursor:pointer}',
    '.fx-extension .fxe-pt{fill:var(--ink);stroke:var(--panel);stroke-width:1.5;cursor:pointer;transition:fill var(--dur)}',
    '.fx-extension .fxe-pt.other{fill:var(--ramp-1);stroke:var(--panel)}',
    '.fx-extension .fxe-pt.a0{fill:var(--panel);stroke:var(--ink);stroke-width:1.5;stroke-dasharray:2 1.6}',
    '.fx-extension .fxe-ring{fill:none;stroke:var(--ink);stroke-width:1;stroke-dasharray:2 2;pointer-events:none}',
    '.fx-extension .fxe-sel{fill:none;stroke:var(--accent);stroke-width:2;pointer-events:none}',
    '.fx-extension .fxe-rep{fill:var(--ink-muted);font-family:var(--font-mono);font-size:10.5px;pointer-events:none}',
    '.fx-extension .fxe-mk circle{fill:var(--panel);stroke:var(--ink-2);stroke-width:1}',
    '.fx-extension .fxe-mk text{fill:var(--ink);font-family:var(--font-mono);font-size:10.5px;font-weight:500}',
    '.fx-extension .fxe-ptg{outline:none}',
    '.fx-extension .fxe-ptg:focus-visible .fxe-focus{stroke:var(--accent);stroke-width:2;fill:none}',
    '.fx-extension .fxe-focus{fill:none;stroke:none;pointer-events:none}',
    '.fx-extension .fxe-seed.hot .fxe-seed-line{stroke:var(--accent);stroke-width:2.4}',
    '.fx-extension .fxe-seed.hot .fxe-seed-lbl{fill:var(--accent);font-weight:500}',
    '.fx-extension .fxe-ptg.hot .fxe-pt:not(.a0){fill:var(--accent)}',
    '.fx-extension .fxe-ptg.hot .fxe-pt.a0{stroke:var(--accent)}',
    '.fx-extension .fxe-ptg.hot .fxe-rep{fill:var(--accent)}',
    '.fx-extension.pinned .fxe-seed:not(.hot),.fx-extension.pinned .fxe-ptg:not(.hot):not(.pin){opacity:.35}',
    '.fx-extension .fxe-readout{font-size:13.5px;line-height:1.5;color:var(--ink-2);margin:6px 0 0;min-height:3em}',
    '.fx-extension .fxe-readout b{color:var(--ink);font-weight:600}',
    '.fx-extension .fxe-readout .m{font-family:var(--font-mono);font-size:12.5px}',
    '.fx-extension .fxe-diff{display:flex;flex-wrap:wrap;align-items:center;gap:4px 14px;margin-top:12px;padding-top:12px;border-top:1px solid var(--rule)}',
    '.fx-extension .fxe-diff .k{font-size:13.5px;font-weight:600;color:var(--ink)}',
    '.fx-extension .fxe-diff .v{font-family:var(--font-mono);font-size:12.5px;color:var(--ink-2)}',
    '.fx-extension .fxe-diff svg{display:block;flex:1 1 180px;max-width:320px;height:30px;overflow:visible}',
    '.fx-extension .fxe-side h4{font-size:14px;font-weight:600;margin:0 0 6px;line-height:1.3}',
    '.fx-extension .fxe-side .sub{font-size:13px;color:var(--ink-muted);margin:0 0 8px;line-height:1.45}',
    '.fx-extension table.fxe-tab{border-collapse:collapse;width:100%;font-size:13px;line-height:1.35;font-variant-numeric:tabular-nums}',
    '.fx-extension table.fxe-tab th,.fx-extension table.fxe-tab td{text-align:left;padding:6px 6px 6px 0;border-bottom:1px solid var(--rule);vertical-align:top}',
    '.fx-extension table.fxe-tab thead th{font-size:11px;font-weight:600;letter-spacing:.05em;text-transform:uppercase;color:var(--ink-muted);border-bottom:1px solid var(--rule-strong)}',
    '.fx-extension table.fxe-tab td .n{font-family:var(--font-mono);font-size:12px;color:var(--ink-2);display:block}',
    '.fx-extension table.fxe-tab td .s{font-family:var(--font-mono);font-size:12.5px;color:var(--ink);display:block}',
    '.fx-extension table.fxe-tab td .na{color:var(--ink-muted);font-size:12px}',
    '.fx-extension table.fxe-tab .tag{margin:3px 0 0;font-size:10.5px}',
    '.fx-extension table.fxe-tab tr.hot{background:var(--accent-wash)}',
    '.fx-extension table.fxe-tab tr.hot th{box-shadow:inset 2px 0 0 var(--accent)}',
    '.fx-extension .fxe-seedbtn{font:inherit;font-family:var(--font-mono);font-size:12.5px;color:var(--ink);background:transparent;border:1px solid var(--rule-strong);',
    '  border-radius:3px;padding:6px 8px;min-height:40px;min-width:44px;cursor:pointer;line-height:1.2;text-align:left}',
    '.fx-extension .fxe-seedbtn small{display:block;font-size:10.5px;color:var(--ink-muted)}',
    '.fx-extension .fxe-seedbtn:hover{border-color:var(--accent-hover);color:var(--accent-hover)}',
    '.fx-extension .fxe-seedbtn[aria-pressed="true"]{border-color:var(--accent);color:var(--accent);background:var(--accent-wash)}',
    '.fx-extension ol.fxe-notes{list-style:none;margin:16px 0 0;padding:0;font-size:13.5px;line-height:1.5;color:var(--ink-2)}',
    '.fx-extension ol.fxe-notes li{display:grid;grid-template-columns:22px 1fr;gap:6px;margin:0 0 10px}',
    '.fx-extension ol.fxe-notes .no{display:inline-flex;align-items:center;justify-content:center;width:18px;height:18px;border-radius:50%;',
    '  border:1px solid var(--ink-2);font-family:var(--font-mono);font-size:10.5px;color:var(--ink);margin-top:2px}',
    '.fx-extension ol.fxe-notes b{color:var(--ink);font-weight:600}',
    '.fx-extension .fxe-key{display:flex;flex-wrap:wrap;gap:4px 16px;font-size:12.5px;color:var(--ink-2);margin:8px 0 0}',
    '.fx-extension .fxe-key span{display:inline-flex;align-items:center;gap:6px}',
    '.fx-extension .fxe-key svg{width:16px;height:16px;overflow:visible}',
    '.fx-extension .fxe-unpin{margin-left:auto}'
  ].join('\n');

  function injectCSS(){
    if(document.getElementById('fx-extension-css')) return;
    var st = document.createElement('style'); st.id = 'fx-extension-css'; st.textContent = CSS;
    document.head.appendChild(st);
  }

  var GENS = [0, 12, 20, 40];
  var SEEDS = [0, 1, 2, 3];
  var MINUS = '−';

  EX.mount('extension', function(node, ctx){
    injectCSS();
    return EX.loadAll(['summary', 'trees']).then(function(res){
      var S = res[0], T = res[1].trees, F = EX.fmt, E = S.extension;
      var finals = {}; (S.final_runs || []).forEach(function(f){ finals[f.run] = f; });

      /* ---------- points ---------- */
      var pts = E.points.map(function(p){
        var t = T[p.run] || {}, o = t.coach_origin || {};
        var lin = o.source_lineage || null;
        var fin = finals[p.run] || {};
        var src = o.source_run || null;
        var m = src ? /^source_s(\d)$/.exec(src) : null;
        var seed = (p.seed_index != null && p.seed_index >= 0 && p.seed_index <= 3 && m && (+m[1] - 1) === p.seed_index) ? p.seed_index : null;
        return {
          run: p.run, gen: p.generation, score: p.heldout, seed: seed, seedIndex: p.seed_index,
          src: src, node: o.source_node != null ? String(o.source_node) : null, rule: o.rule || '',
          tokens: lin ? lin.cum_meta_tokens : 0, depth: lin ? lin.depth : 0, calls: lin ? lin.cum_meta_calls : 0,
          finalNode: fin.final_node != null ? String(fin.final_node) : (t.final ? String(t.final.final_node) : null),
          repeatOf: null, sameAs: []
        };
      });
      var byRun = {}; pts.forEach(function(p){ byRun[p.run] = p; });
      // repeated coach nodes (same source run + same node picked at an earlier generation)
      var seedPts = {};
      SEEDS.forEach(function(s){
        seedPts[s] = pts.filter(function(p){ return p.seed === s; }).sort(function(a, b){ return a.gen - b.gen; });
        var list = seedPts[s];
        list.forEach(function(p, i){
          for(var j = 0; j < i; j++){ if(list[j].node === p.node){ if(p.repeatOf == null) p.repeatOf = list[j].gen; } }
          p.sameAs = list.filter(function(q){ return q !== p && q.node === p.node; }).map(function(q){ return q.gen; });
        });
      });
      var others = pts.filter(function(p){ return p.seed == null; });
      // dodge: seeds by seed index, grey dots alternate around the column
      SEEDS.forEach(function(s){ seedPts[s].forEach(function(p){ p.dx = (s - 1.5) * 5; }); });
      GENS.forEach(function(g){
        var o = others.filter(function(p){ return p.gen === g; }).sort(function(a, b){ return a.score - b.score; });
        o.forEach(function(p, i){ p.dx = g === 0 ? (i % 2 ? 5 : -5) : 11 + (i % 2) * 4; });
      });
      var PG = E.per_generation;
      var seedName = function(s){ return 's' + (s + 1); };
      var srcOf = function(s){ return 'source_s' + (s + 1); };

      /* facts computed from data for the notes */
      var s0 = seedPts[0];
      var s0same = s0.length > 1 && s0.every(function(p){ return p.node === s0[0].node; });
      var a0Pts = pts.filter(function(p){ return p.finalNode === 'initial'; });
      var gen12srcs = pts.filter(function(p){ return p.gen === 12; }).map(function(p){ return p.src; });
      var gen20srcs = pts.filter(function(p){ return p.gen === 20; }).map(function(p){ return p.src; });
      var extra12 = gen12srcs.filter(function(s){ return gen20srcs.indexOf(s) < 0; });
      var miss12 = gen20srcs.filter(function(s){ return gen12srcs.indexOf(s) < 0; });
      var trans = 0, nonInc = 0;
      SEEDS.forEach(function(s){ var l = seedPts[s]; for(var i = 1; i < l.length; i++){ trans++; if(l[i].tokens <= l[i - 1].tokens) nonInc++; } });

      /* ---------- state ---------- */
      var st = { mode: 'gen', hoverSeed: null, hoverRun: null, pinSeed: null, pinRun: null };
      var h0 = EX.hash.get();
      if(h0.section === 'extension'){
        if(h0.params.run && byRun[h0.params.run]){ st.pinRun = h0.params.run; st.pinSeed = byRun[h0.params.run].seed; }
        if(h0.params.x === 'tokens') st.mode = 'tokens';
      }

      /* ---------- skeleton ---------- */
      node.innerHTML = '';
      var root = EX.h('div', { 'class': 'fx-extension' }, node);
      var controls = EX.h('div', { 'class': 'fxe-controls' }, root);
      var seg = EX.seg(controls, [{ value: 'gen', label: 'Generation' }, { value: 'tokens', label: 'Coach tokens in lineage' }], st.mode,
        function(v){ st.mode = v; place(true); writeNote(); }, { label: 'x-axis' });
      var unpin = EX.h('button', { type: 'button', 'class': 'btn quiet small fxe-unpin' }, controls, 'Clear selection');
      unpin.hidden = true;
      unpin.addEventListener('click', function(){ st.pinSeed = null; st.pinRun = null; applyState(); EX.hash.set('extension', {}); });

      var body = EX.h('div', { 'class': 'fxe-body' }, root);
      var main = EX.h('div', { 'class': 'fxe-main' }, body);
      var note = EX.h('p', { 'class': 'fxe-note' }, main);
      var plotWrap = EX.h('div', null, main);
      var key = EX.h('div', { 'class': 'fxe-key', 'aria-label': 'Key' }, main);
      var readout = EX.h('p', { 'class': 'fxe-readout', 'aria-live': 'polite' }, main);
      var diffRow = EX.h('div', { 'class': 'fxe-diff' }, main);
      var side = EX.h('div', { 'class': 'fxe-side side-panel' }, body);

      /* key */
      function keyItem(svgInner, text){
        var sp = EX.h('span', null, key);
        var sv = EX.s('svg', { viewBox: '-8 -8 16 16', 'aria-hidden': 'true' }, sp);
        sv.innerHTML = svgInner; EX.h('span', null, sp, text);
      }
      keyItem('<line x1="-8" x2="8" y1="0" y2="0" class="fxe-seed-line"/><circle r="4" class="fxe-pt"/>', 'one seed (s1–s4)');
      keyItem('<circle r="4" class="fxe-pt other"/>', 'other runs (I₀ at 0; s5, s6 at 12)');
      keyItem('<circle r="4" class="fxe-pt"/><circle r="7.5" class="fxe-ring"/>', 'same coach node as an earlier pick');
      keyItem('<circle r="4" class="fxe-pt a0"/>', 'final player was the unedited A₀');
      keyItem('<rect x="-8" y="-5" width="16" height="10" class="b0-band"/><line x1="-8" x2="8" class="b0-line"/>', 'band: B0, two plain attempts (3 reps, dashed = mean)');

      /* gen40 − gen0 strip */
      var dd = E.gen40_minus_gen0;
      EX.h('span', { 'class': 'k' }, diffRow, 'Gen 40 − gen 0');
      var dsv = EX.s('svg', { 'class': 'fxe-dsv', role: 'img',
        'aria-label': 'Generation 40 minus generation 0: ' + F.ptsU(dd.est) + ', 95% interval ' + F.ci(dd.lo, dd.hi) }, diffRow);
      EX.h('span', { 'class': 'v' }, diffRow, F.ptsU(dd.est) + ' · 95% interval ' + F.ci(dd.lo, dd.hi));
      function drawDiff(){
        dsv.innerHTML = '';
        var w = dsv.getBoundingClientRect().width || 240;
        var lim = Math.max(Math.abs(dd.lo), Math.abs(dd.hi)) * 1.15;
        var x = d3.scaleLinear().domain([-lim, lim]).range([8, w - 8]);
        EX.s('line', { 'class': 'zero-line', x1: x(0), x2: x(0), y1: 2, y2: 22 }, dsv);
        EX.s('line', { 'class': 'ci-line', x1: x(dd.lo), x2: x(dd.hi), y1: 12, y2: 12 }, dsv);
        [dd.lo, dd.hi].forEach(function(v){ EX.s('line', { 'class': 'ci-line', x1: x(v), x2: x(v), y1: 8, y2: 16 }, dsv); });
        EX.s('circle', { cx: x(dd.est), cy: 12, r: 4, fill: 'var(--ink)' }, dsv);
        EX.s('text', { 'class': 'fxe-ax-sub', x: x(0), y: 32, 'text-anchor': 'middle' }, dsv, '0');
      }

      /* side: picks table + notes */
      EX.h('h4', null, side, 'Which coach each seed picked');
      EX.h('p', { 'class': 'sub' }, side, 'Coach node in the source run, and the exam score of the player it built. Choose a seed to highlight it.');
      var tab = EX.h('table', { 'class': 'fxe-tab' }, side);
      var thr = EX.h('tr', null, EX.h('thead', null, tab));
      EX.h('th', { scope: 'col' }, thr, 'seed');
      [12, 20, 40].forEach(function(g){ EX.h('th', { scope: 'col' }, thr, 'gen ' + g); });
      var tb = EX.h('tbody', null, tab);
      var rows = {}, seedBtns = {};
      SEEDS.forEach(function(s){
        var tr = rows[s] = EX.h('tr', null, tb);
        var th = EX.h('th', { scope: 'row' }, tr);
        var b = seedBtns[s] = EX.h('button', { type: 'button', 'class': 'fxe-seedbtn', 'aria-pressed': 'false',
          'aria-label': 'Highlight seed ' + s + ', ' + srcOf(s) }, th);
        b.innerHTML = EX.esc(seedName(s)) + '<small>seed ' + s + '</small>';
        b.addEventListener('click', function(){ pinSeed(s); });
        b.addEventListener('mouseenter', function(){ st.hoverSeed = s; applyState(); });
        b.addEventListener('mouseleave', function(){ st.hoverSeed = null; applyState(); });
        b.addEventListener('focus', function(){ st.hoverSeed = s; applyState(); });
        b.addEventListener('blur', function(){ st.hoverSeed = null; applyState(); });
        [12, 20, 40].forEach(function(g){
          var td = EX.h('td', null, tr);
          var p = seedPts[s].filter(function(q){ return q.gen === g; })[0];
          if(!p){ EX.h('span', { 'class': 'na' }, td, g === 12 ? 'no I_g pick' : 'not tested'); return; }
          EX.h('span', { 'class': 'n' }, td, 'node ' + p.node);
          EX.h('span', { 'class': 's' }, td, F.pct(p.score));
          if(p.repeatOf != null) EX.h('span', { 'class': 'tag' }, td, 'same as g' + p.repeatOf);
          if(p.finalNode === 'initial') EX.h('span', { 'class': 'tag' }, td, 'final = A₀');
        });
      });

      var notes = EX.h('ol', { 'class': 'fxe-notes' }, side);
      var noteItems = [];
      if(s0same){
        var sc = s0.map(function(p){ return p.score; });
        var spread = Math.max.apply(null, sc) - Math.min.apply(null, sc);
        noteItems.push({ at: s0[s0.length - 1], html: '<b>One coach, three players.</b> <code>' + EX.esc(s0[0].src) + '</code> picked node ' + EX.esc(s0[0].node) +
          ' at generations ' + s0.map(function(p){ return p.gen; }).join(', ') + '. Re-running that one fixed coach gave players scoring ' +
          s0.map(function(p){ return F.pct(p.score); }).join(', ') + ': a spread of ' + F.num(spread * 100, 1) + ' points.' });
      }
      a0Pts.forEach(function(p){
        noteItems.push({ at: p, html: '<b>No edit kept.</b> In ' + EX.esc(EX.runLabel(p.run)) + ', the final player chosen after 8 rounds was the unedited A₀ (node <code>initial</code>), so its ' +
          F.pct(p.score) + ' measures no coaching at all.' });
      });
      // other repeated picks, as a plain sentence
      var reps = [];
      SEEDS.slice(1).forEach(function(s){
        seedPts[s].forEach(function(p){ if(p.repeatOf != null) reps.push('<code>' + EX.esc(p.src) + '</code> node ' + EX.esc(p.node) + ' at ' + p.repeatOf + ' and ' + p.gen); });
      });
      if(reps.length) noteItems.push({ at: null, html: '<b>Also re-picked:</b> ' + reps.join('; ') + '. For these seeds a "change" between generations is the noise of re-running one coach.' });
      noteItems.forEach(function(n, i){
        n.no = i + 1;
        var li = EX.h('li', null, notes);
        EX.h('span', { 'class': 'no', 'aria-hidden': 'true' }, li, String(n.no));
        EX.h('span', { html: n.html }, li);
      });

      function writeNote(){
        if(st.mode === 'gen'){
          note.innerHTML = 'x is the generation the coach was picked at, spaced in proportion. Generation 12 is the five I<sub>g</sub> runs: it includes ' +
            extra12.map(function(s){ return '<code>' + EX.esc(s) + '</code>'; }).join(' and ') + ' (grey) and has no ' +
            miss12.map(function(s){ return '<code>' + EX.esc(s) + '</code>'; }).join(', ') + ' pick, so it is not the same set of seeds as 20 and 40.';
        } else {
          note.innerHTML = 'x is the coach tokens spent along the picked coach’s ancestry in its source run (I<sub>0</sub> = 0). In ' + nonInc + ' of ' + trans +
            ' steps from one pick to the next, the later pick had <i>no more</i> coach work behind it: a later generation did not mean a more-evolved coach. Means and intervals are per generation, so they are shown only on the generation axis.';
        }
      }

      /* ---------- plot ---------- */
      var svg, G = {}, X, Y, W, H, M, narrow = false;
      var yLo = Math.min(d3.min(pts, function(p){ return p.score; }), Math.min.apply(null, S.B0.reps)) - 0.02;
      var yHi = Math.max(d3.max(pts, function(p){ return p.score; }), S.xhigh.score) + 0.018;

      function build(){
        var w = Math.max(280, plotWrap.getBoundingClientRect().width || ctx.width());
        narrow = (root.getBoundingClientRect().width || w) < 720;
        root.classList.toggle('narrow', narrow);
        plotWrap.innerHTML = '';
        W = w; H = narrow ? 344 : 414;
        M = { t: 26, r: narrow ? 30 : 40, b: 66, l: 40 };
        svg = EX.s('svg', { 'class': 'fxe-plot', viewBox: '0 0 ' + W + ' ' + H, width: W, height: H, role: 'group',
          'aria-label': 'Exam score by coach generation, one line per seed' }, plotWrap);
        Y = d3.scaleLinear().domain([yLo, yHi]).range([H - M.b, M.t]);
        // y grid + axis
        var gy = EX.s('g', { 'class': 'axis' }, svg);
        Y.ticks(5).forEach(function(v){
          EX.s('line', { 'class': 'gridline', x1: M.l, x2: W - M.r + 6, y1: Y(v), y2: Y(v) }, gy);
          EX.s('text', { x: M.l - 8, y: Y(v), dy: '0.32em', 'text-anchor': 'end' }, gy, F.pct(v, 0));
        });
        EX.s('text', { 'class': 'fxe-ax-title', x: M.l - 8, y: M.t - 12, 'text-anchor': 'start', transform: null }, svg, 'exam score (pass@2)');
        // B0 band + line
        var b0lo = Math.min.apply(null, S.B0.reps), b0hi = Math.max.apply(null, S.B0.reps);
        EX.s('rect', { 'class': 'b0-band', x: M.l, width: W - M.r - M.l + 6, y: Y(b0hi), height: Y(b0lo) - Y(b0hi) }, svg);
        EX.s('line', { 'class': 'b0-line', x1: M.l, x2: W - M.r + 6, y1: Y(S.B0.mean), y2: Y(S.B0.mean) }, svg);
        // xhigh line
        EX.s('line', { 'class': 'fxe-ref-xh', x1: M.l, x2: W - M.r + 6, y1: Y(S.xhigh.score), y2: Y(S.xhigh.score) }, svg);
        var xl = EX.s('text', { 'class': 'fxe-ref-lbl halo', x: M.l + 6, y: Y(S.xhigh.score) - 6 }, svg);
        xl.innerHTML = EX.esc(narrow ? 'A₀ at xhigh effort ' : EX.GROUP_LABEL.xhigh + ' (reference) ') + '<tspan class="v">' + F.pct(S.xhigh.score) + '</tspan>';
        G.b0lbl = EX.s('text', { 'class': 'fxe-ref-lbl halo', y: Y(b0hi) - 6, 'text-anchor': 'middle' }, svg);
        G.b0lbl.innerHTML = 'B0 ' + '<tspan class="v">' + F.pct(S.B0.mean) + '</tspan>';
        G.xaxis = EX.s('g', { 'class': 'axis' }, svg);
        EX.s('line', { x1: M.l, x2: W - M.r + 6, y1: H - M.b, y2: H - M.b }, svg).setAttribute('class', 'zero-line');
        G.xtitle = EX.s('text', { 'class': 'fxe-ax-title', x: W - M.r + 6, y: H - 2, 'text-anchor': 'end' }, svg);
        // CI columns
        G.ci = GENS.map(function(g){
          var c = PG[String(g)], gg = EX.s('g', { 'class': 'fxe-ci' }, svg);
          var o = { g: g, el: gg, c: c };
          o.v = EX.s('line', { 'class': 'ci-line', y1: Y(c.lo), y2: Y(c.hi) }, gg);
          o.t1 = EX.s('line', { 'class': 'ci-line', y1: Y(c.lo), y2: Y(c.lo) }, gg);
          o.t2 = EX.s('line', { 'class': 'ci-line', y1: Y(c.hi), y2: Y(c.hi) }, gg);
          o.m = EX.s('line', { 'class': 'mean-tick', y1: Y(c.mean), y2: Y(c.mean) }, gg);
          var t = EX.s('title', null, gg, 'Generation ' + g + ': mean ' + F.pct(c.mean) + ', 95% interval ' + F.ciPct(c.lo, c.hi) + ', n = ' + c.n);
          return o;
        });
        // seed lines
        G.seeds = SEEDS.map(function(s){
          var gg = EX.s('g', { 'class': 'fxe-seed', 'data-seed': s }, svg);
          var o = { s: s, el: gg };
          o.line = EX.s('path', { 'class': 'fxe-seed-line' }, gg);
          o.hit = EX.s('path', { 'class': 'fxe-seed-hit' }, gg);
          o.lbl = EX.s('text', { 'class': 'fxe-seed-lbl halo', dy: '0.32em' }, gg, seedName(s));
          [o.hit, o.lbl].forEach(function(el){
            el.addEventListener('mouseenter', function(){ st.hoverSeed = s; applyState(); });
            el.addEventListener('mouseleave', function(){ st.hoverSeed = null; applyState(); });
            el.addEventListener('click', function(){ pinSeed(s); });
          });
          return o;
        });
        // points
        G.pts = pts.map(function(p){
          var gg = EX.s('g', { 'class': 'fxe-ptg', tabindex: 0, role: 'button', 'data-run': p.run,
            'aria-label': pointLabel(p) }, svg);
          var o = { p: p, el: gg };
          if(p.repeatOf != null) o.ring = EX.s('circle', { 'class': 'fxe-ring', r: 8.5 }, gg);
          o.sel = EX.s('circle', { 'class': 'fxe-sel', r: 9, style: { display: 'none' } }, gg);
          o.focus = EX.s('circle', { 'class': 'fxe-focus', r: 11 }, gg);
          o.dot = EX.s('circle', { 'class': 'fxe-pt' + (p.seed == null ? ' other' : '') + (p.finalNode === 'initial' ? ' a0' : ''), r: p.seed == null ? 4 : 4.6 }, gg);
          o.hit = EX.s('circle', { r: 12, fill: 'transparent', stroke: 'none' }, gg);
          if(p.repeatOf != null && !narrow) o.rep = EX.s('text', { 'class': 'fxe-rep halo', dy: '0.32em' }, gg, '= g' + p.repeatOf);
          EX.tooltip.attach(gg, function(){ return tipHTML(p); });
          gg.addEventListener('mouseenter', function(){ st.hoverRun = p.run; st.hoverSeed = p.seed; applyState(); });
          gg.addEventListener('mouseleave', function(){ st.hoverRun = null; st.hoverSeed = null; applyState(); });
          gg.addEventListener('focus', function(){ st.hoverRun = p.run; st.hoverSeed = p.seed; applyState(); });
          gg.addEventListener('blur', function(){ st.hoverRun = null; st.hoverSeed = null; applyState(); });
          gg.addEventListener('click', function(){ pinRun(p.run); });
          gg.addEventListener('keydown', function(e){
            if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); pinRun(p.run); }
          });
          return o;
        });
        // numbered markers for the notes
        G.mk = noteItems.filter(function(n){ return n.at; }).map(function(n){
          var gg = EX.s('g', { 'class': 'fxe-mk', 'aria-hidden': 'true' }, svg);
          EX.s('circle', { r: 8 }, gg); EX.s('text', { 'text-anchor': 'middle', dy: '0.35em' }, gg, String(n.no));
          return { n: n, el: gg };
        });
        place(false);
        applyState();
        drawDiff();
      }

      function xOf(p){
        return st.mode === 'gen' ? X(p.gen) + p.dx : X(p.tokens) + (p.seed != null || p.gen === 0 ? p.dx : 0);
      }
      function place(animate){
        var dur = animate ? EX.dur(260) : 0;
        var x0 = M.l + (narrow ? 34 : 46), x1 = W - M.r - (narrow ? 8 : 14);
        if(st.mode === 'gen') X = d3.scaleLinear().domain([0, 40]).range([x0, x1]);
        else X = d3.scaleLinear().domain([0, d3.max(pts, function(p){ return p.tokens; }) * 1.04]).range([x0, x1]);
        // x axis
        G.xaxis.innerHTML = '';
        if(st.mode === 'gen'){
          GENS.forEach(function(g){
            var c = PG[String(g)];
            EX.s('line', { x1: X(g), x2: X(g), y1: H - M.b, y2: H - M.b + 5 }, G.xaxis);
            EX.s('text', { x: X(g), y: H - M.b + 18, 'text-anchor': 'middle' }, G.xaxis, String(g));
            EX.s('text', { 'class': 'fxe-ax-sub', x: X(g), y: H - M.b + 32, 'text-anchor': 'middle' }, G.xaxis,
              narrow ? 'n=' + c.n : (g === 0 ? 'I₀' : g === 12 ? 'I_g' : 'ext') + ' · n=' + c.n);
            EX.s('text', { 'class': 'fxe-mean-lbl', x: X(g), y: H - M.b + 46, 'text-anchor': 'middle' }, G.xaxis,
              narrow ? F.num(c.mean * 100, 1) : 'mean ' + F.pct(c.mean));
          });
          G.xtitle.textContent = 'coach picked at generation';
        } else {
          X.ticks(narrow ? 3 : 5).forEach(function(v){
            EX.s('line', { x1: X(v), x2: X(v), y1: H - M.b, y2: H - M.b + 5 }, G.xaxis);
            EX.s('text', { x: X(v), y: H - M.b + 18, 'text-anchor': 'middle' }, G.xaxis, v === 0 ? '0' : F.tokens(v));
          });
          G.xtitle.textContent = narrow ? 'coach tokens in lineage' : 'cumulative coach tokens in the picked coach’s lineage';
        }
        var b0x = st.mode === 'gen' ? X(narrow ? 30 : 6) : W - M.r + 6;
        G.b0lbl.setAttribute('text-anchor', st.mode === 'gen' ? 'middle' : 'end');
        G.b0lbl.setAttribute('y', st.mode === 'gen' && !narrow ? Y(Math.max.apply(null, S.B0.reps)) - 6 : Y(Math.min.apply(null, S.B0.reps)) + 15);
        d3.select(G.b0lbl).transition().duration(dur).attr('x', b0x);
        // CI columns
        G.ci.forEach(function(o){
          o.el.style.display = st.mode === 'gen' ? '' : 'none';
          var cx = X(o.g) - (o.g === 0 ? 16 : 18);
          [o.v].forEach(function(l){ l.setAttribute('x1', cx); l.setAttribute('x2', cx); });
          [o.t1, o.t2].forEach(function(l){ l.setAttribute('x1', cx - 3); l.setAttribute('x2', cx + 3); });
          o.m.setAttribute('x1', cx - 6); o.m.setAttribute('x2', cx + 6);
        });
        // seed lines
        G.seeds.forEach(function(o){
          var list = seedPts[o.s];
          var d = list.map(function(p, i){ return (i ? 'L' : 'M') + xOf(p).toFixed(1) + ',' + Y(p.score).toFixed(1); }).join('');
          d3.select(o.line).transition().duration(dur).attr('d', d);
          o.hit.setAttribute('d', d);
          // label: right of the last point (gen mode) / right of the right-most point (tokens)
          var last = list[list.length - 1];
          if(st.mode === 'tokens') last = list.slice().sort(function(a, b){ return xOf(b) - xOf(a) || b.gen - a.gen; })[0];
          d3.select(o.lbl).transition().duration(dur).attr('x', xOf(last) + 9).attr('y', Y(last.score));
        });
        G.pts.forEach(function(o){
          var x = xOf(o.p), y = Y(o.p.score);
          d3.select(o.el).transition().duration(dur).attr('transform', 'translate(' + x.toFixed(1) + ',' + y.toFixed(1) + ')');
          if(o.rep){ o.rep.setAttribute('x', 0); o.rep.setAttribute('y', 16); o.rep.setAttribute('text-anchor', 'middle'); o.rep.style.display = st.mode === 'gen' ? '' : 'none'; }
        });
        G.mk.forEach(function(m){
          var p = m.n.at, x = xOf(p), y = Y(p.score);
          var dy = Y(p.score) - 30 < M.t ? 18 : -18;
          d3.select(m.el).transition().duration(dur).attr('transform', 'translate(' + (x + 12).toFixed(1) + ',' + (y + dy).toFixed(1) + ')');
        });
      }

      function pointLabel(p){
        var s = EX.runLabel(p.run) + ', exam ' + F.pct(p.score);
        if(p.node != null) s += ', coach ' + p.src + ' node ' + p.node;
        if(p.repeatOf != null) s += ', same coach as the generation ' + p.repeatOf + ' pick';
        if(p.finalNode === 'initial') s += ', final player was the unedited A0';
        return s;
      }
      function tipHTML(p){
        var h = '<b>' + EX.esc(EX.runLabel(p.run)) + '</b><br>exam ' + F.pct(p.score);
        if(p.node != null){
          h += '<br>coach: ' + EX.esc(p.src) + ' node ' + EX.esc(p.node) + ' · ' + F.tokens(p.tokens) + ' coach tokens in lineage';
          if(p.sameAs.length) h += '<br>same coach node also picked at g' + p.sameAs.join(', g');
        } else h += '<br>coach: original I₀';
        if(p.finalNode != null) h += '<br>final player: node ' + EX.esc(p.finalNode) + (p.finalNode === 'initial' ? ' (unedited A₀)' : '');
        return h;
      }

      /* ---------- state rendering ---------- */
      function seedSentence(s){
        var list = seedPts[s];
        var parts = list.map(function(p){
          var t = 'g' + p.gen + ' node <span class="m">' + EX.esc(p.node) + '</span> → ' + F.pct(p.score);
          if(p.repeatOf != null) t += ' <i>(same coach as g' + p.repeatOf + ')</i>';
          if(p.finalNode === 'initial') t += ' <i>(final player = unedited A₀)</i>';
          return t;
        });
        return '<b>' + EX.esc(srcOf(s)) + '</b> (seed ' + s + '): ' + parts.join(' · ');
      }
      function applyState(){
        var seedOn = st.hoverSeed != null ? st.hoverSeed : st.pinSeed;
        var runOn = st.hoverRun || st.pinRun;
        root.classList.toggle('pinned', st.pinSeed != null || st.pinRun != null);
        unpin.hidden = !(st.pinSeed != null || st.pinRun != null);
        if(G.seeds) G.seeds.forEach(function(o){ o.el.classList.toggle('hot', o.s === seedOn); });
        if(G.pts) G.pts.forEach(function(o){
          var hot = (seedOn != null && o.p.seed === seedOn) || o.p.run === runOn;
          o.el.classList.toggle('hot', hot);
          o.el.classList.toggle('pin', o.p.run === st.pinRun);
          o.sel.style.display = o.p.run === st.pinRun ? '' : 'none';
        });
        SEEDS.forEach(function(s){
          rows[s].classList.toggle('hot', s === seedOn);
          seedBtns[s].setAttribute('aria-pressed', String(s === st.pinSeed));
        });
        // readout
        var p = runOn ? byRun[runOn] : null;
        if(p){
          var h = '<b>' + EX.esc(EX.runLabel(p.run)) + '</b>: exam ' + F.pct(p.score) + '. ';
          if(p.node != null){
            h += 'Coach <span class="m">' + EX.esc(p.src) + '</span> node <span class="m">' + EX.esc(p.node) + '</span>, ' + F.tokens(p.tokens) + ' coach tokens along its ' + p.depth + '-step ancestry.';
            if(p.sameAs.length) h += ' The same coach node was also picked at generation ' + p.sameAs.join(' and ') + '.';
          } else h += 'Coach: the original I<sub>0</sub>.';
          if(p.finalNode === 'initial') h += ' Its final player was the unedited A₀.';
          if(p.seed != null) h += '<br>' + seedSentence(p.seed);
          readout.innerHTML = h;
        } else if(seedOn != null){
          readout.innerHTML = seedSentence(seedOn);
        } else {
          readout.innerHTML = 'Hover over or tap a line, point or seed row to see which coach node was picked at each generation. Click to pin.';
        }
      }
      function pinSeed(s){
        if(st.pinSeed === s && st.pinRun == null){ st.pinSeed = null; applyState(); EX.hash.set('extension', {}); return; }
        st.pinSeed = s; st.pinRun = null; applyState();
        EX.select('run', { run: srcOf(s), source: 'extension' });
      }
      function pinRun(run){
        if(st.pinRun === run){ st.pinRun = null; st.pinSeed = null; applyState(); EX.hash.set('extension', {}); return; }
        st.pinRun = run; st.pinSeed = byRun[run].seed; applyState();
        EX.hash.set('extension', { run: run });
        EX.select('run', { run: run, source: 'extension' });
      }

      EX.on('select-run', function(pl){
        if(!pl || pl.source === 'extension') return;
        if(byRun[pl.run]){ st.pinRun = pl.run; st.pinSeed = byRun[pl.run].seed; applyState(); }
        else {
          var m = /^source_s(\d)$/.exec(pl.run || '');
          if(m && +m[1] - 1 <= 3){ st.pinSeed = +m[1] - 1; st.pinRun = null; applyState(); }
        }
      });

      writeNote();
      build();
      ctx.onResize(function(){ build(); });
    });
  });
})();
