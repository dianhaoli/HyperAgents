/* fig-demo.js — Figure 6, "Inside one coaching round" (mount `demo`).
   A separate, traced re-run of one coaching round, with the model's reasoning summaries saved.
   Two tabs (the puzzle the edit fixed / the puzzle still wrong) and a five-step stepper:
     1 the player tries, 2 the coach reads the misses, 3 the coach thinks and edits,
     4 the player tries again, 5 did it hold up (repeat runs).
   ONE interaction: the stepper (Back / Next, clickable step dots, ←/→ while focus is in the figure).
   Data: demo.json (built by arcexp/build_demo_bundle.py; NOT part of the experiment's results).
   Emits / listens: nothing.
   CSS: assets/fig-demo.css (injected as a <link> if index.html does not already load it). */
(function(){
  'use strict';

  function ensureCSS(){
    if(document.querySelector('link[href*="fig-demo.css"]')) return;
    var l = document.createElement('link'); l.rel = 'stylesheet'; l.href = 'assets/fig-demo.css';
    document.head.appendChild(l);
  }

  var STEPS = [
    { key: 'try',   label: 'The player tries' },
    { key: 'read',  label: 'The coach reads the misses' },
    { key: 'edit',  label: 'The coach thinks and edits' },
    { key: 'again', label: 'The player tries again' },
    { key: 'hold',  label: 'Did it hold up?' }
  ];
  var TABS = [
    { kind: 'fixed', label: 'Fixed by the coach' },
    { kind: 'still_wrong', label: 'Still wrong' }
  ];
  /* Plain-language names for the turns of the traced round. Written by hand from each turn's
     command (shown right below the name), so they are used only for that round. */
  var TURN_NAMES = { c4: {
    1: 'Looks around the code', 2: 'Reads the run log and the code', 3: 'Reads how practice runs are scored',
    4: 'Opens the practice report', 5: 'Skims the failure logs', 6: 'Rewrites the prompt and the second try',
    7: 'Rewords the review instruction', 8: 'Checks that the code still compiles', 9: 'Describes its change',
    10: 'Says it is done'
  } };
  /* One-line reading of what went wrong, written by hand from the player's own summaries; keyed by task. */
  var WRONG_IDEA = {
    b15fca0b: 'In its thoughts the player treats the 1s as maze walls and fills the zeros they enclose. That idea does not match the examples, and the review try kept it.'
  };

  var fmt = EX.fmt;
  function isGrid(g){ return Array.isArray(g) && g.length > 0 && Array.isArray(g[0]); }
  function cellsOff(g, t){
    if(!isGrid(g) || !isGrid(t)) return null;
    if(g.length !== t.length || g[0].length !== t[0].length) return -1;
    var n = 0;
    for(var r = 0; r < g.length; r++) for(var c = 0; c < g[0].length; c++) if(g[r][c] !== t[r][c]) n++;
    return n;
  }
  function plural(n, one, many){ return n + ' ' + (n === 1 ? one : (many || one + 's')); }
  var WORDS = ['no', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten'];
  function word(n){ return WORDS[n] != null ? WORDS[n] : String(n); }
  function cap(s){ return s.charAt(0).toUpperCase() + s.slice(1); }

  /* reasoning summaries use **bold** headings and blank-line paragraphs; everything else is escaped */
  function mdHTML(text){
    return String(text || '').trim().split(/\n\s*\n/).map(function(p){
      var e = EX.esc(p).replace(/\*\*([^*\n]+)\*\*/g, '<b>$1</b>').replace(/\n/g, '<br>');
      return '<p>' + e + '</p>';
    }).join('');
  }

  EX.mount('demo', function(node, ctx){
    ensureCSS();
    node.innerHTML = '';
    var st = { tab: 0, step: 0 };
    var D = null;

    var root = EX.h('div', { 'class': 'fx-demo' }, node);
    var tabsEl = EX.h('div', { 'class': 'tabs fxd-tabs', role: 'tablist', 'aria-label': 'Which puzzle' }, root);
    var stageId = EX.uid('fxd-stage');
    var tabBtns = TABS.map(function(t, i){
      var b = EX.h('button', { type: 'button', role: 'tab', id: stageId + '-tab' + i, 'aria-controls': stageId,
        'aria-selected': i === 0 ? 'true' : 'false', tabindex: i === 0 ? '0' : '-1' }, tabsEl, t.label);
      b.addEventListener('click', function(){ setTab(i, false); });
      return b;
    });
    tabsEl.addEventListener('keydown', function(e){
      if(e.key !== 'ArrowRight' && e.key !== 'ArrowLeft' && e.key !== 'Home' && e.key !== 'End') return;
      e.preventDefault(); e.stopPropagation();
      var i = e.key === 'Home' ? 0 : e.key === 'End' ? TABS.length - 1 : (st.tab + (e.key === 'ArrowRight' ? 1 : -1) + TABS.length) % TABS.length;
      setTab(i, true);
    });

    var stepper = EX.h('ol', { 'class': 'fxd-steps', 'aria-label': 'Steps' }, root);
    var stepBtns = STEPS.map(function(s, i){
      var li = EX.h('li', { 'class': 'fxd-stepli' }, stepper);
      var b = EX.h('button', { type: 'button', 'class': 'fxd-stepbtn', 'aria-label': 'Step ' + (i + 1) + ': ' + s.label }, li);
      EX.h('span', { 'class': 'fxd-num', 'aria-hidden': 'true' }, b, String(i + 1));
      EX.h('span', { 'class': 'fxd-steplab', 'aria-hidden': 'true' }, b, s.label);
      b.addEventListener('click', function(){ go(i, false); });
      return b;
    });

    var stage = EX.h('div', { 'class': 'fxd-stage', id: stageId, role: 'tabpanel', tabindex: '0',
      'aria-labelledby': stageId + '-tab0' }, root);
    var stageHead = EX.h('div', { 'class': 'fxd-stagehead', 'aria-live': 'polite' }, stage);
    var body = EX.h('div', { 'class': 'fxd-body' }, stage);
    EX.h('div', { 'class': 'fxd-wait' }, body, 'Loading the traced run…');

    var nav = EX.h('div', { 'class': 'fxd-nav' }, root);
    var back = EX.h('button', { type: 'button', 'class': 'btn quiet fxd-back' }, nav, '← Back');
    var next = EX.h('button', { type: 'button', 'class': 'btn primary big fxd-next' }, nav, 'Next →');
    back.addEventListener('click', function(){ go(st.step - 1, true); });
    next.addEventListener('click', function(){
      if(st.step < STEPS.length - 1) return go(st.step + 1, true);
      if(st.tab < TABS.length - 1){ st.step = 0; setTab(st.tab + 1, false); bringIntoView(); }
      else { st.tab = 0; setTab(0, false); go(0, true); }
    });

    root.addEventListener('keydown', function(e){
      if(e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
      if(e.altKey || e.ctrlKey || e.metaKey) return;
      var tag = (e.target.tagName || '').toLowerCase();
      if(tag === 'input' || tag === 'select' || tag === 'textarea' || e.target.closest('[role=tablist]')) return;
      e.preventDefault();
      go(st.step + (e.key === 'ArrowRight' ? 1 : -1), false);
    });

    function bringIntoView(){
      var r = root.getBoundingClientRect();
      if(r.top < 0) root.scrollIntoView({ block: 'start', behavior: EX.reduceMotion ? 'auto' : 'smooth' });
    }
    function setTab(i, focus){
      st.tab = i;
      tabBtns.forEach(function(b, j){
        b.setAttribute('aria-selected', j === i ? 'true' : 'false');
        b.setAttribute('tabindex', j === i ? '0' : '-1');
      });
      stage.setAttribute('aria-labelledby', tabBtns[i].id);
      if(focus) tabBtns[i].focus();
      render();
    }
    function go(i, fromButton){
      if(i < 0 || i >= STEPS.length) return;
      var hadFocusInStage = stage.contains(document.activeElement);
      st.step = i;
      render();
      if(hadFocusInStage && !stage.contains(document.activeElement)) stage.focus({ preventScroll: true });
      if(fromButton) bringIntoView();
    }

    function sizes(){
      var w = Math.max(280, root.clientWidth || ctx.width() || 336);
      return { w: w, narrow: w < 680, ex: w < 680 ? Math.max(56, Math.min(84, Math.floor((w - 40) / 4))) : 92,
        big: w < 680 ? Math.min(200, Math.floor((w - 24) / 2)) : 190 };
    }

    /* ---------- shared pieces ---------- */
    function thoughts(parent, text, opts){
      opts = opts || {};
      var wrap = EX.h('div', { 'class': 'fxd-thought' }, parent);
      EX.h('div', { 'class': 'fxd-lbl' }, wrap, opts.label || 'Its thoughts');
      if(!text || !String(text).trim()){
        EX.h('div', { 'class': 'fxd-none' }, wrap, 'No summary came back for this call.');
        return wrap;
      }
      var box = EX.h('div', { 'class': 'fxd-tbody', html: mdHTML(text) }, wrap);
      if(opts.lines) box.style.maxHeight = 'calc(' + opts.lines + ' * 1.55em)';
      var btn = EX.h('button', { type: 'button', 'class': 'btn quiet small fxd-readall', 'aria-expanded': 'false' }, wrap, 'Read all');
      if(box.scrollHeight <= box.clientHeight + 2){ btn.remove(); box.classList.add('fits'); return wrap; }
      var words = String(text).trim().split(/\s+/).length;
      btn.textContent = 'Read all (' + fmt.int(words) + ' words)';
      btn.addEventListener('click', function(){
        var open = box.classList.toggle('open');
        btn.setAttribute('aria-expanded', open ? 'true' : 'false');
        btn.textContent = open ? 'Show less' : 'Read all (' + fmt.int(words) + ' words)';
        if(opts.lines) box.style.maxHeight = open ? '' : 'calc(' + opts.lines + ' * 1.55em)';
        if(open){ box.setAttribute('tabindex', '0'); box.setAttribute('aria-label', 'Thoughts, full text'); }
        else { box.removeAttribute('tabindex'); box.scrollTop = 0; }
      });
      return wrap;
    }
    function codeBlock(parent, text, cls, label){
      var pre = EX.h('pre', { 'class': 'code wrap fxd-code ' + (cls || ''), tabindex: '0', 'aria-label': label || 'Code' }, parent);
      pre.textContent = text;
      return pre;
    }
    function collapse(parent, label, build){
      var d = EX.h('details', { 'class': 'fxd-coll' }, parent);
      EX.h('summary', null, d, label);
      var b = EX.h('div', { 'class': 'fxd-collbody' }, d);
      var built = false;
      d.addEventListener('toggle', function(){ if(d.open && !built){ built = true; build(b); } });
      return d;
    }
    function verdictText(call, i, calls, truth){
      var g = call.parsed_grid;
      if(!isGrid(g)) return { ok: false, text: '× no answer' };
      if(call.parsed_correct) return { ok: true, text: '✓ correct' };
      if(i > 0 && EX.gridsEqual(g, calls[0].parsed_grid)) return { ok: false, text: '× same as try 1, so not sent again' };
      var n = cellsOff(g, truth);
      if(n === -1) return { ok: false, text: '× wrong size' };
      return { ok: false, text: '× ' + plural(n, 'cell') + ' off' };
    }

    function examples(parent, P, z){
      var ex = EX.h('div', { 'class': 'fxd-examples' }, parent);
      P.train.forEach(function(p, k){
        var it = EX.h('div', { 'class': 'fxd-ex' }, ex);
        EX.h('div', { 'class': 'fxd-lbl' }, it, 'Example ' + (k + 1));
        EX.arcPair(it, p.input, p.output, { maxSize: z.ex, maxCell: 12 });
      });
    }
    function testRow(parent, P, z){
      var row = EX.h('div', { 'class': 'fxd-test' }, parent);
      var t = P.test[0];
      var a = EX.h('div', { 'class': 'fxd-gridcol' }, row);
      EX.h('div', { 'class': 'fxd-lbl' }, a, 'Test input');
      EX.arcGrid(a, t.input, { maxSize: z.narrow ? z.big - 8 : 130, maxCell: 14, title: 'Test input' });
      EX.h('span', { 'class': 'arc-arrow fxd-arrow', 'aria-hidden': 'true' }, row, '→');
      var b = EX.h('div', { 'class': 'fxd-gridcol' }, row);
      EX.h('div', { 'class': 'fxd-lbl' }, b, 'Correct answer');
      EX.arcGrid(b, t.output, { maxSize: z.narrow ? z.big - 8 : 130, maxCell: 14, title: 'Correct answer' });
    }

    function attempt(parent, side, P, z, isAfter){
      var truth = P.test[0].output;
      var calls = side.calls || [];
      var solvedOn = null;
      calls.forEach(function(c, i){ if(solvedOn == null && c.parsed_correct) solvedOn = i + 1; });
      var res = EX.h('div', { 'class': 'fxd-result' }, parent);
      if(side.solved) EX.h('span', { 'class': 'ok' }, res, '✓ Solved' + (solvedOn ? ' on try ' + solvedOn : ''));
      else EX.h('span', { 'class': 'no' }, res, '× Not solved: ' + (calls.length > 1 ? 'both tries wrong' : 'the try was wrong'));

      calls.forEach(function(c, i){
        var row = EX.h('div', { 'class': 'fxd-call' }, parent);
        var isReview = /A previous attempt proposed/.test(c.prompt_summary || '');
        var head = EX.h('div', { 'class': 'fxd-callhead' }, row);
        EX.h('span', { 'class': 'fxd-callname' }, head, 'Try ' + (i + 1) + (isReview ? ': a review of try 1' : ''));
        if(c.seconds != null) EX.h('span', { 'class': 'fxd-callmeta' }, head, 'thought for ' + fmt.secs(c.seconds));
        var cols = EX.h('div', { 'class': 'fxd-callcols' }, row);
        var right = EX.h('div', { 'class': 'fxd-callright' }, cols);
        var left = EX.h('div', { 'class': 'fxd-callleft' }, cols);
        thoughts(left, c.reasoning_summary, { label: 'Its thoughts' });
        EX.h('div', { 'class': 'fxd-lbl' }, right, 'Its answer');
        EX.arcGrid(right, c.parsed_grid, { maxSize: z.narrow ? z.big - 8 : 150, maxCell: 14,
          diffAgainst: truth, title: 'Try ' + (i + 1) + ' answer', emptyText: 'no answer' });
        var v = verdictText(c, i, calls, truth);
        EX.h('div', { 'class': 'fxd-verdict ' + (v.ok ? 'ok' : 'no') }, right, v.text);
      });
      if(!calls.length) EX.h('div', { 'class': 'empty' }, parent, 'No model calls were recorded for this run.');
    }

    /* ---------- the five steps ---------- */
    function stepTry(P, z){
      head('The player sees the examples and the test input, then gets two tries. Wrong cells are outlined.');
      examples(body, P, z);
      testRow(body, P, z);
      attempt(body, P.before, P, z, false);
    }

    function stepRead(P, z){
      var CR = D.coach_round, rep = CR.baseline_report || {};
      var per = rep.per_task_score || {}, ids = Object.keys(per);
      var nSolved = ids.filter(function(k){ return per[k] >= 1; }).length;
      head('Before editing, the coach gets the practice report: which puzzles the player solved and a log of each miss.');
      var sec = EX.h('div', { 'class': 'fxd-sec' }, body);
      EX.h('div', { 'class': 'fxd-subh' }, sec, 'The practice report: ' + nSolved + ' of ' + ids.length + ' puzzles solved');
      var strip = EX.h('ul', { 'class': 'fxd-strip', 'aria-label': 'Practice puzzles, solved or missed' }, sec);
      ids.forEach(function(k){
        var ok = per[k] >= 1, me = k === P.task;
        var li = EX.h('li', { 'class': 'fxd-cell ' + (ok ? 'ok' : 'no') + (me ? ' me' : ''),
          'aria-label': (me ? 'This puzzle: ' : 'Puzzle ' + k + ': ') + (ok ? 'solved' : 'missed') }, strip);
        EX.h('span', { 'aria-hidden': 'true' }, li, ok ? '✓' : '×');
      });
      EX.h('div', { 'class': 'fxd-striplab' }, sec, 'The outlined square is this puzzle.');

      var shown = CR.baseline_failures_shown || [], read = CR.baseline_failures_read || [];
      var tIdx = -1;
      (CR.turns || []).forEach(function(t, i){ if(tIdx < 0 && /chat_history/.test(t.tool_command || '')) tIdx = i; });
      var T = tIdx >= 0 ? CR.turns[tIdx] : null;
      var sec2 = EX.h('div', { 'class': 'fxd-sec' }, body);
      EX.h('div', { 'class': 'fxd-subh' }, sec2, 'What it looked at');
      var txt = 'Each of the ' + shown.length + ' missed puzzles, this one included, has a log of the player\'s prompt and answers. ';
      if(T){
        var m1 = /head -(\d+)/.exec(T.tool_command), m2 = /cut -c1-(\d+)/.exec(T.tool_command);
        txt += 'The coach opened ' + (read.length === shown.length ? 'all ' + read.length : read.length + ' of them') +
          ' in one command (turn ' + T.turn + '), but printed only the first ' + (m1 ? m1[1] + ' ' : '') +
          'prompt, answer and error lines of each' + (m2 ? ', cut to ' + m2[1] + ' characters' : '') +
          '. It never read a log in full.';
      } else {
        txt += 'No command that opened these logs was found in the trace.';
      }
      EX.h('p', { 'class': 'fxd-p' }, sec2, txt);
      if(T){
        thoughts(sec2, T.reasoning_summary, { label: 'Its thoughts in that turn' });
        EX.h('div', { 'class': 'fxd-lbl fxd-mt' }, sec2, 'The command it ran');
        codeBlock(sec2, T.tool_command, 'fxd-cmd', 'Command in turn ' + T.turn);
        collapse(sec2, 'Show what the command printed', function(b){
          if(T.tool_output_note) EX.h('div', { 'class': 'fxd-note' }, b, 'Shortened here: ' + T.tool_output_note + '. The coach saw all of it.');
          codeBlock(b, T.tool_output || '', 'fxd-out', 'Output of turn ' + T.turn);
        });
      }
    }

    function stepEdit(P, z){
      var CR = D.coach_round, turns = CR.turns || [];
      var names = TURN_NAMES[CR.round] || {};
      head('The coach edits the player\'s code. First what it changed, then how it got there.');

      var sec = EX.h('div', { 'class': 'fxd-sec fxd-edit' }, body);
      EX.h('div', { 'class': 'fxd-subh' }, sec, 'What it changed');
      var summary = String(CR.editor_summary || '').replace(/^Editor's summary:\s*/i, '');
      EX.h('p', { 'class': 'fxd-p fxd-summary' }, sec, summary ? cap(summary) : 'No summary of the edit was written.');
      EX.h('div', { 'class': 'fxd-src' }, sec, 'Our plain-language summary of the code change.');
      if(CR.practice_score_before != null && CR.practice_score_after_child_eval != null){
        EX.h('p', { 'class': 'fxd-p' }, sec, 'Practice score before the edit: ' + fmt.pct(CR.practice_score_before, 0) +
          '. After it, in the round\'s own practice check: ' + fmt.pct(CR.practice_score_after_child_eval, 0) + '.');
      }
      EX.more(sec, 'Show code change', function(b){
        var pre = EX.h('pre', { 'class': 'code diff tall fxd-diff', tabindex: '0', 'aria-label': 'Code change' }, b);
        String(CR.diff || '').split('\n').forEach(function(line){
          var cls = /^(\+\+\+|---|diff |index )/.test(line) ? 'meta' : line[0] === '+' ? 'add' : line[0] === '-' ? 'del' : line.indexOf('@@') === 0 ? 'hunk' : '';
          EX.h('span', { 'class': 'ln ' + cls }, pre, line || ' ');
        });
      });

      var sec2 = EX.h('div', { 'class': 'fxd-sec' }, body);
      EX.h('div', { 'class': 'fxd-subh' }, sec2, 'How it got there, in ' + turns.length + ' turns');
      EX.h('p', { 'class': 'fxd-p fxd-quiet' }, sec2, 'In each turn the coach thinks, then may run one command on the player\'s code.');
      var tl = EX.h('ol', { 'class': 'fxd-timeline' }, sec2);
      turns.forEach(function(t){
        var li = EX.h('li', { 'class': 'fxd-turn' }, tl);
        EX.h('div', { 'class': 'fxd-turnh' }, li, 'Turn ' + t.turn + (names[t.turn] ? ': ' + names[t.turn] : ''));
        if(t.reasoning_summary && t.reasoning_summary.trim()) thoughts(li, t.reasoning_summary, { lines: 4 });
        else EX.h('div', { 'class': 'fxd-none' }, li, 'No thought summary came back for this turn.');
        if(t.visible_message && t.visible_message.trim()){
          EX.h('div', { 'class': 'fxd-lbl fxd-mt' }, li, 'It wrote');
          EX.h('div', { 'class': 'fxd-said' }, li, t.visible_message.trim());
        }
        if(t.tool_command){
          collapse(li, t.tool_output ? 'Show the command and what it printed' : 'Show the command', function(b){
            EX.h('div', { 'class': 'fxd-lbl' }, b, 'The command it ran');
            codeBlock(b, t.tool_command, 'fxd-cmd', 'Command in turn ' + t.turn);
            if(t.tool_output){
              EX.h('div', { 'class': 'fxd-lbl fxd-mt' }, b, 'What it printed' + (t.tool_output_note ? ' (shortened here: ' + t.tool_output_note + '; the coach saw all of it)' : ''));
              codeBlock(b, t.tool_output, 'fxd-out', 'Output of turn ' + t.turn);
            }
          });
        } else if(t.next_input_kind === 'harness_nudge' && t.tool_output){
          collapse(li, 'Show the reminder it got back (it ran no command)', function(b){
            codeBlock(b, t.tool_output, 'fxd-out', 'Reminder after turn ' + t.turn);
          });
        } else if(t.next_input_kind == null){
          EX.h('div', { 'class': 'fxd-none' }, li, 'The round ends here.');
        }
      });

      var others = D.other_rounds || [];
      if(others.length){
        var broke = others.filter(function(o){ return o.patch_bytes > 0 && o.practice_score_after_child_eval === 0; });
        var none = others.filter(function(o){ return !o.patch_bytes; });
        var bits = [];
        if(none.length) bits.push(word(none.length) + ' made no edit');
        if(broke.length) bits.push(word(broke.length) + ' broke the player so that it scored 0');
        EX.h('p', { 'class': 'fxd-p fxd-quiet' }, body, 'We ran ' + word(others.length + 1) + ' coaching rounds for this demo. Of the other ' +
          word(others.length) + ', ' + bits.join(' and ') + '. This is the only one that changed the player without breaking it.');
      }
    }

    function stepAgain(P, z){
      head('The edited player gets the same puzzle and the same two tries.');
      var review = null;
      (P.after.calls || []).forEach(function(c){
        var m = /(A previous attempt proposed[\s\S]*)$/.exec(c.prompt_summary || '');
        if(m && !review) review = m[1].replace(/\[grid \d+x\d+\]/, '[its first answer]').trim();
      });
      if(review){
        var q = EX.h('div', { 'class': 'fxd-sec fxd-review' }, body);
        EX.h('div', { 'class': 'fxd-lbl' }, q, 'New since the edit: try 2 is a review. Its prompt ends with');
        EX.h('blockquote', { 'class': 'fxd-quote' }, q, review);
      }
      testRow(body, P, z);
      attempt(body, P.after, P, z, true);
      if(WRONG_IDEA[P.task] && !P.after.solved) EX.h('p', { 'class': 'fxd-p fxd-why' }, body, WRONG_IDEA[P.task]);
    }

    function stepHold(P, z){
      var R = P.repeats || {};
      head('Runs are not deterministic: the same player can solve a puzzle once and miss it the next time. So we ran each player on this puzzle ' + word(R.A0_runs || 0) + ' more times.');
      function runsOf(main, detail){
        var out = [{ solved: !!main.solved, label: 'Run shown', calls: main.calls || [] }];
        (detail || []).forEach(function(r, i){ out.push({ solved: !!r.solved, label: 'Repeat ' + (i + 1), calls: r.calls || [] }); });
        return out;
      }
      var rows = [
        { name: 'Before coaching', runs: runsOf(P.before, R.A0_runs_detail) },
        { name: 'After coaching', runs: runsOf(P.after, R.edited_runs_detail) }
      ];
      var tbl = EX.h('div', { 'class': 'fxd-hold' }, body);
      rows.forEach(function(row){
        var k = row.runs.filter(function(r){ return r.solved; }).length;
        var line = EX.h('div', { 'class': 'fxd-holdrow' }, tbl);
        var nm = EX.h('div', { 'class': 'fxd-holdname' }, line);
        EX.h('div', { 'class': 'fxd-subh' }, nm, row.name);
        EX.h('div', { 'class': 'fxd-holdk' }, nm, 'solved in ' + k + ' of ' + row.runs.length + ' runs');
        var marks = EX.h('ul', { 'class': 'fxd-runs' }, line);
        row.runs.forEach(function(r){
          var li = EX.h('li', { 'class': 'fxd-run' }, marks);
          EX.h('span', { 'class': 'fxd-runmark ' + (r.solved ? 'ok' : 'no'), 'aria-hidden': 'true' }, li, r.solved ? '✓' : '×');
          EX.h('span', { 'class': 'fxd-runlab' }, li, r.label);
          EX.h('span', { 'class': 'sr-only fxd-sr' }, li, r.solved ? ': solved' : ': not solved');
        });
        row.k = k;
      });

      var a = rows[0], b = rows[1];
      var reviewFixes = b.runs.filter(function(r){
        return r.solved && r.calls.length > 1 && r.calls[0].parsed_correct === false && r.calls[1].parsed_correct === true;
      }).length;
      var sent = 'Before coaching, the player solved this puzzle in ' + a.k + ' of ' + a.runs.length + ' runs; after coaching, in ' + b.k + ' of ' + b.runs.length + '.';
      if(b.k > 0 && reviewFixes === b.k) sent += ' Every one of the edited player\'s solves came the same way: try 1 was wrong and the review in try 2 fixed it.';
      else if(b.k === 0) sent += ' The review try did not help on this puzzle.';
      EX.h('p', { 'class': 'fxd-p fxd-holdtext' }, body, sent);
      EX.h('p', { 'class': 'fxd-p fxd-quiet' }, body, 'Four runs each is a small sample, and these two puzzles were picked to illustrate, so they show how the edit works, not whether it helps on average.'
        .replace('Four', cap(word(a.runs.length))));
      var M = D.meta || {};
      if(M.demo_cost_usd_total != null) EX.h('p', { 'class': 'fxd-src' }, body, 'This traced demo cost ' + fmt.usd(M.demo_cost_usd_total) + ' in model calls. It is not part of the experiment\'s results.');
    }

    var headEl = null;
    function head(text){ headEl.textContent = text; }

    function render(){
      var z = sizes();
      root.classList.toggle('narrow', z.narrow);
      stepBtns.forEach(function(b, i){
        if(i === st.step) b.setAttribute('aria-current', 'step'); else b.removeAttribute('aria-current');
        b.classList.toggle('done', i < st.step);
      });
      back.disabled = st.step === 0;
      next.textContent = st.step < STEPS.length - 1 ? 'Next: ' + STEPS[st.step + 1].label.toLowerCase().replace(/^the /, '') + ' →'
        : (st.tab < TABS.length - 1 ? 'See the puzzle that stayed wrong →' : 'Back to the start');
      if(z.narrow && st.step < STEPS.length - 1) next.textContent = 'Next step →';
      stageHead.innerHTML = '';
      EX.h('div', { 'class': 'fxd-stepnum' }, stageHead, 'Step ' + (st.step + 1) + ' of ' + STEPS.length);
      EX.h('div', { 'class': 'fxd-steptitle' }, stageHead, STEPS[st.step].label);
      headEl = EX.h('p', { 'class': 'fxd-lead' }, stageHead);
      body.innerHTML = '';
      if(!D) return;
      var P = D.puzzles.filter(function(p){ return p.kind === TABS[st.tab].kind; })[0];
      if(!P){ EX.h('div', { 'class': 'empty' }, body, 'This puzzle is missing from demo.json.'); return; }
      [stepTry, stepRead, stepEdit, stepAgain, stepHold][st.step](P, z);
    }

    var lastW = 0;
    ctx.onResize(function(){ var w = root.clientWidth; if(w !== lastW){ lastW = w; render(); } });

    return EX.load('demo').then(function(d){
      D = d;
      lastW = root.clientWidth;
      render();
    });
  });
})();
