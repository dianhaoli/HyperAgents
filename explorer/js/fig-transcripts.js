/* fig-transcripts.js — Figure 7, transcript reader.
   Tabs: Player | Coach.
   Player: filterable list of the 60 saved (failed) player transcripts plus the 30 answer-only solved replays;
           a step-through replay of the turns (play/pause, speed, typewriter for model output, instant "show all");
           the puzzle from tasks.json beside it with the final answers diffed against the truth.
           "Evolution series" view: one task across the saved generations of a run, failed -> solved.
   Coach:  the 12 saved coach transcripts, with the node's record, practice score parent -> child and its diff (trees.json).
   Data: transcripts.json, tasks.json, trees.json — loaded lazily when the figure nears the viewport
         (or at once on a deep link / 'open-transcript').
   Emits: select-task {task, set} (player pick), select-node {run, node} (coach pick / "show in tree").
   Listens: open-transcript {run, node} (switches to it and scrolls to this figure);
            select-node (offers "open coach transcript" when one exists; never switches silently). */
(function(){
  'use strict';
  var F = EX.fmt;
  var NAME = 'transcripts';
  var MODEL_ROLES = /^(Output|Refinement output|Verification output)$/;   // typewritten during replay

  /* ---------- small helpers ---------- */
  function genNum(g){ return g === 'initial' || g == null ? 0 : +g; }
  function genLabel(g){ return g === 'initial' ? 'gen 0 (A₀)' : 'gen ' + g; }
  function shortRun(run){ return EX.runLabel(run, { short: true }); }
  function decodeRepr(t){
    // Coach turns were stored as Python string reprs ('...\n...'); decode the common escapes for reading.
    if(typeof t !== 'string' || t.length < 1) return t || '';
    var q = t.charAt(0);
    if(q !== "'" && q !== '"') return t;
    var s = t.slice(1);
    if(s.length && s.charAt(s.length - 1) === q) s = s.slice(0, -1);
    return s.replace(/\\(n|t|'|"|\\)/g, function(m, c){ return c === 'n' ? '\n' : c === 't' ? '\t' : c; });
  }
  var ELIDE_RE = /(\[\.\.\.[^\]]*\]|\[\d+ turns? elided\]|…\s*\[clipped[^\]]*\])/g;
  function fillText(pre, text){
    pre.textContent = '';
    var last = 0, m;
    ELIDE_RE.lastIndex = 0;
    while((m = ELIDE_RE.exec(text))){
      if(m.index > last) pre.appendChild(document.createTextNode(text.slice(last, m.index)));
      EX.h('span', { 'class': 'elide' }, pre, m[0]);
      last = m.index + m[0].length;
    }
    if(last < text.length) pre.appendChild(document.createTextNode(text.slice(last)));
  }
  function parseAnswer(text){
    var m = /<answer>\s*([\s\S]*?)<\/answer>/.exec(text || '');
    if(!m) return null;
    try {
      var g = JSON.parse(m[1]);
      if(Array.isArray(g) && g.length && Array.isArray(g[0]) && g.every(function(r){ return Array.isArray(r) && r.every(function(v){ return v >= 0 && v <= 9; }); })) return g;
    } catch(e){}
    return null;
  }
  function dims(g){ return g && g.length ? g.length + '×' + g[0].length : '—'; }
  function diffText(g, truth){
    if(!g) return '';
    if(!truth) return dims(g);
    if(g.length !== truth.length || g[0].length !== truth[0].length) return 'wrong size: ' + dims(g) + ' vs ' + dims(truth);
    var w = 0, n = 0;
    for(var r = 0; r < g.length; r++) for(var c = 0; c < g[r].length; c++){ n++; if(g[r][c] !== truth[r][c]) w++; }
    return w === 0 ? 'matches the truth' : w + ' of ' + n + ' cells wrong';
  }
  function kindOf(it){
    if(it.kind === 'pred_only') return 'solved';
    var w = it.why || '';
    if(/^evolution series/.test(w)) return 'series';
    if(/second model call/.test(w)) return 'twocall';
    if(/crashed/.test(w)) return 'crash';
    return 'sample';
  }
  var KIND_TAG = { series: 'series', twocall: 'two calls', crash: 'crashed', sample: 'sample', solved: 'answer only' };
  var GROUP_RANK = { source: 0, I0: 1, Ig: 2, g20: 3, g40: 4 };
  function runRank(run){ var g = EX.runGroup(run); return (GROUP_RANK[g] != null ? GROUP_RANK[g] : 9) * 100 + (parseInt((/(\d+)(?!.*\d)/.exec(run) || [0, 0])[1], 10) || 0) + (/g40$/.test(run) ? 50 : 0); }

  EX.mount(NAME, function(node, ctx){
    node.innerHTML = '';
    var root = EX.h('div', { 'class': 'fx-transcripts' }, node);
    var loading = EX.h('div', { 'class': 'fxt-loading', role: 'status' }, root, 'Transcripts load when this figure comes into view…');

    var st = {
      tab: 'player', view: 'single', runF: 'all', kindF: 'all',
      cur: { player: null, coach: null }, series: 0,
      cursor: -1, stepping: false, playing: false, speed: 1, timer: 0, raf: 0,
      mode: null
    };
    var D = null;            // loaded data bundle
    var pendingOpen = null;  // open-transcript that arrived before data
    var started = false;
    var ui = {};

    /* ---------- lazy start ---------- */
    function start(){
      if(started) return; started = true;
      loading.textContent = 'Loading transcripts…';
      EX.loadAll(['transcripts', 'tasks', 'trees']).then(function(res){
        try { build(res[0], res[1], res[2]); }
        catch(err){ fail(err); }
      }, fail);
    }
    function fail(err){
      console.error('[EX] figure "transcripts" failed:', err);
      root.innerHTML = '';
      var b = EX.h('div', { 'class': 'fxt-err', role: 'status' }, root);
      EX.h('b', null, b, 'The transcripts could not be loaded. ');
      EX.h('span', null, b, String(err && err.message || err));
    }
    var hash0 = EX.hash.get();
    if(hash0.section === NAME || !('IntersectionObserver' in window)) start();
    else {
      var io = new IntersectionObserver(function(ents){
        if(ents.some(function(e){ return e.isIntersecting; })){ io.disconnect(); start(); }
      }, { rootMargin: '1200px 0px 1200px 0px' });
      io.observe(ctx.figure || node);
    }

    EX.on('open-transcript', function(p){
      if(!p || p.source === NAME) return;
      pendingOpen = p;
      start();
      if(D) applyOpen();
      var fig = ctx.figure || node;
      fig.scrollIntoView({ behavior: EX.reduceMotion ? 'auto' : 'smooth', block: 'start' });
    });
    EX.on('select-node', function(p){
      if(!p || p.source === NAME || !D) return;
      offerFor(p.run, p.node);
    });

    /* ---------- build once data is here ---------- */
    function build(TX, TK, TR){
      var tasks = TK.tasks, trees = TR.trees;
      var player = TX.player.map(function(p, i){ return Object.assign({ uid: 'p' + i, k: kindOf(p) }, p); });
      var solved = TX.solved_replays.map(function(p, i){ return Object.assign({ uid: 's' + i, k: 'solved' }, p); });
      var coach = TX.coach.map(function(c, i){ return Object.assign({ uid: 'c' + i, k: 'coach' }, c); });
      var series = TX.evolution_series.map(function(s){
        var items = player.concat(solved).filter(function(p){ return p.run === s.run && p.task === s.task && p.test_input === s.test_input; })
          .sort(function(a, b){ return genNum(a.generation) - genNum(b.generation); });
        return { run: s.run, task: s.task, test_input: s.test_input, items: items };
      });
      player.concat(solved).forEach(function(p){
        p.series = -1;
        series.forEach(function(s, i){ if(s.items.indexOf(p) >= 0) p.series = i; });
      });
      var allPlayer = player.concat(solved).sort(function(a, b){
        return runRank(a.run) - runRank(b.run) || (a.task < b.task ? -1 : a.task > b.task ? 1 : 0) || genNum(a.generation) - genNum(b.generation);
      });
      D = { TX: TX, tasks: tasks, trees: trees, player: player, solved: solved, coach: coach, series: series, allPlayer: allPlayer };

      // default: a two-call (refine) transcript with a mid-size grid, else the first transcript
      var def = player.filter(function(p){
        var t = tasks[p.task] && tasks[p.task].test[p.test_input];
        return p.k === 'twocall' && t && t.output && t.output.length <= 16 && p.answers && p.answers.length;
      })[0] || player[0];
      st.cur.player = def;
      st.cur.coach = coach.filter(function(c){ return /I_g pick/.test(c.why || ''); })[0] || coach[0];

      // restore from hash
      var h = EX.hash.get();
      if(h.section === NAME){
        var pr = h.params;
        if(pr.tab === 'coach'){
          st.tab = 'coach';
          var c = findCoach(pr.run, pr.node); if(c) st.cur.coach = c;
        } else if(pr.tab === 'player'){
          if(pr.view === 'series' && pr.series != null && series[+pr.series]){ st.view = 'series'; st.series = +pr.series; }
          var p = allPlayer.filter(function(x){ return x.run === pr.run && String(x.node) === pr.node && x.task === pr.task; })[0];
          if(p) st.cur.player = p;
        }
      }

      root.innerHTML = '';
      var nt = EX.h('p', { 'class': 'notice' }, root);
      EX.h('b', null, nt, 'What was recorded.');
      EX.h('span', null, nt, 'The harness saved player transcripts only for practice inputs the player failed (' +
        F.int(player.length) + ' are shown here); solved inputs appear as answer-only replays (' + F.int(solved.length) +
        '). Hidden reasoning is never recorded: each output is only the visible response.');

      var tl = EX.h('div', { 'class': 'tabs', role: 'tablist', 'aria-label': 'Transcript type' }, root);
      ui.tabs = {};
      [['player', 'Player', player.length + solved.length], ['coach', 'Coach', coach.length]].forEach(function(t){
        var b = EX.h('button', { type: 'button', role: 'tab', id: EX.uid('fxt-tab'), 'aria-selected': String(st.tab === t[0]), tabindex: st.tab === t[0] ? '0' : '-1' }, tl);
        b.appendChild(document.createTextNode(t[1]));
        EX.h('span', { 'class': 'cnt' }, b, String(t[2]));
        b.addEventListener('click', function(){ setTab(t[0], true); });
        ui.tabs[t[0]] = b;
      });
      tl.addEventListener('keydown', function(e){
        if(e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
        e.preventDefault(); e.stopPropagation();
        var nx = st.tab === 'player' ? 'coach' : 'player';
        setTab(nx, true); ui.tabs[nx].focus();
      });
      ui.offer = EX.h('div', { 'class': 'fxt-offer hidden', role: 'status' }, root);
      ui.panel = EX.h('div', { role: 'tabpanel' }, root);
      ui.live = EX.h('div', { 'class': 'sr-only', 'aria-live': 'polite' }, root);

      root.addEventListener('keydown', onKey);
      st.mode = modeFor(ctx.width());
      applyMode();
      render();
      ctx.onResize(function(w){
        var m = modeFor(w);
        if(m !== st.mode){ st.mode = m; applyMode(); stopPlay(); render(); }
      });
      if(pendingOpen) applyOpen();
      if(EX.state && EX.state.node && EX.state.run) offerFor(EX.state.run, EX.state.node);
    }

    function modeFor(w){ return w >= 1000 ? 'wide' : w >= 700 ? 'mid' : 'narrow'; }
    function applyMode(){ root.classList.toggle('mid', st.mode === 'mid'); root.classList.toggle('narrow', st.mode === 'narrow'); }
    function sideWidth(){
      var w = ctx.width();
      if(st.mode === 'wide') return 340;
      if(st.mode === 'mid') return w - 220 - 20;
      return w;
    }
    function findCoach(run, nodeId){ return D.coach.filter(function(c){ return c.run === run && String(c.node) === String(nodeId); })[0]; }

    function setTab(t, user){
      if(st.tab === t && user) { /* still re-render nothing */ return; }
      stopPlay();
      st.tab = t;
      Object.keys(ui.tabs).forEach(function(k){
        ui.tabs[k].setAttribute('aria-selected', String(k === t));
        ui.tabs[k].setAttribute('tabindex', k === t ? '0' : '-1');
      });
      render();
      if(user) writeHash();
    }
    function writeHash(){
      if(st.tab === 'coach'){ var c = st.cur.coach; EX.hash.set(NAME, { tab: 'coach', run: c.run, node: c.node }); }
      else if(st.view === 'series'){ EX.hash.set(NAME, { tab: 'player', view: 'series', series: st.series }); }
      else { var p = st.cur.player; EX.hash.set(NAME, { tab: 'player', run: p.run, node: p.node, task: p.task }); }
    }

    /* ---------- link offers ---------- */
    function offerFor(run, nodeId){
      var c = findCoach(run, nodeId);
      var o = ui.offer; o.innerHTML = '';
      if(!c || (st.tab === 'coach' && st.cur.coach === c)){ o.classList.add('hidden'); return; }
      o.classList.remove('hidden');
      EX.h('span', null, o, 'Linked from another figure: ');
      EX.h('span', { 'class': 'mono' }, o, run + ' · node ' + nodeId);
      EX.h('span', null, o, ' has a saved coach transcript.');
      var b = EX.h('button', { type: 'button', 'class': 'btn small' }, o, 'Open coach transcript');
      b.addEventListener('click', function(){ openCoach(c, true); });
      var x = EX.h('button', { type: 'button', 'class': 'btn small quiet', 'aria-label': 'Dismiss' }, o, 'Dismiss');
      x.addEventListener('click', function(){ o.classList.add('hidden'); });
    }
    function applyOpen(){
      var p = pendingOpen; pendingOpen = null;
      if(!p) return;
      var c = findCoach(p.run, p.node);
      if(c){ openCoach(c, false); return; }
      var pl = D.player.filter(function(x){ return x.run === p.run && String(x.node) === String(p.node); })[0];
      if(pl){ st.view = 'single'; st.cur.player = pl; setTab('player', false); render(); return; }
      var o = ui.offer; o.innerHTML = ''; o.classList.remove('hidden');
      EX.h('span', null, o, 'No transcript was saved for ' + p.run + ' · node ' + p.node + '. Only ' + D.coach.length + ' coach transcripts were kept.');
    }
    function openCoach(c, user){
      ui.offer.classList.add('hidden');
      st.cur.coach = c;
      if(st.tab !== 'coach') setTab('coach', false); else { stopPlay(); render(); }
      if(user) writeHash();
    }

    /* ---------- keyboard: ←/→ step turns, ↑/↓ move in the list ---------- */
    function onKey(e){
      if(e.altKey || e.ctrlKey || e.metaKey) return;
      var t = e.target, tag = (t.tagName || '').toLowerCase();
      if(tag === 'select' || tag === 'input' || tag === 'textarea') return;
      if(t.closest && t.closest('[role="tablist"]')) return;
      if(t.closest && t.closest('.fxt-list') && (e.key === 'ArrowDown' || e.key === 'ArrowUp')){
        var btns = Array.prototype.slice.call(ui.list.querySelectorAll('.fxt-item'));
        var i = btns.indexOf(t.closest('.fxt-item'));
        var j = Math.max(0, Math.min(btns.length - 1, i + (e.key === 'ArrowDown' ? 1 : -1)));
        if(btns[j]){ e.preventDefault(); btns[j].focus(); }
        return;
      }
      if(!ui.turns || !ui.turns.length) return;
      if(e.key === 'ArrowRight'){ e.preventDefault(); step(1); }
      else if(e.key === 'ArrowLeft'){ e.preventDefault(); step(-1); }
    }

    /* ---------- top-level render ---------- */
    function render(){
      stopPlay();
      ui.panel.innerHTML = '';
      ui.panel.setAttribute('aria-labelledby', ui.tabs[st.tab].id);
      ui.turns = null;
      if(st.tab === 'coach') renderCoach();
      else renderPlayer();
    }

    /* ======================= PLAYER ======================= */
    function filteredPlayer(){
      return D.allPlayer.filter(function(p){
        if(st.runF !== 'all' && p.run !== st.runF) return false;
        var k = st.kindF;
        if(k === 'all') return true;
        if(k === 'series') return p.series >= 0;
        if(/^series:/.test(k)) return p.series === +k.slice(7);
        return p.k === k;
      });
    }
    function renderPlayer(){
      var P = ui.panel;
      var ctl = EX.h('div', { 'class': 'controls' }, P);
      EX.seg(ctl, [{ value: 'single', label: 'One transcript' }, { value: 'series', label: 'Evolution series' }], st.view, function(v){
        st.view = v; render(); writeHash();
      }, { label: 'View' });
      if(st.view === 'series'){ renderSeries(P, ctl); return; }

      var runs = []; D.allPlayer.forEach(function(p){ if(runs.indexOf(p.run) < 0) runs.push(p.run); });
      var byGroup = {};
      runs.forEach(function(r){ var g = EX.runGroup(r); (byGroup[g] = byGroup[g] || []).push(r); });
      var opts = [{ value: 'all', label: 'All runs (' + runs.length + ')' }];
      ['source', 'I0', 'Ig', 'g20', 'g40'].forEach(function(g){
        if(byGroup[g]) opts.push({ group: EX.GROUP_LABEL[g], options: byGroup[g].map(function(r){ return { value: r, label: EX.runLabel(r) }; }) });
      });
      EX.selectBox(ctl, opts, st.runF, function(v){ st.runF = v; renderPlayerBody(); }, { label: 'Run' });
      var kopts = [
        { value: 'all', label: 'All kinds' },
        { group: 'Evolution series', options: [{ value: 'series', label: 'All 6 series' }].concat(D.series.map(function(s, i){
          return { value: 'series:' + i, label: shortRun(s.run) + ' · ' + s.task };
        })) },
        { group: 'Saved transcripts (failed)', options: [
          { value: 'twocall', label: 'Two model calls (refine/verify)' },
          { value: 'crash', label: 'Player crashed' },
          { value: 'sample', label: 'Sampled across runs' }] },
        { value: 'solved', label: 'Solved (answer only)' }
      ];
      EX.selectBox(ctl, kopts, st.kindF, function(v){ st.kindF = v; renderPlayerBody(); }, { label: 'Show' });
      ui.body = EX.h('div', { 'class': 'fxt-body' }, P);
      renderPlayerBody();
    }
    function renderPlayerBody(){
      stopPlay();
      var B = ui.body; B.innerHTML = '';
      var items = filteredPlayer();
      if(items.length && items.indexOf(st.cur.player) < 0) st.cur.player = items.filter(function(p){ return p.k !== 'solved'; })[0] || items[0];
      var lc = EX.h('div', { 'class': 'fxt-listcol' }, B);
      var sec = EX.h('div', { 'class': 'fxt-sec', id: EX.uid('fxt-lh') }, lc, 'Inputs');
      EX.h('span', { 'class': 'n' }, sec, String(items.length));
      ui.list = EX.h('ul', { 'class': 'fxt-list', 'aria-labelledby': sec.id }, lc);
      if(!items.length) EX.h('li', { 'class': 'empty' }, ui.list, 'No transcripts match these filters.');
      items.forEach(function(p){
        var li = EX.h('li', null, ui.list);
        var b = EX.h('button', { type: 'button', 'class': 'fxt-item', 'aria-current': String(p === st.cur.player) }, li);
        var l1 = EX.h('span', { 'class': 'l1' }, b);
        EX.h('span', { 'class': 'id' }, l1, shortRun(p.run) + ' · ' + (p.generation === 'initial' ? 'gen 0' : 'gen ' + p.generation) + ' · ' + p.task);
        EX.h('span', { 'class': 'v ' + (p.correct ? 'ok' : 'no'), 'aria-label': p.correct ? 'solved' : 'failed' }, l1, p.correct ? '✓' : '✗');
        EX.h('span', { 'class': 'l2' }, b, KIND_TAG[p.k] + (p.segments ? ' · ' + p.segments.length + ' turns' : ' · no transcript'));
        b.addEventListener('click', function(){
          st.cur.player = p;
          Array.prototype.forEach.call(ui.list.querySelectorAll('.fxt-item'), function(x){ x.setAttribute('aria-current', 'false'); });
          b.setAttribute('aria-current', 'true');
          renderPlayerItem();
          EX.select('task', { task: p.task, set: p.task_set, source: NAME });
          writeHash();
        });
      });
      ui.txcol = EX.h('div', { 'class': 'fxt-txcol' }, B);
      ui.side = EX.h('div', { 'class': 'fxt-sidecol side-panel' }, B);
      renderPlayerItem();
      // keep the selected item in view inside the list (not the page)
      var cur = ui.list.querySelector('[aria-current="true"]');
      if(cur){ var li2 = cur.parentNode; ui.list.scrollTop = Math.max(0, li2.offsetTop - ui.list.offsetTop - 60); }
    }
    function renderPlayerItem(){
      stopPlay();
      var p = st.cur.player, T = ui.txcol, S = ui.side;
      T.innerHTML = ''; S.innerHTML = '';
      if(!p){ EX.h('p', { 'class': 'empty' }, T, 'Pick an input from the list.'); return; }
      var task = D.tasks[p.task], test = task && task.test[p.test_input], truth = test && test.output;
      var hd = EX.h('div', { 'class': 'fxt-head' }, T);
      EX.h('h4', null, hd, 'Player · ' + EX.runLabel(p.run));
      EX.h('span', { 'class': 'mono' }, hd, 'node ' + p.node + ' · ' + genLabel(p.generation) + ' · task ' + p.task + ' · test input ' + (p.test_input + 1) + ' · ' + p.task_set + ' practice set');
      var why = p.k === 'solved' ? 'Solved at this generation. No transcript is saved for solved inputs; only the answer grids survive, from the result rows.' : whyText(p);
      EX.h('p', { 'class': 'fxt-why' }, T, why);
      if(p.segments && p.segments.length){
        buildTurns(T, p.segments, false, truth);
      } else {
        EX.h('p', { 'class': 'empty' }, T, 'No transcript: this input was solved, and only failures were saved. The answers are on the right.');
      }
      renderPuzzleSide(S, p, task, test, truth);
    }
    function whyText(p){
      var t = { series: 'Part of an evolution series: the same input failed at several generations of this run (switch to “Evolution series” to compare).',
        twocall: 'This edited player makes a second model call (' + (p.segments.some(function(s){ return /^Verification/.test(s.role); }) ? 'verify' : 'refine') + ') on its first answer.',
        crash: 'The player crashed before calling the model: ' + (p.segments[0] ? p.segments[0].text : 'agent error') ,
        sample: 'A failed input sampled from this run.' }[p.k] || '';
      return t + ' Answer' + (p.n_answers === 1 ? '' : 's') + ' returned: ' + (p.n_answers == null ? '—' : p.n_answers) + '.';
    }
    function renderPuzzleSide(S, p, task, test, truth){
      var w = sideWidth();
      var ansMax = Math.max(64, Math.min(st.mode === 'wide' ? 100 : 120, Math.floor((w - 32) / 3)));
      EX.h('div', { 'class': 'side-sec' }, S, 'Answers vs truth');
      var row = EX.h('div', { 'class': 'fxt-answers' }, S);
      var answers = p.answers || [];
      var nAtt = Math.max(answers.length, p.k === 'solved' ? 2 : (p.n_answers || 0));
      if(nAtt === 0){
        EX.arcGrid(row, null, { label: 'Attempts', emptyText: p.k === 'crash' ? 'crashed: no answer' : 'no answer', emptySize: ansMax });
      }
      for(var i = 0; i < nAtt; i++){
        var g = answers[i] || null;
        var ok = p.attempt_correct ? !!p.attempt_correct[i] : false;
        var cap = 'Attempt ' + (i + 1) + ' <span class="' + (ok ? 'ok' : 'no') + '">' + (ok ? '✓' : '✗') + '</span>';
        EX.arcGrid(row, g, { label: cap, maxSize: ansMax, diffAgainst: truth, title: 'Attempt ' + (i + 1) + (ok ? ' (correct)' : ' (wrong)'),
          emptyText: 'no grid recorded', emptySize: ansMax });
      }
      EX.arcGrid(row, truth, { label: '<b>Truth</b>', maxSize: ansMax, title: 'Truth grid', emptyText: 'no truth' });
      var v = EX.h('p', { 'class': 'fxt-verdict' }, S);
      if(p.correct){
        EX.h('b', { 'class': 'ok' }, v, '✓ Solved. ');
        v.appendChild(document.createTextNode('Attempt ' + (p.attempt_correct || []).map(function(c, i){ return c ? (i + 1) : null; }).filter(Boolean).join(' and ') + ' matched the truth exactly.'));
      } else {
        EX.h('b', { 'class': 'no' }, v, '✗ Failed. ');
        var parts = answers.map(function(g, i){ return 'attempt ' + (i + 1) + ': ' + (g ? diffText(g, truth) : 'no grid'); });
        v.appendChild(document.createTextNode(parts.length ? parts.join('; ') + '.' : (p.k === 'crash' ? 'The player crashed, so no answer was returned.' : 'No answer grid was recorded.')));
      }
      if(answers.length < (p.n_answers || 0)) EX.h('p', { 'class': 'fxt-note' }, S, 'The run recorded ' + p.n_answers + ' answer' + (p.n_answers > 1 ? 's' : '') + ' but kept ' + (answers.length || 'no') + ' answer grid' + (answers.length === 1 ? '' : 's') + '.');
      EX.h('p', { 'class': 'fxt-note' }, S, 'Wrong cells are outlined; a dashed outline means the size is wrong.');

      if(!task){ EX.h('p', { 'class': 'empty' }, S, 'Task ' + p.task + ' is not in tasks.json.'); return; }
      EX.h('div', { 'class': 'side-sec' }, S, 'Puzzle · ' + task.train.length + ' examples');
      var tr = EX.h('div', { 'class': 'fxt-train' }, S);
      var pairMax = Math.max(60, Math.min(130, Math.floor((w - 30) / 2)));
      task.train.forEach(function(pr, i){
        EX.arcPair(tr, pr.input, pr.output, { maxSize: pairMax, labels: ['Example ' + (i + 1) + ' in · ' + dims(pr.input), 'out · ' + dims(pr.output)] });
      });
      EX.h('div', { 'class': 'side-sec' }, S, 'Test input ' + (p.test_input + 1) + ' of ' + task.test.length);
      EX.arcGrid(S, test.input, { maxSize: Math.min(2 * pairMax, 160), label: dims(test.input), title: 'Test input' });
    }

    /* ---------- evolution series ---------- */
    function renderSeries(P, ctl){
      var opts = D.series.map(function(s, i){ return { value: String(i), label: EX.runLabel(s.run) + ' · ' + s.task }; });
      EX.selectBox(ctl, opts, String(st.series), function(v){ st.series = +v; render(); writeHash(); }, { label: 'Series' });
      var s = D.series[st.series];
      var task = D.tasks[s.task], test = task.test[s.test_input], truth = test.output;
      var tree = D.trees[s.run];
      var nf = s.items.filter(function(x){ return !x.correct; }).length, ns = s.items.length - nf;
      var hd = EX.h('div', { 'class': 'fxt-series-head' }, P);
      EX.h('h4', { 'class': 'fig-sub-title', style: { margin: 0 } }, hd, 'Task ' + s.task + ' across ' + s.items.length + ' generations of ' + EX.runLabel(s.run));
      EX.h('span', { 'class': 'small muted' }, hd, nf + ' failed (with transcripts)' + (ns ? ', ' + ns + ' solved (answer only)' : '; never solved in the generations saved'));
      var sc = EX.h('div', null, P);
      var strip = EX.h('div', { 'class': 'fxt-strip' }, sc);
      var gmax = st.mode === 'narrow' ? 92 : 112;
      var colW = (gmax + 30) + 'px';
      var ref = EX.h('div', { 'class': 'fxt-gcol ref', style: { width: colW } }, strip);
      EX.h('div', { 'class': 'gh' }, ref, 'Truth');
      EX.h('div', { 'class': 'gs' }, ref, 'test input ' + dims(test.input) + ' → output ' + dims(truth));
      EX.arcGrid(ref, test.input, { maxSize: gmax, label: 'Test input', title: 'Test input' });
      EX.arcGrid(ref, truth, { maxSize: gmax, label: '<b>Truth</b>', title: 'Truth' });
      var selCol = null;
      s.items.forEach(function(it){
        var col = EX.h('div', { 'class': 'fxt-gcol' + (it === st.cur.player ? ' is-sel' : ''), style: { width: colW } }, strip);
        if(it === st.cur.player) selCol = col;
        var gh = EX.h('div', { 'class': 'gh' }, col);
        EX.h('span', null, gh, it.generation === 'initial' ? 'gen 0' : 'gen ' + it.generation);
        EX.h('span', { 'class': it.correct ? 'ok' : 'no' }, gh, it.correct ? '✓ solved' : '✗ failed');
        var nd = tree && tree.nodes.filter(function(n){ return n.id === String(it.node); })[0];
        var ps = nd && nd.practice ? nd.practice.per_task && nd.practice.per_task[s.task] : null;
        EX.h('div', { 'class': 'gs' }, col, 'node ' + it.node + (nd && nd.practice_score != null ? ' · practice ' + F.pct(nd.practice_score) : '') +
          (ps != null ? ' · this task ' + F.pct(ps, 0) : ''));
        for(var i = 0; i < 2; i++){
          var g = (it.answers || [])[i] || null;
          var ok = it.attempt_correct ? !!it.attempt_correct[i] : false;
          EX.arcGrid(col, g, { maxSize: gmax, diffAgainst: truth, label: 'Attempt ' + (i + 1) + ' <span class="' + (ok ? 'ok' : 'no') + '">' + (ok ? '✓' : '✗') + '</span>',
            title: 'Generation ' + genNum(it.generation) + ' attempt ' + (i + 1), emptyText: 'no grid recorded', emptySize: gmax });
        }
        if(it.segments){
          var b = EX.h('button', { type: 'button', 'class': 'btn small' }, col, 'Read transcript');
          b.addEventListener('click', function(){ st.cur.player = it; st.view = 'single'; st.runF = 'all'; st.kindF = 'series:' + st.series; render(); writeHash(); EX.select('task', { task: it.task, set: it.task_set, source: NAME }); });
        } else EX.h('div', { 'class': 'gs' }, col, 'answer only: no transcript for solved inputs');
      });
      var sh = EX.scrollHint(sc);
      if(selCol) sh.scrollTo(selCol.offsetLeft + selCol.offsetWidth / 2);
      EX.h('p', { 'class': 'fxt-legend' }, P, 'Columns run left to right by generation. Every saved generation of this input is shown: failures come from player transcripts, solved ones from answer-only replays. Wrong cells are outlined; a dashed outline marks a wrong-size answer. “This task” is the node’s practice score on this task.');
    }

    /* ======================= COACH ======================= */
    function renderCoach(){
      var P = ui.panel;
      ui.body = EX.h('div', { 'class': 'fxt-body' }, P);
      var B = ui.body;
      var lc = EX.h('div', { 'class': 'fxt-listcol' }, B);
      var sec = EX.h('div', { 'class': 'fxt-sec', id: EX.uid('fxt-lh') }, lc, 'Coach generations');
      EX.h('span', { 'class': 'n' }, sec, String(D.coach.length));
      ui.list = EX.h('ul', { 'class': 'fxt-list', 'aria-labelledby': sec.id }, lc);
      D.coach.forEach(function(c){
        var li = EX.h('li', null, ui.list);
        var b = EX.h('button', { type: 'button', 'class': 'fxt-item', 'aria-current': String(c === st.cur.coach) }, li);
        var l1 = EX.h('span', { 'class': 'l1' }, b);
        EX.h('span', { 'class': 'id' }, l1, shortRun(c.run) + ' · node ' + c.node);
        var d = (c.practice_score != null && c.parent_practice_score != null) ? c.practice_score - c.parent_practice_score : null;
        EX.h('span', { 'class': 'v' }, l1, d == null ? '' : F.pts(d));
        EX.h('span', { 'class': 'l2' }, b, coachTag(c));
        b.addEventListener('click', function(){
          st.cur.coach = c;
          Array.prototype.forEach.call(ui.list.querySelectorAll('.fxt-item'), function(x){ x.setAttribute('aria-current', 'false'); });
          b.setAttribute('aria-current', 'true');
          ui.offer.classList.add('hidden');
          renderCoachItem();
          EX.select('node', { run: c.run, node: String(c.node), source: NAME });
          writeHash();
        });
      });
      EX.h('p', { 'class': 'fxt-note' }, lc, 'Kept: the I_g picks, two generation-40 picks, the largest practice-score jumps, the largest drop and one I₀ step.');
      ui.txcol = EX.h('div', { 'class': 'fxt-txcol' }, B);
      ui.side = EX.h('div', { 'class': 'fxt-sidecol side-panel' }, B);
      renderCoachItem();
    }
    function coachTag(c){
      var w = c.why || '';
      var tags = [];
      if(/I_g pick/.test(w)) tags.push('I_g pick');
      var m = /extension pick at generation (\d+)/.exec(w); if(m) tags.push('gen-' + m[1] + ' pick');
      if(/jump/.test(w)) tags.push('big jump');
      if(/drop/.test(w)) tags.push('big drop');
      if(/^I_0/.test(w)) tags.push('I₀ step');
      return (tags.join(' · ') || 'coach step') + ' · gen ' + c.generation;
    }
    function renderCoachItem(){
      stopPlay();
      var c = st.cur.coach, T = ui.txcol, S = ui.side;
      T.innerHTML = ''; S.innerHTML = '';
      var hd = EX.h('div', { 'class': 'fxt-head' }, T);
      EX.h('h4', null, hd, 'Coach · ' + EX.runLabel(c.run) + ' · node ' + c.node);
      EX.h('span', { 'class': 'mono' }, hd, 'gen ' + c.generation + ' · parent ' + c.parent + ' · ' + F.int(c.full_chars) + ' chars in full');
      EX.h('p', { 'class': 'fxt-why' }, T, (c.why || '') + '. Each turn is clipped to about 900 characters; escapes in the stored text are decoded for reading.');
      buildTurns(T, c.segments, true, null);

      // side: record
      var tree = D.trees[c.run];
      var nd = tree && tree.nodes.filter(function(n){ return n.id === String(c.node); })[0];
      EX.h('div', { 'class': 'side-sec' }, S, 'Practice score, parent → child');
      drawDumbbell(S, c.parent_practice_score, c.practice_score, Math.min(sideWidth(), 420));
      var tb = EX.h('table', { 'class': 'kv' }, S), body = EX.h('tbody', null, tb);
      function row(k, v, sub){ var r = EX.h('tr', null, body); EX.h('th', { scope: 'row' }, r, k); var td = EX.h('td', null, r, v); if(sub) EX.h('span', { 'class': 'sub' }, td, sub); }
      row('Run', c.run);
      row('Node', String(c.node), 'generation ' + c.generation);
      row('Parent', String(c.parent));
      var d = (c.practice_score != null && c.parent_practice_score != null) ? c.practice_score - c.parent_practice_score : null;
      row('Practice score', F.pct(c.practice_score), 'parent ' + F.pct(c.parent_practice_score) + ' · ' + (d == null ? '—' : F.ptsU(d)));
      if(nd && nd.meta){
        row('Coach calls', F.int(nd.meta.calls));
        row('Coach tokens', F.tokens(nd.meta.tokens));
        row('Coach cost', F.usd(nd.meta.ledger_cost, 4));
      }
      var files = (nd && nd.files_changed) || c.files_changed || [];
      EX.h('div', { 'class': 'side-sec' }, S, 'Files changed · ' + files.length);
      var ul = EX.h('ul', { 'class': 'fxt-files' }, S);
      if(!files.length) EX.h('li', { 'class': 'empty' }, ul, 'No files changed.');
      files.forEach(function(f){
        var li = EX.h('li', null, ul);
        EX.h('span', { 'class': 'p' }, li, f.path);
        EX.h('span', { 'class': 'r' }, li, f.role + ' ' + (f.binary ? 'binary' : '+' + f.added + ' ' + F.MINUS + f.removed));
      });
      var bt = EX.h('button', { type: 'button', 'class': 'btn small', style: { marginTop: '10px' } }, S, 'Show this node in the tree');
      bt.addEventListener('click', function(){
        EX.select('node', { run: c.run, node: String(c.node), source: NAME });
        var tf = document.getElementById('fig-tree');
        if(tf && tree && tree.kind === 'source') tf.scrollIntoView({ behavior: EX.reduceMotion ? 'auto' : 'smooth', block: 'start' });
      });
      if(!tree || tree.kind !== 'source') EX.h('p', { 'class': 'fxt-note' }, S, 'Fig 5 draws source runs only; this pay-off node is not in it.');
      EX.h('div', { 'class': 'side-sec' }, S, 'Resulting diff');
      if(nd && nd.diff){
        EX.h('p', { 'class': 'fxt-note', style: { marginTop: 0, marginBottom: '6px' } }, S,
          nd.diff_truncated ? 'Excerpt: the first ' + F.int(nd.diff.length) + ' of ' + F.int(nd.diff_full_chars) + ' characters.' : 'Full diff, ' + F.int(nd.diff.length) + ' characters.');
        var pre = EX.h('pre', { 'class': 'code diff', tabindex: '0', 'aria-label': 'Diff for node ' + c.node }, S);
        nd.diff.split('\n').forEach(function(l){
          var cls = /^(diff |index |\+\+\+|---|new file|deleted file|similarity|rename|Binary)/.test(l) ? 'meta' : /^@@/.test(l) ? 'hunk' : /^\+/.test(l) ? 'add' : /^-/.test(l) ? 'del' : '';
          EX.h('span', { 'class': 'ln' + (cls ? ' ' + cls : '') }, pre, l || ' ');
        });
      } else EX.h('p', { 'class': 'empty' }, S, 'No diff was stored for this node.');
    }
    function drawDumbbell(host, a, b, w){
      w = Math.max(220, w); var h = 46, x0 = 8, x1 = w - 12;
      var lo = Math.min(a, b), hi = Math.max(a, b);
      var dLo = Math.max(0, Math.floor((lo - 0.05) * 10) / 10), dHi = Math.min(1, Math.ceil((hi + 0.05) * 10) / 10);
      var X = function(v){ return x0 + (v - dLo) / (dHi - dLo) * (x1 - x0); };
      var svg = EX.s('svg', { 'class': 'fxt-dumb', width: w, height: h, viewBox: '0 0 ' + w + ' ' + h, role: 'img',
        'aria-label': 'Practice score went from ' + F.pct(a) + ' (parent) to ' + F.pct(b) + ' (this node)' }, host);
      EX.s('line', { 'class': 'ax', x1: x0, x2: x1, y1: 30, y2: 30 }, svg);
      for(var t = dLo; t <= dHi + 1e-9; t += 0.1){
        EX.s('line', { 'class': 'ax', x1: X(t), x2: X(t), y1: 30, y2: 34 }, svg);
        EX.s('text', { 'class': 'tk', x: X(t), y: 45, 'text-anchor': 'middle' }, svg, Math.round(t * 100) + '%');
      }
      EX.s('line', { 'class': 'ln', x1: X(a), x2: X(b), y1: 18, y2: 18 }, svg);
      EX.s('circle', { 'class': 'p0', cx: X(a), cy: 18, r: 5 }, svg);
      EX.s('circle', { 'class': 'p1', cx: X(b), cy: 18, r: 5 }, svg);
      var same = Math.abs(X(a) - X(b)) < 40;
      EX.s('text', { 'class': 'lb', x: X(a) + (b >= a ? -8 : 8), y: 10, 'text-anchor': b >= a ? 'end' : 'start' }, svg, same ? '' : 'parent');
      EX.s('text', { 'class': 'lb', x: X(b) + (b >= a ? 8 : -8), y: 10, 'text-anchor': b >= a ? 'start' : 'end' }, svg, same ? 'parent = child' : 'child');
    }

    /* ======================= TURNS + REPLAY ======================= */
    function buildTurns(T, segs, isCoach, truth){
      var bar = EX.h('div', { 'class': 'fxt-bar', role: 'group', 'aria-label': 'Replay controls' }, T);
      ui.play = EX.h('button', { type: 'button', 'class': 'btn small', 'aria-label': 'Play replay' }, bar);
      ui.prev = EX.h('button', { type: 'button', 'class': 'btn small', 'aria-label': 'Previous turn' }, bar);
      ui.prev.innerHTML = '<span class="ic" aria-hidden="true">‹</span> Prev';
      ui.next = EX.h('button', { type: 'button', 'class': 'btn small', 'aria-label': 'Next turn' }, bar);
      ui.next.innerHTML = 'Next <span class="ic" aria-hidden="true">›</span>';
      ui.all = EX.h('button', { type: 'button', 'class': 'btn small quiet' }, bar, 'Show all');
      EX.seg(bar, [{ value: 1, label: '1×' }, { value: 2, label: '2×' }, { value: 4, label: '4×' }], st.speed, function(v){ st.speed = +v; }, { ariaLabel: 'Replay speed', mono: true });
      ui.pos = EX.h('span', { 'class': 'fxt-pos', 'aria-hidden': 'true' }, bar);
      ui.play.addEventListener('click', function(){ if(st.playing) stopPlay(); else startPlay(); });
      ui.prev.addEventListener('click', function(){ step(-1); });
      ui.next.addEventListener('click', function(){ step(1); });
      ui.all.addEventListener('click', function(){ showAll(); });

      var box = EX.h('div', { 'class': 'fxt-tx', tabindex: '0', role: 'region', 'aria-label': (isCoach ? 'Coach' : 'Player') + ' transcript turns' }, T);
      ui.box = box;
      ui.turns = [];
      segs.forEach(function(sg){
        var role = sg.role || 'Turn';
        var text = isCoach ? decodeRepr(sg.text) : (sg.text || '');
        var t = { role: role, text: text, model: MODEL_ROLES.test(role) };
        if(role === 'Elided'){
          t.el = EX.h('div', { 'class': 'turn t-elided' }, box, text.replace(/^\[|\]$/g, '') || 'turns elided');
          ui.turns.push(t); return;
        }
        var cls = 'turn' + (t.model ? ' r-model' : '') + (role === 'Error' ? ' r-error' : '') + (role === 'Nudge' ? ' r-nudge' : '');
        t.el = EX.h('div', { 'class': cls }, box);
        var rl = EX.h('div', { 'class': 'turn-role' }, t.el);
        EX.h('span', { 'class': 'who' }, rl, roleLabel(role, isCoach));
        EX.h('span', { 'class': 'len' }, rl, F.int(text.length) + ' chars');
        t.pre = EX.h('pre', { 'class': 'code wrap' }, t.el);
        if(text.trim()) fillText(t.pre, text); else EX.h('span', { 'class': 'elide' }, t.pre, '(empty response)');
        var long = text.length > 650 || text.split('\n').length > 11;
        if(long){
          var xb = EX.h('button', { type: 'button', 'class': 'xbtn', 'aria-expanded': 'false' }, t.el, 'Expand');
          xb.addEventListener('click', function(){
            var open = t.el.classList.toggle('is-open');
            xb.setAttribute('aria-expanded', String(open)); xb.textContent = open ? 'Collapse' : 'Expand';
          });
        }
        if(!isCoach && t.model){
          var g = parseAnswer(text);
          if(g){
            t.inl = EX.h('div', { 'class': 'inl' }, t.el);
            var ok = truth && EX.gridsEqual(g, truth);
            EX.arcGrid(t.inl, g, { maxSize: 84, diffAgainst: truth, title: 'Answer parsed from this turn',
              label: 'parsed answer <span class="' + (ok ? 'ok' : 'no') + '">' + (ok ? '✓' : '✗') + '</span>' });
            EX.h('span', { 'class': 'cap2' }, t.inl, diffText(g, truth));
          }
        }
        ui.turns.push(t);
      });
      ui.more = EX.h('div', { 'class': 'fxt-more hidden' }, box);
      st.cursor = ui.turns.length - 1; st.stepping = false;
      applyCursor(false);
    }
    function roleLabel(role, isCoach){
      if(!isCoach){
        return { 'Input': 'Prompt (call 1)', 'Output': 'Model answer (call 1)', 'Refinement input': 'Refine prompt (call 2)', 'Refinement output': 'Model answer (call 2)',
          'Verification input': 'Verify prompt (call 2)', 'Verification output': 'Model answer (call 2)', 'Error': 'Error' }[role] || role;
      }
      return { 'Input': 'Task given to the coach', 'Output': 'Coach (tool call or reply)', 'Tool output': 'Tool output', 'Nudge': 'Harness nudge' }[role] || role;
    }
    function applyCursor(scroll){
      var n = ui.turns.length, c = st.cursor;
      ui.turns.forEach(function(t, i){
        t.el.classList.toggle('hidden', i > c);
        t.el.classList.toggle('is-cur', st.stepping && i === c);
      });
      var rest = n - 1 - c;
      ui.more.classList.toggle('hidden', rest <= 0);
      ui.more.textContent = rest > 0 ? rest + ' more turn' + (rest > 1 ? 's' : '') + ' hidden. Press Next, Play or Show all.' : '';
      ui.pos.textContent = 'turn ' + Math.max(0, c + 1) + ' of ' + n;
      ui.prev.disabled = c <= 0;
      ui.next.disabled = c >= n - 1;
      ui.all.disabled = c >= n - 1 && !st.playing;
      setPlayBtn();
      if(scroll && c >= 0 && ui.turns[c]){
        var el = ui.turns[c].el, box = ui.box;
        var top = el.offsetTop, bottom = top + el.offsetHeight;
        if(top < box.scrollTop || bottom > box.scrollTop + box.clientHeight) box.scrollTop = Math.max(0, top - 8);
      }
    }
    function setPlayBtn(){
      if(!ui.play) return;
      ui.play.innerHTML = st.playing ? '<span class="ic" aria-hidden="true">❚❚</span> Pause' : '<span class="ic" aria-hidden="true">▶</span> ' + (st.cursor >= ui.turns.length - 1 ? 'Replay' : 'Play');
      ui.play.setAttribute('aria-label', st.playing ? 'Pause replay' : 'Play replay');
      ui.play.setAttribute('aria-pressed', String(st.playing));
    }
    function announce(){
      var t = ui.turns[st.cursor];
      if(t && ui.live) ui.live.textContent = 'Turn ' + (st.cursor + 1) + ' of ' + ui.turns.length + ': ' + roleLabel(t.role, st.tab === 'coach');
    }
    function step(d){
      if(!ui.turns || !ui.turns.length) return;
      stopPlay();
      var c = Math.max(0, Math.min(ui.turns.length - 1, st.cursor + d));
      st.cursor = c; st.stepping = true;
      applyCursor(true); announce();
    }
    function showAll(){
      stopPlay();
      st.cursor = ui.turns.length - 1; st.stepping = false;
      applyCursor(false);
      if(ui.live) ui.live.textContent = 'All ' + ui.turns.length + ' turns shown.';
    }
    function startPlay(){
      if(!ui.turns || !ui.turns.length) return;
      if(st.cursor >= ui.turns.length - 1){ st.cursor = -1; ui.box.scrollTop = 0; }
      st.playing = true; st.stepping = true;
      applyCursor(false);
      advance();
    }
    function advance(){
      if(!st.playing) return;
      if(st.cursor >= ui.turns.length - 1){ st.playing = false; applyCursor(false); return; }
      st.cursor++;
      var t = ui.turns[st.cursor];
      applyCursor(true); announce();
      var sp = st.speed || 1;
      if(t.model && t.pre && !EX.reduceMotion){
        typewrite(t, sp, function(){ st.timer = setTimeout(advance, 500 / sp); });
      } else {
        st.timer = setTimeout(advance, (t.model ? 900 : 700) / sp);
      }
    }
    function typewrite(t, sp, done){
      var text = t.text, len = text.length;
      var dur = Math.min(len / 450, 3.2) * 1000 / sp;     // ≤ 3.2 s at 1×
      if(t.inl) t.inl.classList.add('hidden');
      t.pre.textContent = '';
      var caret = EX.h('span', { 'class': 'caret', 'aria-hidden': 'true' });
      var tn = document.createTextNode('');
      t.pre.appendChild(tn); t.pre.appendChild(caret);
      var t0 = performance.now();
      t.typing = true;
      function frame(now){
        if(!t.typing) return;
        var k = Math.min(len, Math.ceil(len * (now - t0) / Math.max(1, dur)));
        tn.nodeValue = text.slice(0, k);
        t.pre.scrollTop = t.pre.scrollHeight;
        var box = ui.box, bottom = t.el.offsetTop + t.el.offsetHeight;
        if(bottom > box.scrollTop + box.clientHeight) box.scrollTop = bottom - box.clientHeight + 8;
        if(k >= len){ finishType(t); done(); return; }
        st.raf = requestAnimationFrame(frame);
      }
      st.raf = requestAnimationFrame(frame);
    }
    function finishType(t){
      if(!t.typing) return;
      t.typing = false;
      fillText(t.pre, t.text);
      t.pre.scrollTop = 0;
      if(t.inl) t.inl.classList.remove('hidden');
    }
    function stopPlay(){
      clearTimeout(st.timer); cancelAnimationFrame(st.raf);
      var was = st.playing;
      st.playing = false;
      if(ui.turns) ui.turns.forEach(function(t){ if(t.typing) finishType(t); });
      if(was && ui.turns) applyCursor(false);
    }
  });
})();
