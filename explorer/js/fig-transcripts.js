/* fig-transcripts.js — Explore › Transcripts (mount "transcripts").
   Tabs: Player | Coach. List on the left (one tab stop, arrow keys), the turns in the middle
   (all shown at rest), the puzzle and final answers (diffed against the truth) or the coach node's record on the right.
   Behind "More options": run / kind filters, the evolution-series view, and step-by-step replay (Prev / Next).
   Data: transcripts.json, tasks.json, trees.json (loaded when the tab is first shown).
   Emits: select-task (player pick), select-node (coach pick / "Show in tree").
   Listens: open-transcript {run, node} (also reads EX.pendingTranscript at start); never switches tabs itself. */
(function(){
  'use strict';
  var F = EX.fmt;
  var NAME = 'transcripts';
  var MODEL_ROLES = /^(Output|Refinement output|Verification output)$/;

  function genNum(g){ return g === 'initial' || g == null ? 0 : +g; }
  function genText(g){ return 'Generation ' + genNum(g); }
  function plain(run){ return EX.runLabel(run, { plain: true }); }
  function decodeRepr(t){
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
    if(!g) return 'no grid';
    if(!truth) return dims(g);
    if(g.length !== truth.length || g[0].length !== truth[0].length) return 'wrong size';
    var w = 0;
    for(var r = 0; r < g.length; r++) for(var c = 0; c < g[r].length; c++) if(g[r][c] !== truth[r][c]) w++;
    return w === 0 ? 'right' : w + ' cell' + (w > 1 ? 's' : '') + ' off';
  }
  function kindOf(it){
    if(it.kind === 'pred_only') return 'solved';
    var w = it.why || '';
    if(/^evolution series/.test(w)) return 'series';
    if(/second model call/.test(w)) return 'twocall';
    if(/crashed/.test(w)) return 'crash';
    return 'sample';
  }
  var GROUP_RANK = { source: 0, I0: 1, Ig: 2, g20: 3, g40: 4 };
  function runRank(run){ var g = EX.runGroup(run); return (GROUP_RANK[g] != null ? GROUP_RANK[g] : 9) * 100 + (parseInt((/(\d+)(?!.*\d)/.exec(run) || [0, 0])[1], 10) || 0) + (/g40$/.test(run) ? 50 : 0); }

  EX.mount(NAME, function(node, ctx){
    node.innerHTML = '';
    var root = EX.h('div', { 'class': 'fx-transcripts' }, node);
    EX.h('div', { 'class': 'fxt-loading', role: 'status' }, root, 'Loading transcripts…');
    var st = { tab: 'player', view: 'single', runF: 'all', kindF: 'all', cur: { player: null, coach: null }, series: 0, step: false, cursor: 0, mode: null };
    var D = null, pendingOpen = null, ui = {};

    EX.on('open-transcript', function(p){
      if(!p || p.source === NAME) return;
      pendingOpen = p;
      if(D) applyOpen();
    });

    return EX.loadAll(['transcripts', 'tasks', 'trees']).then(function(res){ build(res[0], res[1], res[2]); });

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
      player.concat(solved).forEach(function(p){ p.series = -1; series.forEach(function(s, i){ if(s.items.indexOf(p) >= 0) p.series = i; }); });
      var allPlayer = player.concat(solved).sort(function(a, b){
        return runRank(a.run) - runRank(b.run) || (a.task < b.task ? -1 : a.task > b.task ? 1 : 0) || genNum(a.generation) - genNum(b.generation);
      });
      D = { tasks: tasks, trees: trees, player: player, solved: solved, coach: coach, series: series, allPlayer: allPlayer };

      st.cur.player = allPlayer.filter(function(p){ return p.k !== 'solved' && p.segments && p.segments.length; })[0] || allPlayer[0];
      st.cur.coach = coach.filter(function(c){ return /I_g pick/.test(c.why || ''); })[0] || coach[0];

      var h = EX.hash.get();
      if(h.section === NAME){
        var pr = h.params;
        if(pr.tab === 'coach'){ st.tab = 'coach'; var c = findCoach(pr.run, pr.node); if(c) st.cur.coach = c; }
        else if(pr.run){
          var p = allPlayer.filter(function(x){ return x.run === pr.run && String(x.node) === pr.node && x.task === pr.task; })[0];
          if(p) st.cur.player = p;
        }
      }
      if(!pendingOpen && EX.pendingTranscript) pendingOpen = EX.pendingTranscript;
      EX.pendingTranscript = null;

      root.innerHTML = '';
      var tl = EX.h('div', { 'class': 'tabs', role: 'tablist', 'aria-label': 'Transcript type' }, root);
      ui.tabs = {};
      [['player', 'Player', player.length + solved.length], ['coach', 'Coach', coach.length]].forEach(function(t){
        var b = EX.h('button', { type: 'button', role: 'tab', id: EX.uid('fxt-tab'), 'aria-selected': String(st.tab === t[0]), tabindex: st.tab === t[0] ? '0' : '-1' }, tl, t[1] + ' (' + t[2] + ')');
        b.addEventListener('click', function(){ setTab(t[0], true); });
        ui.tabs[t[0]] = b;
      });
      tl.addEventListener('keydown', function(e){
        if(e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
        e.preventDefault(); e.stopPropagation();
        var nx = st.tab === 'player' ? 'coach' : 'player';
        setTab(nx, true); ui.tabs[nx].focus();
      });
      ui.panel = EX.h('div', { role: 'tabpanel' }, root);
      ui.live = EX.h('div', { 'class': 'sr-only', 'aria-live': 'polite' }, root);
      root.addEventListener('keydown', onKey);
      st.mode = modeFor(ctx.width());
      applyMode();
      render();
      ctx.onResize(function(w){ var m = modeFor(w); if(m !== st.mode){ st.mode = m; applyMode(); render(); } });
      ctx.onShow(function(w){ var m = modeFor(w); if(w && m !== st.mode){ st.mode = m; applyMode(); render(); } });
      if(pendingOpen) applyOpen();
    }

    function modeFor(w){ return w >= 1000 ? 'wide' : w >= 700 ? 'mid' : 'narrow'; }
    function applyMode(){ root.classList.toggle('mid', st.mode === 'mid'); root.classList.toggle('narrow', st.mode === 'narrow'); }
    function sideWidth(){ var w = ctx.width(); return st.mode === 'wide' ? 320 : st.mode === 'mid' ? w - 220 - 24 : w; }
    function findCoach(run, nodeId){ return D.coach.filter(function(c){ return c.run === run && String(c.node) === String(nodeId); })[0]; }

    function setTab(t, user){
      if(st.tab === t && user) return;
      st.tab = t; st.step = false;
      Object.keys(ui.tabs).forEach(function(k){
        ui.tabs[k].setAttribute('aria-selected', String(k === t));
        ui.tabs[k].setAttribute('tabindex', k === t ? '0' : '-1');
      });
      render();
      if(user) writeHash();
    }
    function writeHash(){
      if(st.tab === 'coach'){ var c = st.cur.coach; EX.hash.set(NAME, { tab: 'coach', run: c.run, node: c.node }); }
      else { var p = st.cur.player; EX.hash.set(NAME, { tab: 'player', run: p.run, node: p.node, task: p.task }); }
    }
    function applyOpen(){
      var p = pendingOpen; pendingOpen = null;
      if(!p) return;
      var c = findCoach(p.run, p.node);
      if(c){ st.cur.coach = c; if(st.tab !== 'coach') setTab('coach', false); else render(); return; }
      var pl = D.player.filter(function(x){ return x.run === p.run && String(x.node) === String(p.node); })[0];
      if(pl){ st.view = 'single'; st.cur.player = pl; if(st.tab !== 'player') setTab('player', false); else render(); }
    }

    /* ←/→ step turns in step-by-step mode */
    function onKey(e){
      if(!st.step || e.altKey || e.ctrlKey || e.metaKey) return;
      var t = e.target, tag = (t.tagName || '').toLowerCase();
      if(tag === 'select' || tag === 'input' || (t.closest && (t.closest('[role="tablist"]') || t.closest('.fxt-list')))) return;
      if(e.key === 'ArrowRight'){ e.preventDefault(); stepBy(1); }
      else if(e.key === 'ArrowLeft'){ e.preventDefault(); stepBy(-1); }
    }

    function render(){
      ui.panel.innerHTML = '';
      ui.panel.setAttribute('aria-labelledby', ui.tabs[st.tab].id);
      ui.turns = null;
      if(st.tab === 'coach') renderCoach(); else renderPlayer();
    }

    /* "More options": filters, series view, step-by-step */
    function buildMoreRow(P){
      var m = EX.more(P, 'More options', function(body){
        var ctl = EX.h('div', { 'class': 'controls fxt-ctl' }, body);
        if(st.tab === 'player'){
          var runs = []; D.allPlayer.forEach(function(p){ if(runs.indexOf(p.run) < 0) runs.push(p.run); });
          var byGroup = {};
          runs.forEach(function(r){ var g = EX.runGroup(r); (byGroup[g] = byGroup[g] || []).push(r); });
          var opts = [{ value: 'all', label: 'All runs' }];
          ['source', 'I0', 'Ig', 'g20', 'g40'].forEach(function(g){
            if(byGroup[g]) opts.push({ group: (EX.ARM_LABEL && EX.ARM_LABEL[g]) || g, options: byGroup[g].map(function(r){ return { value: r, label: plain(r) }; }) });
          });
          EX.selectBox(ctl, opts, st.runF, function(v){ st.runF = v; st.view = 'single'; render(); }, { label: 'Run' });
          EX.selectBox(ctl, [
            { value: 'all', label: 'All kinds' },
            { value: 'twocall', label: 'Two model calls (refine or verify)' },
            { value: 'crash', label: 'Player crashed' },
            { value: 'series', label: 'Same puzzle across generations' },
            { value: 'sample', label: 'Sampled failures' },
            { value: 'solved', label: 'Solved (answer only)' }
          ], st.kindF, function(v){ st.kindF = v; st.view = 'single'; render(); }, { label: 'Kind' });
          var sb = EX.h('button', { type: 'button', 'class': 'btn', 'aria-pressed': String(st.view === 'series') }, ctl,
            st.view === 'series' ? 'Back to one transcript' : 'Evolution series view');
          sb.addEventListener('click', function(){ st.view = st.view === 'series' ? 'single' : 'series'; st.step = false; render(); ui.more.open(); });
        }
        if(st.view !== 'series'){
          var rb = EX.h('button', { type: 'button', 'class': 'btn', 'aria-pressed': String(st.step) }, ctl, st.step ? 'Show all turns' : 'Replay step by step');
          rb.addEventListener('click', function(){ st.step = !st.step; st.cursor = 0; render(); ui.more.open(); });
        }
      });
      ui.more = m;
      if(st.step || st.view === 'series' || st.runF !== 'all' || st.kindF !== 'all') m.open();
    }

    /* ======================= PLAYER ======================= */
    function filteredPlayer(){
      return D.allPlayer.filter(function(p){
        if(st.runF !== 'all' && p.run !== st.runF) return false;
        var k = st.kindF;
        if(k === 'all') return true;
        if(k === 'series') return p.series >= 0;
        return p.k === k;
      });
    }
    function renderPlayer(){
      var P = ui.panel;
      buildMoreRow(P);
      if(st.view === 'series'){ renderSeries(P); return; }
      var B = EX.h('div', { 'class': 'fxt-body' }, P);
      var items = filteredPlayer();
      if(items.length && items.indexOf(st.cur.player) < 0) st.cur.player = items.filter(function(p){ return p.k !== 'solved'; })[0] || items[0];
      var lc = EX.h('div', { 'class': 'fxt-listcol' }, B);
      EX.h('p', { 'class': 'fxt-listnote' }, lc, 'Saved player transcripts are all failed attempts; solved ones show the answer only.');
      ui.list = EX.h('ul', { 'class': 'fxt-list', 'aria-label': 'Player transcripts' }, lc);
      if(!items.length) EX.h('li', { 'class': 'empty' }, ui.list, 'No transcripts match these filters.');
      items.forEach(function(p){
        var li = EX.h('li', null, ui.list);
        var b = EX.h('button', { type: 'button', 'class': 'fxt-item', tabindex: '-1', 'aria-current': String(p === st.cur.player) }, li);
        EX.h('span', { 'class': 'l1' }, b, plain(p.run));
        EX.h('span', { 'class': 'l2' }, b, genText(p.generation) + ', puzzle ' + p.task + (p.k === 'solved' ? ' (answer only)' : ''));
        b.addEventListener('click', function(){ pickPlayer(p, b); });
      });
      listRoving();
      ui.txcol = EX.h('div', { 'class': 'fxt-txcol' }, B);
      ui.side = EX.h('div', { 'class': 'fxt-sidecol side-panel' }, B);
      renderPlayerItem();
      keepCurInView();
    }
    function pickPlayer(p, b){
      st.cur.player = p; st.cursor = 0;
      markCur(b);
      renderPlayerItem();
      EX.select('task', { task: p.task, set: p.task_set, source: NAME });
      writeHash();
    }
    function markCur(b){
      Array.prototype.forEach.call(ui.list.querySelectorAll('.fxt-item'), function(x){ x.setAttribute('aria-current', String(x === b)); });
      if(ui.rov) ui.rov.refresh();
    }
    function listRoving(){
      ui.rov = EX.roving(ui.list, '.fxt-item', { orientation: 'vertical', onActivate: function(el){ el.click(); } });
    }
    function keepCurInView(){
      var cur = ui.list.querySelector('[aria-current="true"]');
      if(cur){ var li = cur.parentNode; ui.list.scrollTop = Math.max(0, li.offsetTop - ui.list.offsetTop - 60); }
    }
    function renderPlayerItem(){
      var p = st.cur.player, T = ui.txcol, S = ui.side;
      T.innerHTML = ''; S.innerHTML = '';
      if(!p){ EX.h('p', { 'class': 'empty' }, T, 'Pick an item from the list.'); return; }
      var task = D.tasks[p.task], test = task && task.test[p.test_input], truth = test && test.output;
      var hd = EX.h('div', { 'class': 'fxt-head' }, T);
      EX.h('h4', null, hd, plain(p.run) + ', ' + genText(p.generation).toLowerCase());
      EX.h('p', { 'class': 'fxt-why' }, T, p.k === 'solved' ? 'Solved, so no transcript was saved: only the answer survives (right).' : whyText(p));
      if(p.segments && p.segments.length) buildTurns(T, p.segments, false, truth);
      renderPuzzleSide(S, p, task, test, truth);
    }
    function whyText(p){
      return { series: 'This practice puzzle failed at several generations of this run.',
        twocall: 'This edited player makes a second model call to ' + (p.segments.some(function(s){ return /^Verification/.test(s.role); }) ? 'verify' : 'refine') + ' its first answer.',
        crash: 'The player crashed before it could answer.',
        sample: 'A failed practice answer sampled from this run.' }[p.k] || '';
    }
    function renderPuzzleSide(S, p, task, test, truth){
      var w = sideWidth();
      var ansMax = Math.max(64, Math.min(st.mode === 'wide' ? 92 : 120, Math.floor((w - 32) / 3)));
      EX.h('div', { 'class': 'side-sec' }, S, 'Final answers vs the correct answer');
      var row = EX.h('div', { 'class': 'fxt-answers' }, S);
      var answers = p.answers || [];
      var nAtt = Math.max(answers.length, p.k === 'solved' ? 2 : (p.n_answers || 0));
      if(nAtt === 0) EX.arcGrid(row, null, { label: 'Answer', emptyText: p.k === 'crash' ? 'crashed' : 'no answer', emptySize: ansMax });
      for(var i = 0; i < nAtt; i++){
        var g = answers[i] || null, ok = p.attempt_correct ? !!p.attempt_correct[i] : false;
        EX.arcGrid(row, g, { label: 'Try ' + (i + 1) + ' <span class="' + (ok ? 'ok' : 'no') + '">' + (ok ? '✓' : '× ' + EX.esc(diffText(g, truth))) + '</span>',
          maxSize: ansMax, diffAgainst: truth, title: 'Try ' + (i + 1) + (ok ? ' (right)' : ' (wrong)'), emptyText: 'not recorded', emptySize: ansMax });
      }
      EX.arcGrid(row, truth, { label: '<b>Correct</b>', maxSize: ansMax, title: 'Correct answer', emptyText: 'no truth' });
      if(!task) return;
      EX.h('div', { 'class': 'side-sec' }, S, 'The puzzle');
      var tr = EX.h('div', { 'class': 'fxt-train' }, S);
      var pairMax = Math.max(60, Math.min(st.mode === 'narrow' ? 88 : 120, Math.floor((w - 30) / 2)));
      task.train.forEach(function(pr, i){ EX.arcPair(tr, pr.input, pr.output, { maxSize: pairMax, labels: ['Example ' + (i + 1), null] }); });
      EX.arcGrid(S, test.input, { maxSize: Math.min(2 * pairMax, 150), label: 'Test input', title: 'Test input' });
    }

    /* evolution series (More options) */
    function renderSeries(P){
      var ctl = EX.h('div', { 'class': 'controls' }, P);
      var opts = D.series.map(function(s, i){ return { value: String(i), label: plain(s.run) + ' · ' + s.task }; });
      EX.selectBox(ctl, opts, String(st.series), function(v){ st.series = +v; render(); }, { label: 'Series' });
      var s = D.series[st.series];
      var task = D.tasks[s.task], test = task.test[s.test_input], truth = test.output;
      EX.h('p', { 'class': 'fxt-why' }, P, 'Puzzle ' + s.task + ' across ' + s.items.length + ' saved generations of ' + plain(s.run) + ', left to right.');
      var sc = EX.h('div', null, P);
      var strip = EX.h('div', { 'class': 'fxt-strip' }, sc);
      var gmax = st.mode === 'narrow' ? 88 : 104, colW = (gmax + 24) + 'px';
      var ref = EX.h('div', { 'class': 'fxt-gcol ref', style: { width: colW } }, strip);
      EX.h('div', { 'class': 'gh' }, ref, 'Puzzle');
      EX.arcGrid(ref, test.input, { maxSize: gmax, label: 'Test input', title: 'Test input' });
      EX.arcGrid(ref, truth, { maxSize: gmax, label: '<b>Correct</b>', title: 'Correct answer' });
      s.items.forEach(function(it){
        var col = EX.h('div', { 'class': 'fxt-gcol', style: { width: colW } }, strip);
        var gh = EX.h('div', { 'class': 'gh' }, col);
        EX.h('span', null, gh, genText(it.generation));
        EX.h('span', { 'class': it.correct ? 'ok' : 'no' }, gh, it.correct ? '✓' : '×');
        for(var i = 0; i < 2; i++){
          var g = (it.answers || [])[i] || null;
          EX.arcGrid(col, g, { maxSize: gmax, diffAgainst: truth, label: 'Try ' + (i + 1), title: genText(it.generation) + ' try ' + (i + 1), emptyText: 'not recorded', emptySize: gmax });
        }
        if(it.segments){
          var b = EX.h('button', { type: 'button', 'class': 'btn small' }, col, 'Read');
          b.addEventListener('click', function(){ st.cur.player = it; st.view = 'single'; st.runF = 'all'; st.kindF = 'all'; render(); writeHash(); });
        }
      });
      EX.scrollHint(sc);
    }

    /* ======================= COACH ======================= */
    function renderCoach(){
      var P = ui.panel;
      buildMoreRow(P);
      var B = EX.h('div', { 'class': 'fxt-body' }, P);
      var lc = EX.h('div', { 'class': 'fxt-listcol' }, B);
      EX.h('p', { 'class': 'fxt-listnote' }, lc, 'Kept: the self-improved picks, two generation-40 picks, and, in source runs, the largest practice-score jumps and the largest drop; plus one original-coach step.');
      ui.list = EX.h('ul', { 'class': 'fxt-list', 'aria-label': 'Coach transcripts' }, lc);
      D.coach.forEach(function(c){
        var li = EX.h('li', null, ui.list);
        var b = EX.h('button', { type: 'button', 'class': 'fxt-item', tabindex: '-1', 'aria-current': String(c === st.cur.coach) }, li);
        EX.h('span', { 'class': 'l1' }, b, plain(c.run) + ', node ' + c.node);
        EX.h('span', { 'class': 'l2' }, b, coachTag(c));
        b.addEventListener('click', function(){
          st.cur.coach = c; st.cursor = 0;
          markCur(b);
          renderCoachItem();
          EX.select('node', { run: c.run, node: String(c.node), source: NAME });
          writeHash();
        });
      });
      listRoving();
      ui.txcol = EX.h('div', { 'class': 'fxt-txcol' }, B);
      ui.side = EX.h('div', { 'class': 'fxt-sidecol side-panel' }, B);
      renderCoachItem();
      keepCurInView();
    }
    function coachTag(c){
      var w = c.why || '', tags = [];
      if(/I_g pick/.test(w)) tags.push('self-improved pick');
      var m = /extension pick at generation (\d+)/.exec(w); if(m) tags.push('gen ' + m[1] + ' pick');
      if(/jump/.test(w)) tags.push('big jump');
      if(/drop/.test(w)) tags.push('big drop');
      if(/^I_0/.test(w)) tags.push('original coach');
      return genText(c.generation) + (tags.length ? ' · ' + tags.join(', ') : '');
    }
    function renderCoachItem(){
      var c = st.cur.coach, T = ui.txcol, S = ui.side;
      T.innerHTML = ''; S.innerHTML = '';
      var hd = EX.h('div', { 'class': 'fxt-head' }, T);
      EX.h('h4', null, hd, plain(c.run) + ', node ' + c.node);
      EX.h('p', { 'class': 'fxt-why' }, T, 'The coach’s session: the task it was given, its tool calls and what came back. Each turn is clipped to about 900 characters.');
      buildTurns(T, c.segments, true, null);

      var tree = D.trees[c.run];
      var nd = tree && tree.nodes.filter(function(n){ return n.id === String(c.node); })[0];
      var tb = EX.h('table', { 'class': 'kv' }, S), body = EX.h('tbody', null, tb);
      function row(k, v){ var r = EX.h('tr', null, body); EX.h('th', { scope: 'row' }, r, k); EX.h('td', null, r, v); }
      row('Generation', String(genNum(c.generation)));
      row('Practice score', F.pct(c.parent_practice_score, 0) + ' → ' + F.pct(c.practice_score, 0));
      var files = (nd && nd.files_changed) || c.files_changed || [];
      var roles = {}; files.forEach(function(f){ roles[f.role] = true; });
      row('What changed', roles.coach && roles.player ? 'player and coach' : roles.coach ? 'coach' : roles.player ? 'player' : files.length ? 'other files' : 'nothing');
      var acts = EX.h('div', { 'class': 'fxt-acts' }, S);
      if(tree){
        var bt = EX.h('button', { type: 'button', 'class': 'btn small' }, acts, 'Show in tree');
        bt.addEventListener('click', function(){
          if(EX.explore && EX.explore.open) EX.explore.open('tree', { scroll: true });
          EX.select('node', { run: c.run, node: String(c.node), source: NAME });
        });
      }
      if(nd && nd.diff){
        var det = EX.h('details', { 'class': 'more fxt-diffdet' }, S);
        EX.h('summary', null, det, 'Show code change');
        var pre = EX.h('pre', { 'class': 'code diff wrap', tabindex: '0', 'aria-label': 'Code change for node ' + c.node }, det);
        nd.diff.split('\n').forEach(function(l){
          var cls = /^(diff |index |\+\+\+|---|new file|deleted file|similarity|rename|Binary)/.test(l) ? 'meta' : /^@@/.test(l) ? 'hunk' : /^\+/.test(l) ? 'add' : /^-/.test(l) ? 'del' : '';
          EX.h('span', { 'class': 'ln' + (cls ? ' ' + cls : '') }, pre, l || ' ');
        });
      }
    }

    /* ======================= TURNS ======================= */
    function buildTurns(T, segs, isCoach, truth){
      if(st.step){
        var bar = EX.h('div', { 'class': 'fxt-bar', role: 'group', 'aria-label': 'Step through turns' }, T);
        ui.prev = EX.h('button', { type: 'button', 'class': 'btn' }, bar, '‹ Prev');
        ui.next = EX.h('button', { type: 'button', 'class': 'btn' }, bar, 'Next ›');
        ui.pos = EX.h('span', { 'class': 'fxt-pos' }, bar);
        ui.prev.addEventListener('click', function(){ stepBy(-1); });
        ui.next.addEventListener('click', function(){ stepBy(1); });
      }
      var box = EX.h('div', { 'class': 'fxt-tx', tabindex: '0', role: 'region', 'aria-label': (isCoach ? 'Coach' : 'Player') + ' transcript' }, T);
      ui.box = box; ui.turns = [];
      segs.forEach(function(sg){
        var role = sg.role || 'Turn';
        var text = isCoach ? decodeRepr(sg.text) : (sg.text || '');
        var t = { role: role, model: MODEL_ROLES.test(role) };
        if(role === 'Elided'){ t.el = EX.h('div', { 'class': 'turn t-elided' }, box, text.replace(/^\[|\]$/g, '') || 'turns elided'); ui.turns.push(t); return; }
        t.el = EX.h('div', { 'class': 'turn' + (t.model ? ' r-model' : '') + (role === 'Error' ? ' r-error' : '') }, box);
        EX.h('div', { 'class': 'turn-role' }, t.el, roleLabel(role, isCoach));
        var pre = EX.h('pre', { 'class': 'code wrap' }, t.el);
        if(text.trim()) fillText(pre, text); else EX.h('span', { 'class': 'elide' }, pre, '(empty response)');
        if(text.length > 400 || text.split('\n').length > 8){
          var xb = EX.h('button', { type: 'button', 'class': 'xbtn', 'aria-expanded': 'false' }, t.el, 'Expand');
          xb.addEventListener('click', function(){
            var open = t.el.classList.toggle('is-open');
            xb.setAttribute('aria-expanded', String(open)); xb.textContent = open ? 'Collapse' : 'Expand';
          });
        }
        if(!isCoach && t.model){
          var g = parseAnswer(text);
          if(g){
            var inl = EX.h('div', { 'class': 'inl' }, t.el);
            var ok = truth && EX.gridsEqual(g, truth);
            EX.arcGrid(inl, g, { maxSize: 84, diffAgainst: truth, title: 'Answer in this turn',
              label: 'answer in this turn <span class="' + (ok ? 'ok' : 'no') + '">' + (ok ? '✓' : '× ' + EX.esc(diffText(g, truth))) + '</span>' });
          }
        }
        ui.turns.push(t);
      });
      if(st.step){ st.cursor = Math.min(st.cursor, ui.turns.length - 1); applyCursor(); }
    }
    function roleLabel(role, isCoach){
      if(!isCoach){
        return { 'Input': 'Prompt (call 1)', 'Output': 'Model answer (call 1)', 'Refinement input': 'Refine prompt (call 2)', 'Refinement output': 'Model answer (call 2)',
          'Verification input': 'Verify prompt (call 2)', 'Verification output': 'Model answer (call 2)', 'Error': 'Error' }[role] || role;
      }
      return { 'Input': 'Task given to the coach', 'Output': 'Coach', 'Tool output': 'Tool output', 'Nudge': 'Harness nudge' }[role] || role;
    }
    function applyCursor(scroll){
      var n = ui.turns.length, c = st.cursor;
      ui.turns.forEach(function(t, i){ t.el.hidden = i > c; t.el.classList.toggle('is-cur', i === c); });
      ui.pos.textContent = 'Turn ' + (c + 1) + ' of ' + n;
      ui.prev.disabled = c <= 0; ui.next.disabled = c >= n - 1;
      var el = ui.turns[c] && ui.turns[c].el, box = ui.box;
      void box;
      if(scroll && el && el.scrollIntoView) el.scrollIntoView({ block: 'nearest', behavior: EX.reduceMotion ? 'auto' : 'smooth' });
    }
    function stepBy(d){
      if(!ui.turns || !ui.turns.length || !st.step) return;
      st.cursor = Math.max(0, Math.min(ui.turns.length - 1, st.cursor + d));
      applyCursor(true);
      var t = ui.turns[st.cursor];
      if(ui.live) ui.live.textContent = 'Turn ' + (st.cursor + 1) + ' of ' + ui.turns.length + ': ' + roleLabel(t.role, st.tab === 'coach');
    }
  });
})();
