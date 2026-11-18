/* fig-tree.js — Explore › Evolution trees (mount "tree").
   One run at a time as a PERFORMANCE CHART: x = generation (or round, for test runs), y = practice score.
   Each saved version is a dot; thin grey lines join each version to its parent; a dark step line is the
   best score so far in the whole run; a thin ink ring = the coach edited its own code; a blue diamond +
   "Tested coach" label = a coach that was frozen and tested with a fresh player. Versions that failed
   checks sit as hollow marks on a strip under the axis.
   Picking a version (self-improvement runs) picks ITS COACH: the coach code it carries (made where the
   coach last edited itself, or the original coach). Every version that coach made turns blue and a blue
   step line shows their best practice score so far, generation by generation. In test runs the coach is
   frozen, so picking a version shows its family line (fresh player -> this version) instead.
   The side panel: plain facts, "Show code change", "Read coach transcript", and, if the picked coach was
   tested, a second small chart of its test runs (best practice so far by round) plus a small table of
   practice and exam scores against the original coach's six tests.
   Behind "More options": six sparkline charts (one per self-improvement run; click to open) and the
   picked version's practice puzzles and files.
   Data: trees.json, summary.json; coach/index.json (lazy: which versions have a coach transcript).
   Emits: select-run, select-node (user picks), open-transcript (button; also sets EX.pendingTranscript).
   Listens: select-run, select-node (never switches tabs). Hash: #tree?run=…&node=… */
