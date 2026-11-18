/* fig-setup.js — Figure 1, "Two loops".
   Source runs (coach + player co-evolve, archive tree, I_g pick) and pay-off runs
   (frozen coach trains a fresh player, final player sits the exam), over a gateway strip.
   Wide layout: one SVG spanning both panels (the I_g transplant arrow crosses over).
   Narrow layout (< 760 px mount): stacked — Source, gateway band, Pay-off.
   Data: summary.json, trees.json. Emits nothing; lights [data-term] spans in the prose. */
(function(){
  'use strict';

  var CSS = [
    '.fx-setup{position:relative}',
    '.fx-setup .fx-heads{display:grid;grid-template-columns:57.5fr 42.5fr;gap:0}',
    '.fx-setup .fx-head{padding-right:28px}',
    '.fx-setup .fx-head + .fx-head{padding-left:22px;padding-right:0;border-left:1px dashed var(--rule)}',
    '.fx-setup .fig-sub-text{min-height:4.5em;transition:color var(--dur)}',
    '.fx-setup .fig-sub-text b{color:var(--ink);font-weight:600}',
    '.fx-setup .fx-head.is-live .fig-sub-text{color:var(--ink)}',
    '.fx-setup svg{display:block;width:100%;height:auto;overflow:visible}',
    '.fx-setup .bx{fill:var(--bg);stroke:var(--rule-strong);stroke-width:1;transition:stroke var(--dur),stroke-width var(--dur)}',
    '.fx-setup .bx-strip{fill:var(--panel-strong)}',
    '.fx-setup .bx-title{font-size:15px;font-weight:600;fill:var(--ink)}',
    '.fx-setup .bx-sub{font-family:var(--font-mono);font-size:11.5px;fill:var(--ink-2)}',
    '.fx-setup .ln{stroke:var(--rule-strong);stroke-width:1.2;fill:none;transition:stroke var(--dur),stroke-width var(--dur)}',
    '.fx-setup .ln-acc{stroke:var(--accent);stroke-width:1.6;fill:none;transition:stroke-width var(--dur)}',
    '.fx-setup .ah{fill:var(--rule-strong)} .fx-setup .ah-acc{fill:var(--accent)} .fx-setup .ah-hot{fill:var(--ink)}',
    '.fx-setup .lab{font-family:var(--font-mono);font-size:11.5px;fill:var(--ink-muted)}',
    '.fx-setup .lab-acc{font-family:var(--font-mono);font-size:11.5px;fill:var(--accent)}',
    '.fx-setup .halo{paint-order:stroke;stroke:var(--panel);stroke-width:5px;stroke-linejoin:round}',
    '.fx-setup .gen-strip{fill:var(--panel-strong)}',
    '.fx-setup .gen-t{font-family:var(--font-mono);font-size:10px;fill:var(--ink-muted)}',
    '.fx-setup .t-edge{stroke:var(--rule-strong);stroke-width:1;fill:none}',
    '.fx-setup .t-node{stroke:var(--ink-muted);stroke-width:.8}',
    '.fx-setup .t-na{fill:var(--bg);stroke:var(--ink-muted);stroke-width:.8;stroke-dasharray:1.5 1.5}',
    '.fx-setup .t-coach{fill:none;stroke:var(--ink);stroke-width:1}',
    '.fx-setup .t-pick{fill:none;stroke:var(--accent);stroke-width:1.8}',
    '.fx-setup .lock{fill:none;stroke:var(--ink-2);stroke-width:1.3}',
    '.fx-setup .part{cursor:pointer;outline:none}',
    '.fx-setup .part .hit{fill:transparent;stroke:transparent;stroke-width:16}',
    '.fx-setup .part.is-hot .bx{stroke:var(--ink);stroke-width:1.8}',
    '.fx-setup .part.is-hot .ln{stroke:var(--ink);stroke-width:2.2}',
    '.fx-setup .part.is-hot .ln-acc{stroke-width:2.8}',
    '.fx-setup .part.is-hot .lab{fill:var(--ink)}',
    '.fx-setup .part.is-hot .t-edge{stroke:var(--ink-2)}',
    '.fx-setup .part:focus-visible .bx,.fx-setup .part:focus-visible .hit{stroke:var(--accent);stroke-opacity:.35}',
    '.fx-setup .part.is-pinned .bx{stroke-dasharray:none}',
    '.fx-setup .fx-gw{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 14px;margin-top:14px;background:var(--panel-strong);',
    '  border-radius:3px;padding:9px 14px;font-size:13.5px;line-height:1.45;color:var(--ink);cursor:pointer;transition:box-shadow var(--dur)}',
    '.fx-setup .fx-gw .k{font-weight:600}',
    '.fx-setup .fx-gw .m{font-family:var(--font-mono);font-size:12px;color:var(--ink-2)}',
    '.fx-setup .fx-gw .sep{color:var(--ink-muted)}',
    '.fx-setup .fx-gw.is-hot{box-shadow:inset 0 0 0 1.5px var(--ink)}',
    '.fx-setup .fx-gw:focus-visible{box-shadow:var(--focus-ring)}',
    '.fx-setup.narrow .fx-heads{display:block}',
    '.fx-setup.narrow .fx-head{padding:0;min-height:0;border:0}',
    '.fx-setup.narrow .fig-sub-text{min-height:6em}',
    '.fx-setup.narrow .fx-gw{margin:14px 0 22px}',
    '.fx-setup .fx-reset{margin-top:10px;font-size:12.5px;color:var(--ink-muted)}'
  ].join('\n');

  function injectCSS(){
    if(document.getElementById('fx-setup-css')) return;
    var st = document.createElement('style'); st.id = 'fx-setup-css'; st.textContent = CSS;
    document.head.appendChild(st);
  }

  EX.mount('setup', function(node, ctx){
    injectCSS();
    return EX.loadAll(['summary', 'trees']).then(function(res){
      var S = res[0], TR = res[1], T = TR.trees, F = EX.fmt, D = EX.derive(S);
      var EXAMPLE = 'source_s3';
      var ex = T[EXAMPLE];
      var gens = T.source_s1.max_generation_committed || 12;
      var sourceRuns = TR.runs.filter(function(r){ return T[r].kind === 'source'; });
      var extRuns = sourceRuns.filter(function(r){ return T[r].max_generation > gens; });
      var extMax = Math.max.apply(null, extRuns.map(function(r){ return T[r].max_generation; }));
      var payRun = TR.runs.filter(function(r){ return T[r].kind === 'payoff_I0'; })[0];
      var rounds = T[payRun].max_generation;
      var nI0 = D.nI0, nIg = D.nIg, sets = S.sets;
      var exNodes = ex.nodes.filter(function(n){ return gx(n) <= gens; });
      var pick = exNodes.filter(function(n){ return n.is_Ig_pick; })[0];
      var exSelf = exNodes.filter(function(n){ return n.touched_coach; }).length;
      var sub = function(s){ return s.replace(/I_g/g, 'I<sub>g</sub>').replace(/I₀/g, 'I<sub>0</sub>').replace(/A₀/g, 'A<sub>0</sub>'); };

      /* ---------- part explanations (all counts bound to data) ---------- */
      var DEFAULT = {
        source: 'Coach and player evolve together for ' + gens + ' generations on a ' + sets.source_practice_tasks +
          '-task practice set, in ' + S.n_source_seeds + ' separate runs. Every generation adds a node to the run\'s archive tree.',
        payoff: 'A coach is frozen and trains a fresh player A₀ for ' + rounds + ' rounds on a second practice set. That coach is the original I₀ or an I_g picked from a tree. The final player takes the exam once.'
      };
      var PARTS = {
        'coach-src':  { panel: 'source', name: 'Coach', term: 'coach',
          text: 'An LLM agent with file and shell tools. Each generation it reads the practice results of one node in the tree and writes a diff. All ' + S.n_source_seeds + ' runs start from the same original coach, I₀.' },
        'self-edit':  { panel: 'source', name: 'Self-edit', term: 'coach',
          text: 'In source runs the coach may also edit its own code: its prompt, its tools and its helpers. Only ' + D.selfEditGens + ' of ' + D.totalGens + ' generations did (' + F.pct(S.self_edit_rate, 0) + ').' },
        'edit-src':   { panel: 'source', name: 'Edits the player', term: 'player',
          text: 'Most generations edit only the player. Typical edits change its prompt or its answer parsing, or add a "refine" call within the two-call budget.' },
        'player-src': { panel: 'source', name: 'Player', term: 'player',
          text: 'The player solves one puzzle with at most 2 model calls and 2 answers per test input. Every run starts from A₀, which just asks the model twice.' },
        'plays-src':  { panel: 'source', name: 'Plays', term: 'player',
          text: 'Each new node\'s player is scored once on the ' + sets.source_practice_tasks + ' source practice tasks.' },
        'practice-src': { panel: 'source', name: 'Source practice set', term: 'source',
          text: sets.source_practice_tasks + ' training tasks. The starting player solves 19 of them sometimes, 3 always and 3 never. No exam task is in it.' },
        'scores-src': { panel: 'source', name: 'Practice scores', term: 'coach',
          text: 'Scores go back to the coach and decide which nodes the next generation builds on.' },
        'archive':    { panel: 'source', name: 'Archive tree', term: 'source',
          text: 'Every generation saves a node: the coach and player code plus the practice score. There are ' + S.n_source_seeds + ' runs of ' + gens + ' generations, and ' + extRuns.length + ' of them continued to ' + extMax + '. In this tree (' + EXAMPLE + '), ' + exSelf + ' nodes changed the coach (thin ring).' },
        'pick':       { panel: 'source', name: 'Pick I_g', term: 'ig',
          text: 'The rule picks I_g: among changed coaches with a scored child, the one whose children gained most. ' + S.n_qualifying_Ig + ' of ' + S.n_source_seeds + ' runs had one. Here it is node ' + (pick ? pick.id : '?') + ', from generation ' + (pick ? gx(pick) : '?') + '.' },
        'transplant': { panel: 'payoff', name: 'I_g transplanted', term: 'ig',
          text: 'The picked coach\'s code is copied into a pay-off run and locked. It can no longer edit itself, only the player.' },
        'coach-pay':  { panel: 'payoff', name: 'Frozen coach', term: 'payoff',
          text: 'The coach is frozen: the original I₀ in ' + nI0 + ' runs, an evolved I_g in ' + nIg + ' runs. Same model and the same token budget per round.' },
        'edit-pay':   { panel: 'payoff', name: rounds + ' rounds', term: 'player',
          text: rounds + ' rounds of player edits, always starting from the plain player A₀.' },
        'player-pay': { panel: 'payoff', name: 'Fresh player', term: 'a0',
          text: 'Each run begins with A₀ and keeps every edited version as a node, just like a source tree.' },
        'plays-pay':  { panel: 'payoff', name: 'Plays', term: 'player',
          text: 'Each new player is scored once on the pay-off practice set.' },
        'practice-pay': { panel: 'payoff', name: 'Pay-off practice set', term: 'payoff',
          text: 'A second set of ' + sets.payoff_practice_tasks + ' training tasks, disjoint from the source set, so no coach evolved on it.' },
        'scores-pay': { panel: 'payoff', name: 'Practice scores', term: 'coach',
          text: 'The frozen coach sees these scores and chooses what to edit next.' },
        'final':      { panel: 'payoff', name: 'Final player', term: 'exam',
          text: 'The two best players are re-scored, and the one with the higher combined score takes the exam. The unedited A₀ is eligible, and it won once.' },
        'exam':       { panel: 'payoff', name: 'Held-out exam', term: 'exam',
          text: 'All ' + sets.heldout_tasks + ' public ARC-AGI-2 evaluation tasks, with ' + sets.heldout_test_inputs + ' test inputs. No coach ever saw them. The score is pass@2 averaged over tasks.' },
        'gateway':    { panel: 'both', name: 'Gateway', term: 'gateway',
          text: 'The only route to the model, and no agent can edit it. It fixes the model and effort, caps calls, answers and coach tokens, and keeps the spending ledger.' }
      };
      // text term -> parts (for prose -> figure linking)
      var TERM_PARTS = { coach: ['coach-src', 'coach-pay'], player: ['player-src', 'player-pay'], source: ['archive'],
        payoff: ['coach-pay'], ig: ['pick', 'transplant'], i0: ['coach-src'], a0: ['player-pay'], exam: ['exam'], gateway: ['gateway'] };

      /* ---------- state ---------- */
      var hot = null, pinned = null, mode = null;
      var heads = {}, partEls = {};

      function render(){
        var w = node.clientWidth || 900;
        var m = w < 760 ? 'narrow' : 'wide';
        if(m === mode && node.firstChild) return;
        mode = m;
        node.innerHTML = '';
        partEls = {}; heads = {};
        var root = EX.h('div', { 'class': 'fx-setup ' + m }, node);
        var headsWrap = EX.h('div', { 'class': 'fx-heads' }, root);
        function head(key, title, parent){
          var d = EX.h('div', { 'class': 'fx-head', 'data-panel': key }, parent || headsWrap);
          EX.h('div', { 'class': 'fig-sub-title' }, d, title);
          var p = EX.h('p', { 'class': 'fig-sub-text', 'aria-live': 'polite' }, d);
          p.innerHTML = sub(DEFAULT[key]);
          heads[key] = d;
          return d;
        }
        if(m === 'wide'){
          head('source', 'Source runs: coach and player evolve together');
          head('payoff', 'Pay-off runs: a frozen coach trains a fresh player');
          var svg = EX.s('svg', { viewBox: '0 0 1000 392', role: 'group', 'aria-label': 'Diagram: source runs on the left, pay-off runs on the right' }, root);
          drawWide(svg);
          gateway(root);
        } else {
          head('source', 'Source runs: coach and player evolve together', root);
          var s1 = EX.s('svg', { viewBox: '0 0 360 404', role: 'group', 'aria-label': 'Diagram: source runs' }, root);
          drawNarrowSource(s1);
          gateway(root);
          head('payoff', 'Pay-off runs: a frozen coach trains a fresh player', root);
          var s2 = EX.s('svg', { viewBox: '0 0 360 336', role: 'group', 'aria-label': 'Diagram: pay-off runs' }, root);
          drawNarrowPayoff(s2);
        }
        EX.h('div', { 'class': 'fx-reset hint', 'aria-live': 'polite' }, root);
        applyHot(pinned);
      }

      /* ---------- drawing primitives ---------- */
      function defs(svg){
        var d = EX.s('defs', null, svg), ids = {};
        [['n', 'ah'], ['a', 'ah-acc'], ['h', 'ah-hot']].forEach(function(p){
          var id = EX.uid('fxs-' + p[0]); ids[p[0]] = id;
          var mk = EX.s('marker', { id: id, viewBox: '0 0 10 10', refX: 8.5, refY: 5, markerWidth: 7, markerHeight: 7, orient: 'auto-start-reverse', markerUnits: 'userSpaceOnUse' }, d);
          EX.s('path', { d: 'M0,1 L9,5 L0,9 z', 'class': p[1] }, mk);
        });
        svg.__mk = ids;
        return ids;
      }
      function part(svg, id){
        var info = PARTS[id];
        var g = EX.s('g', { 'class': 'part', 'data-part': id, tabindex: 0, role: 'button',
          'aria-label': info.name.replace('I_g', 'I g') + ': ' + info.text.replace(/I_g/g, 'I g') }, svg);
        (partEls[id] = partEls[id] || []).push(g);
        wire(g, id);
        return g;
      }
      function box(svg, id, x, y, w, h, title, subt, opt){
        opt = opt || {};
        var g = part(svg, id);
        EX.s('rect', { 'class': 'bx', x: x, y: y, width: w, height: h, rx: 4 }, g);
        EX.s('rect', { 'class': 'bx-strip', x: x + 0.5, y: y + h - 21, width: w - 1, height: 20.5 }, g);
        EX.s('line', { x1: x, x2: x + w, y1: y + h - 21, y2: y + h - 21, stroke: 'var(--rule)', 'stroke-width': 1 }, g);
        EX.s('text', { 'class': 'bx-title', x: x + 12, y: y + 24 }, g, title);
        if(subt) EX.s('text', { 'class': 'bx-sub', x: x + 12, y: y + h - 6.5 }, g, subt);
        if(opt.lock){
          var lx = x + w - 24, ly = y + 12;
          EX.s('rect', { 'class': 'lock', x: lx, y: ly + 5, width: 13, height: 10, rx: 1.5 }, g);
          EX.s('path', { 'class': 'lock', d: 'M' + (lx + 3) + ',' + (ly + 5) + ' v-3 a3.5,3.5 0 0 1 7,0 v3' }, g);
        }
        return g;
      }
      function arrow(svg, id, d, opt){
        opt = opt || {};
        var g = part(svg, id);
        EX.s('path', { 'class': 'hit', d: d }, g);
        var p = EX.s('path', { 'class': opt.acc ? 'ln-acc' : 'ln', d: d, 'marker-end': 'url(#' + svg.__mk[opt.acc ? 'a' : 'n'] + ')' }, g);
        if(opt.dash) p.setAttribute('stroke-dasharray', opt.dash);
        p.__acc = !!opt.acc;
        (opt.labels || []).forEach(function(l){
          EX.s('text', { 'class': (opt.acc ? 'lab-acc' : 'lab') + ' halo', x: l[0], y: l[1], 'text-anchor': l[3] || 'middle' }, g, l[2]);
        });
        return g;
      }

      /* tree of the example run: nodes by generation (x) and DFS order (y) */
      function tree(svg, X, Y0, rowH, opt){
        opt = opt || {};
        var byId = {}, kids = {};
        exNodes.forEach(function(n){ byId[n.id] = n; });
        exNodes.forEach(function(n){ if(n.parent && byId[n.parent]) (kids[n.parent] = kids[n.parent] || []).push(n.id); });
        var row = 0, ry = {};
        (function dfs(id){
          var k = (kids[id] || []).sort(function(a, b){ return (+a) - (+b); });
          if(!k.length){ ry[id] = row++; return; }
          k.forEach(dfs); ry[id] = (ry[k[0]] + ry[k[k.length - 1]]) / 2;
        })('initial');
        var Y = function(id){ return Y0 + ry[id] * rowH; };
        var g = part(svg, 'archive');
        // generation strip
        EX.s('rect', { 'class': 'gen-strip', x: opt.stripX, y: opt.stripY, width: opt.stripW, height: 16, rx: 2 }, g);
        for(var i = 0; i <= gens; i++){
          if(opt.every && i % opt.every && i !== gens) continue;
          EX.s('text', { 'class': 'gen-t', x: X(i), y: opt.stripY + 11.5, 'text-anchor': 'middle' }, g, i === 0 ? 'gen 0' : String(i));
        }
        EX.s('rect', { 'class': 'hit', x: opt.stripX, y: opt.stripY, width: opt.stripW, height: Y0 + row * rowH - opt.stripY, fill: 'transparent' }, g);
        exNodes.forEach(function(n){
          if(!n.parent || !byId[n.parent]) return;
          var p = byId[n.parent], x1 = X(gx(p)), y1 = Y(p.id), x2 = X(gx(n)), y2 = Y(n.id), mx = (x2 - x1) * 0.5;
          EX.s('path', { 'class': 't-edge', d: 'M' + x1 + ',' + y1 + ' C' + (x1 + mx) + ',' + y1 + ' ' + (x2 - mx) + ',' + y2 + ' ' + x2 + ',' + y2 }, g);
        });
        var pickXY = null;
        exNodes.forEach(function(n){
          var x = X(gx(n)), y = Y(n.id), r = opt.r || 4.2;
          if(n.practice_score == null) EX.s('circle', { 'class': 't-na', cx: x, cy: y, r: r }, g);
          else EX.s('circle', { 'class': 't-node', cx: x, cy: y, r: r, fill: 'var(--ramp-' + Math.max(0, Math.min(4, Math.round((n.practice_score - 0.6) / 0.1))) + ')' }, g);
          if(n.touched_coach) EX.s('circle', { 'class': 't-coach', cx: x, cy: y, r: r + 2.4 }, g);
          if(n.is_Ig_pick) pickXY = [x, y];
        });
        if(pickXY){
          var pg = part(svg, 'pick');
          EX.s('circle', { 'class': 'hit', cx: pickXY[0], cy: pickXY[1], r: 12 }, pg);
          EX.s('circle', { 'class': 't-pick', cx: pickXY[0], cy: pickXY[1], r: (opt.r || 4.2) + 4.6 }, pg);
          EX.s('text', { 'class': 'lab-acc halo', x: pickXY[0], y: pickXY[1] - 11, 'text-anchor': 'middle' }, pg, 'I_g');
        }
        return { pick: pickXY, bottom: Y0 + (row - 1) * rowH, g: g };
      }

      /* ---------- wide layout: 1000 x 392 ---------- */
      function drawWide(svg){
        defs(svg);
        // dashed divider between panels
        EX.s('line', { x1: 575, x2: 575, y1: 0, y2: 392, stroke: 'var(--rule)', 'stroke-dasharray': '3 4' }, svg);
        /* source */
        arrow(svg, 'self-edit', 'M136,40 C150,-2 52,-2 64,38', { acc: true, labels: [[156, 16, 'edits its own code', 'start']] });
        box(svg, 'coach-src', 24, 40, 150, 66, 'Coach', 'I₀ at the start');
        box(svg, 'player-src', 300, 40, 150, 66, 'Player', 'A₀ at the start');
        arrow(svg, 'edit-src', 'M175,73 L297,73', { labels: [[236, 65, 'edits code']] });
        box(svg, 'practice-src', 300, 150, 150, 58, 'Practice set', sets.source_practice_tasks + ' tasks · source');
        arrow(svg, 'plays-src', 'M375,107 L375,147', { labels: [[383, 131, 'plays', 'start']] });
        arrow(svg, 'scores-src', 'M299,179 C190,179 99,170 99,109', { labels: [[196, 196, 'practice scores']] });
        arrow(svg, 'archive', 'M375,209 L375,247', { labels: [[383, 233, 'saves a node per generation', 'start']] });
        EX.s('text', { 'class': 'lab', x: 24, y: 238 }, svg, 'archive tree · ' + EXAMPLE + ' · gens 0–' + gens);
        var X = function(g){ return 44 + g * 39.5; };
        var t = tree(svg, X, 280, 12.5, { stripX: 24, stripY: 248, stripW: 512, r: 4.6 });
        /* transplant: from the I_g node, along the bottom, up to the frozen coach */
        if(t.pick){
          var px = t.pick[0], py = t.pick[1];
          arrow(svg, 'transplant', 'M' + px + ',' + (py + 9) + ' C' + px + ',378 ' + (px + 10) + ',380 ' + (px + 30) + ',380 L586,380 C598,380 600,372 600,360 L600,86 C600,76 606,73 616,73',
            { acc: true, labels: [[px + 34, 372, 'pick I_g: the changed coach whose children gained most', 'start'], [610, 236, 'I_g transplanted,', 'start'], [610, 251, 'code frozen', 'start']] });
        }
        /* pay-off */
        box(svg, 'coach-pay', 620, 40, 142, 66, 'Coach', 'I₀ or I_g, frozen', { lock: true });
        box(svg, 'player-pay', 826, 40, 150, 66, 'Player', 'A₀ → final');
        arrow(svg, 'edit-pay', 'M763,73 L823,73', { labels: [[793, 65, 'edits'], [793, 92, '×' + rounds]] });
        box(svg, 'practice-pay', 826, 150, 150, 58, 'Practice set', sets.payoff_practice_tasks + ' tasks · pay-off');
        arrow(svg, 'plays-pay', 'M901,107 L901,147', { labels: [[909, 131, 'plays', 'start']] });
        arrow(svg, 'scores-pay', 'M825,179 C740,179 691,170 691,109', { labels: [[752, 196, 'practice scores']] });
        arrow(svg, 'final', 'M901,209 L901,265', { labels: [[893, 236, 'best player', 'end'], [893, 251, 'sits it once', 'end']] });
        box(svg, 'exam', 780, 268, 196, 66, 'Held-out exam', sets.heldout_tasks + ' tasks · ' + sets.heldout_test_inputs + ' inputs');
        EX.s('text', { 'class': 'lab', x: 616, y: 306 }, svg, nI0 + ' runs with I₀');
        EX.s('text', { 'class': 'lab', x: 616, y: 322 }, svg, nIg + ' runs with I_g');
      }

      /* ---------- narrow layout ---------- */
      function drawNarrowSource(svg){
        defs(svg);
        arrow(svg, 'self-edit', 'M112,38 C124,2 34,2 44,36', { acc: true, labels: [[128, 16, 'edits its own code', 'start']] });
        box(svg, 'coach-src', 12, 38, 134, 62, 'Coach', 'I₀ at start');
        box(svg, 'player-src', 214, 38, 134, 62, 'Player', 'A₀ at start');
        arrow(svg, 'edit-src', 'M147,69 L211,69', { labels: [[179, 61, 'edits']] });
        box(svg, 'practice-src', 214, 138, 134, 56, 'Practice', sets.source_practice_tasks + ' tasks');
        arrow(svg, 'plays-src', 'M281,101 L281,135', { labels: [[289, 122, 'plays', 'start']] });
        arrow(svg, 'scores-src', 'M213,166 C130,166 79,156 79,103', { labels: [[138, 186, 'practice scores']] });
        arrow(svg, 'archive', 'M281,195 L281,229', { labels: [[273, 216, 'saves a node', 'end']] });
        EX.s('text', { 'class': 'lab', x: 12, y: 222 }, svg, 'archive tree · ' + EXAMPLE);
        var X = function(g){ return 26 + g * 25.5; };
        var t = tree(svg, X, 258, 10, { stripX: 12, stripY: 230, stripW: 336, every: 2, r: 3.6 });
        if(t.pick){
          var px = t.pick[0], py = t.pick[1];
          arrow(svg, 'transplant', 'M' + px + ',' + (py + 8) + ' L' + px + ',401', { acc: true,
            labels: [[px + 10, 362, 'pick I_g: the changed coach', 'start'], [px + 10, 377, 'whose children gained most', 'start'], [px + 10, 396, 'I_g transplanted ↓', 'start']] });
        }
      }
      function drawNarrowPayoff(svg){
        defs(svg);
        arrow(svg, 'transplant', 'M79,0 L79,35', { acc: true, labels: [[87, 18, 'I_g arrives frozen', 'start']] });
        box(svg, 'coach-pay', 12, 38, 134, 62, 'Coach', 'I₀ or I_g', { lock: true });
        box(svg, 'player-pay', 214, 38, 134, 62, 'Player', 'A₀ → final');
        arrow(svg, 'edit-pay', 'M147,69 L211,69', { labels: [[179, 61, 'edits'], [179, 86, '×' + rounds]] });
        box(svg, 'practice-pay', 214, 138, 134, 56, 'Practice', sets.payoff_practice_tasks + ' tasks');
        arrow(svg, 'plays-pay', 'M281,101 L281,135', { labels: [[289, 122, 'plays', 'start']] });
        arrow(svg, 'scores-pay', 'M213,166 C130,166 79,156 79,103', { labels: [[138, 186, 'practice scores']] });
        arrow(svg, 'final', 'M281,195 L281,249', { labels: [[273, 218, 'best player', 'end'], [273, 233, 'sits it once', 'end']] });
        box(svg, 'exam', 150, 252, 198, 64, 'Held-out exam', sets.heldout_tasks + ' tasks · ' + sets.heldout_test_inputs + ' inputs');
        EX.s('text', { 'class': 'lab', x: 12, y: 276 }, svg, nI0 + ' runs, I₀');
        EX.s('text', { 'class': 'lab', x: 12, y: 292 }, svg, nIg + ' runs, I_g');
      }

      function gateway(parent){
        var gw = EX.h('div', { 'class': 'fx-gw', 'data-part': 'gateway', tabindex: 0, role: 'button',
          'aria-label': 'Gateway: ' + PARTS.gateway.text }, parent);
        gw.innerHTML = '<span class="k">Gateway · fixed for every player</span>' +
          '<span class="m">gpt-6-luna</span><span class="sep">·</span><span class="m">effort high</span><span class="sep">·</span>' +
          '<span class="m">≤ 2 model calls</span><span class="sep">·</span><span class="m">2 answers per test input</span><span class="sep">·</span>' +
          '<span class="m">no agent can edit it</span>';
        (partEls.gateway = partEls.gateway || []).push(gw);
        wire(gw, 'gateway');
      }

      /* ---------- interaction ---------- */
      function wire(el, id){
        el.addEventListener('mouseenter', function(){ applyHot(id); });
        el.addEventListener('mouseleave', function(){ applyHot(pinned); });
        el.addEventListener('focus', function(){ applyHot(id); });
        el.addEventListener('blur', function(){ applyHot(pinned); });
        el.addEventListener('click', function(e){ e.stopPropagation(); pinned = pinned === id ? null : id; applyHot(pinned || id); note(); });
        el.addEventListener('keydown', function(e){
          if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); pinned = pinned === id ? null : id; applyHot(pinned || id); note(); }
          if(e.key === 'Escape'){ pinned = null; applyHot(null); note(); }
        });
      }
      function note(){
        var n = node.querySelector('.fx-reset'); if(!n) return;
        n.textContent = pinned ? 'Pinned: ' + PARTS[pinned].name + '. Click it again, or press Esc, to release.' : '';
      }
      function applyHot(id){
        hot = id;
        Object.keys(partEls).forEach(function(k){
          partEls[k].forEach(function(el){
            el.classList.toggle('is-hot', k === id);
            el.classList.toggle('is-pinned', k === pinned);
            // arrowheads follow the hot colour (not the accent ones)
            el.querySelectorAll && el.querySelectorAll('path.ln').forEach(function(p){
              var svg = p.ownerSVGElement; if(!svg || !svg.__mk) return;
              p.setAttribute('marker-end', 'url(#' + svg.__mk[k === id ? 'h' : 'n'] + ')');
            });
          });
        });
        ['source', 'payoff'].forEach(function(key){
          var hd = heads[key]; if(!hd) return;
          var p = hd.querySelector('.fig-sub-text');
          var info = id ? PARTS[id] : null;
          var live = info && (info.panel === key || info.panel === 'both' && key === 'source');
          p.innerHTML = live ? '<b>' + sub(info.name) + '.</b> ' + sub(info.text) : sub(DEFAULT[key]);
          hd.classList.toggle('is-live', !!live);
        });
        document.querySelectorAll('[data-term].term-hl').forEach(function(t){ t.classList.remove('term-hl'); });
        if(id && PARTS[id].term){
          document.querySelectorAll('[data-term="' + PARTS[id].term + '"]').forEach(function(t){ t.classList.add('term-hl'); });
        }
      }
      // prose -> figure: hovering a marked term lights the matching box
      document.querySelectorAll('[data-term]').forEach(function(t){
        var parts = TERM_PARTS[t.getAttribute('data-term')]; if(!parts) return;
        t.addEventListener('mouseenter', function(){
          if(pinned) return;
          Object.keys(partEls).forEach(function(k){ partEls[k].forEach(function(el){ el.classList.toggle('is-hot', parts.indexOf(k) >= 0); }); });
        });
        t.addEventListener('mouseleave', function(){ if(!pinned) applyHot(null); });
      });
      document.addEventListener('click', function(e){
        if(pinned && !node.contains(e.target)){ pinned = null; applyHot(null); note(); }
      });

      render();
      ctx.onResize(function(){ render(); });
    });
  });

  function gx(n){ return n.generation === 'initial' ? 0 : n.generation; }
})();
