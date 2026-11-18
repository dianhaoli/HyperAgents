/* fig-replay.js — Figure 3, held-out puzzle replays.
   Left: a searchable, filterable list of the 120 exam tasks (mini solve-rate bar each).
   Main: the selected task's train pairs, test input and truth; a "stage" that shows one run's two
   attempts large beside the truth, driven by a run scrubber (prev / play / next / slider); and a
   matrix of every exam run (grouped by arm) x attempt 1 / attempt 2 as thumbnails with right/wrong marks.
   Runs whose grids were not kept show their right/wrong flags only.
   Data: tasks.json, heldout.json (4.4 MB; fetched only once the figure nears the viewport).
   Emits: select-task {task, set:'heldout'} on a task pick; select-run {run} when a row or thumbnail is pinned.
   Listens: select-task (set heldout) -> switch task; select-run -> mark that row and move the scrubber;
            hash #replay?task=..&run=.. */
(function(){
  'use strict';

  var ARM_ORDER = ['B0', 'I0', 'Ig', 'g20', 'g40', 'xhigh'];
  var ARM_LABEL = {
    B0: 'B0 · two plain attempts', I0: 'I₀ · original coach', Ig: 'I_g · evolved coach',
    g20: 'Extension · gen-20 coach', g40: 'Extension · gen-40 coach', xhigh: 'Reference · A₀ at xhigh effort'
  };
  var TICK = '✓', CROSS = '✗';

  /* Wait until the figure is near the viewport before pulling the 4.4 MB answers file. */
  function whenNear(el){
    return new Promise(function(resolve){
      if(!('IntersectionObserver' in window)) return resolve();
      var h = (location.hash || '').replace(/^#/, '').split('?')[0];
      if(h === 'replay' || h === 'fig-replay') return resolve();
      var io = new IntersectionObserver(function(ents){
        if(ents.some(function(e){ return e.isIntersecting; })){ io.disconnect(); resolve(); }
      }, { rootMargin: '900px 0px 900px 0px' });
      io.observe(el);
    });
  }

  function shape(g){ return (g && g.length && g[0]) ? g.length + '×' + g[0].length : '—'; }
  function isGrid(g){ return Array.isArray(g) && g.length > 0 && Array.isArray(g[0]); }
  function diffInfo(g, truth){
    if(!isGrid(g)) return { kind: 'none' };
    if(g.length !== truth.length || g[0].length !== truth[0].length) return { kind: 'size', text: 'wrong size ' + shape(g) };
    var n = 0;
    for(var r = 0; r < g.length; r++) for(var c = 0; c < g[0].length; c++) if(g[r][c] !== truth[r][c]) n++;
    return n ? { kind: 'cells', n: n, text: n + ' cell' + (n > 1 ? 's' : '') + ' off' } : { kind: 'equal' };
  }
  /* one exam record -> two attempts {grid, ok, same, missing} */
  function attempts(rec, hasPreds){
    var out = [];
    for(var i = 0; i < 2; i++){
      var a = { ok: !!(rec && rec.c && rec.c[i]), grid: null, same: false, missing: false, noPred: !hasPreds };
      if(!rec || rec.n == null || rec.n <= i) a.missing = true;
      if(hasPreds && rec && rec.p){
        var p = rec.p[i];
        if(p === '=1'){ a.same = true; p = rec.p[0]; }
        if(isGrid(p)) a.grid = p; else a.missing = true;
      }
      out.push(a);
    }
    return out;
  }

  EX.mount('replay', function(node, ctx){
    ctx.setStatus('Loading the exam answers…');
    return whenNear(node).then(function(){
      return EX.loadAll(['tasks', 'heldout']);
    }).then(function(res){
      var TK = res[0], H = res[1], F = EX.fmt;
      node.innerHTML = '';

      /* ---------- derived data ---------- */
      var runIds = Object.keys(H.runs).filter(function(r){ return ARM_ORDER.indexOf(H.runs[r].group) >= 0; });
      runIds.sort(function(a, b){
        var ga = ARM_ORDER.indexOf(H.runs[a].group), gb = ARM_ORDER.indexOf(H.runs[b].group);
        return ga - gb || runIds.indexOf(a) - runIds.indexOf(b);
      });
      var nRuns = runIds.length;
      var noPredRuns = runIds.filter(function(r){ return !H.runs[r].has_preds; });
      var taskInfo = H.task_order.map(function(id, idx){
        var scores = runIds.map(function(r){ var v = H.runs[r].per_task[id]; return v == null ? 0 : v; });
        var any = scores.filter(function(s){ return s > 0; }).length;
        var full = scores.filter(function(s){ return s >= 1; }).length;
        var mean = scores.reduce(function(a, b){ return a + b; }, 0) / scores.length;
        var cat = any === 0 ? 'none' : (full === nRuns ? 'all' : 'some');
        return { id: id, idx: idx, mean: mean, any: any, full: full, cat: cat, nIn: (TK.tasks[id].test || []).length };
      });
      var byId = {}; taskInfo.forEach(function(t){ byId[t.id] = t; });
      var catCount = { all: taskInfo.length, none: 0, some: 0, every: 0 };
      taskInfo.forEach(function(t){ if(t.cat === 'none') catCount.none++; else if(t.cat === 'all') catCount.every++; else catCount.some++; });

      /* Default: a single-input task with small grids, solved by some runs, with the most
         distinct near-miss answers (same size as the truth, a few cells off). */
      function pickDefault(){
        var best = null, bestScore = -1;
        taskInfo.forEach(function(t){
          var T = TK.tasks[t.id]; if(t.cat !== 'some' || T.test.length !== 1) return;
          var truth = T.test[0].output; if(Math.max(truth.length, truth[0].length) > 14) return;
          var seen = {}, distinct = 0, solved = 0;
          runIds.forEach(function(r){
            if(!H.runs[r].has_preds) return;
            var rec = (H.runs[r].results[t.id] || [])[0];
            if(rec && (rec.c[0] || rec.c[1])){ solved++; return; }
            attempts(rec, true).forEach(function(a){
              var d = diffInfo(a.grid, truth);
              if(d.kind === 'cells' && d.n <= 12){ var k = JSON.stringify(a.grid); if(!seen[k]){ seen[k] = 1; distinct++; } }
            });
          });
          if(solved < 4) return;
          var sc = distinct * 10 - Math.abs(t.mean - 0.5) * 10;
          if(sc > bestScore){ bestScore = sc; best = t.id; }
        });
        return best || taskInfo[0].id;
      }

      /* ---------- state ---------- */
      var hp = EX.hash.get();
      var fromHash = hp.section === 'replay' ? hp.params : {};
      var st = {
        task: (fromHash.task && byId[fromHash.task]) ? fromHash.task : pickDefault(),
        input: 0, filter: 'all', sort: 'order', q: '', diff: true,
        pos: 0, att: 0, pinned: null, playing: false, linkNote: ''
      };
      var narrow = ctx.width() < 760;
      var timer = null;

      /* ---------- skeleton ---------- */
      var root = EX.h('div', { 'class': 'fx-replay' + (narrow ? ' narrow' : '') }, node);
      var layout = EX.h('div', { 'class': 'rp-layout' }, root);
      var side = EX.h('div', { 'class': 'rp-side' }, layout);
      var main = EX.h('div', { 'class': 'rp-main' }, layout);

      /* side: search, filter, sort, list */
      EX.h('div', { 'class': 'rp-side-title' }, side, 'Exam tasks');
      var search = EX.h('input', { type: 'search', 'class': 'rp-search', placeholder: 'Search task id', 'aria-label': 'Search exam tasks by id', autocomplete: 'off', spellcheck: 'false' }, side);
      var filt = EX.h('div', { 'class': 'rp-filt' }, side);
      var filterSeg = EX.seg(filt, [
        { value: 'all', label: 'All ' + catCount.all, title: 'All exam tasks' },
        { value: 'none', label: 'None ' + catCount.none, title: 'Solved by no run' },
        { value: 'some', label: 'Some ' + catCount.some, title: 'Solved fully or partly by some runs' },
        { value: 'every', label: 'Every ' + catCount.every, title: 'Solved fully by every run' }
      ], st.filter, function(v){ st.filter = v; renderList(); }, { ariaLabel: 'Filter tasks by how many runs solved them' });
      var sortRow = EX.h('div', { 'class': 'rp-sort' }, side);
      EX.selectBox(sortRow, [
        { value: 'order', label: 'Exam order' },
        { value: 'desc', label: 'Solve rate, high first' },
        { value: 'asc', label: 'Solve rate, low first' }
      ], st.sort, function(v){ st.sort = v; renderList(); }, { label: 'Sort' });
      var listCount = EX.h('div', { 'class': 'rp-count', 'aria-live': 'polite' }, side);
      var list = EX.h('ul', { 'class': 'rp-list', 'aria-label': 'Exam tasks' }, side);
      EX.h('div', { 'class': 'rp-legend' }, side,
        'Bar: mean task score over all ' + nRuns + ' exam runs. Count: runs that solved at least one test input.');

      search.addEventListener('input', function(){ st.q = search.value.trim().toLowerCase(); renderList(); });

      function renderList(){
        var items = taskInfo.filter(function(t){
          if(st.q && t.id.indexOf(st.q) < 0) return false;
          if(st.filter === 'none') return t.cat === 'none';
          if(st.filter === 'some') return t.cat === 'some';
          if(st.filter === 'every') return t.cat === 'all';
          return true;
        });
        if(st.sort === 'desc') items.sort(function(a, b){ return b.mean - a.mean || a.idx - b.idx; });
        if(st.sort === 'asc') items.sort(function(a, b){ return a.mean - b.mean || a.idx - b.idx; });
        list.innerHTML = '';
        listCount.textContent = 'Showing ' + items.length + ' of ' + taskInfo.length;
        if(!items.length){ EX.h('li', { 'class': 'empty' }, list, 'No task matches.'); return; }
        items.forEach(function(t){
          var li = EX.h('li', null, list);
          var b = EX.h('button', { type: 'button', 'class': 'rp-item', 'data-task': t.id, 'aria-pressed': String(t.id === st.task),
            'aria-label': 'Task ' + t.id + ', mean score ' + F.pct(t.mean) + ', solved by ' + t.any + ' of ' + nRuns + ' runs' }, li);
          EX.h('span', { 'class': 'rp-id' }, b, t.id);
          var bar = EX.h('span', { 'class': 'rp-bar', 'aria-hidden': 'true' }, b);
          EX.h('span', { 'class': 'rp-fill', style: { width: (t.mean * 100).toFixed(1) + '%' } }, bar);
          EX.h('span', { 'class': 'rp-n' }, b, t.any + '/' + nRuns);
          b.addEventListener('click', function(){ setTask(t.id, true); });
        });
      }
      list.addEventListener('keydown', function(e){
        if(e.key !== 'ArrowDown' && e.key !== 'ArrowUp' && e.key !== 'Home' && e.key !== 'End') return;
        var btns = Array.prototype.slice.call(list.querySelectorAll('.rp-item'));
        var i = btns.indexOf(document.activeElement); if(i < 0) return;
        e.preventDefault();
        var j = e.key === 'ArrowDown' ? Math.min(btns.length - 1, i + 1) : e.key === 'ArrowUp' ? Math.max(0, i - 1) : e.key === 'Home' ? 0 : btns.length - 1;
        btns[j].focus();
      });
      function scrollListTo(id){
        var b = list.querySelector('.rp-item[data-task="' + id + '"]'); if(!b) return;
        var top = b.getBoundingClientRect().top - list.getBoundingClientRect().top + list.scrollTop, h = list.clientHeight;
        if(top < list.scrollTop || top > list.scrollTop + h - b.offsetHeight) list.scrollTop = Math.max(0, top - h / 3);
      }

      /* main: head, train, inputs, stage, scrubber, matrix */
      var head = EX.h('div', { 'class': 'rp-head' }, main);
      var trainBox = EX.h('div', { 'class': 'rp-train-box' }, main);
      var inputRow = EX.h('div', { 'class': 'rp-inputs' }, main);
      var stageTitle = EX.h('div', { 'class': 'rp-sec' }, main, 'Replay: one run at a time');
      var stage = EX.h('div', { 'class': 'rp-stage' }, main);
      var scrub = EX.h('div', { 'class': 'rp-scrub' }, main);
      var readout = EX.h('div', { 'class': 'rp-readout', 'aria-live': 'polite' }, main);
      var matHead = EX.h('div', { 'class': 'rp-mat-head' }, main);
      EX.h('div', { 'class': 'rp-sec' }, matHead, 'Every exam run, attempt 1 and attempt 2');
      var diffLab = EX.h('label', { 'class': 'check' }, matHead);
      var diffBox = EX.h('input', { type: 'checkbox' }, diffLab); diffBox.checked = st.diff;
      EX.h('span', null, diffLab, 'Outline wrong cells');
      diffBox.addEventListener('change', function(){ st.diff = diffBox.checked; renderStage(); renderMatrix(); });
      var matrix = EX.h('div', { 'class': 'rp-matrix' }, main);
      var foot = EX.h('p', { 'class': 'rp-foot' }, main);

      /* scrubber controls */
      var bPrev = EX.h('button', { type: 'button', 'class': 'btn small', 'aria-label': 'Previous run' }, scrub, '‹ Prev');
      var bPlay = EX.h('button', { type: 'button', 'class': 'btn small rp-play', 'aria-pressed': 'false', 'aria-label': 'Play through runs' }, scrub, '▶ Play');
      var bNext = EX.h('button', { type: 'button', 'class': 'btn small', 'aria-label': 'Next run' }, scrub, 'Next ›');
      var slider = EX.h('input', { type: 'range', 'class': 'slider', min: 0, max: nRuns - 1, step: 1, value: 0, 'aria-label': 'Exam run' }, scrub);
      var out = EX.h('output', { 'class': 'rp-out' }, scrub);
      bPrev.addEventListener('click', function(){ stop(); go(st.pos - 1); });
      bNext.addEventListener('click', function(){ stop(); go(st.pos + 1); });
      slider.addEventListener('input', function(){ stop(); go(+slider.value); });
      bPlay.addEventListener('click', function(){ st.playing ? stop() : play(); });

      function play(){
        if(st.pos >= nRuns - 1) go(0);
        st.playing = true; bPlay.setAttribute('aria-pressed', 'true'); bPlay.textContent = '❚❚ Pause'; bPlay.setAttribute('aria-label', 'Pause');
        timer = setInterval(function(){
          if(st.pos >= nRuns - 1){ stop(); return; }
          go(st.pos + 1);
        }, 1200);
      }
      function stop(){
        if(timer){ clearInterval(timer); timer = null; }
        st.playing = false; bPlay.setAttribute('aria-pressed', 'false'); bPlay.textContent = '▶ Play'; bPlay.setAttribute('aria-label', 'Play through runs');
      }
      function go(i){
        st.pos = Math.max(0, Math.min(nRuns - 1, i));
        renderStage(); markRows();
      }

      /* ---------- helpers for the current task ---------- */
      function T(){ return TK.tasks[st.task]; }
      function truth(){ return T().test[st.input].output; }
      function rec(run){ return (H.runs[run].results[st.task] || [])[st.input] || null; }
      function solvedInput(run){ var r = rec(run); return !!(r && (r.c[0] || r.c[1])); }

      function sizes(){
        var w = Math.max(280, main.clientWidth || ctx.width());
        return {
          train: narrow ? 52 : 68,
          stage: narrow ? Math.min(150, Math.floor((w - 30 - 12) / 2) - 2) : Math.min(190, Math.floor((w - 3 * 24) / 4)),
          thumb: narrow ? 52 : 60
        };
      }

      function renderHead(){
        var t = byId[st.task], TT = T();
        head.innerHTML = '';
        var l1 = EX.h('div', { 'class': 'rp-title' }, head);
        EX.h('span', null, l1, 'Exam task ');
        EX.h('code', { 'class': 'rp-tid' }, l1, st.task);
        var meta = EX.h('div', { 'class': 'rp-meta' }, head);
        var parts = [
          TT.train.length + ' example pair' + (TT.train.length > 1 ? 's' : ''),
          TT.test.length + ' test input' + (TT.test.length > 1 ? 's' : ''),
          'solved fully by ' + t.full + ' of ' + nRuns + ' runs' + (t.any > t.full ? ', partly by ' + (t.any - t.full) + ' more' : ''),
          'mean task score ' + F.pct(t.mean)
        ];
        meta.textContent = parts.join(' · ');
        if(st.linkNote) EX.h('span', { 'class': 'rp-link' }, meta, ' · ' + st.linkNote);
      }

      function renderTrain(){
        trainBox.innerHTML = '';
        var det = EX.h('div', { 'class': 'rp-sec' }, trainBox, 'Examples: input → output');
        var sc = EX.h('div', { 'class': 'rp-train' }, trainBox);
        var sz = sizes();
        T().train.forEach(function(p, i){
          EX.arcPair(sc, p.input, p.output, { maxSize: sz.train, maxCell: 10, labels: ['Ex ' + (i + 1) + ' · ' + shape(p.input), shape(p.output)],
            title: 'Example ' + (i + 1) });
        });
        EX.scrollHint(sc);
        void det;
      }

      function renderInputs(){
        inputRow.innerHTML = '';
        var n = T().test.length;
        if(n < 2){ inputRow.classList.add('hidden'); return; }
        inputRow.classList.remove('hidden');
        var opts = []; for(var i = 0; i < n; i++) opts.push({ value: String(i), label: 'Test input ' + (i + 1) });
        EX.seg(inputRow, opts, String(st.input), function(v){ st.input = +v; renderStage(); renderMatrix(); }, { label: 'This task has ' + n + ' test inputs' });
      }

      function attCaption(run, a, i, tr){
        var lab = 'Attempt ' + (i + 1);
        if(a.missing && !a.grid) return lab + ' · <span class="no">' + CROSS + ' no answer</span>';
        if(a.ok) return lab + (a.same ? ' (same as 1)' : '') + ' · <span class="ok">' + TICK + ' right</span>';
        var d = a.grid ? diffInfo(a.grid, tr) : null;
        return lab + (a.same ? ' (same as 1)' : '') + ' · <span class="no">' + CROSS + ' ' + (d && d.text ? EX.esc(d.text) : 'wrong') + '</span>';
      }

      function renderStage(){
        var run = runIds[st.pos], R = H.runs[run], tr = truth(), inp = T().test[st.input].input;
        var r = rec(run), at = attempts(r, R.has_preds);
        slider.value = st.pos;
        out.textContent = (st.pos + 1) + ' / ' + nRuns;
        bPrev.disabled = st.pos === 0; bNext.disabled = st.pos === nRuns - 1;
        stage.innerHTML = '';
        var sz = sizes();
        var grids = [inp, tr].concat(at.map(function(a){ return a.grid; })).filter(isGrid);
        var m = Math.max.apply(null, grids.map(function(g){ return Math.max(g.length, g[0].length); }));
        var cell = Math.max(2, Math.min(18, Math.floor((sz.stage - 1) / m)));
        var c1 = EX.h('div', { 'class': 'rp-cell' }, stage);
        EX.arcGrid(c1, inp, { cell: cell, label: 'Test input · ' + shape(inp), title: 'Test input' });
        var c2 = EX.h('div', { 'class': 'rp-cell rp-truth' }, stage);
        EX.arcGrid(c2, tr, { cell: cell, label: '<b>Truth</b> · ' + shape(tr), title: 'True output' });
        var runBox = EX.h('div', { 'class': 'rp-runbox' }, stage);
        var rl = EX.h('div', { 'class': 'rp-runlab' }, runBox);
        EX.h('span', { 'class': 'rp-runname' }, rl, EX.runLabel(run));
        EX.h('span', { 'class': 'rp-runarm' }, rl, ARM_LABEL[R.group]);
        var pair = EX.h('div', { 'class': 'rp-runpair' }, runBox);
        at.forEach(function(a, i){
          var c = EX.h('div', { 'class': 'rp-cell' + (st.pinned === run && st.att === i ? ' is-focus' : '') }, pair);
          if(!R.has_preds){
            var cap = 'Attempt ' + (i + 1) + ' · ' + (a.ok ? '<span class="ok">' + TICK + ' right</span>' : '<span class="no">' + CROSS + ' wrong</span>');
            EX.arcGrid(c, null, { label: cap, emptySize: Math.min(sz.stage, cell * m + 1), emptyText: 'grid not kept' });
          } else {
            EX.arcGrid(c, a.grid, { cell: cell, label: attCaption(run, a, i, tr), diffAgainst: showDiff(a, tr, 0.5) ? tr : null,
              emptyText: 'no answer', emptySize: Math.min(sz.stage, cell * m + 1), title: EX.runLabel(run) + ', attempt ' + (i + 1) });
          }
        });
        var verdict = (r && (r.c[0] || r.c[1])) ? 'solved this input' : 'missed this input';
        var extra = [];
        if(r && r.err) extra.push(r.err);
        if(!R.has_preds) extra.push('answer grids were not kept for this run; right/wrong flags only');
        if(r && r.calls) extra.push(F.tokens(r.tok) + ' tokens, ' + r.calls + ' model call' + (r.calls === 1 ? '' : 's'));
        else if(r && r.calls === 0 && !r.err) extra.push('no model calls were logged for this input (shown as recorded)');
        readout.textContent = EX.runLabel(run) + ' (' + ARM_LABEL[R.group] + ') ' + verdict + (extra.length ? ' · ' + extra.join(' · ') : '') + '.';
      }

      /* Outline wrong cells only while they stay readable: a size mismatch always shows (one dashed
         frame); per-cell outlines are skipped when more than `frac` of the cells are wrong, since
         the outlines would then hide the answer itself. The count stays in the caption/mark. */
      function showDiff(a, tr, frac){
        if(!st.diff || a.ok || !a.grid) return false;
        var d = diffInfo(a.grid, tr);
        if(d.kind !== 'cells') return d.kind === 'size';
        return d.n <= Math.max(6, frac * tr.length * tr[0].length);
      }

      function rowFor(run){ return matrix.querySelector('.rp-row[data-run="' + run + '"]'); }
      function markRows(){
        matrix.querySelectorAll('.rp-row[data-run]').forEach(function(rw){
          var run = rw.getAttribute('data-run');
          rw.classList.toggle('is-cur', run === runIds[st.pos]);
          rw.classList.toggle('rp-sel', run === st.pinned);
        });
        matrix.querySelectorAll('.rp-th').forEach(function(b){
          b.classList.toggle('is-focus', b.getAttribute('data-run') === st.pinned && +b.getAttribute('data-att') === st.att);
        });
      }

      function pin(run, att, emit){
        stop();
        st.pinned = run; st.att = att || 0;
        st.pos = Math.max(0, runIds.indexOf(run));
        renderStage(); markRows();
        if(emit){
          EX.hash.set('replay', { task: st.task, run: run });
          EX.select('run', { run: run, source: 'replay' });
        }
      }

      function renderMatrix(){
        matrix.innerHTML = '';
        var tr = truth(), sz = sizes();
        ARM_ORDER.forEach(function(g){
          var runs = runIds.filter(function(r){ return H.runs[r].group === g; });
          if(!runs.length) return;
          var box = EX.h('div', { 'class': 'rp-grp' + (g === 'xhigh' ? ' rp-ref' : '') }, matrix);
          var gh = EX.h('div', { 'class': 'rp-grp-head' }, box);
          EX.h('span', { 'class': 'rp-grp-name' }, gh, ARM_LABEL[g]);
          var k = runs.filter(solvedInput).length;
          EX.h('span', { 'class': 'rp-grp-n' }, gh, k + ' / ' + runs.length + ' solved');
          var ch = EX.h('div', { 'class': 'rp-row rp-colhead', 'aria-hidden': 'true' }, box);
          EX.h('span', null, ch, 'run'); EX.h('span', null, ch, 'attempt 1'); EX.h('span', null, ch, 'attempt 2');
          runs.forEach(function(run){
            var R = H.runs[run], r = rec(run), at = attempts(r, R.has_preds);
            var row = EX.h('div', { 'class': 'rp-row', 'data-run': run }, box);
            var lb = EX.h('button', { type: 'button', 'class': 'rp-rowlab', 'aria-label': 'Show ' + EX.runLabel(run) + ' in the replay' }, row);
            EX.h('span', { 'class': 'rp-rn' }, lb, EX.runLabel(run, { short: true }));
            EX.h('span', { 'class': 'rp-rs ' + (solvedInput(run) ? 'ok' : 'no') }, lb, solvedInput(run) ? 'solved' : 'missed');
            lb.addEventListener('click', function(){ pin(run, 0, true); });
            if(!R.has_preds){
              var fl = EX.h('div', { 'class': 'rp-flags' }, row);
              at.forEach(function(a, i){
                EX.h('span', { 'class': 'rp-flag ' + (a.ok ? 'ok' : 'no') }, fl, (i + 1) + ' ' + (a.ok ? TICK : CROSS));
              });
              EX.h('span', { 'class': 'rp-nogrid' }, fl, 'grids not kept');
              return;
            }
            at.forEach(function(a, i){
              var d = a.grid ? diffInfo(a.grid, tr) : { kind: 'none' };
              var desc = a.ok ? 'right' : (a.grid ? (d.text || 'wrong') : 'no answer');
              var b = EX.h('button', { type: 'button', 'class': 'rp-th', 'data-run': run, 'data-att': i,
                'aria-label': EX.runLabel(run) + ', attempt ' + (i + 1) + ': ' + desc + '. Enlarge beside the truth.' }, row);
              EX.arcGrid(b, a.grid, { maxSize: sz.thumb, maxCell: 8, gap: a.grid && Math.max(a.grid.length, a.grid[0].length) > 16 ? 0 : 1,
                diffAgainst: showDiff(a, tr, 0.2) ? tr : null, emptyText: '—', emptySize: Math.round(sz.thumb * 0.6) });
              var mk = EX.h('span', { 'class': 'rp-mk ' + (a.ok ? 'ok' : 'no') }, b);
              mk.textContent = a.ok ? TICK : (a.same ? CROSS + ' =1' : (d.kind === 'cells' ? CROSS + ' ' + d.n : d.kind === 'size' ? CROSS + ' size' : CROSS));
              b.addEventListener('click', function(){ pin(run, i, true); });
            });
          });
        });
        var bits = [];
        if(noPredRuns.length) bits.push('Answer grids were not kept for ' + noPredRuns.length + ' extension runs (' + noPredRuns.map(function(r){ return EX.runLabel(r, { short: true }); }).join(', ') + ') to keep the page small; they show right/wrong only.');
        bits.push('Mark under a thumbnail: ' + TICK + ' right, ' + CROSS + ' n = n cells off, ' + CROSS + ' size = wrong grid size, =1 = attempt 2 repeated attempt 1.');
        bits.push('xhigh is a reference run, not a compared arm.');
        foot.textContent = bits.join(' ');
        markRows();
      }

      function defaultPos(){
        var tr = truth();
        for(var i = 0; i < nRuns; i++){
          var run = runIds[i]; if(!H.runs[run].has_preds || solvedInput(run)) continue;
          var a = attempts(rec(run), true);
          if(a.some(function(x){ var d = diffInfo(x.grid, tr); return d.kind === 'cells'; })) return i;
        }
        return 0;
      }

      function setTask(id, user, note){
        if(!byId[id]) return;
        stop();
        st.task = id; st.input = 0; st.pinned = null; st.att = 0;
        st.linkNote = note || '';
        st.pos = defaultPos();
        list.querySelectorAll('.rp-item').forEach(function(b){ b.setAttribute('aria-pressed', String(b.getAttribute('data-task') === id)); });
        renderAll();
        scrollListTo(id);
        if(user){
          EX.hash.set('replay', { task: id });
          EX.select('task', { task: id, set: 'heldout', source: 'replay' });
        }
      }

      function renderAll(){
        renderHead(); renderTrain(); renderInputs(); renderStage(); renderMatrix();
      }

      /* ---------- init ---------- */
      renderList();
      st.pos = defaultPos();
      if(fromHash.run && runIds.indexOf(fromHash.run) >= 0){ st.pinned = fromHash.run; st.pos = runIds.indexOf(fromHash.run); }
      renderAll();
      scrollListTo(st.task);

      /* ---------- linking ---------- */
      var FIGNO = { puzzle: 'Fig 2', results: 'Fig 4', tree: 'Fig 5', extension: 'Fig 6', transcripts: 'Fig 7' };
      EX.on('select-task', function(p){
        if(!p || p.source === 'replay' || p.set !== 'heldout' || !byId[p.task] || p.task === st.task) return;
        setTask(p.task, false, FIGNO[p.source] ? 'linked from ' + FIGNO[p.source] : '');
      });
      EX.on('select-run', function(p){
        if(!p || p.source === 'replay' || runIds.indexOf(p.run) < 0) return;
        pin(p.run, 0, false);
      });
      EX.on('hash', function(h){
        if(!h || h.section !== 'replay') return;
        if(h.params.task && byId[h.params.task] && h.params.task !== st.task) setTask(h.params.task, false);
        if(h.params.run && runIds.indexOf(h.params.run) >= 0 && h.params.run !== st.pinned) pin(h.params.run, 0, false);
      });
      document.addEventListener('visibilitychange', function(){ if(document.hidden) stop(); });

      ctx.onResize(function(w){
        var n = w < 760;
        if(n !== narrow){ narrow = n; root.classList.toggle('narrow', n); }
        renderTrain(); renderStage(); renderMatrix();
      });
    });
  });
})();
