/* fig-tree.js — Explore › Evolution trees (mount "tree").
   One run's archive tree at a time: x = generation (or pay-off round), y = lineage.
   Fill = practice score (5-step --ramp, stronger = higher), thin ink ring = the coach edited its own code
   (coach files incl. utils/**), hollow dashed = never scored, accent text = coach picked for testing,
   ink text = the final player that sat the exam.
   Side panel: 5 facts for the picked node, then "Show code change" (diff, full width below the tree)
   and "Read coach transcript" (when one was saved).
   Behind "More options": all six source trees, best-practice-score-so-far chart, the node's
   25 practice puzzles and its files by role.
   Data: trees.json, summary.json; transcripts.json (lazy, only to know which nodes have a coach transcript).
   Emits: select-run, select-node (user picks), open-transcript (button; also sets EX.pendingTranscript).
   Listens: select-run, select-node (never switches tabs). Hash: #tree?run=…&node=… */
(function(){
  'use strict';

  var F = EX.fmt;
  var SRC_GEN = 12;   // main-experiment cut (gen-12 picks); re-read from data

  function gen(n){ return n.generation === 'initial' ? 0 : +n.generation; }
  function nodeName(n){ return n.id === 'initial' ? 'Starting code' : 'Version ' + n.id; }
  function deltaText(d){ var s = ptsShort(d); return s === '0' ? 'same as parent' : s + ' vs parent'; }
  function ptsShort(d){
    var v = d * 100, dec = Math.abs(v - Math.round(v)) < 1e-6 ? 0 : 1;
    return F.signed(v, dec);
  }

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

      /* ---------- score ramp: 5 bins per practice set ---------- */
      var RAMP = {};
      ['source', 'payoff'].forEach(function(set){
        var sc = [];
        runs.forEach(function(r){ if(T[r].task_set === set) T[r].nodes.forEach(function(n){ if(n.valid && n.practice_score != null) sc.push(n.practice_score); }); });
        sc.sort(function(a, b){ return a - b; });
        if(!sc.length){ RAMP[set] = { th: [0.2, 0.4, 0.6, 0.8] }; return; }
        var lo = Math.floor(sc[Math.floor(sc.length * 0.05)] * 20) / 20, hi = Math.ceil(sc[sc.length - 1] * 20) / 20;
        if(hi <= lo) hi = lo + 0.05;
        var step = (hi - lo) / 5;
        RAMP[set] = { th: [1, 2, 3, 4].map(function(i){ return lo + i * step; }) };
      });
      function rampIdx(set, v){ var th = RAMP[set].th, i = 0; while(i < 4 && v >= th[i] - 1e-9) i++; return i; }
      function fillFor(run, n){ return 'var(--ramp-' + rampIdx(T[run].task_set, n.practice_score) + ')'; }
      function scored(n){ return n.valid && n.practice_score != null; }
      function hasScore(n){ return scored(n) || (n.id === 'initial' && n.practice_score != null); }

      /* ---------- picks in plain words ---------- */
      function pickParts(n){
        var a = [];
        if(n.is_Ig_pick) a.push({ k: 'Ig', short: 'self-improved', long: 'self-improved coach (generation-12 pick)', tested: true });
        (n.ext_pick_at || []).forEach(function(x){
          var g = +String(x).replace(/\D/g, '');
          var tested = g === 20 || g === 40;
          a.push({ k: x, short: 'gen ' + g, long: tested ? 'generation-' + g + ' coach' : 'generation-' + g + ' pick (stored, not tested)', tested: tested });
        });
        return a;
      }
      function pickedText(pl){
        var out = [], gens = [];
        pl.forEach(function(x){ if(x.k === 'Ig') out.push('self-improved coach'); else gens.push(x.short.replace('gen ', '')); });
        if(gens.length) out.push('generation-' + gens.join(' and -') + ' coach');
        return out.join('; ');
      }
      function pickLabel(n){
        var p = pickParts(n).filter(function(x){ return x.tested; });
        if(!p.length) return null;
        return p.map(function(x){ return x.short; }).join(' · ') + ' pick';
      }

      /* ---------- transcripts (lazy) ---------- */
      var TX = null, txState = 'loading';
      EX.load('transcripts').then(function(X){
        TX = {}; (X.coach || []).forEach(function(c){ TX[c.run + ':' + c.node] = c; });
        txState = 'ready'; renderSide();
      }, function(){ txState = 'error'; renderSide(); });

      /* ---------- state ---------- */
      var st = { run: 'source_s1', node: null, xMode: 'gen', diffOpen: false };
      var h0 = EX.hash.get();
      if(h0.section === 'tree' && h0.params.run && T[h0.params.run]){
        st.run = h0.params.run;
        st.node = (h0.params.node && IDX[st.run].by[h0.params.node]) ? h0.params.node : null;
      } else if(EX.state && EX.state.run && T[EX.state.run] && EX.state.node && IDX[EX.state.run].by[EX.state.node]){
        st.run = EX.state.run; st.node = EX.state.node;
      }

      /* ---------- skeleton ---------- */
      node.innerHTML = '';
      var root = EX.h('div', { 'class': 'fx-tree' }, node);
      var top = EX.h('div', { 'class': 'fxt-top' }, root);
      var groups = [
        { group: 'Step 1: self-improvement runs', kinds: ['source'] },
        { group: 'Step 2: tests of the original coach', kinds: ['payoff_I0'] },
        { group: 'Step 2: tests of self-improved coaches', kinds: ['payoff_Ig'] },
        { group: 'Follow-up: generation-20 and -40 coaches', kinds: ['extension_test'] }
      ].map(function(g){
        return { group: g.group, options: runs.filter(function(r){ return g.kinds.indexOf(T[r].kind) >= 0; }).map(function(r){
          var t = T[r];
          return { value: r, label: EX.runLabel(r, { plain: true }) + (t.kind === 'source' ? ' (' + t.max_generation + ' generations)' : '') };
        }) };
      }).filter(function(g){ return g.options.length; });
      var runSel = EX.selectBox(top, groups, st.run, function(v){ openRun(v, null, true); }, { label: 'Run' });
      runSel.setAttribute('aria-label', 'Run to show');
      var runSum = EX.h('p', { 'class': 'fxt-runsum' }, root);
      var key = EX.h('div', { 'class': 'fxt-key', 'aria-hidden': 'true' }, root);

      var main = EX.h('div', { 'class': 'fxt-main' }, root);
      var left = EX.h('div', { 'class': 'fxt-left' }, main);
      var scroller = EX.h('div', { 'class': 'fxt-scroll' }, left);
      var hint = EX.scrollHint(scroller);
      var side = EX.h('aside', { 'class': 'side-panel fxt-side', 'aria-live': 'polite', 'aria-label': 'Selected node' }, main);
      var diffBox = EX.h('div', { 'class': 'fxt-diffbox', hidden: '' }, root);
      var more = EX.more(root, 'More options', buildMore);
      var moreUI = null;

      var treeSvg = null, nodeEls = {}, edgeEls = [], pos = {}, layoutInfo = null, chartPts = {};

      /* ---------- key (one quiet line, theme-neutral wording) ---------- */
      function drawKey(){
        key.innerHTML = '';
        function it(draw, label){
          var s = EX.h('span', { 'class': 'it' }, key);
          var svg = EX.s('svg', { width: 18, height: 18, viewBox: '-9 -9 18 18' }, s); draw(svg);
          EX.h('span', null, s, label);
        }
        it(function(g){ EX.s('circle', { cx: -3, r: 3.5, fill: 'var(--ramp-1)' }, g); EX.s('circle', { cx: 4, r: 3.5, fill: 'var(--ramp-4)' }, g); }, 'stronger fill = higher practice score');
        it(function(g){ EX.s('circle', { r: 4, fill: 'var(--ramp-2)' }, g); EX.s('circle', { r: 7, fill: 'none', stroke: 'var(--ink)', 'stroke-width': 1.1 }, g); }, 'ring = coach edited its own code');
        it(function(g){ EX.s('circle', { r: 4, fill: 'none', stroke: 'var(--ink-muted)', 'stroke-dasharray': '1.6 1.6' }, g); }, 'not scored');
      }

      /* ---------- layout: x = generation, y = lineage rows ---------- */
      function layout(run){
        var by = IDX[run].by, list = IDX[run].order;
        var inSet = {}; list.forEach(function(n){ inSet[n.id] = true; });
        var kids = {};
        list.forEach(function(n){ if(n.parent && inSet[n.parent]) (kids[n.parent] = kids[n.parent] || []).push(n); });
        Object.keys(kids).forEach(function(k){ kids[k].sort(function(a, b){ return gen(a) - gen(b); }); });
        var row = 0, P = {};
        function visit(n){
          var ch = kids[n.id] || [];
          if(!ch.length){ P[n.id] = { y: row++, g: gen(n) }; return; }
          ch.forEach(visit);
          P[n.id] = { y: P[ch[0].id].y, g: gen(n) };   // git-graph style: long chains stay straight
        }
        list.filter(function(n){ return !n.parent || !inSet[n.parent]; }).forEach(visit);
        return { list: list, pos: P, rows: row, kids: kids, by: by };
      }
      function edgePath(x1, y1, x2, y2, bend){
        if(Math.abs(y1 - y2) < 0.5) return 'M' + x1 + ',' + y1 + 'L' + x2 + ',' + y2;
        var b = Math.min(bend, x2 - x1);
        return 'M' + x1 + ',' + y1 + 'C' + (x1 + b * 0.5) + ',' + y1 + ' ' + (x1 + b * 0.5) + ',' + y2 + ' ' + (x1 + b) + ',' + y2 + 'L' + x2 + ',' + y2;
      }

      /* ---------- run summary (one plain line) ---------- */
      function drawRunSum(){
        var t = T[st.run], nodes = t.nodes;
        var nCoach = nodes.filter(function(n){ return n.touched_coach; }).length;
        runSum.innerHTML = '';
        if(t.kind === 'source'){
          var se = (S.self_edit || {})[st.run];
          runSum.textContent = nodes.length + ' saved versions over ' + t.max_generation + ' generations. The coach edited its own code in ' +
            nCoach + ' of them' + (se && t.max_generation > se.gens && se.self_edit_gens !== nCoach ? ' (' + se.self_edit_gens + ' in the first ' + se.gens + ' generations)' : '') + '.';
        } else {
          var o = t.coach_origin || {}, fin = t.final || {};
          var who = o.source_run ? 'the coach from self-improvement run ' + o.source_run.replace('source_s', '') + ', version ' + o.source_node : 'the original coach, unchanged';
          runSum.appendChild(document.createTextNode('A frozen coach (' + who + ') trained a fresh player for ' + t.max_generation + ' rounds.' +
            (fin.heldout != null ? ' The final player scored ' + F.pct(fin.heldout) + ' on the exam' + (fin.final_node === 'initial' ? ' (it was the untouched starting player)' : '') + '.' : '')));
          if(o.source_run && T[o.source_run]){
            runSum.appendChild(document.createTextNode(' '));
            var b = EX.h('button', { type: 'button', 'class': 'linkbtn' }, runSum, 'Show where this coach came from');
            b.addEventListener('click', function(){ openRun(o.source_run, String(o.source_node), true); });
          }
        }
      }

      /* ---------- the tree ---------- */
      function drawTree(){
        var run = st.run, t = T[run];
        var L = layout(run); layoutInfo = L; pos = L.pos;
        scroller.innerHTML = ''; nodeEls = {}; edgeEls = [];
        var avail = scroller.clientWidth || 600;
        var maxG = Math.max(1, t.max_generation);
        var showRule = t.kind === 'source' && maxG > SRC_GEN;
        var ruleH = showRule ? 22 : 0;
        var ml = 16, mr = 24, laneH = ruleH + 44, rowH = 18, axisH = 40;
        // phone: fit the whole run to the width (no sideways scrolling); desktop keeps roomier spacing
        var pg = Math.max(avail < 500 ? 6 : 17, Math.min(64, (avail - ml - mr) / maxG));
        var W = Math.ceil(ml + mr + pg * maxG), H = laneH + L.rows * rowH + axisH;
        var X = function(g){ return ml + g * pg; }, Y = function(y){ return laneH + y * rowH + rowH / 2; };
        var unit = t.kind === 'source' ? 'Generation' : 'Round';
        var svg = treeSvg = EX.s('svg', { 'class': 'fxt-svg', width: W, height: H, viewBox: '0 0 ' + W + ' ' + H,
          role: 'group', 'aria-label': 'Tree of ' + EX.runLabel(run, { plain: true }) + ', ' + L.list.length + ' nodes. Arrow keys move between nodes; Enter picks one.' }, scroller);
        // axis
        var ax = EX.s('g', { 'class': 'axis' }, svg), axY = H - axisH + 6;
        EX.s('line', { x1: X(0), x2: X(maxG), y1: axY, y2: axY }, ax);
        var stepT = maxG > 24 ? 5 : (maxG > 10 ? 2 : 1);
        for(var g = 0; g <= maxG; g++){
          var major = g % stepT === 0;
          EX.s('line', { x1: X(g), x2: X(g), y1: axY, y2: axY + (major ? 4 : 2) }, ax);
          if(major) EX.s('text', { x: X(g), y: axY + 17, 'text-anchor': 'middle' }, ax, String(g));
        }
        EX.s('text', { 'class': 'fxt-axt', x: X(maxG), y: H - 2, 'text-anchor': 'end' }, svg, unit);
        if(showRule){
          EX.s('line', { 'class': 'gen-rule', x1: X(SRC_GEN), x2: X(SRC_GEN), y1: 16, y2: axY }, svg);
          EX.s('text', { 'class': 'gen-rule-t', x: X(SRC_GEN), y: 11, 'text-anchor': 'middle' }, svg, 'gen ' + SRC_GEN + ': end of main run');
        }
        // edges
        var eg = EX.s('g', null, svg);
        L.list.forEach(function(n){
          if(!n.parent || !pos[n.parent]) return;
          var p = pos[n.parent], c = pos[n.id];
          var e = EX.s('path', { 'class': 'e' + (hasScore(n) ? '' : ' inv'), d: edgePath(X(p.g), Y(p.y), X(c.g), Y(c.y), Math.min(pg, 16)) }, eg);
          e.__child = n.id; edgeEls.push(e);
        });
        // labels lane: tested picks (accent) + final player (ink)
        var marks = [];
        L.list.forEach(function(n){
          var pl = pickLabel(n);
          if(pl) marks.push({ n: n, text: pl, cls: 'pk' });
          if(n.is_final_player) marks.push({ n: n, text: 'exam ' + F.pct(n.heldout_score), cls: 'fn' });
        });
        marks.sort(function(a, b){ return pos[a.n.id].g - pos[b.n.id].g; });
        var levelEnd = [-1e9, -1e9];
        var lg = EX.s('g', null, svg);
        marks.forEach(function(m){
          var x = X(pos[m.n.id].g), y = Y(pos[m.n.id].y);
          var tw = m.text.length * 7 + 8;
          var x0 = Math.max(2, Math.min(W - tw - 2, x - 6));
          var lev = x0 > levelEnd[0] ? 0 : (x0 > levelEnd[1] ? 1 : (levelEnd[0] <= levelEnd[1] ? 0 : 1));
          levelEnd[lev] = x0 + tw;
          var ly = ruleH + 14 + lev * 16;
          EX.s('path', { 'class': m.cls + '-l', d: 'M' + x + ',' + (ly + 4) + 'L' + x + ',' + (y - 9) }, lg);
          EX.s('text', { 'class': m.cls + '-t halo', x: x0, y: ly }, lg, m.text);
        });
        // nodes
        var ng = EX.s('g', null, svg);
        L.list.forEach(function(n){
          var c = pos[n.id], x = X(c.g), y = Y(c.y), r = 5;
          var gg = EX.s('g', { 'class': 'nd', transform: 'translate(' + x + ',' + y + ')', tabindex: -1,
            role: 'button', 'aria-label': ariaFor(run, n), 'data-id': n.id }, ng);
          EX.s('circle', { 'class': 'hit', r: 9 }, gg);
          if(n.touched_coach) EX.s('circle', { 'class': 'ring', r: r + 2.8 }, gg);
          if(hasScore(n)) EX.s('circle', { 'class': 'nd-dot', r: r, fill: fillFor(run, n) }, gg);
          else EX.s('circle', { 'class': 'nd-dot hollow', r: r - .5 }, gg);
          EX.s('circle', { 'class': 'focring', r: r + 7 }, gg);
          EX.s('circle', { 'class': 'selring', r: r + (n.touched_coach ? 5 : 3.4) }, gg);
          gg.addEventListener('mouseenter', function(e){ hoverNode(n.id, e); });
          gg.addEventListener('mousemove', function(e){ EX.tooltip.move(e); });
          gg.addEventListener('mouseleave', function(){ hoverNode(null); });
          gg.addEventListener('click', function(){ selectNode(st.node === n.id ? null : n.id, true); });
          gg.addEventListener('focus', function(){ hoverNode(n.id, gg); });
          gg.addEventListener('blur', function(){ hoverNode(null); });
          nodeEls[n.id] = gg;
        });
        svg.addEventListener('keydown', onKey);
        markSel();
        hint.update();
        var sp = pos[st.node]; if(sp) hint.scrollTo(X(sp.g));
      }
      function ariaFor(run, n){
        var s = nodeName(n) + ', ' + (T[run].kind === 'source' ? 'generation ' : 'round ') + gen(n) + ', ';
        s += hasScore(n) ? 'practice score ' + F.pct(n.practice_score, 0) : 'not scored';
        if(n.touched_coach) s += ', coach edited its own code';
        var pl = pickParts(n); if(pl.length) s += ', picked as ' + pl.map(function(p){ return p.long; }).join(', ');
        if(n.is_final_player) s += ', final player, exam ' + F.pct(n.heldout_score);
        return s;
      }
      function lineage(id){
        var by = IDX[st.run].by, out = {}, n = by[id];
        while(n){ out[n.id] = true; n = by[n.parent]; }
        return out;
      }
      function changedText(n){
        if(n.id === 'initial') return 'nothing (starting code)';
        return n.touched_coach && n.touched_player ? 'player and coach code' : n.touched_coach ? 'coach code' : n.touched_player ? 'player code' : 'no code change';
      }
      function tipHTML(n){
        var by = IDX[st.run].by, p = by[n.parent];
        var s = '<b>' + EX.esc(nodeName(n)) + '</b><br>';
        if(hasScore(n)) s += 'practice score ' + F.pct(n.practice_score, 0) + (p && hasScore(p) && n.id !== 'initial' ? ' <span class="t-muted">(' + ptsShort(n.practice_score - p.practice_score) + ' vs parent)</span>' : '');
        else s += '<span class="t-muted">not scored</span>';
        s += '<br>changed: ' + changedText(n);
        var pl = pickLabel(n); if(pl) s += '<br>' + EX.esc(pl);
        if(n.is_final_player) s += '<br>final player · exam ' + F.pct(n.heldout_score);
        return s;
      }
      function hoverNode(id, evt){
        Object.keys(nodeEls).forEach(function(k){ nodeEls[k].classList.remove('hov', 'on'); });
        edgeEls.forEach(function(e){ e.classList.remove('on'); });
        Object.keys(chartPts).forEach(function(k){ chartPts[k].classList.toggle('hov', k === id); });
        if(!id || !treeSvg){ if(treeSvg) treeSvg.classList.remove('lin'); EX.tooltip.hide(); return; }
        var lin = lineage(id);
        treeSvg.classList.add('lin');
        Object.keys(lin).forEach(function(k){ if(nodeEls[k]) nodeEls[k].classList.add('on'); });
        edgeEls.forEach(function(e){ if(lin[e.__child]) e.classList.add('on'); });
        if(nodeEls[id]) nodeEls[id].classList.add('hov');
        if(evt) EX.tooltip.show(tipHTML(IDX[st.run].by[id]), evt);
      }
      function markSel(){
        var stop = st.node && nodeEls[st.node] ? st.node : 'initial';
        if(!nodeEls[stop]) stop = Object.keys(nodeEls)[0];
        Object.keys(nodeEls).forEach(function(k){
          var on = k === st.node;
          nodeEls[k].classList.toggle('sel', on);
          nodeEls[k].setAttribute('tabindex', k === stop ? 0 : -1);
          nodeEls[k].setAttribute('aria-pressed', String(on));
        });
        Object.keys(chartPts).forEach(function(k){ chartPts[k].classList.toggle('sel', k === st.node); });
      }
      function onKey(e){
        var L = layoutInfo; if(!L) return;
        var cur = L.by[(document.activeElement && document.activeElement.getAttribute && document.activeElement.getAttribute('data-id')) || st.node || 'initial'];
        if(!cur) return;
        var next = null, P = L.pos;
        if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); selectNode(cur.id, true); return; }
        if(e.key === 'Escape'){ selectNode(null, true); return; }
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

      /* ---------- side panel: run overview or 5 facts ---------- */
      function renderSide(){
        var run = st.run, t = T[run], by = IDX[run].by, n = st.node ? by[st.node] : null;
        side.innerHTML = '';
        if(!n){
          EX.h('h4', null, side, EX.runLabel(run, { plain: true }));
          var kv0 = EX.h('table', { 'class': 'kv' }, side), tb0 = EX.h('tbody', null, kv0);
          var sc = t.nodes.filter(scored).map(function(x){ return x.practice_score; });
          var rows0 = [
            ['Saved versions', String(t.nodes.length)],
            [t.kind === 'source' ? 'Generations' : 'Rounds', String(t.max_generation)],
            ['Best practice score', sc.length ? F.pct(Math.max.apply(null, sc), 0) : '—'],
            ['Coach edited itself', t.kind === 'source' ? (function(k){ return k === 1 ? 'once' : k + ' times'; })(t.nodes.filter(function(x){ return x.touched_coach; }).length) : 'never (frozen)']
          ];
          if(t.final && t.final.heldout != null) rows0.push(['Exam score', F.pct(t.final.heldout)]);
          rows0.forEach(function(r){ var tr = EX.h('tr', null, tb0); EX.h('th', { scope: 'row' }, tr, r[0]); EX.h('td', null, tr, r[1]); });
          EX.h('p', { 'class': 'fxt-pick-hint' }, side, 'Pick a dot in the tree to see what changed.');
          return;
        }
        EX.h('h4', null, side, nodeName(n));
        var kv = EX.h('table', { 'class': 'kv' }, side), tb = EX.h('tbody', null, kv);
        function row(k, v){ var tr = EX.h('tr', null, tb); EX.h('th', { scope: 'row' }, tr, k); return EX.h('td', null, tr, v); }
        var p = by[n.parent];
        row(t.kind === 'source' ? 'Generation' : 'Round', String(gen(n)));
        if(hasScore(n)) row('Practice score', F.pct(n.practice_score, 0) + (p && hasScore(p) && n.id !== 'initial' ? ' (' + deltaText(n.practice_score - p.practice_score) + ')' : ''));
        else row('Practice score', 'not scored');
        row('What changed', changedText(n));
        var pl = pickParts(n).filter(function(x){ return x.tested; });
        if(pl.length){ var pc = row('Tested as', pickedText(pl)); pc.classList.add('fxt-left-td'); }
        if(n.is_final_player) row('Exam score', F.pct(n.heldout_score) + (n.id === 'initial' ? ' (untouched player)' : ''));

        var acts = EX.h('div', { 'class': 'fxt-acts' }, side);
        if(n.diff){
          var db = EX.h('button', { type: 'button', 'class': 'btn small', 'aria-expanded': String(st.diffOpen), 'aria-controls': diffId }, acts, st.diffOpen ? 'Hide code change' : 'Show code change');
          db.addEventListener('click', function(){ st.diffOpen = !st.diffOpen; renderSide(); renderDiff(); if(st.diffOpen) diffBox.scrollIntoView({ behavior: EX.reduceMotion ? 'auto' : 'smooth', block: 'nearest' }); });
        }
        if(txState === 'ready' && TX[run + ':' + n.id]){
          var btn = EX.h('button', { type: 'button', 'class': 'btn small' }, acts, 'Read coach transcript');
          btn.addEventListener('click', function(){
            var req = { run: run, node: n.id, source: 'tree' };
            EX.pendingTranscript = req;
            EX.select('node', req);
            if(EX.explore && EX.explore.open) EX.explore.open('transcripts', { scroll: true });
            EX.emit('open-transcript', req);
          });
        }
        if(!acts.firstChild) acts.remove();
      }
      var diffId = EX.uid('fxt-diff');
      diffBox.id = diffId;
      function renderDiff(){
        var n = st.node ? IDX[st.run].by[st.node] : null;
        diffBox.innerHTML = '';
        if(!st.diffOpen || !n || !n.diff){ diffBox.hidden = true; return; }
        diffBox.hidden = false;
        var hd = EX.h('div', { 'class': 'fxt-diffhead' }, diffBox);
        EX.h('b', null, hd, 'Code change in ' + nodeName(n).toLowerCase());
        if(n.diff_truncated) EX.h('span', null, hd, ' · first ' + F.int(n.diff.length) + ' of ' + F.int(n.diff_full_chars) + ' characters');
        var pre = EX.h('pre', { 'class': 'code diff wrap', tabindex: 0, 'aria-label': 'Code change in ' + nodeName(n) }, diffBox);
        pre.innerHTML = n.diff.split('\n').map(function(l){
          var c = /^(diff |index |--- |\+\+\+ |new file|deleted file|similarity|rename |Binary )/.test(l) ? 'meta' : /^@@/.test(l) ? 'hunk' : /^\+/.test(l) ? 'add' : /^-/.test(l) ? 'del' : '';
          return '<span class="ln' + (c ? ' ' + c : '') + '">' + (EX.esc(l) || ' ') + '</span>';
        }).join('');
      }

      /* ---------- More options ---------- */
      function buildMore(body){
        moreUI = {};
        var s1 = EX.h('section', { 'class': 'fxt-msec' }, body);
        EX.h('h5', null, s1, 'All six self-improvement runs');
        moreUI.sm = EX.h('div', { 'class': 'fxt-sm', role: 'group', 'aria-label': 'The six self-improvement runs; choose one to open its tree' }, s1);
        EX.h('p', { 'class': 'fxt-mnote' }, s1, 'Same generation axis (0–' + SM_MAX + '). Dashed line: generation ' + SRC_GEN + '. Blue circle: the self-improved pick.');
        var s2 = EX.h('section', { 'class': 'fxt-msec' }, body);
        var h2 = EX.h('div', { 'class': 'fxt-mhead' }, s2);
        EX.h('h5', null, h2, 'Best practice score so far');
        moreUI.seg = EX.seg(h2, [{ value: 'gen', label: 'By generation' }, { value: 'tok', label: 'By coach tokens' }], st.xMode,
          function(v){ st.xMode = v; drawChart(); }, { ariaLabel: 'x-axis of the chart' });
        moreUI.chart = EX.h('div', { 'class': 'fxt-chart' }, s2);
        var s3 = EX.h('section', { 'class': 'fxt-msec' }, body);
        moreUI.nodeH = EX.h('h5', null, s3);
        moreUI.nodeBox = EX.h('div', null, s3);
        drawSM(); drawChart(); drawNodeMore();
      }
      function drawMore(){ if(moreUI){ drawSM(); drawChart(); drawNodeMore(); } }

      function drawSM(){
        if(!moreUI) return;
        var wrap = moreUI.sm; wrap.innerHTML = '';
        var w = wrap.clientWidth || (ctx.width() - 48) || 600, cols = w < 520 ? 2 : 3;
        var tw = Math.max(120, (w - (cols - 1) * 10) / cols - 18), th = 70;
        sourceRuns.forEach(function(r){
          var t = T[r];
          var b = EX.h('button', { type: 'button', 'class': 'fxt-thumb', 'aria-pressed': String(r === st.run),
            'aria-label': 'Open self-improvement run ' + r.replace('source_s', '') + ', ' + t.nodes.length + ' versions over ' + t.max_generation + ' generations' }, wrap);
          var hd = EX.h('div', { 'class': 'fxt-thumb-h' }, b);
          EX.h('b', null, hd, 'Run ' + r.replace('source_s', ''));
          EX.h('span', null, hd, t.max_generation + ' generations');
          var L = layout(r);
          var pad = 4, sx = function(g){ return pad + g / SM_MAX * (tw - 2 * pad); };
          var rowH = Math.min(6, (th - 16) / Math.max(1, L.rows));
          var sy = function(y){ return 4 + y * rowH + rowH / 2; };
          var svg = EX.s('svg', { width: tw, height: th, viewBox: '0 0 ' + tw + ' ' + th, 'aria-hidden': 'true' }, b);
          var axY = th - 6;
          EX.s('line', { 'class': 'thumb-base', x1: sx(0), x2: sx(SM_MAX), y1: axY, y2: axY }, svg);
          EX.s('line', { 'class': 'gen-rule', x1: sx(SRC_GEN), x2: sx(SRC_GEN), y1: 0, y2: axY }, svg);
          L.list.forEach(function(n){
            if(!n.parent || !L.pos[n.parent]) return;
            var p = L.pos[n.parent], c = L.pos[n.id];
            EX.s('path', { 'class': 'thumb-e', d: edgePath(sx(p.g), sy(p.y), sx(c.g), sy(c.y), 4) }, svg);
          });
          L.list.forEach(function(n){
            var c = L.pos[n.id], x = sx(c.g), y = sy(c.y), r0 = 2.1;
            if(hasScore(n)) EX.s('circle', { 'class': 'thumb-n', cx: x, cy: y, r: r0, fill: fillFor(r, n) }, svg);
            else EX.s('circle', { 'class': 'thumb-n hollow', cx: x, cy: y, r: r0 - .4 }, svg);
            if(n.touched_coach) EX.s('circle', { 'class': 'thumb-ring', cx: x, cy: y, r: r0 + 1.6 }, svg);
            if(n.is_Ig_pick) EX.s('circle', { 'class': 'thumb-pick', cx: x, cy: y, r: r0 + 3.2 }, svg);
          });
          b.addEventListener('click', function(){ openRun(r, null, true); });
        });
      }

      /* best practice score so far (no d3: hand-drawn axes) */
      function drawChart(){
        if(!moreUI) return;
        var box = moreUI.chart; box.innerHTML = ''; chartPts = {};
        var t = T[st.run], idx = IDX[st.run];
        var pts = idx.order.filter(scored);
        if(!pts.length){ EX.h('p', { 'class': 'empty' }, box, 'No scored versions in this run.'); return; }
        var W = Math.max(280, box.clientWidth || 600), H = 180, m = { l: 46, r: 14, t: 10, b: 40 };
        var maxX = st.xMode === 'gen' ? Math.max(1, t.max_generation) : Math.max(1, idx.cumTok[idx.order[idx.order.length - 1].id]);
        var lo = Math.max(0, Math.floor((Math.min.apply(null, pts.map(function(n){ return n.practice_score; })) - 0.02) * 10) / 10);
        var xs = function(v){ return m.l + v / maxX * (W - m.l - m.r); };
        var ys = function(v){ return H - m.b - (v - lo) / (1 - lo) * (H - m.t - m.b); };
        var svg = EX.s('svg', { width: W, height: H, viewBox: '0 0 ' + W + ' ' + H, role: 'group',
          'aria-label': 'Best practice score so far, by ' + (st.xMode === 'gen' ? 'generation' : 'coach tokens spent') }, box);
        var ax = EX.s('g', { 'class': 'axis' }, svg);
        for(var v = lo; v <= 1.0001; v += 0.1){
          EX.s('line', { 'class': 'gridline', x1: m.l, x2: W - m.r, y1: ys(v), y2: ys(v) }, svg);
          EX.s('text', { x: m.l - 6, y: ys(v) + 4, 'text-anchor': 'end' }, ax, Math.round(v * 100) + '%');
        }
        EX.s('line', { x1: m.l, x2: W - m.r, y1: H - m.b, y2: H - m.b }, ax);
        var nT = Math.max(2, Math.min(8, Math.floor((W - m.l) / 80))), stepX = niceStep(maxX / nT);
        for(var x = 0; x <= maxX + 1e-9; x += stepX){
          EX.s('line', { x1: xs(x), x2: xs(x), y1: H - m.b, y2: H - m.b + 4 }, ax);
          EX.s('text', { x: xs(x), y: H - m.b + 18, 'text-anchor': 'middle' }, ax, st.xMode === 'gen' ? String(Math.round(x)) : F.tokens(x));
        }
        EX.s('text', { 'class': 'fxt-axt', x: W - m.r, y: H - 2, 'text-anchor': 'end' }, svg,
          st.xMode === 'gen' ? (t.kind === 'source' ? 'Generation' : 'Round') : 'Coach tokens spent so far (all branches)');
        var xOf = function(n){ return st.xMode === 'gen' ? xs(gen(n)) : xs(idx.cumTok[n.id]); };
        var best = -1, d = '', bestIds = {};
        pts.forEach(function(n, i){
          var x = xOf(n);
          if(i === 0){ best = n.practice_score; bestIds[n.id] = true; d = 'M' + x + ',' + ys(best); return; }
          d += 'L' + x + ',' + ys(best);
          if(n.practice_score > best){ best = n.practice_score; bestIds[n.id] = true; d += 'L' + x + ',' + ys(best); }
        });
        d += 'L' + xs(maxX) + ',' + ys(best);
        EX.s('path', { 'class': 'bsf-line', d: d }, svg);
        pts.forEach(function(n){
          var c = EX.s('circle', { 'class': 'bsf-pt' + (bestIds[n.id] ? ' best' : '') + (n.id === st.node ? ' sel' : ''), cx: xOf(n), cy: ys(n.practice_score), r: bestIds[n.id] ? 3.6 : 3 }, svg);
          c.addEventListener('mouseenter', function(e){ hoverNode(n.id, e); });
          c.addEventListener('mousemove', function(e){ EX.tooltip.move(e); });
          c.addEventListener('mouseleave', function(){ hoverNode(null); });
          c.addEventListener('click', function(){ selectNode(n.id, true); });
          chartPts[n.id] = c;
        });
        EX.s('text', { 'class': 'bsf-lab halo', x: xs(maxX), y: ys(best) - 8, 'text-anchor': 'end' }, svg, 'best ' + F.pct(best, 0));
      }
      function niceStep(x){
        var p = Math.pow(10, Math.floor(Math.log10(x))), f = x / p;
        return (f <= 1 ? 1 : f <= 2 ? 2 : f <= 5 ? 5 : 10) * p;
      }

      function drawNodeMore(){
        if(!moreUI) return;
        var n = st.node ? IDX[st.run].by[st.node] : null, box = moreUI.nodeBox;
        box.innerHTML = '';
        if(!n){ moreUI.nodeH.textContent = 'Practice puzzles and files'; EX.h('p', { 'class': 'fxt-mnote' }, box, 'Pick a dot to see which practice puzzles it solved and which files it changed.'); return; }
        moreUI.nodeH.textContent = nodeName(n) + ': practice puzzles and files';
        var p = IDX[st.run].by[n.parent];
        var cols = EX.h('div', { 'class': 'fxt-mcols' }, box);
        var c1 = EX.h('div', null, cols), c2 = EX.h('div', null, cols);
        if(n.practice && n.practice.per_task){
          var pt = n.practice.per_task, pp = p && p.practice && p.practice.per_task;
          var grid = EX.h('div', { 'class': 'fxt-tasks', role: 'img' }, c1);
          var ids = Object.keys(pt), solved = 0, gained = 0, lost = 0;
          ids.forEach(function(id){
            var v = pt[id]; solved += v;
            var ch = pp && pp[id] != null && pp[id] !== v;
            if(ch){ if(v > pp[id]) gained++; else lost++; }
            EX.h('i', { 'class': (v >= 1 ? 's1' : (v > 0 ? 'sh' : '')) + (ch ? ' chg' : ''),
              title: id + ': ' + (v >= 1 ? 'solved' : v > 0 ? 'partly solved' : 'missed') + (ch ? ' (changed vs parent)' : '') }, grid);
          });
          grid.setAttribute('aria-label', F.num(solved, 1).replace(/\.0$/, '') + ' of ' + ids.length + ' practice puzzles solved');
          EX.h('p', { 'class': 'fxt-mnote' }, c1, F.num(solved, 1).replace(/\.0$/, '') + ' of ' + ids.length + ' solved. Filled: solved; half: partly; outlined: changed vs parent' +
            (pp ? ' (' + gained + ' gained, ' + lost + ' lost).' : '.'));
        } else EX.h('p', { 'class': 'fxt-mnote' }, c1, 'No practice result for this version.');
        if(n.files_changed && n.files_changed.length){
          var ft = EX.h('table', { 'class': 'fxt-files' }, c2), fb = EX.h('tbody', null, ft);
          var ord = { coach: 0, player: 1, other: 2 };
          n.files_changed.slice().sort(function(a, b){ return ord[a.role] - ord[b.role]; }).forEach(function(f){
            var tr = EX.h('tr', { 'class': f.role }, fb);
            EX.h('td', { 'class': 'role' }, tr, f.role);
            EX.h('td', { 'class': 'path' }, tr, f.path);
            EX.h('td', { 'class': 'n' }, tr, f.binary ? 'binary' : '+' + f.added + ' ' + F.MINUS + f.removed);
          });
        } else EX.h('p', { 'class': 'fxt-mnote' }, c2, n.id === 'initial' ? 'The starting code: no edits.' : 'No files changed.');
      }

      /* ---------- actions ---------- */
      function selectNode(id, user){
        if(id && !IDX[st.run].by[id]) return;
        st.node = id || null;
        markSel(); renderSide(); renderDiff(); drawNodeMore();
        if(user){
          if(id) EX.select('node', { run: st.run, node: id, source: 'tree' });
          EX.hash.set('tree', id ? { run: st.run, node: id } : { run: st.run });
        }
      }
      function openRun(run, nodeId, user){
        if(!T[run]) return;
        st.run = run;
        st.node = nodeId && IDX[run].by[nodeId] ? nodeId : null;
        runSel.value = run;
        drawAll();
        if(user){
          EX.select('run', { run: run, source: 'tree' });
          if(st.node) EX.select('node', { run: run, node: st.node, source: 'tree' });
          EX.hash.set('tree', st.node ? { run: run, node: st.node } : { run: run });
        }
      }
      function drawAll(){
        drawRunSum(); drawTree(); renderSide(); renderDiff(); drawMore();
      }

      /* ---------- linking (never switches tabs) ---------- */
      EX.on('select-run', function(p){
        if(!p || p.source === 'tree' || !T[p.run] || p.run === st.run) return;
        openRun(p.run, null, false);
      });
      EX.on('select-node', function(p){
        if(!p || p.source === 'tree' || !T[p.run]) return;
        if(p.run === st.run && p.node === st.node) return;
        if(p.run === st.run) selectNode(String(p.node), false);
        else openRun(p.run, String(p.node), false);
      });

      /* ---------- first draw + resize ---------- */
      function narrowCheck(){ root.classList.toggle('is-narrow', (node.clientWidth || 0) < 760); }
      narrowCheck(); drawKey(); drawAll();
      ctx.onResize(function(){ narrowCheck(); drawTree(); drawMore(); });
      ctx.onShow(function(){ narrowCheck(); drawTree(); drawMore(); });
    });
  });
})();
