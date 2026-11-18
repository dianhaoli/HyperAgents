/* fig-tree.js — Figure 5, evolution tree explorer (the centrepiece).
   Small multiples of the six source trees (shared 0–40 generation axis) double as the run picker;
   a grouped select also opens pay-off and extension trees. Detail tree: x = generation, y = lineage,
   fill = practice score (5-step --ramp), thin ink ring = coach edited its own code, hollow dashed =
   invalid / never scored, accent labels = I_g and extension picks, ink label = final player.
   Side panel: record table, files by role, 25-task solved grid, diff excerpt, coach-transcript button.
   Below: best-so-far practice score by generation | cumulative coach tokens, linked to the tree.
   Data: trees.json, summary.json (at rest); transcripts.json (lazy, only to know which nodes have a
   coach transcript). heldout.json is not needed (final nodes carry heldout_score).
   Emits: select-run {run}, select-node {run, node}, open-transcript {run, node}.
   Listens: select-run, select-node. Hash: #tree?run=…&node=… */
(function(){
  'use strict';

  var F = EX.fmt;
  var SRC_GEN = 12;   // main-experiment cut (I_g picks come from generations ≤ 12); also read from data below

  function gen(n){ return n.generation === 'initial' ? 0 : +n.generation; }
  function sub(s){ return EX.esc(s).replace(/I_g/g, 'I<sub>g</sub>').replace(/I₀/g, 'I<sub>0</sub>').replace(/A₀/g, 'A<sub>0</sub>'); }
  function nodeName(n){ return n.id === 'initial' ? 'initial (A₀)' : 'node ' + n.id; }

  EX.mount('tree', function(node, ctx){
    return EX.loadAll(['trees', 'summary']).then(function(res){
      var TR = res[0], S = res[1], T = TR.trees;
      var runs = TR.runs.filter(function(r){ return T[r]; });
      var sourceRuns = runs.filter(function(r){ return T[r].kind === 'source'; });
      SRC_GEN = (T[sourceRuns[0]] && T[sourceRuns[0]].max_generation_committed) || SRC_GEN;
      var SM_MAX = Math.max.apply(null, sourceRuns.map(function(r){ return T[r].max_generation; }));

      /* ---------- per-run indexes ---------- */
      var IDX = {};
      runs.forEach(function(r){
        var t = T[r], by = {};
        t.nodes.forEach(function(n){ by[n.id] = n; });
        var order = t.nodes.slice().sort(function(a, b){ return gen(a) - gen(b); });
        var cum = 0, cumTok = {};
        order.forEach(function(n){ cum += (n.meta && n.meta.tokens) || 0; cumTok[n.id] = cum; });
        IDX[r] = { by: by, order: order, cumTok: cumTok };
      });

      /* ---------- score ramp: 5 bins per practice set, from the data ---------- */
      var RAMP = {};
      ['source', 'payoff'].forEach(function(set){
        var sc = [];
        runs.forEach(function(r){ if(T[r].task_set === set) T[r].nodes.forEach(function(n){ if(n.valid && n.practice_score != null) sc.push(n.practice_score); }); });
        sc.sort(function(a, b){ return a - b; });
        var lo = Math.floor(sc[Math.floor(sc.length * 0.05)] * 20) / 20, hi = Math.ceil(sc[sc.length - 1] * 20) / 20;
        if(hi <= lo) hi = lo + 0.05;
        var step = (hi - lo) / 5, th = [1, 2, 3, 4].map(function(i){ return lo + i * step; });
        RAMP[set] = { lo: lo, hi: hi, th: th };
      });
      function rampIdx(set, v){ var th = RAMP[set].th, i = 0; while(i < 4 && v >= th[i] - 1e-9) i++; return i; }
      function fillFor(run, n){ return 'var(--ramp-' + rampIdx(T[run].task_set, n.practice_score) + ')'; }
      function scored(n){ return n.valid && n.practice_score != null; }

      /* ---------- transcripts (lazy) ---------- */
      var TX = null, txState = 'loading';
      EX.load('transcripts').then(function(X){
        TX = {}; (X.coach || []).forEach(function(c){ TX[c.run + ':' + c.node] = c; });
        txState = 'ready'; renderSide();
      }, function(){ txState = 'error'; renderSide(); });

      /* ---------- state ---------- */
      var st = { run: 'source_s1', node: null, maxGen: null, xMode: 'gen', showSM: true, note: null, hover: null };
      function defaultNode(run){
        var t = T[run], pick = t.nodes.filter(function(n){ return n.is_Ig_pick; })[0];
        if(pick) return pick.id;
        if(t.final && t.final.final_node && IDX[run].by[t.final.final_node]) return t.final.final_node;
        var ext = t.nodes.filter(function(n){ return n.ext_pick_at && n.ext_pick_at.length; })[0];
        return ext ? ext.id : 'initial';
      }
      var h0 = EX.hash.get();
      if(h0.section === 'tree' && h0.params.run && T[h0.params.run]){
        st.run = h0.params.run;
        st.node = (h0.params.node && IDX[st.run].by[h0.params.node]) ? h0.params.node : defaultNode(st.run);
      } else st.node = defaultNode(st.run);
      st.maxGen = T[st.run].max_generation;

      /* ---------- skeleton ---------- */
      node.innerHTML = '';
      var root = EX.h('div', { 'class': 'fx-tree' }, node);
      var controls = EX.h('div', { 'class': 'fxt-controls' }, root);
      var groups = [
        { group: 'Source runs (coach + player co-evolve)', kinds: ['source'] },
        { group: 'Pay-off runs · original coach I₀', kinds: ['payoff_I0'] },
        { group: 'Pay-off runs · evolved coach I_g', kinds: ['payoff_Ig'] },
        { group: 'Extension tests · gen 20 / 40 coaches', kinds: ['extension_test'] }
      ].map(function(g){
        return { group: g.group, options: runs.filter(function(r){ return g.kinds.indexOf(T[r].kind) >= 0; }).map(function(r){
          var t = T[r];
          var lab = t.kind === 'source' ? r + ' · ' + t.max_generation + ' gens' : EX.runLabel(r) + (t.final && t.final.heldout != null ? ' · exam ' + F.pct(t.final.heldout) : '');
          return { value: r, label: lab };
        }) };
      });
      var runSel = EX.selectBox(controls, groups, st.run, function(v){ openRun(v, null, true); }, { label: 'Run', mono: false });
      runSel.setAttribute('aria-label', 'Run to show in the tree');

      var smToggle = EX.h('label', { 'class': 'check' }, controls);
      var smCb = EX.h('input', { type: 'checkbox' }, smToggle); smCb.checked = true;
      EX.h('span', null, smToggle, 'Show all six source trees');
      smCb.addEventListener('change', function(){ st.showSM = smCb.checked; smWrap.hidden = !st.showSM; smAxis.hidden = !st.showSM; });

      var genWrap = EX.h('label', { 'class': 'fxt-gen' }, controls);
      var genLbl = EX.h('span', { 'class': 'control-label' }, genWrap, 'Up to gen');
      var genIn = EX.h('input', { type: 'range', 'class': 'slider', min: 1, step: 1 }, genWrap);
      var genOut = EX.h('output', null, genWrap);
      genIn.addEventListener('input', function(){
        st.maxGen = +genIn.value; genOut.textContent = genIn.value;
        // keep the selection visible: walk up to the nearest ancestor inside the range
        var by = IDX[st.run].by, n = by[st.node];
        while(n && gen(n) > st.maxGen) n = by[n.parent];
        if(n && n.id !== st.node){ st.node = n.id; renderSide(); }
        drawTree(); drawChart();
      });

      var smWrap = EX.h('div', { 'class': 'fxt-sm', role: 'group', 'aria-label': 'The six source runs; choose one to open its tree' }, root);
      var smAxis = EX.h('p', { 'class': 'fxt-sm-axis' }, root);
      smAxis.innerHTML = 'Thumbnails share one generation axis (0–' + SM_MAX + '). The dashed line is generation ' + SRC_GEN +
        ', where the main experiment picked I<sub>g</sub>; <code>source_s5</code> and <code>source_s6</code> stop there. Blue ring: the I<sub>g</sub> pick.';

      var note = EX.h('div', { 'class': 'fxt-note', role: 'status' }, root); note.hidden = true;

      var main = EX.h('div', { 'class': 'fxt-main' }, root);
      var left = EX.h('div', { 'class': 'fxt-left', style: { minWidth: 0 } }, main);
      var runHead = EX.h('div', { 'class': 'fxt-runhead' }, left);
      var runSum = EX.h('p', { 'class': 'fxt-runsum' }, left);
      var legend = EX.h('div', { 'class': 'fxt-legend', 'aria-label': 'Legend' }, left);
      var scroller = EX.h('div', { 'class': 'fxt-scroll' }, left);
      var hint = EX.scrollHint(scroller);
      var readout = EX.h('p', { 'class': 'fxt-readout', 'aria-live': 'polite' }, left);
      var chartBox = EX.h('div', { 'class': 'fxt-chart' }, left);
      var side = EX.h('aside', { 'class': 'side-panel fxt-side', 'aria-live': 'polite', 'aria-label': 'Selected node record' }, main);

      var treeSvg = null, nodeEls = {}, edgeEls = [], pos = {}, layoutInfo = null, chartPts = {};

      /* ---------- small multiples ---------- */
      function drawSM(){
        smWrap.innerHTML = '';
        var w = smWrap.clientWidth || 600, cols = w < 520 ? 2 : 3;
        var tw = Math.max(120, (w - (cols - 1) * 10) / cols - 18), th = 74;
        sourceRuns.forEach(function(r){
          var t = T[r], se = (S.self_edit || {})[r];
          var b = EX.h('button', { type: 'button', 'class': 'fxt-thumb', 'aria-pressed': String(r === st.run),
            'aria-label': 'Open ' + r + ': ' + t.nodes.length + ' nodes, ' + t.max_generation + ' generations' + (se ? ', ' + se.self_edit_gens + ' of ' + se.gens + ' early generations changed the coach' : '') }, smWrap);
          var hd = EX.h('div', { 'class': 'fxt-thumb-h' }, b);
          EX.h('b', null, hd, r.replace('source_', 'source_'));
          var best = Math.max.apply(null, t.nodes.filter(scored).map(function(n){ return n.practice_score; }));
          EX.h('span', null, hd, cols === 2 ? (se ? se.self_edit_gens + '/' + se.gens + ' · ' : '') + F.pct(best, 0) : (se ? se.self_edit_gens + '/' + se.gens + ' self-edits · ' : '') + 'best ' + F.pct(best, 0));
          var L = layout(r, t.max_generation);
          var pad = 4, sx = function(g){ return pad + g / SM_MAX * (tw - 2 * pad); };
          var rowH = Math.min(6, (th - 16) / Math.max(1, L.rows));
          var sy = function(y){ return 3 + y * rowH + rowH / 2; };
          var svg = EX.s('svg', { width: tw, height: th, viewBox: '0 0 ' + tw + ' ' + th, 'aria-hidden': 'true' }, b);
          var axY = th - 11;
          EX.s('line', { 'class': 'thumb-base', x1: sx(0), x2: sx(SM_MAX), y1: axY, y2: axY }, svg);
          [0, SRC_GEN, 20, SM_MAX].filter(function(v, i, a){ return a.indexOf(v) === i && v <= SM_MAX; }).forEach(function(g){
            EX.s('text', { 'class': 'thumb-ax', x: sx(g), y: th - 1, 'text-anchor': g === 0 ? 'start' : (g === SM_MAX ? 'end' : 'middle') }, svg, String(g));
          });
          EX.s('line', { 'class': 'gen-rule', x1: sx(SRC_GEN), x2: sx(SRC_GEN), y1: 0, y2: axY }, svg);
          L.list.forEach(function(n){
            if(!n.parent || !L.pos[n.parent]) return;
            var p = L.pos[n.parent], c = L.pos[n.id];
            EX.s('path', { 'class': 'thumb-e', d: edgePath(sx(p.g), sy(p.y), sx(c.g), sy(c.y), 4) }, svg);
          });
          L.list.forEach(function(n){
            var c = L.pos[n.id], x = sx(c.g), y = sy(c.y), r0 = 2.1;
            if(scored(n)) EX.s('circle', { 'class': 'thumb-n', cx: x, cy: y, r: r0, fill: fillFor(r, n) }, svg);
            else EX.s('circle', { 'class': 'thumb-n hollow', cx: x, cy: y, r: r0 - .4 }, svg);
            if(n.touched_coach) EX.s('circle', { 'class': 'thumb-ring', cx: x, cy: y, r: r0 + 1.6 }, svg);
            if(n.is_Ig_pick) EX.s('circle', { 'class': 'thumb-pick', cx: x, cy: y, r: r0 + 3.2 }, svg);
          });
          b.addEventListener('click', function(){ openRun(r, null, true); });
        });
      }

      /* ---------- layout: x = generation, y = lineage rows ---------- */
      function layout(run, maxG){
        var by = IDX[run].by, list = IDX[run].order.filter(function(n){ return gen(n) <= maxG; });
        var inSet = {}; list.forEach(function(n){ inSet[n.id] = true; });
        var kids = {};
        list.forEach(function(n){ if(n.parent && inSet[n.parent]) (kids[n.parent] = kids[n.parent] || []).push(n); });
        Object.keys(kids).forEach(function(k){ kids[k].sort(function(a, b){ return gen(a) - gen(b); }); });
        var row = 0, P = {};
        function visit(n){
          var ch = kids[n.id] || [];
          if(!ch.length){ P[n.id] = { y: row++, g: gen(n) }; return; }
          ch.forEach(visit);
          // a node sits on its first child's row (git-graph style): long chains stay straight
          P[n.id] = { y: P[ch[0].id].y, g: gen(n) };
        }
        var roots = list.filter(function(n){ return !n.parent || !inSet[n.parent]; });
        roots.forEach(visit);
        return { list: list, pos: P, rows: row, kids: kids, by: by };
      }
      function edgePath(x1, y1, x2, y2, bend){
        if(Math.abs(y1 - y2) < 0.5) return 'M' + x1 + ',' + y1 + 'L' + x2 + ',' + y2;
        var b = Math.min(bend, x2 - x1);
        return 'M' + x1 + ',' + y1 + 'C' + (x1 + b * 0.5) + ',' + y1 + ' ' + (x1 + b * 0.5) + ',' + y2 + ' ' + (x1 + b) + ',' + y2 + 'L' + x2 + ',' + y2;
      }

      /* ---------- legend ---------- */
      function drawLegend(){
        var set = T[st.run].task_set, R = RAMP[set];
        legend.innerHTML = '';
        var it = EX.h('span', { 'class': 'it' }, legend);
        EX.h('span', null, it, 'Practice score');
        var ramp = EX.h('span', { 'class': 'fxt-ramp', title: 'Five equal bins from ' + F.pct(R.lo, 0) + ' to ' + F.pct(R.hi, 0) + ' (' + set + ' practice set)' }, it);
        EX.h('span', { 'class': 'fxt-ramp-l' }, ramp, '<' + F.pct(R.th[0], 0));
        for(var i = 0; i < 5; i++) EX.h('i', { style: { background: 'var(--ramp-' + i + ')' } }, ramp);
        EX.h('span', { 'class': 'fxt-ramp-l' }, ramp, '≥' + F.pct(R.th[3], 0));
        function mk(label, draw){
          var s = EX.h('span', { 'class': 'it' }, legend);
          var svg = EX.s('svg', { width: 18, height: 18, viewBox: '-9 -9 18 18', 'aria-hidden': 'true' }, s); draw(svg);
          EX.h('span', null, s, label);
        }
        mk('coach edited its own code', function(g){ EX.s('circle', { r: 4.5, fill: 'var(--ramp-2)', stroke: 'var(--rule-strong)', 'stroke-width': .8 }, g); EX.s('circle', { r: 7.3, fill: 'none', stroke: 'var(--ink)', 'stroke-width': 1.1 }, g); });
        mk('invalid or never scored', function(g){ EX.s('circle', { r: 4.5, fill: 'var(--bg)', stroke: 'var(--ink-muted)', 'stroke-dasharray': '1.6 1.6' }, g); });
        mk('selected', function(g){ EX.s('circle', { r: 4.5, fill: 'var(--ramp-2)' }, g); EX.s('circle', { r: 7.5, fill: 'none', stroke: 'var(--accent)', 'stroke-width': 2 }, g); });
        var pk = EX.h('span', { 'class': 'it' }, legend);
        EX.h('span', { style: { fontFamily: 'var(--font-mono)', fontSize: '11px', color: 'var(--accent)' }, html: 'I<sub>g</sub> · g20' }, pk);
        EX.h('span', null, pk, 'coach picks');
        if(T[st.run].kind !== 'source'){
          var fn = EX.h('span', { 'class': 'it' }, legend);
          EX.h('span', { style: { fontFamily: 'var(--font-mono)', fontSize: '11px', color: 'var(--ink)' } }, fn, 'final');
          EX.h('span', null, fn, 'player that took the exam');
        }
      }

      /* ---------- run header ---------- */
      function drawRunHead(){
        var t = T[st.run], L = IDX[st.run];
        runHead.innerHTML = '';
        EX.h('div', { 'class': 'fig-sub-title', html: sub(t.kind === 'source' ? st.run : EX.runLabel(st.run)) }, runHead);
        EX.h('span', { 'class': 'mono muted', style: { fontSize: '12px' } }, runHead, t.kind === 'source' ? 'source run' : st.run);
        var nodes = t.nodes, nInv = nodes.filter(function(n){ return !scored(n) && n.id !== 'initial'; }).length;
        var nCoach = nodes.filter(function(n){ return n.touched_coach; }).length;
        var unit = t.kind === 'source' ? 'generations' : 'rounds';
        var txt = nodes.length + ' nodes over ' + t.max_generation + ' ' + unit + '. ' + (nodes.length - 1 - nInv) + ' new nodes were scored on the ' + t.task_set + ' practice set; ' + nInv + ' were invalid or never scored. ';
        if(t.kind === 'source'){
          var se = (S.self_edit || {})[st.run];
          txt += nCoach + ' node' + (nCoach === 1 ? '' : 's') + ' changed the coach\'s own code' + (se ? ' (' + se.self_edit_gens + ' of the first ' + se.gens + ' generations)' : '') + '.';
          runSum.innerHTML = EX.esc(txt);
        } else {
          var o = t.coach_origin || {};
          var oTxt = o.source_run ? 'Frozen coach: ' + o.source_run + ' node ' + o.source_node + ' (' + o.rule + ').' : 'Frozen coach: the original I₀, unchanged.';
          var fin = t.final || {};
          var fTxt = fin.final_node ? ' Final player: ' + (fin.final_node === 'initial' ? 'the unedited A₀' : 'node ' + fin.final_node) + ', exam score ' + F.pct(fin.heldout) + '.' : '';
          runSum.innerHTML = sub(txt + oTxt + fTxt) + (o.source_run ? ' <button type="button" class="linkbtn" data-open-origin>Open the coach in ' + EX.esc(o.source_run) + '</button>' : '');
          var ob = runSum.querySelector('[data-open-origin]');
          if(ob) ob.addEventListener('click', function(){ openRun(o.source_run, o.source_node, true); });
        }
      }

      /* ---------- detail tree ---------- */
      function drawTree(){
        var run = st.run, t = T[run];
        var L = layout(run, st.maxGen); layoutInfo = L; pos = L.pos;
        scroller.innerHTML = ''; nodeEls = {}; edgeEls = [];
        var avail = scroller.clientWidth || 600;
        var ml = 18, mr = 30, laneH = 34, rowH = 17, axisH = 30;
        var maxG = Math.max(1, st.maxGen);
        var pg = Math.max(17, Math.min(64, (avail - ml - mr) / maxG));
        var W = Math.ceil(ml + mr + pg * maxG), H = laneH + L.rows * rowH + axisH;
        var X = function(g){ return ml + g * pg; }, Y = function(y){ return laneH + y * rowH + rowH / 2; };
        var unit = t.kind === 'source' ? 'Generation' : 'Round';
        var svg = treeSvg = EX.s('svg', { 'class': 'fxt-svg', width: W, height: H, viewBox: '0 0 ' + W + ' ' + H,
          role: 'group', 'aria-label': 'Archive tree of ' + run + ', ' + L.list.length + ' nodes. Arrow keys move between nodes; Enter selects.' }, scroller);
        // generation grid + axis
        var ax = EX.s('g', { 'class': 'axis' }, svg), axY = H - axisH + 6;
        EX.s('line', { x1: X(0), x2: X(maxG), y1: axY, y2: axY }, ax);
        var stepT = maxG > 24 ? 5 : (maxG > 10 ? 2 : 1);
        for(var g = 0; g <= maxG; g++){
          var major = g % stepT === 0 || g === maxG;
          EX.s('line', { x1: X(g), x2: X(g), y1: axY, y2: axY + (major ? 4 : 2) }, ax);
          var lastMajor = Math.floor(maxG / stepT) * stepT;
          if(g % stepT === 0 || (g === maxG && maxG - lastMajor >= stepT / 2)) EX.s('text', { x: X(g), y: axY + 15, 'text-anchor': 'middle' }, ax, String(g));
        }
        EX.s('text', { 'class': 'gen-rule-t', x: X(maxG), y: H - 1, 'text-anchor': 'end' }, svg, unit + ' →');
        if(t.kind === 'source' && maxG > SRC_GEN){
          EX.s('line', { 'class': 'gen-rule', x1: X(SRC_GEN), x2: X(SRC_GEN), y1: laneH - 6, y2: axY }, svg);
          EX.s('text', { 'class': 'gen-rule-t halo', x: X(SRC_GEN) + 4, y: axY - 4 }, svg, 'end of main run (gen ' + SRC_GEN + ')');
        }
        // edges
        var eg = EX.s('g', null, svg);
        L.list.forEach(function(n){
          if(!n.parent || !pos[n.parent]) return;
          var p = pos[n.parent], c = pos[n.id];
          var e = EX.s('path', { 'class': 'e' + (scored(n) || n.id === 'initial' ? '' : ' inv'), d: edgePath(X(p.g), Y(p.y), X(c.g), Y(c.y), Math.min(pg, 16)) }, eg);
          e.__child = n.id; edgeEls.push(e);
        });
        // picks lane (accent) + final player (ink)
        var marks = [];
        L.list.forEach(function(n){
          var labs = [];
          if(n.is_Ig_pick) labs.push('I_g');
          (n.ext_pick_at || []).forEach(function(x){ labs.push(x); });
          if(labs.length) marks.push({ n: n, text: labs.join(' · '), cls: 'pk' });
          if(n.is_final_player) marks.push({ n: n, text: (n.id === 'initial' ? 'final = A₀ ' : 'final ') + F.pct(n.heldout_score), cls: 'fn' });
        });
        marks.sort(function(a, b){ return pos[a.n.id].g - pos[b.n.id].g; });
        var levelEnd = [-1e9, -1e9];
        var lg = EX.s('g', null, svg);
        marks.forEach(function(m){
          var x = X(pos[m.n.id].g), y = Y(pos[m.n.id].y);
          var tw = m.text.length * 6.7 + 6;
          var x0 = Math.max(2, Math.min(W - tw - 2, x - 6));
          var lev = x0 > levelEnd[0] ? 0 : (x0 > levelEnd[1] ? 1 : (levelEnd[0] <= levelEnd[1] ? 0 : 1));
          levelEnd[lev] = x0 + tw;
          var ly = 12 + lev * 13;
          EX.s('path', { 'class': m.cls + '-l', d: 'M' + x + ',' + (ly + 3) + 'L' + x + ',' + (y - 8) }, lg);
          var te = EX.s('text', { 'class': m.cls + '-t halo', x: x0, y: ly }, lg);
          m.text.split(/(I_g|A₀)/).forEach(function(part){
            if(part === 'I_g' || part === 'A₀'){ EX.s('tspan', null, te, part.charAt(0)); EX.s('tspan', { dy: 3, 'font-size': '8.5px' }, te, part === 'I_g' ? 'g' : '0'); EX.s('tspan', { dy: -3 }, te, '\u200a'); }
            else if(part) EX.s('tspan', null, te, part);
          });
        });
        // nodes
        var ng = EX.s('g', null, svg);
        L.list.forEach(function(n){
          var c = pos[n.id], x = X(c.g), y = Y(c.y), r = 5;
          var g = EX.s('g', { 'class': 'nd', transform: 'translate(' + x + ',' + y + ')', tabindex: n.id === st.node ? 0 : -1,
            role: 'button', 'aria-label': ariaFor(run, n), 'data-id': n.id }, ng);
          EX.s('circle', { 'class': 'hit', r: 9 }, g);
          if(n.touched_coach) EX.s('circle', { 'class': 'ring', r: r + 2.8 }, g);
          if(scored(n) || (n.id === 'initial' && n.practice_score != null)) EX.s('circle', { 'class': 'nd-dot', r: r, fill: fillFor(run, n) }, g);
          else EX.s('circle', { 'class': 'nd-dot hollow', r: r - .5 }, g);
          if(n.is_final_player) EX.s('rect', { 'class': 'final-mk', x: -r - 2.5, y: -r - 2.5, width: 2 * r + 5, height: 2 * r + 5, rx: 1 }, g);
          EX.s('circle', { 'class': 'focring', r: r + 7 }, g);
          EX.s('circle', { 'class': 'selring', r: r + (n.touched_coach ? 5 : 3.2) }, g);
          g.addEventListener('mouseenter', function(e){ hoverNode(n.id, e); });
          g.addEventListener('mousemove', function(e){ EX.tooltip.move(e); });
          g.addEventListener('mouseleave', function(){ hoverNode(null); });
          g.addEventListener('click', function(){ selectNode(n.id, true); });
          g.addEventListener('focus', function(){ hoverNode(n.id, g); });
          g.addEventListener('blur', function(){ hoverNode(null); });
          nodeEls[n.id] = g;
        });
        svg.addEventListener('keydown', onKey);
        markSel();
        hint.update();
        var sp = pos[st.node]; if(sp) hint.scrollTo(X(sp.g));
        setReadout(null);
      }
      function ariaFor(run, n){
        var s = nodeName(n) + ', ' + (T[run].kind === 'source' ? 'generation ' : 'round ') + gen(n) + ', ';
        s += scored(n) ? 'practice ' + F.pct(n.practice_score) : 'not scored';
        if(n.touched_coach) s += ', coach edited its own code';
        if(n.is_Ig_pick) s += ', I_g pick';
        if(n.ext_pick_at && n.ext_pick_at.length) s += ', extension pick at ' + n.ext_pick_at.join(', ');
        if(n.is_final_player) s += ', final player, exam ' + F.pct(n.heldout_score);
        return s;
      }
      function lineage(id){
        var by = IDX[st.run].by, out = {}, n = by[id];
        while(n){ out[n.id] = true; n = by[n.parent]; }
        return out;
      }
      function tipHTML(n){
        var by = IDX[st.run].by, p = by[n.parent], t = T[st.run];
        var s = '<b>' + EX.esc(nodeName(n)) + '</b> <span class="t-muted">· ' + (t.kind === 'source' ? 'gen ' : 'round ') + gen(n) + '</span><br>';
        if(scored(n)) s += 'practice ' + F.pct(n.practice_score) + (p && scored(p) ? ' <span class="t-muted">(' + F.pts(n.practice_score - p.practice_score) + ' vs parent)</span>' : '');
        else s += '<span class="t-muted">' + (n.valid ? 'not scored' : 'invalid: not scored') + '</span>';
        var roles = rolesOf(n);
        if(roles.length) s += '<br>edited: ' + roles.join(', ');
        var picks = [];
        if(n.is_Ig_pick) picks.push('I<sub>g</sub> pick');
        if(n.ext_pick_at && n.ext_pick_at.length) picks.push('extension ' + n.ext_pick_at.join(', '));
        if(picks.length) s += '<br>picked as ' + picks.join('; ');
        if(n.is_final_player) s += '<br>final player · exam ' + F.pct(n.heldout_score);
        return s;
      }
      function rolesOf(n){
        var r = [];
        if(n.touched_coach) r.push('coach (its own code)');
        if(n.touched_player) r.push('player');
        return r;
      }
      function hoverNode(id, evt){
        st.hover = id;
        Object.keys(nodeEls).forEach(function(k){ nodeEls[k].classList.remove('hov', 'on'); });
        edgeEls.forEach(function(e){ e.classList.remove('on'); });
        Object.keys(chartPts).forEach(function(k){ chartPts[k].classList.toggle('hov', k === id); });
        if(!id || !treeSvg){ if(treeSvg) treeSvg.classList.remove('lin'); EX.tooltip.hide(); setReadout(null); return; }
        var lin = lineage(id);
        treeSvg.classList.add('lin');
        Object.keys(lin).forEach(function(k){ if(nodeEls[k]) nodeEls[k].classList.add('on'); });
        edgeEls.forEach(function(e){ if(lin[e.__child]) e.classList.add('on'); });
        if(nodeEls[id]) nodeEls[id].classList.add('hov');
        var n = IDX[st.run].by[id];
        if(evt) EX.tooltip.show(tipHTML(n), evt);
        setReadout(n);
      }
      function setReadout(n){
        var showing = n || IDX[st.run].by[st.node];
        if(!showing){ readout.textContent = ''; return; }
        var t = T[st.run], by = IDX[st.run].by, p = by[showing.parent];
        var depth = showing.lineage ? showing.lineage.depth : 0;
        var s = '<b>' + (n ? 'Hovering' : 'Selected') + ': ' + EX.esc(nodeName(showing)) + '</b> · ' + (t.kind === 'source' ? 'gen ' : 'round ') + gen(showing) + ' · ';
        s += scored(showing) ? 'practice ' + F.pct(showing.practice_score) + (p && scored(p) ? ' (' + F.pts(showing.practice_score - p.practice_score) + ' vs parent)' : '') : (showing.valid ? 'not scored' : 'invalid, not scored');
        s += ' · lineage depth ' + depth;
        var picks = [];
        if(showing.is_Ig_pick) picks.push('I<sub>g</sub> pick');
        if(showing.ext_pick_at && showing.ext_pick_at.length) picks.push('extension pick at ' + showing.ext_pick_at.join(', '));
        if(picks.length) s += ' · <span class="acc">' + picks.join('; ') + '</span>';
        if(showing.touched_coach) s += ' · coach edited its own code';
        if(showing.is_final_player) s += ' · final player, exam ' + F.pct(showing.heldout_score);
        if(n) s += '. The highlighted path runs back to the root.';
        readout.innerHTML = s;
      }
      function markSel(){
        Object.keys(nodeEls).forEach(function(k){
          var on = k === st.node;
          nodeEls[k].classList.toggle('sel', on);
          nodeEls[k].setAttribute('tabindex', on ? 0 : -1);
          nodeEls[k].setAttribute('aria-pressed', String(on));
        });
        Object.keys(chartPts).forEach(function(k){ chartPts[k].classList.toggle('sel', k === st.node); });
      }
      function onKey(e){
        var L = layoutInfo; if(!L) return;
        var cur = L.by[(document.activeElement && document.activeElement.getAttribute && document.activeElement.getAttribute('data-id')) || st.node];
        if(!cur) return;
        var next = null, P = L.pos;
        if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); selectNode(cur.id, true); return; }
        if(e.key === 'ArrowLeft'){ next = cur.parent && P[cur.parent] ? cur.parent : null; }
        else if(e.key === 'ArrowRight'){ var k = L.kids[cur.id]; next = k && k.length ? k[0].id : null; }
        else if(e.key === 'ArrowUp' || e.key === 'ArrowDown'){
          var dir = e.key === 'ArrowUp' ? -1 : 1, cy = P[cur.id].y, cg = P[cur.id].g, best = null, bd = 1e9;
          L.list.forEach(function(n){
            var p = P[n.id]; if(n.id === cur.id || (p.y - cy) * dir <= 0) return;
            var d = Math.abs(p.y - cy) * 100 + Math.abs(p.g - cg);
            if(d < bd){ bd = d; best = n.id; }
          });
          next = best;
        }
        else if(e.key === 'Home'){ next = 'initial'; }
        else return;
        e.preventDefault();
        if(next && nodeEls[next]){ selectNode(next, true); nodeEls[next].focus(); }
      }

      /* ---------- best-so-far chart ---------- */
      var chartSeg = null;
      function drawChart(){
        chartBox.innerHTML = ''; chartPts = {};
        var t = T[st.run], idx = IDX[st.run];
        var head = EX.h('div', { 'class': 'fxt-chart-h' }, chartBox);
        EX.h('div', { 'class': 'fig-sub-title' }, head, 'Best practice score so far');
        chartSeg = EX.seg(head, [{ value: 'gen', label: t.kind === 'source' ? 'Generation' : 'Round' }, { value: 'tok', label: 'Coach tokens (cumulative)' }],
          st.xMode, function(v){ st.xMode = v; drawChart(); }, { label: 'x-axis' });
        var pts = idx.order.filter(function(n){ return gen(n) <= st.maxGen && scored(n); });
        var W = Math.max(280, chartBox.clientWidth || 600), H = 168, m = { l: 44, r: 14, t: 10, b: 34 };
        var maxX = st.xMode === 'gen' ? Math.max(1, st.maxGen) : Math.max(1, d3.max(idx.order.filter(function(n){ return gen(n) <= st.maxGen; }), function(n){ return idx.cumTok[n.id]; }));
        var xs = d3.scaleLinear().domain([0, maxX]).range([m.l, W - m.r]);
        var ys0 = d3.min(pts, function(n){ return n.practice_score; });
        var ys = d3.scaleLinear().domain([Math.max(0, Math.floor((ys0 - 0.02) * 20) / 20), 1]).range([H - m.b, m.t]).nice();
        var svg = EX.s('svg', { width: W, height: H, viewBox: '0 0 ' + W + ' ' + H, role: 'group', 'aria-label': 'Best practice score so far in ' + st.run + ', by ' + (st.xMode === 'gen' ? 'generation' : 'cumulative coach tokens') }, chartBox);
        var sel = d3.select(svg);
        ys.ticks(4).forEach(function(v){ EX.s('line', { 'class': 'gridline', x1: m.l, x2: W - m.r, y1: ys(v), y2: ys(v) }, svg); });
        sel.append('g').attr('class', 'axis').attr('transform', 'translate(0,' + (H - m.b) + ')')
          .call(d3.axisBottom(xs).ticks(Math.min(8, Math.floor(W / 80))).tickSizeOuter(0).tickFormat(st.xMode === 'gen' ? d3.format('d') : function(v){ return F.tokens(v); }));
        sel.append('g').attr('class', 'axis').attr('transform', 'translate(' + m.l + ',0)')
          .call(d3.axisLeft(ys).ticks(4).tickSizeOuter(0).tickFormat(function(v){ return Math.round(v * 100) + '%'; }));
        EX.s('text', { 'class': 'tick-label', x: W - m.r, y: H - 2, 'text-anchor': 'end' }, svg, st.xMode === 'gen' ? (t.kind === 'source' ? 'generation' : 'round') : 'coach tokens spent in the run so far');
        var xOf = function(n){ return st.xMode === 'gen' ? xs(gen(n)) : xs(idx.cumTok[n.id]); };
        // best-so-far step line
        var best = -1, d = '', bestIds = {};
        pts.forEach(function(n, i){
          var x = xOf(n);
          if(i === 0){ best = n.practice_score; bestIds[n.id] = true; d = 'M' + x + ',' + ys(best); return; }
          d += 'L' + x + ',' + ys(best);
          if(n.practice_score > best){ best = n.practice_score; bestIds[n.id] = true; d += 'L' + x + ',' + ys(best); }
        });
        var lastX = st.xMode === 'gen' ? xs(st.maxGen) : xs(maxX);
        if(pts.length) d += 'L' + lastX + ',' + ys(best);
        EX.s('path', { 'class': 'bsf-line', d: d }, svg);
        pts.forEach(function(n){
          var c = EX.s('circle', { 'class': 'bsf-pt' + (bestIds[n.id] ? ' best' : '') + (n.id === st.node ? ' sel' : ''), cx: xOf(n), cy: ys(n.practice_score), r: bestIds[n.id] ? 3.6 : 3,
            tabindex: -1, 'aria-label': ariaFor(st.run, n) }, svg);
          c.addEventListener('mouseenter', function(e){ hoverNode(n.id, e); });
          c.addEventListener('mousemove', function(e){ EX.tooltip.move(e); });
          c.addEventListener('mouseleave', function(){ hoverNode(null); });
          c.addEventListener('click', function(){ selectNode(n.id, true); });
          chartPts[n.id] = c;
        });
        var finalBest = best;
        var capTxt = st.xMode === 'gen'
          ? 'Each dot is one scored node; filled dots set a new best. The line is the best score reached so far, which rose to ' + F.pct(finalBest) + '.'
          : 'Same dots, placed by the coach tokens the whole run had spent (all branches, ' + F.tokens(maxX) + ' by ' + (t.kind === 'source' ? 'generation ' : 'round ') + st.maxGen + ').';
        EX.h('p', { 'class': 'bsf-cap' }, chartBox, capTxt);
      }

      /* ---------- side panel ---------- */
      function renderSide(){
        var run = st.run, t = T[run], by = IDX[run].by, n = by[st.node];
        side.innerHTML = '';
        if(!n){ EX.h('p', { 'class': 'empty' }, side, 'Choose a node in the tree.'); return; }
        var h4 = EX.h('h4', null, side);
        h4.innerHTML = EX.esc(nodeName(n)) + ' <span class="mono">' + EX.esc(run) + '</span>';
        var tags = EX.h('div', { 'class': 'fxt-tags' }, side);
        if(n.is_Ig_pick) EX.h('span', { 'class': 'tag acc', html: 'I<sub>g</sub> pick' }, tags);
        (n.ext_pick_at || []).forEach(function(x){ EX.h('span', { 'class': 'tag acc' }, tags, 'extension ' + x); });
        if(n.is_final_player) EX.h('span', { 'class': 'tag' }, tags, 'final player');
        else if(n.final_candidate) EX.h('span', { 'class': 'tag' }, tags, 'final candidate');
        if(n.touched_coach) EX.h('span', { 'class': 'tag' }, tags, 'coach self-edit');
        if(n.touched_player) EX.h('span', { 'class': 'tag' }, tags, 'player edit');
        if(!n.valid && n.id !== 'initial') EX.h('span', { 'class': 'tag' }, tags, 'invalid');
        if(!tags.firstChild) tags.remove();

        var kv = EX.h('table', { 'class': 'kv' }, side), tb = EX.h('tbody', null, kv);
        function row(k, v, subTxt){
          var tr = EX.h('tr', null, tb); EX.h('th', { scope: 'row', html: k }, tr);
          var td = EX.h('td', null, tr, v); if(subTxt) EX.h('span', { 'class': 'sub' }, td, subTxt);
        }
        var p = by[n.parent];
        row(t.kind === 'source' ? 'Generation' : 'Round', String(gen(n)));
        row('Parent', n.parent ? (n.parent === 'initial' ? 'initial' : 'node ' + n.parent) : '—');
        if(scored(n)){
          row('Practice score', F.pct(n.practice_score), p && scored(p) ? F.pts(n.practice_score - p.practice_score) + ' points vs parent' : null);
        } else if(n.practice_score != null){
          row('Practice score', F.pct(n.practice_score), 'scored, but the node is marked invalid');
        } else row('Practice score', 'not scored', n.valid ? null : 'invalid node: no player was evaluated');
        if(n.rescore_combined != null) row('Re-score (combined)', F.pct(n.rescore_combined));
        if(n.heldout_score != null) row('Exam score', F.pct(n.heldout_score), 'held-out, ' + S.sets.heldout_tasks + ' tasks');
        if(n.meta){
          row('Coach calls', F.int(n.meta.calls));
          row('Coach tokens', F.tokens(n.meta.tokens));
          row('Coach cost', F.usd(n.meta.ledger_cost, 4));
        } else row('Coach step', n.id === 'initial' ? 'none (starting code)' : '—');
        if(n.lineage) row('Lineage coach tokens', F.tokens(n.lineage.cum_meta_tokens), 'depth ' + n.lineage.depth + ', ' + F.int(n.lineage.cum_meta_calls) + ' calls, ' + F.usd(n.lineage.cum_meta_cost, 4));
        var picked = [];
        if(n.is_Ig_pick) picked.push('I_g');
        (n.ext_pick_at || []).forEach(function(x){ picked.push('extension ' + x); });
        row('Picked as', '');
        tb.lastChild.lastChild.innerHTML = picked.length ? sub(picked.join(', ')) : '—';

        if(t.kind !== 'source' && t.coach_origin){
          var o = t.coach_origin, op = EX.h('p', { 'class': 'fxt-origin' }, side);
          op.innerHTML = 'This run\'s frozen coach: ' + (o.source_run ? EX.esc(o.source_run) + ' node ' + EX.esc(o.source_node) : 'the original I<sub>0</sub>') + '.';
        }

        // files changed
        EX.h('div', { 'class': 'side-sec' }, side, 'Files changed');
        if(n.files_changed && n.files_changed.length){
          var ft = EX.h('table', { 'class': 'fxt-files' }, side), fb = EX.h('tbody', null, ft);
          var ord = { coach: 0, player: 1, other: 2 };
          n.files_changed.slice().sort(function(a, b){ return ord[a.role] - ord[b.role]; }).forEach(function(f){
            var tr = EX.h('tr', { 'class': f.role }, fb);
            EX.h('td', { 'class': 'role' }, tr, f.role);
            EX.h('td', { 'class': 'path' }, tr, f.path);
            EX.h('td', { 'class': 'n' }, tr, f.binary ? 'binary' : '+' + f.added + ' ' + F.MINUS + f.removed);
          });
        } else EX.h('p', { 'class': 'empty' }, side, n.id === 'initial' ? 'The starting code: no edits.' : 'No files changed' + (n.valid ? '.' : ': the coach step produced no usable edit.'));

        // 25-task solved grid
        if(n.practice && n.practice.per_task){
          EX.h('div', { 'class': 'side-sec' }, side, 'Practice tasks solved');
          var pt = n.practice.per_task, pp = p && p.practice && p.practice.per_task;
          var grid = EX.h('div', { 'class': 'fxt-tasks', role: 'img' }, side);
          var ids = Object.keys(pt), solved = 0, gained = 0, lost = 0;
          ids.forEach(function(id){
            var v = pt[id]; solved += v;
            var ch = pp && pp[id] != null && pp[id] !== v;
            if(ch){ if(v > pp[id]) gained++; else lost++; }
            var i = EX.h('i', { 'class': (v >= 1 ? 's1' : (v > 0 ? 'sh' : '')) + (ch ? ' chg' : ''),
              title: id + ': ' + (v >= 1 ? 'solved' : v > 0 ? F.pct(v, 0) + ' of test inputs' : 'missed') + (ch ? ' (parent: ' + (pp[id] >= 1 ? 'solved' : pp[id] > 0 ? 'partly' : 'missed') + ')' : '') }, grid);
          });
          grid.setAttribute('aria-label', F.num(solved, 1).replace(/\.0$/, '') + ' of ' + ids.length + ' practice tasks solved');
          EX.h('p', { 'class': 'fxt-tasks-cap' }, side, 'Filled: solved; half: some test inputs solved; outlined: changed vs parent' +
            (pp ? ' (' + gained + ' gained, ' + lost + ' lost).' : '.'));
        }

        // diff
        if(n.diff){
          EX.h('div', { 'class': 'side-sec' }, side, 'Diff');
          if(n.diff_truncated) EX.h('p', { 'class': 'fxt-diffnote' }, side, 'Excerpt: the first ' + F.int(n.diff.length) + ' of ' + F.int(n.diff_full_chars) + ' characters.');
          var pre = EX.h('pre', { 'class': 'code diff', tabindex: 0, 'aria-label': 'Diff of ' + nodeName(n) }, side);
          var html = n.diff.split('\n').map(function(l){
            var c = /^(diff |index |--- |\+\+\+ |new file|deleted file|similarity|rename |Binary )/.test(l) ? 'meta' : /^@@/.test(l) ? 'hunk' : /^\+/.test(l) ? 'add' : /^-/.test(l) ? 'del' : '';
            return '<span class="ln' + (c ? ' ' + c : '') + '">' + EX.esc(l) + '</span>';
          }).join('');
          pre.innerHTML = html;
        }

        // coach transcript
        var tr = EX.h('div', { 'class': 'fxt-tr' }, side);
        if(txState === 'loading') EX.h('p', { 'class': 'empty' }, tr, 'Checking for a saved coach transcript…');
        else if(txState === 'error') EX.h('p', { 'class': 'empty' }, tr, 'Coach transcripts could not be loaded.');
        else if(TX[run + ':' + n.id]){
          var btn = EX.h('button', { type: 'button', 'class': 'btn small' }, tr, 'Read coach transcript');
          btn.addEventListener('click', function(){
            EX.select('node', { run: run, node: n.id, source: 'tree' });
            EX.emit('open-transcript', { run: run, node: n.id, source: 'tree' });
            var target = document.getElementById('fig-transcripts');
            if(target) target.scrollIntoView({ behavior: EX.reduceMotion ? 'auto' : 'smooth', block: 'start' });
          });
        } else {
          EX.h('p', { 'class': 'empty' }, tr, 'No coach transcript for this node. Only ' + Object.keys(TX).length + ' were kept: the picks, the largest practice-score jumps, the largest drop and one I₀ step.');
        }
      }

      /* ---------- actions ---------- */
      function selectNode(id, user){
        if(!IDX[st.run].by[id]) return;
        st.node = id;
        markSel(); renderSide(); setReadout(null);
        if(user){
          EX.select('node', { run: st.run, node: id, source: 'tree' });
          EX.hash.set('tree', { run: st.run, node: id });
        }
      }
      function openRun(run, nodeId, user, noteHTML){
        if(!T[run]) return;
        var changed = run !== st.run;
        st.run = run;
        st.node = nodeId && IDX[run].by[nodeId] ? nodeId : defaultNode(run);
        if(changed || gen(IDX[run].by[st.node]) > st.maxGen) st.maxGen = T[run].max_generation;
        runSel.value = run;
        setNote(noteHTML || null);
        syncGen(); drawAll(false);
        if(user){
          EX.select('run', { run: run, source: 'tree' });
          EX.select('node', { run: run, node: st.node, source: 'tree' });
          EX.hash.set('tree', { run: run, node: st.node });
        }
      }
      function setNote(html){
        if(!html){ note.hidden = true; note.innerHTML = ''; return; }
        note.hidden = false; note.innerHTML = html;
        var b = note.querySelector('[data-open]');
        if(b) b.addEventListener('click', function(){ openRun(b.getAttribute('data-open'), null, true); });
      }
      function syncGen(){
        var t = T[st.run];
        genIn.max = t.max_generation; genIn.value = st.maxGen; genOut.textContent = st.maxGen;
        genLbl.textContent = t.kind === 'source' ? 'Up to gen' : 'Up to round';
        genIn.setAttribute('aria-label', 'Show ' + (t.kind === 'source' ? 'generations' : 'rounds') + ' up to');
      }
      function drawAll(){
        Array.prototype.forEach.call(smWrap.querySelectorAll('.fxt-thumb'), function(b, i){ b.setAttribute('aria-pressed', String(sourceRuns[i] === st.run)); });
        drawRunHead(); drawLegend(); drawTree(); drawChart(); renderSide();
      }

      /* ---------- linking ---------- */
      EX.on('select-run', function(p){
        if(!p || p.source === 'tree' || !T[p.run] && !/^payoff_|^ext_/.test(p.run || '')) return;
        var t = T[p.run]; if(!t) return;
        if(t.kind === 'source'){ if(p.run !== st.run) openRun(p.run, null, false); return; }
        var o = t.coach_origin || {};
        if(o.source_run && T[o.source_run]){
          openRun(o.source_run, o.source_node, false,
            'Linked from another figure: showing the coach of <b>' + sub(EX.runLabel(p.run)) + '</b>, which is node ' + EX.esc(o.source_node) + ' of ' + EX.esc(o.source_run) + '. ' +
            '<button type="button" class="linkbtn" data-open="' + EX.esc(p.run) + '">Open that pay-off run\'s own tree</button>');
        } else {
          openRun(p.run, null, false, 'Linked from another figure: <b>' + sub(EX.runLabel(p.run)) + '</b> used the original coach I<sub>0</sub>, so its own pay-off tree is shown.');
        }
      });
      EX.on('select-node', function(p){
        if(!p || p.source === 'tree' || !T[p.run]) return;
        if(p.run === st.run && p.node === st.node) return;
        if(p.run === st.run){ if(IDX[st.run].by[p.node] && gen(IDX[st.run].by[p.node]) > st.maxGen){ st.maxGen = T[st.run].max_generation; syncGen(); drawTree(); drawChart(); } selectNode(p.node, false); }
        else openRun(p.run, p.node, false);
      });

      /* ---------- first draw + resize ---------- */
      function narrowCheck(){ root.classList.toggle('is-narrow', (node.clientWidth || 0) < 820); }
      narrowCheck(); syncGen(); drawSM(); drawAll();
      ctx.onResize(function(){ narrowCheck(); drawSM(); drawAll(); });
    });
  });
})();
