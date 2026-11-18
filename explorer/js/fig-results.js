/* fig-results.js — Figure 4, main result.
   Dot plot of every final player's exam score, grouped by arm (B0 reps, I₀, I_g, gen-20 picks,
   gen-40 picks; A₀ at xhigh set apart as a reference), with arm mean + 95% t-interval bars
   (display only) and the B0 band. Three views (EX.seg): "Exam score" (by arm),
   "vs test-time compute" (score against mean player tokens per test input, linear x) and
   "Score per 10k tokens" (by arm, linear x). Views animate into each other via EX.dur().
   Beside (wide) or under (narrow) the chart: G, Δ and I_g − B0 as Welch intervals against 0,
   values straight from summary.json.
   Data: summary.json, compute.json (at init, both small); trees.json lazily, only to add the
   coach origin to the run readout. Emits: select-run {run, source:'results'}.
   Listens: select-run (rings that dot, if present). Hash: #results?run=…&view=…           */
(function(){
  'use strict';

  var CSS = [
    '.fx-results{position:relative}',
    '.fx-results .fx-r-ctl{margin-bottom:12px}',
    '.fx-results .fx-r-body{display:flex;flex-wrap:wrap;gap:20px 28px;align-items:flex-start}',
    '.fx-results .fx-r-chart{flex:1 1 0;min-width:0}',
    '.fx-results.stack .fx-r-chart{flex:1 1 100%}',
    '.fx-results .fx-r-side{flex:0 0 292px;min-width:0;border-left:1px solid var(--rule);padding-left:24px}',
    '.fx-results.stack .fx-r-side{flex:1 1 100%;border-left:0;padding-left:0;border-top:1px solid var(--rule);padding-top:16px}',
    '.fx-results svg.fx-r-svg{display:block;overflow:visible;font-variant-numeric:tabular-nums}',
    '.fx-results .dg{cursor:pointer;outline:none}',
    '.fx-results .dg .sym{fill:var(--bg);stroke:var(--ink);stroke-width:1.3;transition:stroke-width var(--dur)}',
    '.fx-results .dg .sym.fill{fill:var(--ink-2);stroke:var(--ink-2)}',
    '.fx-results .dg .sym.ref{fill:var(--ink-muted);stroke:var(--ink-muted)}',
    '.fx-results .dg .ring{fill:none;stroke:none;stroke-width:2}',
    '.fx-results .dg:hover .sym,.fx-results .dg.is-hot .sym{stroke-width:2.2}',
    '.fx-results .dg:focus-visible .ring{stroke:var(--accent);stroke-dasharray:3 2}',
    '.fx-results .dg.is-pinned .ring{stroke:var(--accent);stroke-dasharray:none}',
    '.fx-results .dg.is-pinned .sym{stroke:var(--accent);stroke-width:2}',
    '.fx-results .dg.is-pinned .sym.fill,.fx-results .dg.is-pinned .sym.ref{fill:var(--accent)}',
    '.fx-results .dg .hit{fill:transparent;stroke:none}',
    '.fx-results .ci-line{stroke:var(--ink);stroke-width:1.2}',
    '.fx-results .ci-cap{stroke:var(--ink);stroke-width:1.2}',
    '.fx-results .mean-tick{stroke:var(--ink);stroke-width:2.5}',
    '.fx-results .soft .ci-line,.fx-results .soft .ci-cap{stroke:var(--ink-muted);stroke-width:1}',
    '.fx-results .soft .mean-tick{stroke:var(--ink-muted);stroke-width:2}',
    '.fx-results .ci-arrow{fill:var(--ink-muted);font-size:11px;font-family:var(--font-mono)}',
    '.fx-results .rowlab .lbl{font-size:14px}',
    '.fx-results.narrow .rowlab .lbl{font-size:13px}',
    '.fx-results .rowlab .lbl-sub{font-size:11.5px}',
    '.fx-results .rowlab.ref .lbl{fill:var(--ink-2);font-weight:500}',
    '.fx-results .sep{stroke:var(--rule-strong);stroke-width:1;shape-rendering:crispEdges}',
    '.fx-results .band-lab{font-family:var(--font-mono);font-size:11.5px;fill:var(--ink-2)}',
    '.fx-results .anno{font-family:var(--font-mono);font-size:11px;fill:var(--ink-muted)}',
    '.fx-results .anno-line{stroke:var(--ink-muted);stroke-width:1;fill:none}',
    '.fx-results .ax-title{font-family:var(--font-mono);font-size:11.5px;fill:var(--ink-muted)}',
    '.fx-results .fx-r-legend{display:flex;flex-wrap:wrap;gap:4px 16px;margin:8px 0 0;font-size:12.5px;color:var(--ink-2);line-height:1.4}',
    '.fx-results .fx-r-legend span{display:inline-flex;align-items:center;gap:6px;white-space:nowrap}',
    '.fx-results .fx-r-legend svg{overflow:visible}',
    '.fx-results .fx-r-note{font-size:12.5px;line-height:1.5;color:var(--ink-muted);margin:8px 0 0}',
    '.fx-results .fx-r-readout{margin:10px 0 0;padding:8px 12px;background:var(--bg);border:1px solid var(--rule);border-radius:4px;',
    '  font-size:13.5px;line-height:1.5;color:var(--ink-2);min-height:3.2em;font-variant-numeric:tabular-nums}',
    '.fx-results .fx-r-readout b{color:var(--ink);font-weight:600}',
    '.fx-results .fx-r-readout .m{font-family:var(--font-mono);font-size:12.5px}',
    '.fx-results .fx-r-readout .pin{color:var(--accent);font-weight:500}',
    '.fx-results .fx-r-readout .btn{margin-left:8px;vertical-align:baseline}',
    '.fx-results .fx-r-side .fig-sub-text{margin-bottom:14px}',
    '.fx-results .cmp{margin:0 0 18px}',
    '.fx-results .cmp:last-of-type{margin-bottom:8px}',
    '.fx-results .cmp-name{font-size:14px;font-weight:600;color:var(--ink);line-height:1.35}',
    '.fx-results .cmp-name i{font-weight:600}',
    '.fx-results .cmp-val{font-size:13px;color:var(--ink-2);line-height:1.4;margin-top:2px;font-variant-numeric:tabular-nums}',
    '.fx-results .cmp-val .m{font-family:var(--font-mono);font-size:12.5px;color:var(--ink)}',
    '.fx-results .cmp svg{display:block;overflow:visible;margin-top:4px}',
    '.fx-results .cmp .bar{stroke:var(--ink);stroke-width:2}',
    '.fx-results .cmp .cap{stroke:var(--ink);stroke-width:1.2}',
    '.fx-results .cmp .est{fill:var(--ink)}',
    '.fx-results .cmp .z{stroke:var(--rule-strong);stroke-width:1}',
    '.fx-results .cmp .axl{stroke:var(--rule);stroke-width:1}',
    '.fx-results .cmp .tk{font-family:var(--font-mono);font-size:10.5px;fill:var(--ink-muted)}',
    '.fx-results .cmp .dir{font-size:11px;fill:var(--ink-muted)}',
    '.fx-results .cmp-verdict{font-size:12.5px;color:var(--ink-muted);margin-top:2px}',
    '@media (prefers-reduced-motion: reduce){.fx-results .dg .sym{transition:none}}'
  ].join('\n');

  function injectCSS(){
    if(document.getElementById('fx-results-css')) return;
    var st = document.createElement('style'); st.id = 'fx-results-css'; st.textContent = CSS;
    document.head.appendChild(st);
  }

  /* two-sided 95% Student t critical values by df (display intervals only) */
  var T975 = [NaN, 12.706, 4.303, 3.182, 2.776, 2.571, 2.447, 2.365, 2.306, 2.262, 2.228, 2.201, 2.179];
  function tInterval(vals){
    var n = vals.length, m = d3.mean(vals);
    if(n < 2) return { n: n, mean: m, lo: null, hi: null };
    var sd = d3.deviation(vals), h = (T975[n - 1] || 1.96) * sd / Math.sqrt(n);
    return { n: n, mean: m, lo: m - h, hi: m + h };
  }

  var ARMS = ['B0', 'I0', 'Ig', 'g20', 'g40'];
  var REF = 'xhigh';
  var ROWS = ARMS.concat([REF]);
  var NAME = {
    B0: 'B0 · two plain attempts', I0: 'Original coach (I₀)', Ig: 'Evolved coach (I_g)',
    g20: 'Gen-20 coach picks', g40: 'Gen-40 coach picks', xhigh: 'A₀ at xhigh effort'
  };
  var LONG = {
    B0: 'B0, the unedited player A₀ (two plain attempts)', I0: 'player built by the original coach I₀',
    Ig: 'player built by an evolved coach I_g (gen 12)', g20: 'player built by a gen-20 coach (extension)',
    g40: 'player built by a gen-40 coach (extension)', xhigh: 'A₀ at xhigh effort (reference, not a compared arm)'
  };
  var PERGEN = { I0: '0', Ig: '12', g20: '20', g40: '40' };
  var SYM = { B0: 'square', I0: 'circle', Ig: 'circle', g20: 'triangle', g40: 'diamond', xhigh: 'circle' };
  var VIEWS = [
    { value: 'score', label: 'Exam score' },
    { value: 'tokens', label: 'vs test-time compute' },
    { value: 'eff', label: 'Score per 10k tokens' }
  ];

  function symPath(arm, size){
    var t = { square: d3.symbolSquare, circle: d3.symbolCircle, triangle: d3.symbolTriangle, diamond: d3.symbolDiamond }[SYM[arm]];
    var s = size || (arm === 'B0' ? 62 : arm === 'g20' ? 64 : arm === 'g40' ? 62 : 72);
    return d3.symbol().type(t).size(s)();
  }
  function symClass(arm){ return 'sym' + (arm === 'Ig' ? ' fill' : arm === REF ? ' ref' : ''); }

  EX.mount('results', function(node, ctx){
    injectCSS();
    return EX.loadAll(['summary', 'compute']).then(function(res){
      build(node, ctx, res[0], res[1]);
    });
  });

  function build(node, ctx, S, C){
    var F = EX.fmt;
    node.innerHTML = '';

    /* ---------------- data ---------------- */
    var exact = {};
    (S.B0.reps || []).forEach(function(v, i){ exact['B0_rep' + i] = v; });
    Object.keys(S.I0_runs || {}).forEach(function(k){ exact[k] = S.I0_runs[k]; });
    Object.keys(S.Ig_runs || {}).forEach(function(k){ exact[k] = S.Ig_runs[k]; });
    (S.final_runs || []).forEach(function(r){ if(r.heldout != null) exact[r.run] = r.heldout; });
    if(S.xhigh && S.xhigh.score != null) exact.xhigh = S.xhigh.score;
    var finalNode = {};
    (S.final_runs || []).forEach(function(r){ finalNode[r.run] = r.final_node; });

    var runs = C.runs.filter(function(r){ return ROWS.indexOf(r.group) >= 0; }).map(function(r){
      return {
        id: r.run, arm: r.group,
        score: exact[r.run] != null ? exact[r.run] : r.score,
        tok: r.tokens_per_test_input, eff: r.score_per_10k_tokens, calls: r.calls_per_test_input,
        node: r.final_node != null ? r.final_node : finalNode[r.run], gen: r.generation, raw: r
      };
    });
    runs.sort(function(a, b){ return ROWS.indexOf(a.arm) - ROWS.indexOf(b.arm) || a.id.localeCompare(b.id); });
    var byId = {}; runs.forEach(function(r){ byId[r.id] = r; });
    function armRuns(a){ return runs.filter(function(r){ return r.arm === a; }); }

    /* per-arm display intervals. Score: summary.extension.per_generation where it exists
       (those are the same t-intervals), otherwise computed here. Tokens / per-10k: computed here. */
    var stats = { score: {}, eff: {}, tok: {} };
    ARMS.forEach(function(a){
      var rs = armRuns(a);
      var sc = tInterval(rs.map(function(r){ return r.score; }));
      var pg = PERGEN[a] && S.extension && S.extension.per_generation && S.extension.per_generation[PERGEN[a]];
      if(pg && pg.n === rs.length){ sc = { n: pg.n, mean: pg.mean, lo: pg.lo, hi: pg.hi, fromData: true }; }
      stats.score[a] = sc;
      stats.eff[a] = tInterval(rs.map(function(r){ return r.eff; }));
      stats.tok[a] = tInterval(rs.map(function(r){ return r.tok; }));
    });
    var refRun = armRuns(REF)[0];
    stats.score[REF] = { n: 1, mean: refRun ? refRun.score : null };
    stats.eff[REF] = { n: 1, mean: refRun ? refRun.eff : null };

    var b0 = armRuns('B0');
    var band = {
      score: { lo: d3.min(b0, function(r){ return r.score; }), hi: d3.max(b0, function(r){ return r.score; }), mean: S.B0.mean },
      eff: { lo: d3.min(b0, function(r){ return r.eff; }), hi: d3.max(b0, function(r){ return r.eff; }), mean: d3.mean(b0, function(r){ return r.eff; }) }
    };
    // the B0 rep with the odd call count (shown as recorded; note 8 in the prose)
    function repNo(id){ var m = /rep(\d+)/.exec(id); return m ? m[1] : id; }
    var oddB0 = b0.filter(function(r){ return r.calls != null && r.calls < 1.5; })[0] || null;

    /* ---------------- DOM ---------------- */
    var root = EX.h('div', { 'class': 'fx-results' }, node);
    var ctl = EX.h('div', { 'class': 'controls fx-r-ctl' }, root);
    var hashP = EX.hash.get();
    var view = 'score';
    if(hashP.section === 'results' && VIEWS.some(function(v){ return v.value === hashP.params.view; })) view = hashP.params.view;
    var seg = EX.seg(ctl, VIEWS, view, function(v){ setView(v, true); }, { label: 'View' });

    var body = EX.h('div', { 'class': 'fx-r-body' }, root);
    var chartCol = EX.h('div', { 'class': 'fx-r-chart' }, body);
    var svgEl = EX.s('svg', { 'class': 'fx-r-svg', role: 'group', 'aria-label': 'Exam score of every final player, grouped by arm' }, chartCol);
    var legend = EX.h('div', { 'class': 'fx-r-legend', 'aria-label': 'Marker key' }, chartCol);
    ROWS.forEach(function(a){
      var sp = EX.h('span', null, legend);
      var sv = EX.s('svg', { width: 12, height: 12, viewBox: '-6 -6 12 12', 'aria-hidden': 'true' }, sp);
      EX.s('path', { d: symPath(a, 50), 'class': symClass(a), style: { fill: a === 'Ig' ? 'var(--ink-2)' : a === REF ? 'var(--ink-muted)' : 'var(--bg)', stroke: a === REF ? 'var(--ink-muted)' : a === 'Ig' ? 'var(--ink-2)' : 'var(--ink)', strokeWidth: 1.3 } }, sv);
      EX.h('span', null, sp, NAME[a]);
    });
    var note = EX.h('p', { 'class': 'fx-r-note' }, chartCol);
    var readout = EX.h('div', { 'class': 'fx-r-readout', 'aria-live': 'polite' }, chartCol);

    var side = EX.h('div', { 'class': 'fx-r-side' }, body);
    buildSide(side);

    var svg = d3.select(svgEl);
    var gGrid = svg.append('g').attr('class', 'g-grid');
    var gBand = svg.append('g').attr('class', 'g-band');
    var gAx = svg.append('g').attr('class', 'axis g-ax');
    var gAy = svg.append('g').attr('class', 'axis g-ay');
    var axTitleX = svg.append('text').attr('class', 'ax-title');
    var axTitleY = svg.append('text').attr('class', 'ax-title');
    var gRows = svg.append('g').attr('class', 'g-rows');
    var sepLine = svg.append('line').attr('class', 'sep');
    var gCI = svg.append('g').attr('class', 'g-ci');
    var gAnno = svg.append('g').attr('class', 'g-anno');
    var gDots = svg.append('g').attr('class', 'g-dots');

    var bandRect = gBand.append('rect').attr('class', 'b0-band');
    var bandLine = gBand.append('line').attr('class', 'b0-line');
    var bandLab = gBand.append('text').attr('class', 'band-lab halo');

    /* row labels */
    var rowSel = gRows.selectAll('g.rowlab').data(ROWS).enter().append('g')
      .attr('class', function(a){ return 'rowlab' + (a === REF ? ' ref' : ''); });
    rowSel.append('text').attr('class', 'lbl halo').text(function(a){ return NAME[a]; });
    rowSel.append('text').attr('class', 'lbl-sub halo');

    /* CI marks: one group per compared arm */
    var ciSel = gCI.selectAll('g.ci').data(ARMS).enter().append('g').attr('class', 'ci');
    ciSel.append('line').attr('class', 'ci-line');
    ciSel.append('line').attr('class', 'ci-cap c1');
    ciSel.append('line').attr('class', 'ci-cap c2');
    ciSel.append('line').attr('class', 'mean-tick');
    ciSel.append('text').attr('class', 'ci-arrow a1').attr('text-anchor', 'middle');
    ciSel.append('text').attr('class', 'ci-arrow a2').attr('text-anchor', 'middle');

    /* annotation for the odd B0 rep */
    var anno = gAnno.append('g').attr('class', 'anno-g');
    var annoPath = anno.append('path').attr('class', 'anno-line');
    var annoText = anno.append('text').attr('class', 'anno halo');

    /* dots */
    var pinned = null, hot = null;
    var dotSel = gDots.selectAll('g.dg').data(runs, function(d){ return d.id; }).enter().append('g')
      .attr('class', 'dg').attr('tabindex', 0).attr('role', 'button')
      .attr('aria-pressed', 'false')
      .attr('aria-label', function(d){ return ariaFor(d); });
    dotSel.append('circle').attr('class', 'hit').attr('r', 12);
    dotSel.append('circle').attr('class', 'ring').attr('r', 9);
    dotSel.append('path').attr('class', function(d){ return symClass(d.arm); }).attr('d', function(d){ return symPath(d.arm); });

    /* pointer: nearest dot within reach of the cursor (dots cluster, so per-dot hit areas would
       overlap); keyboard: each dot is a focusable button */
    var REACH = 24;
    function nearest(evt){
      var p = d3.pointer(evt, svgEl), best = null, bd = REACH * REACH;
      runs.forEach(function(d){
        if(d._x == null) return;
        var dx = d._x - p[0], dy = d._y - p[1], dd = dx * dx + dy * dy;
        if(dd < bd){ bd = dd; best = d; }
      });
      return best;
    }
    function dotNode(d){ return dotSel.filter(function(x){ return x.id === d.id; }).node(); }
    svgEl.addEventListener('pointermove', function(e){
      if(e.pointerType === 'touch') return;
      var d = nearest(e);
      if(d !== hot){ setHot(d); }
      if(d){ EX.tooltip.show(tipHTML(d), dotNode(d)); svgEl.style.cursor = 'pointer'; }
      else { EX.tooltip.hide(); svgEl.style.cursor = ''; }
    });
    svgEl.addEventListener('pointerleave', function(){ setHot(null); EX.tooltip.hide(); svgEl.style.cursor = ''; });
    svgEl.addEventListener('click', function(e){
      var d = nearest(e);
      if(!d) return;
      togglePin(d, true);
      if(pinned) EX.tooltip.show(tipHTML(d), dotNode(d)); else EX.tooltip.hide();
    });
    dotSel.each(function(d){
      var el = this;
      el.addEventListener('focus', function(){ setHot(d); EX.tooltip.show(tipHTML(d), el); });
      el.addEventListener('blur', function(){ setHot(null); EX.tooltip.hide(); });
      el.addEventListener('keydown', function(e){
        if(e.key === 'Enter' || e.key === ' ' || e.key === 'Spacebar'){ e.preventDefault(); togglePin(d, true); }
        else if(e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === 'ArrowLeft' || e.key === 'ArrowUp'){
          e.preventDefault();
          var order = focusOrder(), i = order.indexOf(d.id);
          var j = (e.key === 'ArrowRight' || e.key === 'ArrowDown') ? Math.min(order.length - 1, i + 1) : Math.max(0, i - 1);
          var next = dotSel.filter(function(x){ return x.id === order[j]; }).node();
          if(next) next.focus();
        }
        else if(e.key === 'Escape' && pinned){ togglePin(null, true); }
      });
    });

    /* ---------------- coach origin (lazy, optional) ---------------- */
    var origin = {};
    EX.load('trees').then(function(TR){
      Object.keys(TR.trees || {}).forEach(function(k){
        var t = TR.trees[k];
        if(t && t.coach_origin) origin[k] = t.coach_origin;
      });
      renderReadout();
    }, function(){ /* readout simply omits the coach origin */ });

    function coachText(d){
      if(d.arm === 'B0' || d.arm === REF) return 'no coach: the unedited player A₀';
      if(d.arm === 'I0') return 'coach: the original I₀ (frozen)';
      var o = origin[d.id];
      if(o) return 'coach: ' + o.source_run + ' node ' + o.source_node;
      var m = /source_(s\d)/.exec(d.id);
      return m ? 'coach from source_' + m[1] : '';
    }
    function nodeText(d){
      if(d.arm === 'B0' || d.arm === REF) return 'A₀ (unedited)';
      if(d.node === 'initial') return 'initial (unedited A₀)';
      return d.node != null ? 'node ' + d.node : '—';
    }
    function ariaFor(d){
      return EX.runLabel(d.id) + ', ' + NAME[d.arm] + ': exam score ' + F.pct(d.score) +
        ', ' + F.tokens(d.tok) + ' tokens per test input';
    }
    function tipHTML(d){
      return '<b>' + EX.esc(EX.runLabel(d.id)) + '</b> · ' + EX.esc(F.pct(d.score)) +
        '<br><span style="opacity:.85">' + EX.esc(LONG[d.arm]) + '</span>' +
        '<br>final player: ' + EX.esc(nodeText(d)) +
        '<br>' + EX.esc(F.tokens(d.tok)) + ' tokens · ' + EX.esc(F.num(d.calls, d.calls % 1 ? 2 : 0)) + ' calls per test input' +
        '<br>' + EX.esc(F.num(d.eff, 3)) + ' score per 10k tokens';
    }

    /* ---------------- readout ---------------- */
    function readoutFor(d, isPin){
      var parts = [];
      parts.push((isPin ? '<span class="pin">Pinned:</span> ' : '') + '<b>' + EX.esc(EX.runLabel(d.id)) + '</b> <span class="m">' + EX.esc(d.id) + '</span>');
      parts.push('exam score <b>' + EX.esc(F.pct(d.score)) + '</b>');
      parts.push('final player ' + EX.esc(nodeText(d)));
      parts.push('<span class="m">' + EX.esc(F.tokens(d.tok)) + '</span> tokens per test input');
      parts.push('<span class="m">' + EX.esc(F.num(d.calls, d.calls % 1 ? 2 : 0)) + '</span> calls per input');
      var ct = coachText(d); if(ct) parts.push(EX.esc(ct));
      return parts.join(' · ');
    }
    function renderReadout(){
      var d = hot || pinned;
      if(!d){
        readout.innerHTML = 'Hover over, focus or tap a dot to read its run: score, final player, tokens and coach. Click or press Enter to pin it.';
        return;
      }
      readout.innerHTML = readoutFor(d, !hot || hot === pinned ? !!pinned && d === pinned : false);
      if(pinned && (!hot || hot === pinned)){
        var b = EX.h('button', { type: 'button', 'class': 'btn quiet small' }, readout, 'Clear');
        b.addEventListener('click', function(){ togglePin(null, true); });
      }
    }
    function setHot(d){
      hot = d;
      dotSel.classed('is-hot', function(x){ return d && x.id === d.id; });
      renderReadout();
    }
    function applyPin(){
      dotSel.classed('is-pinned', function(x){ return pinned && x.id === pinned.id; })
        .attr('aria-pressed', function(x){ return String(!!(pinned && x.id === pinned.id)); });
      renderReadout();
    }
    function togglePin(d, user){
      pinned = (d && pinned && pinned.id === d.id) ? null : d;
      applyPin();
      if(user){
        if(pinned) EX.select('run', { run: pinned.id, source: 'results' });
        EX.hash.set('results', pinned ? { run: pinned.id, view: view !== 'score' ? view : null } : (view !== 'score' ? { view: view } : {}));
      }
    }
    EX.on('select-run', function(p){
      if(!p || p.source === 'results') return;
      var d = byId[p.run];
      pinned = d || null;
      applyPin();
    });
    if(hashP.section === 'results' && byId[hashP.params.run]){ pinned = byId[hashP.params.run]; }

    function focusOrder(){
      return dotSel.data().slice().sort(function(a, b){
        if(view === 'tokens') return (a._x - b._x) || (a._y - b._y);
        return (ROWS.indexOf(a.arm) - ROWS.indexOf(b.arm)) || (a._x - b._x) || (a._y - b._y);
      }).map(function(d){ return d.id; });
    }

    /* ---------------- layout ---------------- */
    var W = 600, narrow = false;
    function rowGeom(){
      var g = {};
      g.labelW = narrow ? 0 : 196;
      g.mL = narrow ? 6 : g.labelW + 8;
      g.mR = narrow ? 10 : 18;
      g.top = 34;
      g.rowH = narrow ? 62 : 46;
      g.sepGap = 20;
      g.axisH = 44;
      g.labOff = narrow ? 13 : 0;       // label baseline offset from row top (narrow: label above)
      g.stripOff = narrow ? 40 : g.rowH / 2;
      g.rowTop = function(i){ return g.top + i * g.rowH + (i >= ARMS.length ? g.sepGap : 0); };
      g.rowY = function(i){ return g.rowTop(i) + g.stripOff; };
      g.bottom = g.rowTop(ROWS.length - 1) + g.rowH;
      g.H = g.bottom + g.axisH;
      return g;
    }
    function scoreDomain(){
      var lo = d3.min(runs, function(r){ return r.score; }), hi = d3.max(runs, function(r){ return r.score; });
      ARMS.forEach(function(a){ var s = stats.score[a]; if(s.lo != null){ lo = Math.min(lo, s.lo); hi = Math.max(hi, s.hi); } });
      return [Math.floor((lo - 0.005) * 100 / 2) * 2 / 100, Math.ceil((hi + 0.005) * 100 / 2) * 2 / 100];
    }
    function effDomain(){
      var lo = d3.min(runs, function(r){ return r.eff; }), hi = d3.max(runs, function(r){ return r.eff; });
      return [Math.floor((lo - 0.01) * 50) / 50, Math.ceil((hi + 0.01) * 50) / 50];
    }

    function jitter(list, key, step){
      // vertical offsets for near-coincident dots inside one row
      var byArm = {};
      list.forEach(function(d){ (byArm[d.arm] = byArm[d.arm] || []).push(d); });
      var off = {};
      Object.keys(byArm).forEach(function(a){
        var arr = byArm[a].slice().sort(function(p, q){ return key(p) - key(q); });
        var cluster = [], lastX = -1e9;
        function flush(){
          cluster.forEach(function(d, i){
            var k = Math.ceil(i / 2) * (i % 2 ? -1 : 1);
            off[d.id] = cluster.length === 1 ? 0 : k * step;
          });
          cluster = [];
        }
        arr.forEach(function(d){
          var x = key(d);
          if(cluster.length && x - lastX > 7) flush();
          cluster.push(d); lastX = x;
        });
        flush();
      });
      return off;
    }

    function T(sel, animate){ return animate ? sel.transition().duration(EX.dur(250)).ease(d3.easeCubicOut) : sel; }

    function render(animate){
      var isRows = view !== 'tokens';
      var dur = animate ? EX.dur(250) : 0;
      animate = animate && dur > 0;
      var H, xs, ys = null, g = rowGeom();
      var valKey = view === 'eff' ? 'eff' : 'score';

      if(isRows){
        H = g.H;
        xs = d3.scaleLinear().domain(view === 'eff' ? effDomain() : scoreDomain()).range([g.mL, W - g.mR]);
      } else {
        var mL = narrow ? 44 : 56, mR = narrow ? 10 : 18, top = 28, plotH = narrow ? 300 : 360;
        H = top + plotH + 46;
        var maxTok = d3.max(runs, function(r){ return r.tok; });
        xs = d3.scaleLinear().domain([0, Math.ceil(maxTok / 10000) * 10000]).range([mL, W - mR]);
        ys = d3.scaleLinear().domain(scoreDomain()).range([top + plotH, top]);
      }
      svg.attr('height', H).attr('width', W).attr('viewBox', '0 0 ' + W + ' ' + H);
      svgEl.setAttribute('aria-label', view === 'tokens'
        ? 'Exam score against mean player tokens per test input, one mark per final player'
        : view === 'eff' ? 'Exam score per 10k player tokens, one dot per final player, grouped by arm'
        : 'Exam score of every final player, grouped by arm, with arm means and 95% intervals');

      /* axes + grid */
      var nT = narrow ? 4 : 7;
      var xFmt = view === 'score' ? function(v){ return F.pct(v, 0); }
        : view === 'eff' ? function(v){ return F.num(v, 2); } : function(v){ return v === 0 ? '0' : Math.round(v / 1000) + 'k'; };
      var yAxisPos = isRows ? g.bottom + 8 : ys.range()[0] + 8;
      var xAxis = d3.axisBottom(xs).ticks(nT).tickFormat(xFmt).tickSizeOuter(0).tickSize(4);
      T(gAx, animate).attr('transform', 'translate(0,' + yAxisPos + ')').call(xAxis);
      var xTicks = xs.ticks(nT);
      var gridTop = isRows ? g.top - 6 : ys.range()[1];
      var gridBot = isRows ? g.bottom : ys.range()[0];
      var vlines = gGrid.selectAll('line.gv').data(xTicks, function(v){ return view + v; });
      vlines.exit().remove();
      vlines.enter().append('line').attr('class', 'gridline gv').merge(vlines)
        .attr('x1', function(v){ return xs(v); }).attr('x2', function(v){ return xs(v); })
        .attr('y1', gridTop).attr('y2', gridBot);
      if(ys){
        gAy.style('display', null);
        gAy.attr('transform', 'translate(' + (xs.range()[0] - 6) + ',0)')
          .call(d3.axisLeft(ys).ticks(narrow ? 5 : 6).tickFormat(function(v){ return F.pct(v, 0); }).tickSizeOuter(0).tickSize(4));
        var hl = gGrid.selectAll('line.gh').data(ys.ticks(narrow ? 5 : 6));
        hl.exit().remove();
        hl.enter().append('line').attr('class', 'gridline gh').merge(hl)
          .attr('x1', xs.range()[0]).attr('x2', xs.range()[1])
          .attr('y1', function(v){ return ys(v); }).attr('y2', function(v){ return ys(v); });
      } else {
        gAy.style('display', 'none');
        gGrid.selectAll('line.gh').remove();
      }
      axTitleX.attr('x', xs.range()[1]).attr('y', yAxisPos + 34).attr('text-anchor', 'end')
        .text(view === 'score' ? 'exam score (task-averaged pass@2)' : view === 'eff' ? 'exam score per 10k player tokens (linear)' : 'mean player tokens per test input (linear)');
      axTitleY.attr('x', ys ? xs.range()[0] - 6 : 0).attr('y', ys ? ys.range()[1] - 12 : 0).attr('text-anchor', 'middle')
        .style('display', ys ? null : 'none').text('exam score');

      /* B0 band */
      if(isRows){
        var bb = band[valKey];
        var bx0 = xs(bb.lo), bx1 = xs(bb.hi);
        T(bandRect, animate).attr('x', bx0).attr('width', Math.max(1, bx1 - bx0)).attr('y', g.top - 6).attr('height', g.rowTop(ARMS.length) - g.top + 2);
        T(bandLine, animate).attr('x1', xs(bb.mean)).attr('x2', xs(bb.mean)).attr('y1', g.top - 6).attr('y2', g.rowTop(ARMS.length) - 4);
        var labTxt = view === 'eff'
          ? 'B0 range · mean ' + F.num(bb.mean, 3) + ' per 10k'
          : 'B0 · two plain attempts · ' + F.pct(bb.mean);
        bandLab.text(labTxt);
        var lw = labTxt.length * 6.9, cx = xs(bb.mean);
        var anchor = 'middle', lx = cx;
        if(cx + lw / 2 > W - 4){ anchor = 'end'; lx = Math.min(W - 4, bx1); }
        if(cx - lw / 2 < (narrow ? 2 : g.mL - 40)){ anchor = 'start'; lx = Math.max(narrow ? 2 : g.mL - 40, bx0); }
        T(bandLab, animate).attr('x', lx).attr('y', g.top - 12);
        bandLab.attr('text-anchor', anchor);
      } else {
        var by0 = ys(band.score.hi), by1 = ys(band.score.lo);
        T(bandRect, animate).attr('x', xs.range()[0]).attr('width', xs.range()[1] - xs.range()[0]).attr('y', by0).attr('height', Math.max(1, by1 - by0));
        T(bandLine, animate).attr('x1', xs.range()[0]).attr('x2', xs.range()[1]).attr('y1', ys(band.score.mean)).attr('y2', ys(band.score.mean));
        bandLab.text('B0 band · ' + F.pct(band.score.mean)).attr('text-anchor', 'start');
        T(bandLab, animate).attr('x', xs.range()[0] + 6).attr('y', by0 - 6);
      }

      /* row labels + separator */
      if(isRows){
        rowSel.style('display', null);
        T(rowSel, animate).style('opacity', 1).attr('transform', function(a, i){
          return 'translate(' + (narrow ? 0 : 0) + ',' + (narrow ? g.rowTop(i) + g.labOff : g.rowY(i)) + ')';
        });
        rowSel.select('.lbl').attr('x', 0).attr('y', narrow ? 0 : -4);
        rowSel.select('.lbl-sub').attr('x', narrow ? W - g.mR : 0).attr('y', narrow ? 0 : 12)
          .attr('text-anchor', narrow ? 'end' : 'start')
          .text(function(a){
            var s = stats[valKey][a];
            if(a === REF) return 'reference · 1 run';
            var m = view === 'eff' ? F.num(s.mean, 3) : F.pct(s.mean);
            return 'n=' + s.n + ' · mean ' + m;
          });
        var sy = Math.round(g.rowTop(ARMS.length) - g.sepGap / 2) + 0.5;
        sepLine.style('display', null);
        T(sepLine, animate).style('opacity', 1).attr('x1', 0).attr('x2', W).attr('y1', sy).attr('y2', sy);
      } else {
        if(animate){
          rowSel.transition().duration(dur).style('opacity', 0).on('end', function(){ d3.select(this).style('display', 'none'); });
          sepLine.transition().duration(dur).style('opacity', 0).on('end', function(){ d3.select(this).style('display', 'none'); });
        } else { rowSel.style('display', 'none'); sepLine.style('display', 'none'); }
      }

      /* CIs */
      var x0 = xs.range()[0], x1 = xs.range()[1];
      gCI.classed('soft', !isRows);
      ciSel.each(function(a){
        var gsel = d3.select(this), i = ARMS.indexOf(a);
        var s = isRows ? stats[valKey][a] : stats.score[a];
        var lo = s.lo, hi = s.hi, m = s.mean, L, Hh, M, c1, c2, A1 = null, A2 = null;
        if(isRows){
          var y = g.rowY(i);
          var pl = xs(lo), ph = xs(hi), cl = Math.max(x0, pl), ch = Math.min(x1, ph);
          L = [cl, y, ch, y]; M = [xs(m), y - 8, xs(m), y + 8];
          c1 = pl >= x0 ? [pl, y - 4, pl, y + 4] : [cl, y, cl, y];
          c2 = ph <= x1 ? [ph, y - 4, ph, y + 4] : [ch, y, ch, y];
          if(pl < x0) A1 = [cl + 4, y + 4, '◂'];
          if(ph > x1) A2 = [ch - 4, y + 4, '▸'];
        } else {
          var tx = xs(stats.tok[a].mean), yl = ys(lo), yh = ys(hi), ym = ys(m);
          L = [tx, yl, tx, yh]; M = [tx - 8, ym, tx + 8, ym];
          c1 = [tx - 4, yl, tx + 4, yl]; c2 = [tx - 4, yh, tx + 4, yh];
        }
        function setL(sel, v){ T(sel, animate).attr('x1', v[0]).attr('y1', v[1]).attr('x2', v[2]).attr('y2', v[3]); }
        setL(gsel.select('.ci-line'), L); setL(gsel.select('.mean-tick'), M);
        setL(gsel.select('.c1'), c1); setL(gsel.select('.c2'), c2);
        gsel.select('.a1').text(A1 ? A1[2] : '').attr('x', A1 ? A1[0] : 0).attr('y', A1 ? A1[1] : 0);
        gsel.select('.a2').text(A2 ? A2[2] : '').attr('x', A2 ? A2[0] : 0).attr('y', A2 ? A2[1] : 0);
        var title = gsel.select('title'); if(title.empty()) title = gsel.append('title');
        title.text(NAME[a] + ': mean ' + (valKey === 'eff' && isRows ? F.num(m, 3) : F.pct(m)) + ', 95% t-interval ' +
          (valKey === 'eff' && isRows ? '[' + F.num(lo, 3) + ', ' + F.num(hi, 3) + ']' : F.ciPct(lo, hi)) + ' (display only)');
      });

      /* dots */
      var off = isRows ? jitter(runs, function(d){ return xs(d[valKey]); }, 8) : {};
      runs.forEach(function(d){
        if(isRows){ d._x = xs(d[valKey]); d._y = g.rowY(ROWS.indexOf(d.arm)) + (off[d.id] || 0); }
        else { d._x = xs(d.tok); d._y = ys(d.score); }
      });
      T(dotSel, animate).attr('transform', function(d){ return 'translate(' + d._x.toFixed(1) + ',' + d._y.toFixed(1) + ')'; });

      /* annotation for the odd B0 rep (compute views only) */
      if(oddB0 && view !== 'score'){
        var ax = oddB0._x, ay = oddB0._y;
        var txt = 'B0 rep ' + repNo(oddB0.id) + ': ' + F.num(oddB0.calls, 2) + ' calls per input, as logged (note 8)';
        var shortTxt = 'rep ' + repNo(oddB0.id) + ': ' + F.num(oddB0.calls, 2) + ' calls/input (note 8)';
        var lines, tx2, ty2, anchor2;
        if(view === 'eff'){
          lines = [narrow ? shortTxt : txt];
          var tw = lines[0].length * 6.4;
          ty2 = ay + 22; anchor2 = 'end'; tx2 = Math.min(W - 4, ax + 8);
          if(tx2 - tw < 4){ anchor2 = 'start'; tx2 = 4; }
          annoPath.attr('d', 'M' + ax + ',' + (ay + 9) + 'L' + ax + ',' + (ay + 12));
        } else {
          // the upper-left of the scatter is empty: put the note there, with a leader down to the dot
          lines = ['B0 rep ' + repNo(oddB0.id) + ' logged ' + F.num(oddB0.calls, 2) + ' calls', 'per input (note 8)'];
          anchor2 = 'start'; tx2 = Math.max(xs.range()[0] + 6, ax - 30);
          ty2 = ys(band.score.hi) - 64;
          annoPath.attr('d', 'M' + ax + ',' + (ty2 + 20) + 'L' + ax + ',' + (ay - 8));
        }
        annoText.text(null).attr('text-anchor', anchor2);
        lines.forEach(function(l, i){ annoText.append('tspan').attr('x', tx2).attr('dy', i ? 14 : 0).text(l); });
        anno.style('display', null);
        annoText.attr('x', tx2).attr('y', ty2);
      } else {
        anno.style('display', 'none');
      }

      /* legend and note */
      legend.style.display = isRows ? 'none' : '';
      var scoreNote = 'Bars: arm mean and a 95% t-interval, for display only; the pre-registered comparisons are the Welch intervals ' +
        (root.classList.contains('stack') ? 'below' : 'on the right') + '. Shaded band: the range of the three B0 runs. Tied scores are nudged apart vertically.';
      if(view === 'score') note.textContent = scoreNote;
      else if(view === 'eff') note.textContent = 'Each run’s exam score divided by its mean player tokens per test input, per 10k tokens, linear axis. Bars: arm mean and 95% t-interval (display only); ◂ ▸ mark an interval that runs off the scale. B0 rep ' + (oddB0 ? repNo(oddB0.id) : '') + ' logged far fewer calls and tokens, so it sits far right; it is shown as recorded.';
      else note.textContent = 'x: mean player tokens per test input from compute.json (linear, from 0). y: exam score. Bars: each arm’s 95% t-interval for score, drawn at its mean token use (display only). Every compared player used two calls per input, so the arms sit in one cluster.';
    }

    function setView(v, animate){
      view = v; seg.set(v);
      render(animate);
      if(pinned) EX.hash.set('results', { run: pinned.id, view: v !== 'score' ? v : null });
    }

    /* ---------------- G / Δ side panel ---------------- */
    function buildSide(host){
      EX.h('div', { 'class': 'fig-sub-title' }, host, 'The pre-registered comparisons');
      EX.h('p', { 'class': 'fig-sub-text' }, host, 'Differences in exam score, in points, with 95% Welch intervals. An interval that crosses 0 cannot be told apart from no effect.');
      var items = [
        { key: 'G', sym: 'G', name: 'Original coach vs two plain attempts', words: ['B0 better', 'coach better'] },
        { key: 'Delta', sym: 'Δ', name: 'Evolved coach vs original coach', words: ['original better', 'evolved better'] },
        { key: 'Ig_gain_over_B0', sym: '', name: 'Evolved coach vs two plain attempts', words: ['B0 better', 'coach better'] }
      ].filter(function(it){ return S[it.key]; });
      var ext = 0;
      items.forEach(function(it){ var s = S[it.key]; ext = Math.max(ext, Math.abs(s.lo), Math.abs(s.hi)); });
      var lim = Math.ceil(ext * 100 + 0.5) / 100; // in fraction units
      var rowsEls = items.map(function(it){
        var s = S[it.key];
        var box = EX.h('div', { 'class': 'cmp' }, host);
        var nm = EX.h('div', { 'class': 'cmp-name' }, box);
        nm.appendChild(document.createTextNode(it.name));
        if(it.sym){ nm.appendChild(document.createTextNode(' (')); EX.h('i', null, nm, it.sym); nm.appendChild(document.createTextNode(')')); }
        var val = EX.h('div', { 'class': 'cmp-val' }, box);
        val.innerHTML = '<span class="m">' + EX.esc(F.ptsU(s.est)) + '</span>, interval <span class="m">' + EX.esc(F.ci(s.lo, s.hi)) + '</span>';
        var sv = EX.s('svg', { role: 'img', 'aria-label': it.name + ': ' + F.ptsU(s.est) + ', 95% interval ' + F.ci(s.lo, s.hi) + ' points' }, box);
        var crosses = s.lo < 0 && s.hi > 0;
        EX.h('div', { 'class': 'cmp-verdict' }, box, crosses ? 'Crosses 0: no detectable difference.' : (s.lo >= 0 ? 'Above 0.' : 'Below 0.'));
        return { it: it, s: s, svg: sv };
      });
      host.__draw = function(w){
        rowsEls.forEach(function(r){
          var sv = r.svg; while(sv.firstChild) sv.removeChild(sv.firstChild);
          var pad = 10, H = 46, x = d3.scaleLinear().domain([-lim, lim]).range([pad, w - pad]);
          sv.setAttribute('width', w); sv.setAttribute('height', H); sv.setAttribute('viewBox', '0 0 ' + w + ' ' + H);
          var y = 14;
          EX.s('line', { 'class': 'axl', x1: x(-lim), x2: x(lim), y1: y, y2: y }, sv);
          EX.s('line', { 'class': 'z', x1: x(0), x2: x(0), y1: 2, y2: y + 12 }, sv);
          EX.s('line', { 'class': 'bar', x1: x(r.s.lo), x2: x(r.s.hi), y1: y, y2: y }, sv);
          EX.s('line', { 'class': 'cap', x1: x(r.s.lo), x2: x(r.s.lo), y1: y - 5, y2: y + 5 }, sv);
          EX.s('line', { 'class': 'cap', x1: x(r.s.hi), x2: x(r.s.hi), y1: y - 5, y2: y + 5 }, sv);
          EX.s('circle', { 'class': 'est', cx: x(r.s.est), cy: y, r: 4 }, sv);
          var step = lim * 100 > 6 ? 2 : 1, top = Math.floor(lim * 100);
          for(var v = -top; v <= top; v += step){
            if(v !== 0 && Math.abs(v) !== top) continue;
            EX.s('text', { 'class': 'tk', x: x(v / 100), y: y + 18, 'text-anchor': 'middle' }, sv, v === 0 ? '0' : F.signed(v, 0));
          }
          EX.s('text', { 'class': 'dir', x: x(-lim), y: y + 31, 'text-anchor': 'start' }, sv, '← ' + r.it.words[0]);
          EX.s('text', { 'class': 'dir', x: x(lim), y: y + 31, 'text-anchor': 'end' }, sv, r.it.words[1] + ' →');
        });
      };
    }

    /* ---------------- sizing ---------------- */
    function layout(mw){
      var wide = mw >= 820;
      narrow = mw < 560;
      root.classList.toggle('stack', !wide);
      root.classList.toggle('narrow', narrow);
      var sideW = wide ? 292 : mw;
      W = Math.max(280, Math.floor(wide ? mw - 292 - 28 - 1 : mw));
      side.__draw(Math.max(220, (wide ? sideW - 24 : Math.min(mw, 520))));
      render(false);
    }
    layout(ctx.width() || 600);
    applyPin();
    ctx.onResize(function(w){ layout(w); });
  }
})();
