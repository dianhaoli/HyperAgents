/* fig-audit.js — Figure 8, "What the coaches changed": the diff audit of every picked coach.
   Top left: hunks as a stacked bar (general vs ARC-specific), overall and per source run (click a run to filter).
   Top right: self-edit rate per source seed (generations that edited coach code; how many became parents).
   Below: filterable table of the 32 audited hunks, grouped by distinct coach node (one node can be picked
   several times), each row expandable to the judges' full reason and the audited hunk text (coach code vs I_0).
   Data: summary.json (diff_audit_summary, self_edit), trees.json (trees[source].diff_audit[] incl. node + text,
   nodes[], and pay-off / extension runs' coach_origin + final for exam scores).
   Emits: select-node {run, node} ("Select in Fig 5"). Listens: select-node, select-run (marks a group quietly).
   Hash: #audit?run=…&node=… (restored at init). */
(function(){
  'use strict';

  var PICK_ORDER = { Ig: 0, g6: 1, g20: 2, g30: 3, g40: 4 };
  var RUN_RE = /^source_s(\d+)$/;

  function parsePick(pick){
    // "A_gen12:source_s3" -> {kind:'Ig', run:'source_s3'} ; "ext:source_s4_g30" -> {kind:'g30', gen:30, run:'source_s4'}
    var m = /^A_gen12:(source_s\d+)$/.exec(pick);
    if(m) return { kind: 'Ig', run: m[1], gen: null };
    m = /^ext:(source_s\d+)_g(\d+)$/.exec(pick);
    if(m) return { kind: 'g' + m[2], run: m[1], gen: +m[2] };
    return { kind: pick, run: null, gen: null };
  }
  function pickHTML(p){ return p.kind === 'Ig' ? 'I<sub>g</sub>' : 'gen ' + p.gen; }
  function pickText(p){ return p.kind === 'Ig' ? 'I_g' : 'gen ' + p.gen; }
  function seedLabel(run){ var m = RUN_RE.exec(run); return m ? 's' + m[1] : run; }

  EX.mount('audit', function(node, ctx){
    node.innerHTML = '';
    return EX.loadAll(['summary', 'trees']).then(function(res){
      var S = res[0], TR = res[1], T = TR.trees, F = EX.fmt;
      var sourceRuns = TR.runs.filter(function(r){ return T[r] && T[r].kind === 'source'; });

      /* ---------- the run that tested each pick (pay-off I_g or extension) ---------- */
      function testedBy(p){
        var rid = p.kind === 'Ig' ? 'payoff_Ig_' + p.run : 'ext_' + p.run + '_' + p.kind;
        return T[rid] ? rid : null;
      }
      function nodeOf(run, id){
        var ns = T[run].nodes; for(var i = 0; i < ns.length; i++) if(ns[i].id === id) return ns[i];
        return null;
      }

      /* ---------- rows and groups ---------- */
      var rows = [], groups = [], gIndex = {};
      sourceRuns.forEach(function(run){
        (T[run].diff_audit || []).forEach(function(a){
          var p = parsePick(a.pick);
          var nid = a.node != null ? String(a.node) : null;
          var tested = testedBy(p);
          var r = {
            id: 'h' + rows.length, run: run, pick: p, file: a.file, idx: a.idx, tag: a.tag,
            arc: a.tag === 'ARC-specific', agreement: a.agreement, reason: a.reason || '', text: a.text || null,
            node: nid, tested: tested,
            exam: tested && T[tested].final ? T[tested].final.heldout : null,
            unedited: !!(tested && T[tested].final && T[tested].final.final_node === 'initial')
          };
          rows.push(r);
          var gk = run + '|' + (nid || a.pick);
          var g = gIndex[gk];
          if(!g){
            var nd = nid ? nodeOf(run, nid) : null;
            g = gIndex[gk] = { key: gk, run: run, node: nid, gen: nd ? nd.generation : null, picks: [], rows: [] };
            groups.push(g);
          }
          if(g.picks.indexOf(a.pick) < 0) g.picks.push(a.pick);
          g.rows.push(r);
        });
      });
      function pickSort(a, b){ return PICK_ORDER[a.pick.kind] - PICK_ORDER[b.pick.kind] || a.idx - b.idx; }
      groups.forEach(function(g){
        g.rows.sort(pickSort);
        g.picks.sort(function(a, b){ return PICK_ORDER[parsePick(a).kind] - PICK_ORDER[parsePick(b).kind]; });
      });
      groups.sort(function(a, b){
        return sourceRuns.indexOf(a.run) - sourceRuns.indexOf(b.run) ||
          Math.min.apply(null, a.rows.map(function(r){ return PICK_ORDER[r.pick.kind]; })) -
          Math.min.apply(null, b.rows.map(function(r){ return PICK_ORDER[r.pick.kind]; }));
      });

      var SUM = S.diff_audit_summary || {};
      var nArc = rows.filter(function(r){ return r.arc; }).length;
      var nGen = rows.length - nArc;
      if(SUM.hunks != null && SUM.hunks !== rows.length && window.console) console.warn('[audit] diff_audit rows', rows.length, '!= summary.hunks', SUM.hunks);
      var nPicks = 0; groups.forEach(function(g){ nPicks += g.picks.length; });

      /* ---------- state ---------- */
      var state = { tag: 'all', run: 'all', order: 'arc', open: {}, marked: null };
      groups.forEach(function(g, i){ g.runOrder = i; g.hasArc = g.rows.some(function(r){ return r.arc; }); });
      function orderedGroups(){
        if(state.order !== 'arc') return groups;
        return groups.slice().sort(function(a, b){ return (b.hasArc - a.hasArc) || (a.runOrder - b.runOrder); });
      }
      rows.forEach(function(r){ if(r.arc) state.open[r.id] = true; });   // at rest: the ARC-specific hunks are open

      var root = EX.h('div', { 'class': 'fx-audit' }, node);

      /* =============== top: two small charts =============== */
      var top = EX.h('div', { 'class': 'fa-top' }, root);

      // ---- (a) hunks: general vs ARC-specific ----
      var A = EX.h('div', { 'class': 'fa-block' }, top);
      EX.h('div', { 'class': 'fig-sub-title' }, A, 'Audited hunks: general vs ARC-specific');
      EX.h('p', { 'class': 'fig-sub-text' }, A,
        rows.length + ' changed hunks across ' + nPicks + ' picked coaches (' + groups.length + ' distinct coach nodes). Click a run to filter the table.');

      var tot = EX.h('div', { 'class': 'fa-total' }, A);
      var totBar = EX.h('div', { 'class': 'fa-bar', role: 'img',
        'aria-label': nGen + ' general hunks and ' + nArc + ' ARC-specific hunks out of ' + rows.length }, tot);
      EX.h('span', { 'class': 'fa-seg gen', style: { flexGrow: String(nGen) } }, totBar);
      EX.h('span', { 'class': 'fa-seg arc', style: { flexGrow: String(nArc) } }, totBar);
      var totLab = EX.h('div', { 'class': 'fa-total-lab' }, tot);
      totLab.innerHTML = '<span><i class="fa-key gen"></i><b>' + F.int(nGen) + '</b> general</span>' +
        '<span><i class="fa-key arc"></i><b>' + F.int(nArc) + '</b> ARC-specific</span>' +
        '<span class="fa-muted">of ' + F.int(rows.length) + ' · ' + EX.esc(F.pct(rows.length ? nArc / rows.length : 0)) + ' ARC-specific</span>';

      var perRun = EX.h('div', { 'class': 'fa-runs', role: 'group', 'aria-label': 'Filter by source run' }, A);
      var maxRun = 1;
      var runCounts = sourceRuns.map(function(run){
        var rs = rows.filter(function(r){ return r.run === run; });
        var c = { run: run, n: rs.length, arc: rs.filter(function(r){ return r.arc; }).length,
          picks: groups.filter(function(g){ return g.run === run; }).reduce(function(s, g){ return s + g.picks.length; }, 0) };
        maxRun = Math.max(maxRun, c.n); return c;
      });
      var runBtns = {};
      runCounts.forEach(function(c){
        var b = EX.h('button', { type: 'button', 'class': 'fa-run', 'aria-pressed': 'false',
          'aria-label': c.run + ': ' + c.n + ' hunks from ' + c.picks + ' picks, ' + c.arc + ' ARC-specific. Filter table to this run.' }, perRun);
        EX.h('span', { 'class': 'fa-run-name' }, b, seedLabel(c.run));
        var track = EX.h('span', { 'class': 'fa-run-track' }, b);
        for(var i = 0; i < c.n; i++){
          EX.h('span', { 'class': 'fa-unit ' + (i >= c.n - c.arc ? 'arc' : 'gen') }, track);
        }
        if(!c.n) EX.h('span', { 'class': 'fa-none' }, track, 'no picks');
        // reserve space so tracks align (units share one scale across runs)
        track.style.minWidth = 'calc(' + maxRun + ' * var(--fa-u) + ' + (maxRun - 1) + ' * var(--fa-gap))';
        EX.h('span', { 'class': 'fa-run-n' }, b, c.n + (c.arc ? ' · ' + c.arc + ' ARC' : ''));
        b.addEventListener('click', function(){ setRun(state.run === c.run ? 'all' : c.run); });
        runBtns[c.run] = b;
      });
      EX.h('div', { 'class': 'fa-legend' }, A).innerHTML =
        'One square per hunk. A coach picked twice is audited twice, so its hunks count twice.';

      // ---- (b) self-edit rate per source seed ----
      var B = EX.h('div', { 'class': 'fa-block' }, top);
      var SE = S.self_edit || {};
      var seRuns = sourceRuns.filter(function(r){ return SE[r]; });
      var seTot = { gens: 0, ed: 0, par: 0 };
      seRuns.forEach(function(r){ seTot.gens += SE[r].gens; seTot.ed += SE[r].self_edit_gens; seTot.par += SE[r].self_edit_parents; });
      var maxGens = Math.max.apply(null, seRuns.map(function(r){ return SE[r].gens; }).concat([1]));
      EX.h('div', { 'class': 'fig-sub-title' }, B, 'How often the coach edited its own code');
      EX.h('p', { 'class': 'fig-sub-text' }, B,
        'First ' + maxGens + ' generations of each source run: ' + seTot.ed + ' of ' + seTot.gens +
        ' generations (' + F.pct(seTot.gens ? seTot.ed / seTot.gens : 0, 0) + ') changed coach code; ' +
        seTot.par + ' of those were later built on.');
      var seList = EX.h('div', { 'class': 'fa-se', role: 'img',
        'aria-label': seRuns.map(function(r){ return r + ': ' + SE[r].self_edit_gens + ' of ' + SE[r].gens + ' generations edited coach code, ' + SE[r].self_edit_parents + ' became parents'; }).join('; ') }, B);
      seRuns.forEach(function(r){
        var v = SE[r];
        var row = EX.h('div', { 'class': 'fa-se-row' }, seList);
        EX.h('span', { 'class': 'fa-run-name' }, row, seedLabel(r));
        var track = EX.h('span', { 'class': 'fa-se-track' }, row);
        for(var i = 0; i < v.gens; i++){
          var cls = i < v.self_edit_parents ? 'par' : (i < v.self_edit_gens ? 'ed' : 'no');
          EX.h('span', { 'class': 'fa-cell ' + cls }, track);
        }
        EX.h('span', { 'class': 'fa-se-n' }, row).innerHTML = '<b>' + v.self_edit_gens + '</b>/' + v.gens +
          ' <span class="fa-muted">· ' + v.self_edit_parents + ' parent' + (v.self_edit_parents === 1 ? '' : 's') + '</span>';
      });
      EX.h('div', { 'class': 'fa-legend' }, B).innerHTML =
        '<span><i class="fa-cell par"></i>edited coach code, became a parent</span>' +
        '<span><i class="fa-cell ed"></i>edited coach code, no children</span>' +
        '<span><i class="fa-cell no"></i>no coach edit</span>' +
        '<span class="fa-muted">Counts per seed, not generation positions.</span>';

      /* =============== controls =============== */
      var ctr = EX.h('div', { 'class': 'controls fa-controls' }, root);
      var tagSeg = EX.seg(ctr, [
        { value: 'all', label: 'All ' + rows.length },
        { value: 'arc', label: 'ARC-specific ' + nArc },
        { value: 'gen', label: 'General ' + nGen }
      ], 'all', function(v){ state.tag = v; renderTable(); }, { label: 'Tag' });
      var runOpts = [{ value: 'all', label: 'All source runs' }].concat(sourceRuns.map(function(r){ return { value: r, label: r }; }));
      var orderSeg = EX.seg(ctr, [
        { value: 'arc', label: 'ARC-specific first' },
        { value: 'run', label: 'By run' }
      ], 'arc', function(v){ state.order = v; renderTable(); listWrap.scrollTop = 0; }, { label: 'Order' });
      var runSel = EX.selectBox(ctr, runOpts, 'all', function(v){ setRun(v); }, { label: 'Run', mono: true });
      var expBtn = EX.h('button', { type: 'button', 'class': 'btn small quiet fa-exp' }, ctr, 'Open all');
      expBtn.addEventListener('click', function(){
        var vis = visibleRows(); var allOpen = vis.length && vis.every(function(r){ return state.open[r.id]; });
        vis.forEach(function(r){ if(allOpen) delete state.open[r.id]; else state.open[r.id] = true; });
        renderTable();
      });
      var readout = EX.h('div', { 'class': 'fa-readout', 'aria-live': 'polite' }, root);

      /* =============== table =============== */
      var listWrap = EX.h('div', { 'class': 'fa-list', tabindex: '-1' }, root);
      var table = EX.h('table', { 'class': 't fa-table' }, listWrap);
      var thead = EX.h('thead', null, table);
      var htr = EX.h('tr', null, thead);
      ['Pick', 'File', 'Tag', 'Judges', 'Judges’ reason'].forEach(function(h, i){
        EX.h('th', { scope: 'col', 'class': 'c' + i }, htr, h);
      });
      var notes = EX.h('div', { 'class': 'fa-notes' }, root);

      function setRun(v){
        state.run = v; runSel.value = v;
        Object.keys(runBtns).forEach(function(k){ runBtns[k].setAttribute('aria-pressed', String(k === v)); });
        renderTable();
      }
      function visibleRows(){
        return rows.filter(function(r){
          return (state.tag === 'all' || (state.tag === 'arc') === r.arc) && (state.run === 'all' || r.run === state.run);
        });
      }

      function diffHTML(text){
        return text.split('\n').map(function(l){
          var c = l.indexOf('@@') === 0 ? 'hunk' : l.charAt(0) === '+' ? 'add' : l.charAt(0) === '-' ? 'del' : '';
          return '<span class="ln' + (c ? ' ' + c : '') + '">' + (EX.esc(l) || ' ') + '</span>';
        }).join('');
      }

      function pickCellHTML(r){
        var s = '<span class="fa-pick">' + pickHTML(r.pick) + '</span>';
        if(r.exam != null) s += '<span class="fa-exam">exam ' + EX.esc(F.pct(r.exam)) + (r.unedited ? '<sup class="fa-star" title="final player was the unedited A0">*</sup>' : '') + '</span>';
        else s += '<span class="fa-exam fa-untested">never tested</span>';
        return s;
      }

      function renderTable(){
        Array.prototype.slice.call(table.querySelectorAll('tbody')).forEach(function(tb){ tb.remove(); });
        var vis = visibleRows(), visSet = {};
        vis.forEach(function(r){ visSet[r.id] = true; });
        var shownGroups = 0;
        orderedGroups().forEach(function(g){
          var gr = g.rows.filter(function(r){ return visSet[r.id]; });
          if(!gr.length) return;
          shownGroups++;
          var tb = EX.h('tbody', { 'class': 'fa-group' + (state.marked === g.key ? ' is-marked' : ''), 'data-key': g.key }, table);
          var hr = EX.h('tr', { 'class': 'fa-ghead' }, tb);
          var th = EX.h('th', { colspan: '5', scope: 'rowgroup' }, hr);
          var gh = EX.h('div', { 'class': 'fa-gh' }, th);
          var t1 = EX.h('div', { 'class': 'fa-gh-t' }, gh);
          var pk = g.picks.map(function(p){ return pickHTML(parsePick(p)); });
          t1.innerHTML = '<span class="fa-gh-run">' + EX.esc(g.run) + '</span> · node ' + EX.esc(g.node || '?') +
            (g.gen != null ? ' <span class="fa-muted">(gen ' + g.gen + ')</span>' : '') +
            ' <span class="fa-gh-picks">picked as ' + pk.join(', ') + '</span>' +
            (g.picks.length > 1 ? ' <span class="fa-gh-same">same coach code, audited ' + g.picks.length + '×</span>' : '');
          if(g.node){
            var sb = EX.h('button', { type: 'button', 'class': 'btn small quiet fa-gh-btn',
              'aria-label': 'Select ' + g.run + ' node ' + g.node + ' in the tree, Figure 5' }, gh, 'Select in Fig 5 →');
            sb.addEventListener('click', function(){
              state.marked = g.key; markGroups();
              EX.select('node', { run: g.run, node: g.node, source: 'audit' });
              EX.hash.set('audit', { run: g.run, node: g.node }, { replace: true });
            });
          }
          gr.forEach(function(r){
            var open = !!state.open[r.id];
            var tr = EX.h('tr', { 'class': 'fa-row' + (r.arc ? ' is-arc' : '') + (open ? ' is-open' : '') }, tb);
            var c0 = EX.h('td', { 'class': 'c0' }, tr);
            var btn = EX.h('button', { type: 'button', 'class': 'fa-toggle', 'aria-expanded': String(open), 'aria-controls': 'fa-d-' + r.id,
              'aria-label': (open ? 'Close ' : 'Open ') + g.run + ' ' + pickText(r.pick) + ', ' + r.file + ' hunk ' + (r.idx + 1) + ', ' + r.tag }, c0);
            EX.h('span', { 'class': 'fa-caret', 'aria-hidden': 'true' }, btn, open ? '▾' : '▸');
            EX.h('span', { 'class': 'fa-pickcell' }, btn).innerHTML = pickCellHTML(r);
            var c1 = EX.h('td', { 'class': 'c1 m' }, tr);
            c1.innerHTML = '<span class="fa-file">' + EX.esc(r.file || '') + '</span><span class="fa-idx">hunk ' + (r.idx + 1) + '</span>';
            var c2 = EX.h('td', { 'class': 'c2' }, tr);
            EX.h('span', { 'class': 'fa-pill ' + (r.arc ? 'arc' : 'gen') }, c2, r.arc ? 'ARC-specific' : 'general');
            EX.h('td', { 'class': 'c3' }, tr, r.agreement === 'unanimous' ? 'both agree' : (r.agreement || '—'));
            var c4 = EX.h('td', { 'class': 'c4' }, tr);
            EX.h('div', { 'class': 'fa-reason' + (open ? '' : ' clamp') }, c4, r.reason);
            tr.addEventListener('click', function(e){
              if(e.target.closest('button')) return;               // the toggle button handles its own click
              if(window.getSelection && String(window.getSelection()).length) return;   // let readers select text
              toggle(r);
            });
            btn.addEventListener('click', function(e){ e.stopPropagation(); toggle(r); });
            if(open){
              var dr = EX.h('tr', { 'class': 'fa-detail' + (r.arc ? ' is-arc' : ''), id: 'fa-d-' + r.id }, tb);
              var td = EX.h('td', { colspan: '5' }, dr);
              var meta = EX.h('div', { 'class': 'fa-dmeta' }, td);
              meta.innerHTML = 'Audited hunk ' + (r.idx + 1) + ' of <span class="m">' + EX.esc(r.file || '') + '</span> in ' +
                EX.esc(g.run) + ' node ' + EX.esc(r.node || '?') + ', compared with I<sub>0</sub>' +
                (r.tested ? '. Tested as <span class="m">' + EX.esc(r.tested) + '</span>: exam ' + EX.esc(F.pct(r.exam)) +
                  (r.unedited ? ' (its final player was the unedited A<sub>0</sub>, so this score measures A<sub>0</sub>, not the coach)' : '') : '. This pick was stored but never tested on the exam') + '.';
              if(r.text){
                var pre = EX.h('pre', { 'class': 'code diff fa-diff', tabindex: '0', 'aria-label': 'Diff of ' + r.file }, td);
                pre.innerHTML = diffHTML(r.text);
              } else {
                EX.h('div', { 'class': 'empty' }, td, 'No hunk text was saved for this pick.');
              }
            }
          });
        });
        if(!shownGroups) EX.h('tbody', null, table).innerHTML = '<tr><td colspan="5" class="empty">No hunks match this filter.</td></tr>';
        var openN = vis.filter(function(r){ return state.open[r.id]; }).length;
        expBtn.textContent = vis.length && openN === vis.length ? 'Close all' : 'Open all';
        readout.innerHTML = 'Showing <b>' + vis.length + '</b> of ' + rows.length + ' hunks' +
          (state.run !== 'all' ? ' from <span class="m">' + EX.esc(state.run) + '</span>' : '') +
          (state.tag === 'arc' ? ', ARC-specific only' : state.tag === 'gen' ? ', general only' : '') +
          ' · ' + vis.filter(function(r){ return r.arc; }).length + ' ARC-specific · ' + openN + ' open';
      }
      function toggle(r){
        if(state.open[r.id]) delete state.open[r.id]; else state.open[r.id] = true;
        renderTable();
        var b = table.querySelector('[aria-controls="fa-d-' + r.id + '"]');
        if(b) b.focus({ preventScroll: true });
      }
      function markGroups(){
        Array.prototype.slice.call(table.querySelectorAll('tbody.fa-group')).forEach(function(tb){
          tb.classList.toggle('is-marked', tb.getAttribute('data-key') === state.marked);
        });
      }
      function markFromSelection(run, nodeId, scroll){
        var g = groups.filter(function(x){ return x.run === run && x.node === String(nodeId); })[0];
        state.marked = g ? g.key : null;
        markGroups();
        if(g && scroll){
          var tb = table.querySelector('tbody.fa-group[data-key="' + g.key.replace(/"/g, '') + '"]');
          if(tb && listWrap.scrollHeight > listWrap.clientHeight){
            // scroll within the list only, never the page
            listWrap.scrollTop = tb.offsetTop - table.querySelector('thead').offsetHeight;
          }
        }
        return g;
      }

      /* ---------- notes from data ---------- */
      (function(){
        var parts = [];
        groups.forEach(function(g){
          var arc = g.rows.filter(function(r){ return r.arc; });
          if(arc.length > 1 && g.picks.length > 1){
            parts.push(arc.length + ' of the ' + nArc + ' ARC-specific hunks are one edit in <span class="m">' + EX.esc(g.run) +
              '</span> node ' + EX.esc(g.node) + ', a coach picked ' + g.picks.length + ' times (' +
              g.picks.map(function(p){ return pickHTML(parsePick(p)); }).join(' and ') + ') and audited once per pick.');
          }
        });
        rows.filter(function(r){
          return r.arc && !r.tested && !rows.some(function(o){ return o.run === r.run && o.node === r.node && o.tested; });
        }).forEach(function(r){
          parts.push('The ARC-specific hunk in <span class="m">' + EX.esc(r.run) + '</span> ' + pickHTML(r.pick) +
            ' (node ' + EX.esc(r.node) + ') belongs to a coach that was stored but never tested.');
        });
        sourceRuns.forEach(function(run){
          if(!T['payoff_Ig_' + run] && (T[run].diff_audit || []).length) parts.push('<span class="m">' + EX.esc(run) + '</span> had no I<sub>g</sub> pick; only its extension picks were audited.');
        });
        var un = rows.filter(function(r){ return r.unedited; })[0];
        if(un) parts.push('<sup class="fa-star">*</sup> <span class="m">' + EX.esc(un.tested) + '</span>’s final player was the unedited A<sub>0</sub>.');
        var untested = {}; rows.forEach(function(r){ if(!r.tested) untested[r.pick.kind] = r.pick; });
        var uk = Object.keys(untested).sort(function(a, b){ return PICK_ORDER[a] - PICK_ORDER[b]; });
        if(uk.length) parts.push('Picks at ' + uk.map(function(k){ return pickHTML(untested[k]); }).join(' and ') +
          ' were audited but never sat the exam (\u201cnever tested\u201d); exam scores shown are task-averaged pass@2 of the run that tested that pick.');
        notes.innerHTML = parts.map(function(p){ return '<p>' + p + '</p>'; }).join('');
      })();

      renderTable();

      /* ---------- linking ---------- */
      EX.on('select-node', function(p){
        if(!p || p.source === 'audit') return;
        markFromSelection(p.run, p.node, true);
      });
      EX.on('select-run', function(p){
        if(!p || p.source === 'audit' || !p.run) return;
        var t = T[p.run];
        if(t && t.coach_origin && t.coach_origin.source_run && t.coach_origin.source_node != null){
          markFromSelection(t.coach_origin.source_run, t.coach_origin.source_node, true);
        }
      });
      var hs = EX.hash.get();
      if(hs && hs.section === 'audit' && hs.params && hs.params.run && hs.params.node){
        markFromSelection(hs.params.run, hs.params.node, true);
      }

      function layout(){ root.classList.toggle('is-narrow', ctx.width() < 640); }
      layout();
      ctx.onResize(layout);
    });
  });
})();