(function(){
  'use strict';

  var F = EX.fmt;
  var SRC_GEN = 12;   // main-experiment cut (gen-12 picks); re-read from data
  var LETTERS = 'ABCDEFGH';

  function gen(n){ return n.generation === 'initial' ? 0 : +n.generation; }
  function ptsShort(d){
    var v = d * 100, dec = Math.abs(v - Math.round(v)) < 1e-6 ? 0 : 1;
    return F.signed(v, dec);
  }
  function deltaText(d){ var s = ptsShort(d); return s === '0' || s === '+0' ? 'same as parent' : s + ' vs parent'; }
  function pct0(x){ return F.pct(x, 0); }
  function range(a, f){
    if(!a.length) return '—';
    var lo = Math.min.apply(null, a), hi = Math.max.apply(null, a);
    return f(lo) === f(hi) ? f(lo) : f(lo).replace('%', '') + '–' + f(hi);
  }
  function listJoin(a){ return a.length < 2 ? (a[0] || '') : a.slice(0, -1).join(', ') + ' and ' + a[a.length - 1]; }

  EX.mount('tree', function(node, ctx){
    return EX.loadAll(['trees', 'summary']).then(function(res){
      var TR = res[0], T = TR.trees;
      var runs = TR.runs.filter(function(r){ return T[r]; });
      var sourceRuns = runs.filter(function(r){ return T[r].kind === 'source'; });
      SRC_GEN = (T[sourceRuns[0]] && T[sourceRuns[0]].max_generation_committed) || SRC_GEN;
      var SM_MAX = Math.max.apply(null, sourceRuns.map(function(r){ return T[r].max_generation; }));
      var testRuns = runs.filter(function(r){ return T[r].kind !== 'source'; });
      var I0runs = testRuns.filter(function(r){ return T[r].kind === 'payoff_I0'; });

      /* ---------- per-run indexes ---------- */
      function scored(n){ return n.valid && n.practice_score != null; }
      var IDX = {};
      runs.forEach(function(r){
        var t = T[r], by = {}, kids = {}, owner = {}, made = {};
        t.nodes.forEach(function(n){ by[n.id] = n; });
        var order = t.nodes.slice().sort(function(a, b){ return gen(a) - gen(b) || (+a.id || 0) - (+b.id || 0); });
        order.forEach(function(n){ if(n.parent && by[n.parent]) (kids[n.parent] = kids[n.parent] || []).push(n.id); });
        // whose coach code each version carries: itself if it edited the coach (or is the start), else its parent's
        order.forEach(function(n){ owner[n.id] = (n.id === 'initial' || n.touched_coach || !by[n.parent]) ? n.id : owner[n.parent]; });
        // which versions each coach made (the parent's coach edits the child)
        order.forEach(function(n){ if(n.parent && by[n.parent]){ var o = owner[n.parent]; (made[o] = made[o] || []).push(n.id); } });
        // best practice score so far, by generation / round
        var best = [], b = null;
        for(var g = 0; g <= t.max_generation; g++){
          order.forEach(function(n){ if(gen(n) === g && scored(n) && (b == null || n.practice_score > b)) b = n.practice_score; });
          best.push(b);
        }
        IDX[r] = { by: by, order: order, kids: kids, best: best, owner: owner, made: made };
      });
      function runNo(r){ var m = /(?:_s|_)(\d)(?:_g\d+)?$/.exec(r) || /s(\d)/.exec(r); return m ? m[1] : r; }

      /* the coach a version carries, the versions it made, and their best score so far by generation */
      function coachInfo(run, id){
        var idx = IDX[run], o = idx.owner[id], on = idx.by[o], ids = idx.made[o] || [];
        var start = scored(on) ? on.practice_score : null, b = start, pts = [], last = gen(on);
        ids.forEach(function(k){ last = Math.max(last, gen(idx.by[k])); });
        for(var g = gen(on); g <= last; g++){
          ids.forEach(function(k){ var n = idx.by[k]; if(gen(n) === g && scored(n) && (b == null || n.practice_score > b)) b = n.practice_score; });
          if(b != null) pts.push({ g: g, v: b });
        }
        var top = pts.length ? pts[pts.length - 1].v : null, topG = null;
        pts.forEach(function(p){ if(topG == null && p.v === top) topG = p.g; });
        var gens = ids.map(function(k){ return gen(idx.by[k]); });
        return { o: o, on: on, ids: ids, pts: pts, start: start, top: top, topG: topG,
          g0: gens.length ? Math.min.apply(null, gens) : null, g1: gens.length ? Math.max.apply(null, gens) : null };
      }
      function coachName(run, o){
        if(o === 'initial') return 'the original coach';
        return 'the coach from version ' + o;
      }

      /* ---------- tested coaches: source run:node -> [test runs] ---------- */
      var TESTS = {};
      testRuns.forEach(function(r){
        var o = T[r].coach_origin || {};
        if(o.source_run) (TESTS[o.source_run + ':' + o.source_node] = TESTS[o.source_run + ':' + o.source_node] || []).push(r);
      });
      var LABEL = {};   // run:node -> 'Tested coach' | 'Tested coach A' (letters only when a run has two)
      sourceRuns.forEach(function(r){
        var ks = IDX[r].order.filter(function(n){ return TESTS[r + ':' + n.id]; }).map(function(n){ return r + ':' + n.id; });
        ks.forEach(function(k, i){ LABEL[k] = 'Tested coach' + (ks.length > 1 ? ' ' + LETTERS[i] : ''); });
      });
      function testsOf(run, id){ return TESTS[run + ':' + id] || []; }
      function pickGen(r){ var g = EX.runGroup(r); return g === 'Ig' ? SRC_GEN : +g.replace('g', ''); }
      function testShort(r){ return 'picked at gen ' + pickGen(r); }
      function isFallback(r){ return /most descendants/.test((T[r].coach_origin || {}).rule || '') && !/max mean/.test(T[r].coach_origin.rule); }
      function pickGens(run, id){ return testsOf(run, id).map(pickGen).sort(function(a, b){ return a - b; }); }
      function testedText(run, id){   // "picked by the rule at gen 12, 20 and 40"
        var g = pickGens(run, id); return g.length ? 'picked by the rule at gen ' + listJoin(g) : '';
      }
      function untestedPicks(n){   // picks stored in the archive but never tested (g6, g30, ...)
        var tested = {}; testsOf(n.__run, n.id).forEach(function(r){ tested[EX.runGroup(r)] = true; });
        var out = [];
        (n.ext_pick_at || []).forEach(function(x){ var g = +String(x).replace(/\D/g, ''); if(!tested['g' + g]) out.push(g); });
        if(n.is_Ig_pick && !tested.Ig) out.unshift(SRC_GEN);
        return out;
      }
      runs.forEach(function(r){ T[r].nodes.forEach(function(n){ n.__run = r; }); });

      /* ---------- words ---------- */
      function isTest(run){ return T[run].kind !== 'source'; }
      function unit(run){ return isTest(run) ? 'round' : 'generation'; }
      function nodeName(n){ return n.id === 'initial' ? (isTest(n.__run) ? 'Fresh player' : 'Starting code') : 'Version ' + n.id; }
      function changedText(n){
        if(n.id === 'initial') return isTest(n.__run) ? 'nothing (the fresh starting player)' : 'nothing (starting code)';
        var s = n.touched_coach && n.touched_player ? 'player and coach code' : n.touched_coach ? 'coach code' : n.touched_player ? 'player code' : null;
        if(!n.valid) return s ? s + ' (but the version failed checks)' : 'nothing saved (the edit failed checks)';
        return s || 'no code change';
      }
      function scoreText(n){
        if(scored(n)) return null;
        return n.practice_score != null ? 'rejected: failed checks (had scored ' + pct0(n.practice_score) + ')' : 'failed checks, not scored';
      }
      function runName(r){
        var t = T[r], o = t.coach_origin || {};
        if(t.kind === 'source') return 'Self-improvement run ' + runNo(r) + ' (' + t.max_generation + ' generations)';
        if(t.kind === 'payoff_I0') return 'Original coach, test ' + runNo(r);
        return 'Run ' + runNo(o.source_run) + '’s coach (version ' + o.source_node + '), ' + testShort(r);
      }
      function coachFrom(run){
        var o = T[run].coach_origin || {};
        if(!o.source_run) return 'the original coach (never changed)';
        var sn = IDX[o.source_run] && IDX[o.source_run].by[o.source_node];
        return 'the coach from self-improvement run ' + runNo(o.source_run) + ', version ' + o.source_node + (sn ? ' (made at generation ' + gen(sn) + ', ' + testShort(run) + ')' : '');
      }
      function parentScoreDelta(n){
        var p = IDX[n.__run].by[n.parent];
        return (n.id !== 'initial' && p && scored(p) && scored(n)) ? n.practice_score - p.practice_score : null;
      }

      /* ---------- transcripts (lazy) ---------- */
      var TX = null, txState = 'loading';
      EX.load('coach/index').then(function(X){
        TX = {}; (X.sessions || []).forEach(function(c){ TX[c.run + ':' + c.node] = c; });
        txState = 'ready'; renderSide();
      }, function(){ txState = 'error'; renderSide(); });

      /* ---------- state ---------- */
      function defaultNode(run){
        var t = T[run];
        if(isTest(run)){ var f = t.final && t.final.final_node; return f && IDX[run].by[f] ? f : 'initial'; }
        var first = IDX[run].order.filter(function(n){ return LABEL[run + ':' + n.id]; })[0];
        return first ? first.id : 'initial';
      }
      var st = { run: 'source_s1', node: null, diffOpen: false };
      var h0 = EX.hash.get();
      if(h0.section === 'tree' && h0.params.run && T[h0.params.run]){
        st.run = h0.params.run;
        st.node = (h0.params.node && IDX[st.run].by[h0.params.node]) ? h0.params.node : defaultNode(st.run);
      } else if(EX.state && EX.state.run && T[EX.state.run] && EX.state.node && IDX[EX.state.run].by[EX.state.node]){
        st.run = EX.state.run; st.node = EX.state.node;
      } else st.node = defaultNode(st.run);

      /* ---------- skeleton ---------- */
      node.innerHTML = '';
      var root = EX.h('div', { 'class': 'fx-tree' }, node);
      var top = EX.h('div', { 'class': 'fxt-top' }, root);
      var groups = [
        { group: 'Step 1: self-improvement runs (the coach may edit itself)', kinds: ['source'] },
        { group: 'Step 2: the original coach, frozen, with a fresh player', kinds: ['payoff_I0'] },
        { group: 'Step 2: self-improved coaches picked at gen ' + SRC_GEN + ' (none qualified in run 4)', kinds: ['payoff_Ig'] },
        { group: 'Follow-up: coaches picked at gen 20 and 40', kinds: ['extension_test'] }
      ].map(function(g){
        return { group: g.group, options: runs.filter(function(r){ return g.kinds.indexOf(T[r].kind) >= 0; }).map(function(r){
          return { value: r, label: runName(r) };
        }) };
      }).filter(function(g){ return g.options.length; });
      var runSel = EX.selectBox(top, groups, st.run, function(v){ openRun(v, null, true); }, { label: 'Run' });
      runSel.setAttribute('aria-label', 'Run to show');
      var lede = EX.h('p', { 'class': 'fxt-lede' }, root);
      var runSum = EX.h('p', { 'class': 'fxt-runsum' }, root);
      var key = EX.h('div', { 'class': 'fxt-key' }, root);

      var main = EX.h('div', { 'class': 'fxt-main' }, root);
      var left = EX.h('div', { 'class': 'fxt-left' }, main);
      var chartTitle = EX.h('div', { 'class': 'fig-sub-title fxt-ctitle' }, left);
      var chartBox = EX.h('div', { 'class': 'fxt-chart' }, left);
      var testedNote = EX.h('p', { 'class': 'fxt-tnote' }, left);
      var side = EX.h('aside', { 'class': 'side-panel fxt-side', 'aria-label': 'Selected version' }, main);
      var sideFacts = EX.h('div', { 'aria-live': 'polite' }, side);
      var testBox = EX.h('div', { 'class': 'fxt-test' }, side);
      var diffBox = EX.h('div', { 'class': 'fxt-diffbox', hidden: '' }, root);
      var diffId = EX.uid('fxt-diff'); diffBox.id = diffId;
      EX.h('p', { 'class': 'fxt-kbd' }, root, 'Keyboard: Tab to the chart, then ← → step through versions in order, ↑ goes to the parent, ↓ to a child, Enter picks, Esc clears.');
      var moreUI = null;
      EX.more(root, 'More options', buildMore);

      var svgMain = null, nodeEls = {}, edgeEls = {}, famPath = null, famLab = null, P = {}, CH = null;

      /* ---------- key: one quiet line of symbols ---------- */
      function drawKey(){
        key.innerHTML = '';
        var test = isTest(st.run);
        function it(draw, label){
          var s = EX.h('span', { 'class': 'it' }, key);
          var svg = EX.s('svg', { width: 22, height: 18, viewBox: '-11 -9 22 18', 'aria-hidden': 'true' }, s); draw(svg);
          EX.h('span', null, s, label);
        }
        it(function(g){ EX.s('circle', { 'class': 'k-dot', r: 4 }, g); }, test ? 'one version of the player' : 'one version (player + coach)');
        it(function(g){ EX.s('path', { 'class': 'k-best', d: 'M-10,4H-2V-4H10' }, g); }, 'best score so far' + (test ? '' : ' (whole run)'));
        if(!test){
          it(function(g){ EX.s('path', { 'class': 'k-fam', d: 'M-10,4H-2V-4H10' }, g); EX.s('circle', { 'class': 'k-on', cx: -6, cy: 4, r: 3 }, g); }, 'picked coach: the versions it made, best so far');
          it(function(g){ EX.s('circle', { 'class': 'k-dot', r: 3.5 }, g); EX.s('circle', { 'class': 'k-ring', r: 6.5 }, g); }, 'ring: the coach edited its own code');
          it(function(g){ EX.s('path', { 'class': 'k-tested', d: 'M0,-5.5L5.5,0L0,5.5L-5.5,0Z' }, g); }, 'tested coach');
        } else {
          it(function(g){ EX.s('path', { 'class': 'k-fam', d: 'M-10,5L-2,-1L10,-4' }, g); }, 'picked version’s family line');
        }
        it(function(g){ EX.s('circle', { 'class': 'k-hollow', r: 3.5 }, g); }, 'failed checks (under the axis)');
      }

      /* ---------- header lines ---------- */
      function drawText(){
        var t = T[st.run], nodes = t.nodes, idx = IDX[st.run];
        var test = isTest(st.run);
        root.classList.toggle('is-test', test);
        lede.textContent = test
          ? 'Each dot is one version of the player; the coach stays frozen for the whole run. Higher = more practice puzzles solved. Pick a dot to follow its family line.'
          : 'Each dot is one version of the player and coach. Higher = more practice puzzles solved. Pick a dot to pick its coach: every version that coach made turns blue, and the blue line shows how their best score climbed, generation by generation.';
        runSum.innerHTML = '';
        var best = idx.best[idx.best.length - 1];
        if(!test){
          var nCoach = nodes.filter(function(n){ return n.touched_coach; }).length;
          var nTest = Object.keys(LABEL).filter(function(k){ return k.split(':')[0] === st.run; }).length;
          runSum.textContent = 'Self-improvement run ' + runNo(st.run) + ': ' + nodes.length + ' saved versions over ' + t.max_generation + ' generations, best practice score ' + pct0(best) +
            '. The coach edited its own code in ' + nCoach + ' of them; ' + (nTest ? nTest + (nTest === 1 ? ' was' : ' were') + ' later tested as a coach.' : 'none was tested as a coach.');
        } else {
          var fin = t.final || {};
          runSum.appendChild(document.createTextNode('Test run. Coach: ' + coachFrom(st.run) + ', frozen for the whole run. It coached a fresh player for ' + t.max_generation + ' rounds' +
            (fin.heldout != null ? '; the final player scored ' + F.pct(fin.heldout) + ' on the exam' + (fin.final_node === 'initial' ? ' (it was the untouched starting player)' : '') : '') + '.'));
          var o = t.coach_origin || {};
          if(o.source_run && T[o.source_run]){
            runSum.appendChild(document.createTextNode(' '));
            var b = EX.h('button', { type: 'button', 'class': 'linkbtn' }, runSum, 'Show this coach in self-improvement run ' + runNo(o.source_run));
            b.addEventListener('click', function(){ openRun(o.source_run, String(o.source_node), true); });
          }
        }
        chartTitle.textContent = 'Practice score by ' + unit(st.run);
        if(test){ testedNote.textContent = 'The final player (labelled) sat the exam: the better of the two top-scoring versions after a fresh re-score.'; return; }
        // run-specific note on the tested coaches
        var picks = idx.order.filter(function(n){ return LABEL[st.run + ':' + n.id]; }).map(function(n){
          return (LABEL[st.run + ':' + n.id].replace('Tested coach', '').trim() || 'It') + ' is version ' + n.id + ', made at generation ' + gen(n) + ' and ' + testedText(st.run, n.id);
        });
        var hasIg = idx.order.some(function(n){ return testsOf(st.run, n.id).some(function(r){ return EX.runGroup(r) === 'Ig'; }); });
        var fb = idx.order.some(function(n){ return testsOf(st.run, n.id).some(isFallback); });
        testedNote.textContent = 'Tested coach: frozen and given a fresh player to train (results on the right). ' +
          (picks.length ? picks.join('; ') + '. ' : '') +
          (!hasIg ? 'No coach qualified for the gen-' + SRC_GEN + ' pick in this run. ' : '') +
          'The diamond sits where the coach was made, not where it was picked. Pick rule: the changed coach whose versions improved most' +
          (fb ? ' (no coach qualified at one checkpoint here, so the rule fell back to the one with the most versions built on it)' : '') + '.';
      }

      /* ---------- main chart ---------- */
      function stepD(pts, X, Y){
        var d = '', prev = null;
        pts.forEach(function(p, i){ if(!i) d = 'M' + X(p.g) + ',' + Y(p.v); else { d += 'H' + X(p.g); if(p.v !== prev) d += 'V' + Y(p.v); } prev = p.v; });
        return d;
      }
      function drawChart(){
        var run = st.run, t = T[run], idx = IDX[run], test = isTest(run);
        chartBox.innerHTML = ''; nodeEls = {}; edgeEls = {}; P = {};
        var W = Math.max(280, Math.floor(chartBox.clientWidth || 600));
        var narrow = W < 520;
        var maxG = Math.max(1, t.max_generation);
        var sc = t.nodes.filter(scored).map(function(n){ return n.practice_score; });
        var lo = Math.max(0, Math.floor((Math.min.apply(null, sc.concat([1])) - 0.05) * 10) / 10);
        var stepY = (1 - lo) > 0.6 ? 0.2 : 0.1;
        lo = Math.max(0, Math.floor(lo / stepY + 1e-9) * stepY);
        var m = { l: 48, r: narrow ? 12 : 20, lane: 40 };
        var plotTop = m.lane + 8, plotH = narrow ? 240 : 340, plotB = plotTop + plotH;
        var stripY = plotB + 18, tickY = stripY + 26, H = tickY + 22;
        var X = function(g){ return m.l + g / maxG * (W - m.l - m.r); };
        var Y = function(v){ return plotB - (v - lo) / (1 - lo) * plotH; };
        CH = { X: X, Y: Y, W: W, m: m };
        var svg = svgMain = EX.s('svg', { 'class': 'fxt-svg', width: W, height: H, viewBox: '0 0 ' + W + ' ' + H, role: 'group',
          'aria-label': 'Practice score by ' + unit(run) + ' for ' + runName(run) + ', ' + t.nodes.length + ' versions. Arrow keys move between versions; Enter picks one.' }, chartBox);
        // y grid + ticks
        var ax = EX.s('g', { 'class': 'axis', 'aria-hidden': 'true' }, svg);
        for(var k = 0, v = lo; v <= 1.0001; v = lo + (++k) * stepY){
          EX.s('line', { 'class': 'gridline', x1: m.l, x2: W - m.r, y1: Y(v), y2: Y(v) }, ax);
          EX.s('text', { x: m.l - 8, y: Y(v) + 4, 'text-anchor': 'end' }, ax, Math.round(v * 100) + '%');
        }
        // x axis + ticks (below the failed-checks strip)
        EX.s('line', { x1: m.l, x2: W - m.r, y1: plotB, y2: plotB }, ax);
        var stepT = maxG > 24 ? (narrow ? 10 : 5) : (maxG > 10 ? 2 : 1);
        for(var g = 0; g <= maxG; g++){
          var major = g % stepT === 0;
          EX.s('line', { x1: X(g), x2: X(g), y1: plotB, y2: plotB + (major ? 5 : 2) }, ax);
          if(major) EX.s('text', { x: X(g), y: tickY, 'text-anchor': 'middle' }, ax, String(g));
        }
        EX.s('text', { 'class': 'fxt-axt', x: W - m.r, y: H - 2, 'text-anchor': 'end' }, svg, test ? 'Round of the test (fresh player = 0)' : 'Generation');
        // failed-checks strip
        EX.s('rect', { 'class': 'strip', x: m.l, y: stripY - 8, width: W - m.l - m.r, height: 16, rx: 3 }, svg);
        var sl = EX.s('text', { 'class': 'strip-t', x: m.l - 8, y: stripY - 1, 'text-anchor': 'end' }, svg);
        EX.s('tspan', { x: m.l - 8, dy: 0 }, sl, 'failed');
        EX.s('tspan', { x: m.l - 8, dy: 11 }, sl, 'checks');
        // gen-12 rule
        if(!test && maxG > SRC_GEN){
          EX.s('line', { 'class': 'gen-rule', x1: X(SRC_GEN), x2: X(SRC_GEN), y1: plotTop, y2: plotB }, svg);
          EX.s('text', { 'class': 'gen-rule-t halo', x: X(SRC_GEN) + 5, y: plotB - 6 }, svg, narrow ? 'gen ' + SRC_GEN + ': stage 1 ended' : 'gen ' + SRC_GEN + ': first stage ended');
        }
        // positions
        idx.order.forEach(function(n){
          var ok = scored(n);
          P[n.id] = { x: X(gen(n)), y: ok ? Y(n.practice_score) : stripY, ok: ok };
        });
        // parent -> child edges (to failed children only shown when picked)
        var eg = EX.s('g', { 'aria-hidden': 'true' }, svg);
        idx.order.forEach(function(n){
          if(!n.parent || !P[n.parent]) return;
          var p = P[n.parent], c = P[n.id];
          edgeEls[n.id] = EX.s('line', { 'class': 'e' + (c.ok && p.ok ? '' : ' inv'), x1: p.x, y1: p.y, x2: c.x, y2: c.y }, eg);
        });
        // best so far (whole run)
        var pts = idx.best.map(function(b, gi){ return { g: gi, v: b }; }).filter(function(p){ return p.v != null; });
        EX.s('path', { 'class': 'best', d: stepD(pts, X, Y), 'aria-hidden': 'true' }, svg);
        var last = pts.length ? pts[pts.length - 1].v : null;
        if(last != null) EX.s('text', { 'class': 'best-t halo', x: W - m.r, y: Y(last) - 7, 'text-anchor': 'end', 'aria-hidden': 'true' }, svg, 'best so far ' + pct0(last));
        // picked coach's best-so-far line (source) / nothing (test: edges carry the family line)
        famPath = EX.s('path', { 'class': 'fam', d: '', 'aria-hidden': 'true' }, svg);
        famLab = EX.s('text', { 'class': 'fam-t halo', 'aria-hidden': 'true' }, svg);
        // labels lane: tested coaches (accent) or final player (ink)
        var marks = [];
        idx.order.forEach(function(n){
          var L = LABEL[run + ':' + n.id];
          if(L) marks.push({ n: n, text: narrow ? L : L + ' · picked at gen ' + listJoin(pickGens(run, n.id)), cls: 'pk' });
          if(test && n.is_final_player) marks.push({ n: n, text: 'final player · exam ' + F.pct(n.heldout_score), cls: 'fn' });
        });
        var lg = EX.s('g', { 'aria-hidden': 'true' }, svg), levelEnd = [-1e9, -1e9];
        marks.forEach(function(mk){
          var p = P[mk.n.id], tw = mk.text.length * 6.9 + 6;
          var x0 = Math.max(2, Math.min(W - tw - 2, p.x - 8));
          var lev = x0 > levelEnd[0] + 6 ? 0 : (x0 > levelEnd[1] + 6 ? 1 : (levelEnd[0] <= levelEnd[1] ? 0 : 1));
          levelEnd[lev] = x0 + tw;
          var ly = 14 + lev * 17;
          EX.s('path', { 'class': mk.cls + '-l', d: 'M' + p.x + ',' + (ly + 5) + 'V' + (p.y - 9) }, lg);
          EX.s('text', { 'class': mk.cls + '-t halo', x: x0, y: ly }, lg, mk.text);
        });
        // dots
        var ng = EX.s('g', null, svg);
        idx.order.forEach(function(n){
          var p = P[n.id], tested = !!LABEL[run + ':' + n.id];
          var gg = EX.s('g', { 'class': 'nd' + (p.ok ? '' : ' ns') + (tested ? ' tested' : ''), transform: 'translate(' + p.x + ',' + p.y + ')', tabindex: -1,
            role: 'button', 'aria-label': ariaFor(n), 'data-id': n.id }, ng);
          EX.s('circle', { 'class': 'hit', r: narrow ? 8 : 10 }, gg);
          if(n.touched_coach) EX.s('circle', { 'class': 'ring', r: p.ok ? (tested ? 8.5 : 7) : 5.5 }, gg);
          if(!p.ok) EX.s('circle', { 'class': 'dot hollow', r: 3 }, gg);
          else if(tested) EX.s('path', { 'class': 'dot dia', d: 'M0,-6L6,0L0,6L-6,0Z' }, gg);
          else EX.s('circle', { 'class': 'dot', r: 4.2 }, gg);
          EX.s('circle', { 'class': 'selring', r: p.ok ? (n.touched_coach ? 12 : 9.5) : 8.5 }, gg);
          gg.addEventListener('mouseenter', function(e){ hover(n.id, e); });
          gg.addEventListener('mousemove', function(e){ EX.tooltip.move(e); });
          gg.addEventListener('mouseleave', function(){ hover(null); });
          gg.addEventListener('click', function(){ hover(null); selectNode(n.id, true); });
          gg.addEventListener('focus', function(){ hover(n.id, gg); });
          gg.addEventListener('blur', function(){ hover(null); });
          nodeEls[n.id] = gg;
        });
        svg.addEventListener('keydown', onKey);
        markSel();
      }
      function ariaFor(n){
        var s = nodeName(n) + ', made at ' + unit(n.__run) + ' ' + gen(n) + ', ';
        s += scored(n) ? 'practice score ' + pct0(n.practice_score) : scoreText(n);
        if(n.touched_coach) s += ', the coach edited its own code';
        var tt = testedText(n.__run, n.id); if(tt) s += ', ' + LABEL[n.__run + ':' + n.id].toLowerCase() + ', ' + tt;
        if(isTest(n.__run) && n.is_final_player) s += ', final player, exam ' + F.pct(n.heldout_score);
        return s;
      }
      function tipHTML(n){
        var s = '<b>' + EX.esc(nodeName(n)) + (n.id === 'initial' ? '' : ', made at ' + unit(n.__run) + ' ' + gen(n)) + '</b>: ';
        if(scored(n)){ var dd = parentScoreDelta(n); s += 'practice ' + pct0(n.practice_score) + (dd != null ? ' (' + deltaText(dd) + ')' : ''); }
        else s += '<span class="t-muted">' + EX.esc(scoreText(n)) + '</span>';
        s += '.<br>Changed: ' + EX.esc(changedText(n)) + '.';
        var tt = testedText(n.__run, n.id);
        if(tt) s += '<br>Tested as a coach (' + tt + ').';
        if(isTest(n.__run) && n.is_final_player) s += '<br>Final player: exam ' + F.pct(n.heldout_score) + '.';
        return s;
      }
      function hover(id, evt){
        Object.keys(nodeEls).forEach(function(k){ nodeEls[k].classList.toggle('hov', k === id); });
        if(!id){ EX.tooltip.hide(); return; }
        if(evt) EX.tooltip.show(tipHTML(IDX[st.run].by[id]), evt);
      }
      function lineage(id){
        var by = IDX[st.run].by, out = [], n = by[id];
        while(n){ out.unshift(n.id); n = by[n.parent]; }
        return out;
      }
      function markSel(){
        if(!svgMain) return;
        var on = {}, test = isTest(st.run), d = '', lab = '';
        famLab.textContent = '';
        if(st.node){
          if(test) lineage(st.node).forEach(function(k){ on[k] = true; });
          else {
            var ci = coachInfo(st.run, st.node);
            on[ci.o] = true; ci.ids.forEach(function(k){ on[k] = true; });
            d = stepD(ci.pts, CH.X, CH.Y);
            if(ci.pts.length && ci.ids.length){
              var lp = ci.pts[ci.pts.length - 1], xe = CH.X(lp.g), right = xe > CH.m.l + 200;
              famLab.setAttribute('x', right ? xe : CH.X(ci.pts[0].g) + 4);
              famLab.setAttribute('y', CH.Y(lp.v) - 8);
              famLab.setAttribute('text-anchor', right ? 'end' : 'start');
              famLab.textContent = 'best with this coach ' + pct0(lp.v);
            }
          }
        }
        svgMain.classList.toggle('has-sel', !!st.node);
        svgMain.classList.toggle('has-coach', !!d);
        var stop = st.node && nodeEls[st.node] ? st.node : 'initial';
        if(!nodeEls[stop]) stop = Object.keys(nodeEls)[0];
        Object.keys(nodeEls).forEach(function(k){
          nodeEls[k].classList.toggle('sel', k === st.node);
          nodeEls[k].classList.toggle('on', !!on[k]);
          nodeEls[k].setAttribute('tabindex', k === stop ? 0 : -1);
          nodeEls[k].setAttribute('aria-pressed', String(k === st.node));
        });
        var by = IDX[st.run].by;
        Object.keys(edgeEls).forEach(function(k){ edgeEls[k].classList.toggle('on', !!on[k] && !!on[by[k].parent]); });
        famPath.setAttribute('d', d);
      }
      function onKey(e){
        var idx = IDX[st.run];
        var curId = (document.activeElement && document.activeElement.getAttribute && document.activeElement.getAttribute('data-id')) || st.node || 'initial';
        var cur = idx.by[curId]; if(!cur) return;
        var i = idx.order.indexOf(cur), next = null;
        if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); selectNode(cur.id, true); return; }
        if(e.key === 'Escape'){ selectNode(null, true); return; }
        if(e.key === 'ArrowLeft') next = i > 0 ? idx.order[i - 1].id : null;
        else if(e.key === 'ArrowRight') next = i < idx.order.length - 1 ? idx.order[i + 1].id : null;
        else if(e.key === 'ArrowUp') next = cur.parent && idx.by[cur.parent] ? cur.parent : null;
        else if(e.key === 'ArrowDown'){ var k = idx.kids[cur.id]; next = k && k.length ? k[0] : null; }
        else if(e.key === 'Home') next = idx.order[0].id;
        else if(e.key === 'End') next = idx.order[idx.order.length - 1].id;
        else return;
        e.preventDefault();
        if(next && nodeEls[next]){ selectNode(next, true); nodeEls[next].focus(); }
      }

      /* ---------- side panel ---------- */
      function renderSide(){
        var run = st.run, t = T[run], by = IDX[run].by, n = st.node ? by[st.node] : null;
        sideFacts.innerHTML = '';
        if(!n){
          EX.h('h4', null, sideFacts, runName(run));
          var kv0 = EX.h('table', { 'class': 'kv' }, sideFacts), tb0 = EX.h('tbody', null, kv0);
          var b = IDX[run].best[IDX[run].best.length - 1];
          var rows0 = [['Saved versions', String(t.nodes.length)], [isTest(run) ? 'Rounds' : 'Generations', String(t.max_generation)], ['Best practice score', b != null ? pct0(b) : '—']];
          if(isTest(run)) rows0.push(['Coach', coachFrom(run).replace(/^the /, '')]);
          if(t.final && t.final.heldout != null) rows0.push(['Exam score', F.pct(t.final.heldout)]);
          rows0.forEach(function(r){ var tr = EX.h('tr', null, tb0); EX.h('th', { scope: 'row' }, tr, r[0]); EX.h('td', null, tr, r[1]); });
          EX.h('p', { 'class': 'fxt-pick-hint' }, sideFacts, isTest(run) ? 'Pick a dot to see its family line and what changed.' : 'Pick a dot to see its coach’s progress and what changed.');
          renderTest();
          return;
        }
        var hd = EX.h('h4', null, sideFacts, nodeName(n));
        var L = LABEL[run + ':' + n.id];
        if(L) EX.h('span', { 'class': 'tag acc' }, hd, L);
        var kv = EX.h('table', { 'class': 'kv' }, sideFacts), tb = EX.h('tbody', null, kv);
        function row(k, v){ var tr = EX.h('tr', null, tb); EX.h('th', { scope: 'row' }, tr, k); return EX.h('td', null, tr, v); }
        var p = by[n.parent];
        row('Made at', n.id === 'initial' ? (isTest(run) ? 'round 0 (start)' : 'generation 0 (start)') : unit(run) + ' ' + gen(n) + ', from ' + (p ? nodeName(p).toLowerCase() : '—'));
        var dd = parentScoreDelta(n);
        row('Practice score', scored(n) ? pct0(n.practice_score) + (dd != null ? ' (' + deltaText(dd) + ')' : '') : scoreText(n));
        row('What changed', changedText(n));
        var ci = null;
        if(isTest(run)){
          row('Coach (frozen)', coachFrom(run).replace(/^the /, ''));
          row('Sat the exam?', n.is_final_player ? 'yes: ' + F.pct(n.heldout_score) + (n.id === 'initial' ? ' (untouched player)' : '') : 'no (only the final player did)');
        } else {
          ci = coachInfo(run, n.id);
          var on = ci.on;
          row('Its coach', ci.o === 'initial' ? (n.id === 'initial' ? 'the original coach' : 'the original coach (unedited)')
            : ci.o === n.id ? 'new: the coach edited itself here' : 'from version ' + ci.o + ' (coach last edited at generation ' + gen(on) + ')');
          var tg = pickGens(run, ci.o);
          row('Coach tested?', tg.length ? 'yes, ' + testedText(run, ci.o) + (ci.o !== n.id ? ' (as version ' + ci.o + ')' : '') : ci.o === 'initial' ? 'yes, as the original coach (6 tests)' : 'no');
        }
        if(ci){
          var cs = EX.h('p', { 'class': 'fxt-coachsum' }, sideFacts);
          var cname = ci.o === n.id || (ci.o === 'initial' && n.id === 'initial') ? 'This coach' : (ci.o === 'initial' ? 'The original coach' : 'The coach from version ' + ci.o);
          if(!ci.ids.length) cs.textContent = cname + ' made no later versions: nothing was built on it.';
          else {
            var sp = ci.g0 === ci.g1 ? 'at generation ' + ci.g0 : 'between generations ' + ci.g0 + ' and ' + ci.g1;
            var climb = ci.top == null ? (ci.ids.length > 1 ? 'none of them passed the checks' : 'it failed the checks')
              : ci.start == null ? 'their best practice score reached ' + pct0(ci.top) + ' (gen ' + ci.topG + ')'
              : ci.top > ci.start ? 'their best practice score climbed from ' + pct0(ci.start) + ' to ' + pct0(ci.top) + ' (by gen ' + ci.topG + ')'
              : 'none beat its own ' + pct0(ci.start);
            cs.textContent = cname + (ci.ids.length > 1 ? ' made the ' + ci.ids.length + ' blue versions ' : ' made 1 blue version ') + sp + '; ' + climb + '.';
          }
        }
        var acts = EX.h('div', { 'class': 'fxt-acts' }, sideFacts);
        if(n.diff){
          var db = EX.h('button', { type: 'button', 'class': 'btn small', 'aria-expanded': String(st.diffOpen), 'aria-controls': diffId }, acts, st.diffOpen ? 'Hide code change' : 'Show code change');
          db.addEventListener('click', function(){
            st.diffOpen = !st.diffOpen; renderSide(); renderDiff();
            if(st.diffOpen) diffBox.scrollIntoView({ behavior: EX.reduceMotion ? 'auto' : 'smooth', block: 'nearest' });
            var again = sideFacts.querySelector('[aria-controls="' + diffId + '"]'); if(again) again.focus();
          });
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
        var up = untestedPicks(n);
        if(!isTest(run) && up.length) EX.h('p', { 'class': 'fxt-mnote' }, sideFacts, 'Also picked by the rule at the gen-' + up.join(' and gen-') + ' checkpoint' + (up.length > 1 ? 's' : '') + ', but that pick was never tested' +
          (ci && ci.o !== n.id ? (ci.o === 'initial' ? ' (its coach is the original, unedited coach)' : ' (its coach code is the one from version ' + ci.o + ')') : '') + '.');
        if(!isTest(run) && ci){
          var fbr = testsOf(run, ci.o).filter(isFallback);
          if(fbr.length) EX.h('p', { 'class': 'fxt-mnote' }, sideFacts, 'The gen-' + listJoin(fbr.map(pickGen)) + ' pick used the fallback rule: no coach qualified, so the rule took the one with the most versions built on it.');
        }
        renderTest();
      }

      /* ---------- second chart: this coach with fresh players ---------- */
      function bestSeries(r){
        var b = IDX[r].best; return b.map(function(v, i){ return { g: i, v: v }; }).filter(function(p){ return p.v != null; });
      }
      function renderTest(){
        testBox.innerHTML = '';
        var run = st.run, n = st.node ? IDX[run].by[st.node] : null;
        var mine, cmp = [], title, note = '', cur = isTest(run) ? run : null, cmpLabel = '';
        if(isTest(run)){
          var o = T[run].coach_origin || {};
          if(o.source_run){ mine = testsOf(o.source_run, o.source_node); cmp = I0runs; cmpLabel = 'original coach, ' + I0runs.length + ' tests';
            title = mine.length > 1 ? 'Every test of this coach (this run: thick line)' : 'This test (blue) and the original coach’s ' + I0runs.length + ' tests (grey)'; }
          else { mine = [run]; cmp = I0runs.filter(function(r){ return r !== run; }); cmpLabel = 'other ' + cmp.length + ' tests of it';
            title = 'This test (blue) and the original coach’s other ' + cmp.length + ' tests (grey)'; }
        } else {
          if(!n) return;
          var ci = coachInfo(run, n.id);
          if(ci.o === 'initial'){ mine = I0runs.slice(); title = 'The original coach was also frozen and tested with a fresh player, ' + mine.length + ' times'; }
          else {
            mine = testsOf(run, ci.o);
            if(!mine.length){ EX.h('p', { 'class': 'fxt-untested' }, testBox, (ci.o === n.id ? 'This coach' : 'This version’s coach (from version ' + ci.o + ')') + ' was not tested with a fresh player.'); return; }
            cmp = I0runs; cmpLabel = 'original coach, ' + I0runs.length + ' tests';
            title = 'Test: this coach, frozen, trained a fresh player';
            if(mine.length > 1) note = 'Same coach, tested ' + mine.length + ' times (' + testedText(run, ci.o) + '). ';
          }
        }
        EX.h('div', { 'class': 'fxt-test-h' }, testBox, title);
        EX.h('p', { 'class': 'fxt-mnote' }, testBox, note + 'Each line: one test, best practice score so far by round (0 = fresh player).' + (cmp.length ? (T[run].kind === 'payoff_I0' ? ' Grey: its other tests.' : ' Grey: the original coach.') : ''));
        var W = Math.max(260, Math.floor(testBox.clientWidth || 300)), H = 170;
        var m = { l: 38, r: 10, t: 10, b: 30 };
        var all = mine.concat(cmp), vals = [];
        all.forEach(function(r){ bestSeries(r).forEach(function(p){ vals.push(p.v); }); });
        var lo = Math.max(0, Math.floor((Math.min.apply(null, vals) - 0.02) * 10) / 10), hi = Math.min(1, Math.ceil((Math.max.apply(null, vals) + 0.02) * 10) / 10);
        var maxR = 8; all.forEach(function(r){ maxR = Math.max(maxR, T[r].max_generation); });
        var X = function(g){ return m.l + g / maxR * (W - m.l - m.r); };
        var Y = function(v){ return m.t + (hi - v) / (hi - lo) * (H - m.t - m.b); };
        var svg = EX.s('svg', { 'class': 'fxt-tsvg', width: W, height: H, viewBox: '0 0 ' + W + ' ' + H, role: 'img' }, testBox);
        var ax = EX.s('g', { 'class': 'axis' }, svg);
        var step = (hi - lo) > 0.5 ? 0.2 : 0.1;
        for(var k = Math.ceil(lo / step - 1e-9); k * step <= hi + 1e-9; k++){
          var v = k * step;
          EX.s('line', { 'class': 'gridline', x1: m.l, x2: W - m.r, y1: Y(v), y2: Y(v) }, ax);
          EX.s('text', { x: m.l - 6, y: Y(v) + 4, 'text-anchor': 'end' }, ax, Math.round(v * 100) + '%');
        }
        EX.s('line', { x1: m.l, x2: X(maxR), y1: H - m.b, y2: H - m.b }, ax);
        for(var g = 0; g <= maxR; g += 2){
          EX.s('line', { x1: X(g), x2: X(g), y1: H - m.b, y2: H - m.b + 4 }, ax);
          EX.s('text', { x: X(g), y: H - m.b + 17, 'text-anchor': 'middle' }, ax, String(g));
        }
        EX.s('text', { 'class': 'fxt-axt', x: X(maxR), y: H - 1, 'text-anchor': 'end' }, svg, 'Round of the test');
        var lines = {};
        function line(r, cls){
          var s = bestSeries(r), d = stepD(s, X, Y);
          if(s.length) d += 'H' + X(maxR);
          lines[r] = EX.s('path', { 'class': 'tl ' + cls, d: d }, svg);
        }
        cmp.forEach(function(r){ line(r, 'cmp'); });
        mine.forEach(function(r){ line(r, 'mine' + (r === cur && mine.length > 1 ? ' cur' : '')); });

        // table: practice + exam per test; rows highlight their line
        function bestOf(r){ var b = IDX[r].best; return b[b.length - 1]; }
        function examOf(r){ return T[r].final && T[r].final.heldout; }
        var tbl = EX.h('table', { 'class': 'fxt-ttab' }, testBox);
        var th = EX.h('tr', null, EX.h('thead', null, tbl));
        ['Test', 'Best practice', 'Exam'].forEach(function(x){ EX.h('th', { scope: 'col' }, th, x); });
        var tb = EX.h('tbody', null, tbl);
        function trow(label, rs, cls, click){
          var tr = EX.h('tr', { 'class': cls || '' }, tb), c0 = EX.h('td', null, tr);
          if(click){ var bt = EX.h('button', { type: 'button', 'class': 'linkbtn' }, c0, label); bt.addEventListener('click', click);
            ['mouseenter', 'focus'].forEach(function(ev){ (ev === 'focus' ? bt : tr).addEventListener(ev, function(){ hiLine(rs, true); }); });
            ['mouseleave', 'blur'].forEach(function(ev){ (ev === 'blur' ? bt : tr).addEventListener(ev, function(){ hiLine(rs, false); }); });
          } else c0.textContent = label;
          EX.h('td', null, tr, range(rs.map(bestOf).filter(function(x){ return x != null; }), pct0));
          EX.h('td', null, tr, range(rs.map(examOf).filter(function(x){ return x != null; }), F.pct));
        }
        function hiLine(rs, on){ svg.classList.toggle('hi', on); rs.forEach(function(r){ if(lines[r]) lines[r].classList.toggle('hl', on); }); }
        mine.forEach(function(r){
          var lab = T[r].kind === 'payoff_I0' ? 'test ' + runNo(r) : testShort(r);
          if(r === cur) trow(lab + ' (this run)', [r], 'cur');
          else trow(lab, [r], '', function(){ openRun(r, null, true); });
        });
        if(cmp.length) trow(cmpLabel, cmp, 'cmp');
        EX.h('p', { 'class': 'fxt-mnote' }, testBox, 'Exam: 120 new puzzles, sat by each test’s final player (not always its best-scoring version).');
        var a = mine.map(examOf).filter(function(x){ return x != null; }), c = cmp.map(examOf).filter(function(x){ return x != null; });
        svg.setAttribute('aria-label', title + '. Best practice ' + range(mine.map(bestOf), pct0) + ', exam ' + range(a, F.pct) + (c.length ? '; original coach: practice ' + range(cmp.map(bestOf), pct0) + ', exam ' + range(c, F.pct) : '') + '.');
      }

      function renderDiff(){
        var n = st.node ? IDX[st.run].by[st.node] : null;
        diffBox.innerHTML = '';
        if(!st.diffOpen || !n || !n.diff){ diffBox.hidden = true; return; }
        diffBox.hidden = false;
        var hd = EX.h('div', { 'class': 'fxt-diffhead' }, diffBox);
        EX.h('b', null, hd, 'Code change in ' + nodeName(n).toLowerCase() + ' (' + runName(st.run) + ')');
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
        moreUI.sm = EX.h('div', { 'class': 'fxt-sm', role: 'group', 'aria-label': 'The six self-improvement runs; choose one to open it' }, s1);
        EX.h('p', { 'class': 'fxt-mnote' }, s1, 'Same axes in every panel: generation 0–' + SM_MAX + ' across, practice score up. Dots: versions; dark line: best so far; blue diamonds: tested coaches. Runs 5 and 6 stopped at generation ' + SRC_GEN + '.');
        var s3 = EX.h('section', { 'class': 'fxt-msec' }, body);
        moreUI.nodeH = EX.h('h5', null, s3);
        moreUI.nodeBox = EX.h('div', null, s3);
        drawSM(); drawNodeMore();
      }
      function drawMore(){ if(moreUI){ drawSM(); drawNodeMore(); } }

      function drawSM(){
        if(!moreUI) return;
        var wrap = moreUI.sm; wrap.innerHTML = '';
        var w = wrap.clientWidth || (ctx.width() - 48) || 600, cols = w < 520 ? 2 : 3;
        var tw = Math.max(120, (w - (cols - 1) * 10) / cols - 18), th = 74;
        var all = []; sourceRuns.forEach(function(r){ T[r].nodes.forEach(function(n){ if(scored(n)) all.push(n.practice_score); }); });
        var lo = Math.max(0, Math.floor((Math.min.apply(null, all) - 0.05) * 10) / 10);
        sourceRuns.forEach(function(r){
          var t = T[r], idx = IDX[r];
          var b = EX.h('button', { type: 'button', 'class': 'fxt-thumb', 'aria-pressed': String(r === st.run),
            'aria-label': 'Open self-improvement run ' + runNo(r) + ', ' + t.nodes.length + ' versions over ' + t.max_generation + ' generations, best practice score ' + pct0(idx.best[idx.best.length - 1]) }, wrap);
          var hd = EX.h('div', { 'class': 'fxt-thumb-h' }, b);
          EX.h('b', null, hd, 'Run ' + runNo(r));
          EX.h('span', null, hd, 'best ' + pct0(idx.best[idx.best.length - 1]));
          var pad = 4, sx = function(g){ return pad + g / SM_MAX * (tw - 2 * pad); };
          var sy = function(v){ return 4 + (1 - v) / (1 - lo) * (th - 12); };
          var svg = EX.s('svg', { width: tw, height: th, viewBox: '0 0 ' + tw + ' ' + th, 'aria-hidden': 'true' }, b);
          EX.s('line', { 'class': 'thumb-base', x1: sx(0), x2: sx(SM_MAX), y1: th - 4, y2: th - 4 }, svg);
          EX.s('line', { 'class': 'gen-rule', x1: sx(SRC_GEN), x2: sx(SRC_GEN), y1: 0, y2: th - 4 }, svg);
          idx.order.forEach(function(n){ if(scored(n) && !LABEL[r + ':' + n.id]) EX.s('circle', { 'class': 'thumb-n', cx: sx(gen(n)), cy: sy(n.practice_score), r: 1.8 }, svg); });
          var d = '', prev = null;
          idx.best.forEach(function(v, g){ if(v == null) return; if(prev == null) d = 'M' + sx(g) + ',' + sy(v); else { d += 'H' + sx(g); if(v !== prev) d += 'V' + sy(v); } prev = v; });
          EX.s('path', { 'class': 'thumb-best', d: d }, svg);
          idx.order.forEach(function(n){
            if(!LABEL[r + ':' + n.id]) return;
            var x = sx(gen(n)), y = sy(n.practice_score);
            EX.s('path', { 'class': 'thumb-pick', d: 'M' + x + ',' + (y - 3.6) + 'L' + (x + 3.6) + ',' + y + 'L' + x + ',' + (y + 3.6) + 'L' + (x - 3.6) + ',' + y + 'Z' }, svg);
          });
          b.addEventListener('click', function(){ openRun(r, null, true); });
        });
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
          var sv = F.num(solved, 1).replace(/\.0$/, '');
          grid.setAttribute('aria-label', sv + ' of ' + ids.length + ' practice puzzles solved');
          EX.h('p', { 'class': 'fxt-mnote' }, c1, sv + ' of ' + ids.length + ' solved. Filled: solved; half: partly; outlined: changed vs parent' +
            (pp ? ' (' + gained + ' gained, ' + lost + ' lost).' : '.'));
        } else EX.h('p', { 'class': 'fxt-mnote' }, c1, 'No practice result for this version.');
        if(n.files_changed && n.files_changed.length){
          var ft = EX.h('table', { 'class': 'fxt-files' }, c2), fb = EX.h('tbody', null, ft);
          var ord = { coach: 0, player: 1, other: 2 };
          n.files_changed.slice().sort(function(a, b){ return (ord[a.role] || 0) - (ord[b.role] || 0); }).forEach(function(f){
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
        if(id !== st.node) st.diffOpen = false;
        st.node = id || null;
        markSel(); renderSide(); renderDiff(); drawNodeMore();
        if(user){
          if(id) EX.select('node', { run: st.run, node: id, source: 'tree' });
          EX.hash.set('tree', id ? { run: st.run, node: id } : { run: st.run });
        }
      }
      function openRun(run, nodeId, user){
        if(!T[run]) return;
        st.run = run; st.diffOpen = false;
        st.node = nodeId && IDX[run].by[nodeId] ? nodeId : defaultNode(run);
        runSel.value = run;
        drawAll();
        if(user){
          EX.select('run', { run: run, source: 'tree' });
          if(st.node) EX.select('node', { run: run, node: st.node, source: 'tree' });
          EX.hash.set('tree', st.node ? { run: run, node: st.node } : { run: run });
        }
      }
      function drawAll(){ drawKey(); drawText(); drawChart(); renderSide(); renderDiff(); drawMore(); }

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
      function narrowCheck(){ root.classList.toggle('is-narrow', (node.clientWidth || 0) < 820); }
      narrowCheck(); drawAll();
      function relayout(){ narrowCheck(); drawChart(); renderTest(); drawMore(); }
      ctx.onResize(relayout);
      ctx.onShow(relayout);
    });
  });
})();
