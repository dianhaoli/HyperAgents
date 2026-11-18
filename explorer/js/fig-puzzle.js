/* fig-puzzle.js — Figure 2, "Try one": an exam (held-out) ARC-AGI-2 task you can solve yourself.
   Shows the train pairs and the test input, a paint editor (palette, paint/fill, resize, copy input,
   clear), two checks like the player's pass@2, then the truth with wrong cells outlined and how the
   23 exam runs did on the same test input (with any run's two attempts).
   Data: tasks.json at init; heldout.json lazily (prefetched when the figure nears the viewport, or on Check).
   Emits: select-task {task, set:'heldout', source:'puzzle'} on shuffle / task pick and from the Fig 3 link.
   Listens: nothing. Hash: #puzzle?task=ID (read once at init, written on a user pick).
   Styles: assets/fig-puzzle.css. */
(function(){
  'use strict';

  var NAMES = ['black', 'blue', 'red', 'green', 'yellow', 'grey', 'magenta', 'orange', 'sky blue', 'maroon'];
  var MAX_DIM = 20;          // pool: exam tasks whose every grid fits in 20 x 20 (painting stays practical)
  var EASY = 0.7, HARD = 0.3; // difficulty bands on heldout_mean_solve
  var DIFF = [
    { value: 'all', label: 'All' },
    { value: 'easy', label: 'Easy' },
    { value: 'medium', label: 'Medium' },
    { value: 'hard', label: 'Hard' }
  ];

  function band(s){ return s >= EASY ? 'easy' : s >= HARD ? 'medium' : 'hard'; }
  function copyGrid(g){ return g.map(function(r){ return r.slice(); }); }
  function blank(h, w){ var g = []; for(var r = 0; r < h; r++){ g.push([]); for(var c = 0; c < w; c++) g[r].push(0); } return g; }
  function dims(g){ return g.length + '×' + g[0].length; }
  function clamp(x, a, b){ return Math.max(a, Math.min(b, x)); }

  EX.mount('puzzle', function(node, ctx){
    return EX.load('tasks').then(function(TK){
      node.innerHTML = '';
      var F = EX.fmt;

      /* ---------- pool ---------- */
      var pool = TK.heldout.map(function(id){
        var t = TK.tasks[id], m = 0;
        t.train.concat(t.test).forEach(function(p){
          [p.input, p.output].forEach(function(g){ if(g) m = Math.max(m, g.length, g[0].length); });
        });
        return { id: id, t: t, maxDim: m, solve: t.heldout_mean_solve, band: band(t.heldout_mean_solve) };
      }).filter(function(x){ return x.maxDim <= MAX_DIM && x.t.test.length && x.t.test.every(function(p){ return p.output; }); });
      var byId = {}; pool.forEach(function(x){ byId[x.id] = x; });
      var counts = { all: pool.length, easy: 0, medium: 0, hard: 0 };
      pool.forEach(function(x){ counts[x.band]++; });

      // default: a medium task with the smallest grids; ties -> closest to a 50 % solve rate
      function pickDefault(list){
        return list.slice().sort(function(a, b){
          return ((a.t.test.length > 1) - (b.t.test.length > 1)) || (a.maxDim - b.maxDim) || (Math.abs(a.solve - 0.5) - Math.abs(b.solve - 0.5)) || (a.id < b.id ? -1 : 1);
        })[0];
      }
      var hashTask = (EX.hash.get().section === 'puzzle') ? EX.hash.param('task') : null;
      var cur = (hashTask && byId[hashTask]) || pickDefault(pool.filter(function(x){ return x.band === 'medium'; })) || pickDefault(pool);
      var filter = 'all';

      /* ---------- state ---------- */
      var S = { ti: 0, out: null, color: 1, tool: 'paint', tries: [], done: false, run: null, cr: 0, cc: 0 };

      /* ---------- skeleton ---------- */
      var root = EX.h('div', { 'class': 'fx-puzzle' }, node);
      var top = EX.h('div', { 'class': 'pz-top' }, root);
      var diffSeg = EX.seg(top, DIFF.map(function(d){ return { value: d.value, label: d.label + ' · ' + counts[d.value] }; }), filter,
        function(v){ filter = v; if(!inFilter(cur)) shuffle(); updShuffle(); }, { label: 'Difficulty' });
      var shuffleBtn = EX.h('button', { type: 'button', 'class': 'btn' }, top, 'Another task ↻');
      shuffleBtn.addEventListener('click', function(){ shuffle(); });
      var def = EX.h('p', { 'class': 'pz-def' }, root);
      var meta = EX.h('p', { 'class': 'pz-meta' }, root);
      var trainSec = EX.h('div', null, root);
      var work = EX.h('div', { 'class': 'pz-work' }, root);
      var colIn = EX.h('div', { 'class': 'pz-col' }, work);
      var colOut = EX.h('div', { 'class': 'pz-col' }, work);
      var reveal = EX.h('div', { 'class': 'pz-reveal', hidden: true }, root);

      // output column: editor + controls (built once; editor svg rebuilt on size change)
      EX.h('div', { 'class': 'pz-sec' }, colOut, 'Your answer');
      var edHost = EX.h('div', null, colOut);
      var cellInfo = EX.h('div', { 'class': 'pz-cellinfo', 'aria-live': 'polite' }, colOut);
      var pal = EX.h('div', { 'class': 'pz-pal', role: 'radiogroup', 'aria-label': 'Paint colour' }, colOut);
      var chips = NAMES.map(function(nm, i){
        var b = EX.h('button', { type: 'button', 'class': 'pz-chip', role: 'radio', 'aria-checked': String(i === S.color),
          tabindex: i === S.color ? '0' : '-1', 'aria-label': 'Colour ' + i + ', ' + nm, title: i + ' · ' + nm }, pal);
        EX.h('span', { 'class': 'sw', style: { background: EX.ARC[i] } }, b);
        EX.h('span', { 'class': 'd', 'aria-hidden': 'true' }, b, String(i));
        b.addEventListener('click', function(){ setColor(i, false); });
        b.addEventListener('keydown', function(e){
          var k = e.key, n = null;
          if(k === 'ArrowRight' || k === 'ArrowDown') n = (i + 1) % 10;
          else if(k === 'ArrowLeft' || k === 'ArrowUp') n = (i + 9) % 10;
          else if(k === 'Home') n = 0; else if(k === 'End') n = 9;
          if(n != null){ e.preventDefault(); setColor(n, true); }
        });
        return b;
      });
      var tools = EX.h('div', { 'class': 'pz-tools' }, colOut);
      var toolSeg = EX.seg(tools, [{ value: 'paint', label: 'Paint' }, { value: 'fill', label: 'Fill area' }], S.tool,
        function(v){ S.tool = v; }, { ariaLabel: 'Tool' });
      var sizeBox = EX.h('span', { 'class': 'pz-size' }, tools);
      EX.h('span', { 'class': 'control-label' }, sizeBox, 'Size');
      var inR = EX.h('input', { type: 'number', min: 1, max: 30, step: 1, inputmode: 'numeric', 'aria-label': 'Rows' }, sizeBox);
      EX.h('span', { 'class': 'x', 'aria-hidden': 'true' }, sizeBox, '×');
      var inC = EX.h('input', { type: 'number', min: 1, max: 30, step: 1, inputmode: 'numeric', 'aria-label': 'Columns' }, sizeBox);
      [inR, inC].forEach(function(inp){ inp.addEventListener('change', function(){ resize(+inR.value, +inC.value); }); });
      var tools2 = EX.h('div', { 'class': 'pz-tools' }, colOut);
      var copyBtn = EX.h('button', { type: 'button', 'class': 'btn small' }, tools2, 'Copy input');
      var clearBtn = EX.h('button', { type: 'button', 'class': 'btn small' }, tools2, 'Clear');
      copyBtn.addEventListener('click', function(){ if(S.done) return; S.out = copyGrid(testPair().input); drawEditor(); say('Copied the test input (' + dims(S.out) + ').'); });
      clearBtn.addEventListener('click', function(){ if(S.done) return; S.out = blank(S.out.length, S.out[0].length); drawEditor(); say('Cleared to black (' + dims(S.out) + ').'); });
      var actions = EX.h('div', { 'class': 'pz-actions' }, colOut);
      var checkBtn = EX.h('button', { type: 'button', 'class': 'btn primary' }, actions, 'Check');
      var triesEl = EX.h('span', { 'class': 'pz-tries' }, actions);
      var giveBtn = EX.h('button', { type: 'button', 'class': 'btn quiet' }, actions, 'Show the answer');
      var againBtn = EX.h('button', { type: 'button', 'class': 'btn', hidden: true }, actions, 'Start over');
      var feedback = EX.h('p', { 'class': 'pz-feedback', role: 'status', 'aria-live': 'polite' }, colOut);
      checkBtn.addEventListener('click', check);
      giveBtn.addEventListener('click', function(){ finish(false, true); });
      againBtn.addEventListener('click', function(){ loadTest(S.ti); edSvg && edSvg.focus(); });

      def.textContent = 'Showing the ' + pool.length + ' of ' + TK.heldout.length + ' exam tasks whose grids are all at most ' + MAX_DIM + '×' + MAX_DIM +
        '. Difficulty is the average exam-run score on the task: easy ≥ ' + F.pct(EASY, 0) + ', medium ' + F.pct(HARD, 0) + '–' + F.pct(EASY, 0) + ', hard < ' + F.pct(HARD, 0) + '.';

      /* ---------- heldout (lazy) ---------- */
      var HO = null, hoP = null;
      function loadHeldout(){
        if(!hoP) hoP = EX.load('heldout').then(function(d){ HO = d; return d; });
        return hoP;
      }
      if('IntersectionObserver' in window){
        var io = new IntersectionObserver(function(ents){
          if(ents.some(function(e){ return e.isIntersecting; })){ io.disconnect(); loadHeldout().catch(function(){}); }
        }, { rootMargin: '300px 0px' });
        io.observe(work);
      }

      /* ---------- helpers ---------- */
      function inFilter(x){ return filter === 'all' || x.band === filter; }
      function testPair(){ return cur.t.test[S.ti]; }
      function say(t){ cellInfo.textContent = t; }
      function updShuffle(){
        var n = pool.filter(inFilter).length;
        shuffleBtn.disabled = n < 2 && inFilter(cur);
      }
      function setColor(i, focus){
        S.color = i;
        chips.forEach(function(b, j){ b.setAttribute('aria-checked', String(j === i)); b.tabIndex = j === i ? 0 : -1; });
        if(focus) chips[i].focus();
      }
      function shuffle(){
        var list = pool.filter(function(x){ return inFilter(x) && x !== cur; });
        if(!list.length) list = pool.filter(inFilter);
        if(!list.length) return;
        setTask(list[Math.floor(Math.random() * list.length)], true);
      }

      /* ---------- task ---------- */
      function setTask(x, user){
        cur = x;
        if(user){
          EX.hash.set('puzzle', { task: x.id });
          EX.select('task', { task: x.id, set: 'heldout', source: 'puzzle' });
        }
        drawTask();
        loadTest(0);
        updShuffle();
      }
      function trainMax(){
        var w = ctx.width() || 900;
        return w < 520 ? clamp(Math.floor((w - 30) / 2), 90, 170) : 150;
      }
      function drawTask(){
        var t = cur.t;
        meta.innerHTML = '';
        EX.h('span', null, meta, 'Exam task ');
        EX.h('span', { 'class': 'm' }, meta, cur.id);
        EX.h('span', { 'class': 'sep', 'aria-hidden': 'true' }, meta, '·');
        EX.h('span', null, meta, t.train.length + ' example pairs');
        EX.h('span', { 'class': 'sep', 'aria-hidden': 'true' }, meta, '·');
        EX.h('span', null, meta, t.test.length === 1 ? '1 test input' : t.test.length + ' test inputs');
        EX.h('span', { 'class': 'sep', 'aria-hidden': 'true' }, meta, '·');
        EX.h('span', null, meta, cur.band.charAt(0).toUpperCase() + cur.band.slice(1));
        EX.h('span', { 'class': 'note' }, meta, ' (average run score ' + F.pct(cur.solve) + ')');
        trainSec.innerHTML = '';
        EX.h('div', { 'class': 'pz-sec' }, trainSec, 'Examples: input → output');
        var row = EX.h('div', { 'class': 'pz-train' }, trainSec);
        var ms = trainMax();
        t.train.forEach(function(p, i){
          EX.arcPair(row, p.input, p.output, { maxSize: ms, maxCell: 16, labels: ['Example ' + (i + 1) + ' · ' + dims(p.input), dims(p.output)],
            title: 'Example ' + (i + 1) });
        });
      }
      function drawInput(){
        colIn.innerHTML = '';
        var t = cur.t;
        EX.h('div', { 'class': 'pz-sec' }, colIn, 'Test input');
        if(t.test.length > 1){
          var box = EX.h('div', { 'class': 'pz-tests' }, colIn);
          EX.seg(box, t.test.map(function(_, i){ return { value: i, label: String(i + 1) }; }), S.ti,
            function(v){ loadTest(+v); }, { label: 'Input', mono: true });
        }
        var p = testPair();
        EX.arcGrid(colIn, p.input, { maxSize: inputMax(), maxCell: 24, label: dims(p.input), title: 'Test input, ' + dims(p.input) });
      }
      function inputMax(){
        var w = ctx.width() || 900;
        return root.classList.contains('narrow') ? clamp(w, 160, 340) : clamp(Math.floor((w - 40) * 0.42), 180, 300);
      }

      function loadTest(i){
        S.ti = i; S.tries = []; S.done = false; S.run = null; S.cr = 0; S.cc = 0;
        var p = testPair();
        S.out = blank(p.input.length, p.input[0].length);
        drawInput();
        drawEditor();
        reveal.hidden = true; reveal.innerHTML = '';
        feedback.innerHTML = '';
        say('Grid starts as the test input’s size, all black. Change the size if the output should differ.');
        updActions();
      }

      /* ---------- editor ---------- */
      var edSvg = null, edCells = null, edCur = null, edCell = 20, painting = false, lastRC = null;
      function editorMax(){
        var w = ctx.width() || 900;
        return root.classList.contains('narrow') ? clamp(w, 160, 380) : clamp(Math.floor((w - 40) * 0.5), 200, 380);
      }
      function drawEditor(){
        var g = S.out, h = g.length, w = g[0].length;
        inR.value = h; inC.value = w;
        edCell = clamp(Math.floor((editorMax() - 1) / Math.max(h, w)), 8, 32);
        var W = w * edCell + 1, H = h * edCell + 1;
        edHost.innerHTML = '';
        edSvg = EX.s('svg', { 'class': 'pz-editor' + (S.done ? ' locked' : ''), width: W, height: H, viewBox: '0 0 ' + W + ' ' + H,
          tabindex: 0, role: 'application', 'aria-roledescription': 'paint grid',
          'aria-label': 'Your answer, ' + h + ' by ' + w + '. Arrow keys move, Space or Enter paints, digits 0 to 9 pick a colour, F fills an area.' }, edHost);
        EX.s('rect', { 'class': 'bg', x: 0, y: 0, width: W, height: H }, edSvg);
        edCells = [];
        for(var r = 0; r < h; r++){
          edCells.push([]);
          for(var c = 0; c < w; c++){
            edCells[r].push(EX.s('rect', { x: c * edCell + 1, y: r * edCell + 1, width: edCell - 1, height: edCell - 1, fill: EX.ARC[g[r][c]] }, edSvg));
          }
        }
        S.cr = clamp(S.cr, 0, h - 1); S.cc = clamp(S.cc, 0, w - 1);
        edCur = EX.s('rect', { 'class': 'cur', width: edCell - 1, height: edCell - 1 }, edSvg);
        moveCursor(S.cr, S.cc, false);
        edSvg.addEventListener('pointerdown', onDown);
        edSvg.addEventListener('pointermove', onMove);
        edSvg.addEventListener('pointerup', onUp);
        edSvg.addEventListener('pointercancel', onUp);
        edSvg.addEventListener('lostpointercapture', onUp);
        edSvg.addEventListener('keydown', onKey);
      }
      function rcAt(e){
        var b = edSvg.getBoundingClientRect(), sx = (S.out[0].length * edCell + 1) / b.width;
        var c = Math.floor(((e.clientX - b.left) * sx - 1) / edCell), r = Math.floor(((e.clientY - b.top) * sx - 1) / edCell);
        if(r < 0 || c < 0 || r >= S.out.length || c >= S.out[0].length) return null;
        return [r, c];
      }
      function paint(r, c, v){
        if(S.out[r][c] === v) return;
        S.out[r][c] = v; edCells[r][c].setAttribute('fill', EX.ARC[v]);
      }
      function flood(r, c, v){
        var g = S.out, from = g[r][c]; if(from === v) return 0;
        var st = [[r, c]], n = 0;
        while(st.length){
          var p = st.pop(), y = p[0], x = p[1];
          if(y < 0 || x < 0 || y >= g.length || x >= g[0].length || g[y][x] !== from) continue;
          paint(y, x, v); n++;
          st.push([y + 1, x], [y - 1, x], [y, x + 1], [y, x - 1]);
        }
        return n;
      }
      function apply(r, c, first){
        if(S.done) return;
        if(S.tool === 'fill'){ if(first){ var n = flood(r, c, S.color); say('Filled ' + n + ' cell' + (n === 1 ? '' : 's') + ' with ' + NAMES[S.color] + '.'); } }
        else { paint(r, c, S.color); }
        moveCursor(r, c, false);
      }
      function onDown(e){
        if(S.done || (e.button != null && e.button !== 0)) return;
        var rc = rcAt(e); if(!rc) return;
        e.preventDefault();
        painting = S.tool === 'paint';
        try { edSvg.setPointerCapture(e.pointerId); } catch(err){}
        lastRC = rc; apply(rc[0], rc[1], true);
      }
      function onMove(e){
        if(!painting) return;
        var rc = rcAt(e); if(!rc) return;
        if(lastRC && lastRC[0] === rc[0] && lastRC[1] === rc[1]) return;
        lastRC = rc; apply(rc[0], rc[1], false);
      }
      function onUp(){ painting = false; lastRC = null; }
      function moveCursor(r, c, announce){
        S.cr = r; S.cc = c;
        edCur.setAttribute('x', c * edCell + 1); edCur.setAttribute('y', r * edCell + 1);
        if(announce) say('Row ' + (r + 1) + ', column ' + (c + 1) + ': ' + NAMES[S.out[r][c]] + '.');
      }
      function onKey(e){
        var k = e.key, h = S.out.length, w = S.out[0].length, r = S.cr, c = S.cc;
        if(k === 'ArrowUp'){ r = Math.max(0, r - 1); }
        else if(k === 'ArrowDown'){ r = Math.min(h - 1, r + 1); }
        else if(k === 'ArrowLeft'){ c = Math.max(0, c - 1); }
        else if(k === 'ArrowRight'){ c = Math.min(w - 1, c + 1); }
        else if(k === 'Home'){ c = 0; } else if(k === 'End'){ c = w - 1; }
        else if(/^[0-9]$/.test(k)){ e.preventDefault(); setColor(+k, false); say('Colour ' + k + ', ' + NAMES[+k] + '.'); return; }
        else if(k === ' ' || k === 'Enter'){
          e.preventDefault(); if(S.done) return;
          paint(r, c, S.color); say('Painted row ' + (r + 1) + ', column ' + (c + 1) + ' ' + NAMES[S.color] + '.'); return;
        }
        else if(k === 'f' || k === 'F'){ e.preventDefault(); if(S.done) return; var n = flood(r, c, S.color); say('Filled ' + n + ' cell' + (n === 1 ? '' : 's') + ' with ' + NAMES[S.color] + '.'); return; }
        else return;
        e.preventDefault();
        if(e.shiftKey && !S.done) paint(r, c, S.color);   // Shift+arrow paints a stroke
        moveCursor(r, c, true);
      }
      function resize(h, w){
        if(S.done) return;
        h = clamp(Math.round(h) || 1, 1, 30); w = clamp(Math.round(w) || 1, 1, 30);
        var g = blank(h, w);
        for(var r = 0; r < Math.min(h, S.out.length); r++) for(var c = 0; c < Math.min(w, S.out[0].length); c++) g[r][c] = S.out[r][c];
        S.out = g; drawEditor(); say('Resized to ' + dims(g) + '.');
      }

      /* ---------- checking ---------- */
      function updActions(){
        var left = 2 - S.tries.length;
        checkBtn.disabled = S.done; giveBtn.hidden = S.done; againBtn.hidden = !S.done;
        checkBtn.textContent = (S.tries.length && !S.done) ? 'Check try 2' : 'Check';
        triesEl.textContent = S.done ? '' : (left === 2 ? '2 tries' : '1 try left');
        [copyBtn, clearBtn, inR, inC].forEach(function(b){ b.disabled = S.done; });
        if(edSvg) edSvg.classList.toggle('locked', S.done);
      }
      function check(){
        if(S.done) return;
        var truth = testPair().output, g = copyGrid(S.out);
        S.tries.push(g);
        if(EX.gridsEqual(g, truth)) return finish(true, false);
        if(S.tries.length >= 2) return finish(false, false);
        feedback.innerHTML = '<b class="no">Not exact.</b> One try left. Like the player, you get no hint about which cells are off.';
        updActions();
      }
      function finish(ok, gaveUp){
        S.done = true; updActions();
        var n = S.tries.length;
        feedback.innerHTML = ok ? '<b class="ok">Exactly right</b> on try ' + n + '. That counts as solved under pass@2.'
          : gaveUp ? (n ? '<b>Answer shown</b> after ' + n + ' try.' : '<b>Answer shown.</b>')
          : '<b class="no">Both tries missed.</b> Under pass@2 this input is not solved.';
        drawReveal();
      }

      /* ---------- reveal ---------- */
      function cmpMax(){ var w = ctx.width() || 900; return w < 520 ? clamp(Math.floor((w - 16) / 2), 120, 200) : 190; }
      function drawReveal(){
        reveal.hidden = false; reveal.innerHTML = '';
        var truth = testPair().output, ms = cmpMax();
        EX.h('div', { 'class': 'pz-sec' }, reveal, 'The truth' + (S.tries.length ? ' and your tries' : ''));
        var row = EX.h('div', { 'class': 'pz-cmp' }, reveal);
        S.tries.forEach(function(g, i){
          var ok = EX.gridsEqual(g, truth), sameSize = g.length === truth.length && g[0].length === truth[0].length;
          var svg = EX.arcGrid(row, g, { maxSize: ms, maxCell: 20, diffAgainst: truth, title: 'Your try ' + (i + 1),
            label: 'Your try ' + (i + 1) + ' ' + (ok ? '<span class="ok">✓ right</span>' : '<span class="no">✗ ' +
              (sameSize ? '' : 'wrong size') + '</span>') });
          if(!ok && sameSize && svg.__arc){ svg.parentNode.querySelector('.arc-cap .no').textContent = '✗ ' + svg.__arc.wrong + ' cell' + (svg.__arc.wrong === 1 ? '' : 's') + ' off'; }
        });
        EX.arcGrid(row, truth, { maxSize: ms, maxCell: 20, title: 'Truth, ' + dims(truth), label: '<b>Truth</b> · ' + dims(truth) });
        if(S.tries.some(function(g){ return !EX.gridsEqual(g, truth); })){
          var lg = EX.h('p', { 'class': 'pz-legend' }, reveal);
          EX.h('span', { 'class': 'box', 'aria-hidden': 'true' }, lg);
          lg.appendChild(document.createTextNode('Outlined cells differ from the truth. A dashed outline round the whole grid means the size is wrong.'));
        }
        EX.h('div', { 'class': 'pz-sec' }, reveal, 'How the exam runs did on this input');
        var runsBox = EX.h('div', { 'class': 'pz-runs' }, reveal);
        if(HO) drawRuns(runsBox);
        else {
          EX.h('div', { 'class': 'pz-loading', role: 'status' }, runsBox, 'Loading the exam runs’ answers…');
          var taskAt = cur.id, tiAt = S.ti;
          loadHeldout().then(function(){ if(cur.id === taskAt && S.ti === tiAt && S.done){ runsBox.innerHTML = ''; drawRuns(runsBox); } })
            .catch(function(err){ runsBox.innerHTML = ''; EX.h('div', { 'class': 'empty' }, runsBox, 'The exam runs’ answers could not be loaded (' + (err && err.message || err) + ').'); });
        }
        var a = EX.h('a', { 'class': 'pz-link', href: '#replay?task=' + encodeURIComponent(cur.id) }, reveal,
          'See every run’s two attempts on this task in Figure 3 →');
        a.addEventListener('click', function(e){
          e.preventDefault();
          EX.select('task', { task: cur.id, set: 'heldout', source: 'puzzle' });
          EX.hash.set('replay', { task: cur.id }, { scroll: true });
        });
      }

      function recOf(run){
        var R = HO.runs[run]; if(!R || !R.results) return null;
        var arr = R.results[cur.id]; return arr ? arr[S.ti] || null : null;
      }
      function solvedRec(rec){ return !!(rec && rec.c && rec.c.some(function(v){ return !!v; })); }

      function drawRuns(box){
        var runs = Object.keys(HO.runs).sort(function(a, b){
          return EX.GROUP_ORDER.indexOf(EX.runGroup(a)) - EX.GROUP_ORDER.indexOf(EX.runGroup(b));
        });
        var solved = runs.filter(function(r){ return solvedRec(recOf(r)); });
        var total = EX.h('p', { 'class': 'pz-total' }, box);
        total.innerHTML = '<b>' + solved.length + ' of ' + runs.length + '</b> exam runs solved this test input' +
          (cur.t.test.length > 1 ? ' (input ' + (S.ti + 1) + ' of ' + cur.t.test.length + ')' : '') + '.';
        if(!S.run || runs.indexOf(S.run) < 0){
          // default: the plain player (B0 rep 0) if it has answer grids, else the first run with grids
          S.run = runs.filter(function(r){ return /^B0/.test(r) && HO.runs[r].has_preds; })[0] ||
            runs.filter(function(r){ return HO.runs[r].has_preds; })[0] || runs[0];
        }
        var marks = [];
        EX.GROUP_ORDER.forEach(function(gk){
          var rs = runs.filter(function(r){ return EX.runGroup(r) === gk; });
          if(!rs.length) return;
          var k = rs.filter(function(r){ return solvedRec(recOf(r)); }).length;
          var row = EX.h('div', { 'class': 'pz-grp' }, box);
          EX.h('span', { 'class': 'g' }, row, EX.GROUP_LABEL[gk] || gk);
          EX.h('span', { 'class': 'k' }, row, k + ' / ' + rs.length);
          var mk = EX.h('span', { 'class': 'pz-marks' }, row);
          rs.forEach(function(r){
            var rec = recOf(r), ok = solvedRec(rec);
            var lab = EX.runLabel(r, { short: true });
            var b = EX.h('button', { type: 'button', 'class': 'pz-mk ' + (!rec ? 'na' : ok ? 'ok' : 'no'), 'data-run': r,
              'aria-pressed': String(r === S.run), title: EX.runLabel(r) + (!rec ? ': no record' : ok ? ': solved' : ': missed'),
              'aria-label': EX.runLabel(r) + (!rec ? ', no record' : ok ? ', solved' : ', missed') + '. Show its answers.' }, mk, !rec ? '–' : ok ? '✓' : '✗');
            b.addEventListener('click', function(){ S.run = r; marks.forEach(function(m){ m.setAttribute('aria-pressed', String(m.getAttribute('data-run') === r)); }); sel.value = r; drawRunAnswers(ansBox); });
            marks.push(b);
          });
        });
        var pick = EX.h('div', { 'class': 'pz-pick' }, box);
        var sel = EX.selectBox(pick, EX.GROUP_ORDER.map(function(gk){
          return { group: EX.GROUP_LABEL[gk] || gk, options: runs.filter(function(r){ return EX.runGroup(r) === gk; }).map(function(r){
            var rec = recOf(r); return { value: r, label: EX.runLabel(r) + (!rec ? ' · no record' : solvedRec(rec) ? ' · ✓' : ' · ✗') };
          }) };
        }).filter(function(g){ return g.options.length; }), S.run, function(v){
          S.run = v; marks.forEach(function(m){ m.setAttribute('aria-pressed', String(m.getAttribute('data-run') === v)); }); drawRunAnswers(ansBox);
        }, { label: 'Answers from' });
        var ansBox = EX.h('div', null, box);
        drawRunAnswers(ansBox);
      }

      function drawRunAnswers(box){
        box.innerHTML = '';
        var r = S.run, R = HO.runs[r], rec = recOf(r), truth = testPair().output, ms = cmpMax();
        var cap = EX.h('p', { 'class': 'pz-runcap' }, box);
        if(!rec){ cap.textContent = EX.runLabel(r) + ' has no record for this input.'; return; }
        var calls = rec.calls != null ? rec.calls + ' model call' + (rec.calls === 1 ? '' : 's') : null;
        var bits = [EX.runLabel(r) + ' (' + (EX.GROUP_LABEL[EX.runGroup(r)] || '') + ')', solvedRec(rec) ? 'solved' : 'missed'];
        if(calls) bits.push(calls);
        if(rec.tok != null) bits.push(F.tokens(rec.tok) + ' tokens');
        if(rec.timeout) bits.push('timed out');
        if(rec.err) bits.push('error');
        cap.textContent = bits.join(' · ') + '.';
        if(!R.has_preds || !rec.p){
          EX.h('div', { 'class': 'notice' }, box, 'Only the right/wrong flags were kept for this run, not its answer grids, to keep the page under its size budget.');
          return;
        }
        var row = EX.h('div', { 'class': 'pz-cmp' }, box);
        var c = rec.c || [];
        [0, 1].forEach(function(i){
          var g = rec.p[i];
          if(g === '=1') g = rec.p[0];
          var ok = !!c[i];
          var lab = 'Attempt ' + (i + 1) + (rec.p[i] === '=1' ? ' (same as 1)' : '') + ' ' + (ok ? '<span class="ok">✓</span>' : '<span class="no">✗</span>');
          if(Array.isArray(g) && g.length && Array.isArray(g[0])){
            EX.arcGrid(row, g, { maxSize: ms, maxCell: 20, diffAgainst: truth, label: lab, title: EX.runLabel(r) + ' attempt ' + (i + 1) });
          } else {
            EX.arcGrid(row, null, { label: lab, emptySize: Math.min(ms, 96), emptyText: i >= (rec.n || 0) ? 'no answer returned' : 'no grid' });
          }
        });
        EX.arcGrid(row, truth, { maxSize: ms, maxCell: 20, label: '<b>Truth</b>', title: 'Truth' });
      }

      /* ---------- layout ---------- */
      function layout(w){
        root.classList.toggle('narrow', w < 640);
      }
      layout(ctx.width());
      drawTask(); loadTest(0); updShuffle();
      ctx.onResize(function(w){
        layout(w);
        drawTask(); drawInput(); drawEditor();
        if(S.done) drawReveal();
      });
    });
  });
})();
