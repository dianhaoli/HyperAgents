/* =====================================================================
   core.js — shared runtime for "Coaching the Coach" (window.EX)
   Plain script, no modules. Loaded after d3 7.8.5 and before js/fig-*.js.

   API (see CONTRACT.md for the full contract)
   ---------------------------------------------------------------------
   Data
     EX.load(name) -> Promise<object>     cached fetch of data/<name>.json
     EX.loadAll([names]) -> Promise<[..]>
   Formatting (EX.fmt)
     pct(x, d=1)      0.2926 -> "29.3%"           (x is a fraction)
     pctRaw(v, d=1)   29.26  -> "29.3%"           (v already in %)
     pts(x, d=1)      0.0042 -> "+0.4"            (fraction -> signed points, U+2212 minus)
     ptsU(x, d=1)     "+0.4 points"
     ci(lo, hi, d=1)  "[−1.9, +2.8]"              (fractions -> signed points)
     ciPct(lo,hi,d=1) "[28.1%, 31.3%]"
     tokens(n)        47645 -> "47.6k", 8555520 -> "8.56M"
     int(n)           12345 -> "12,345"
     usd(x, d=2)      152.227 -> "$152.23"   (d=4 for tiny costs)
     num(x, d=1)
     signed(x, d=1)   "+1.2" / "−1.2"
   Runs and terms
     EX.runLabel(runId, {short}) -> human label ("I₀ run 1", "I_g · source_s3", ...)
     EX.runGroup(runId) -> 'B0'|'xhigh'|'I0'|'Ig'|'g20'|'g40'|'source'
     EX.GROUP_ORDER, EX.GROUP_LABEL
   ARC grids
     EX.ARC                      the 10 palette colours (fixed)
     EX.arcGrid(container, grid, opts) -> <svg> | <div.arc-empty>
         opts: cell (px) | maxSize (px, longest side, default 160) | minCell (2) | maxCell (24)
               diffAgainst (truth grid: wrong cells outlined in --wrong; size mismatch outlines whole grid)
               highlight ([[r,c],..] outlined in --accent)
               label (string/HTML caption above) | title (aria-label) | gap (1 = hairline cell gaps)
               onCell(r,c,value,evt) (click handler; makes cells interactive)
         returns the svg; svg.__arc = {cell, w, h, setCell(r,c,v), wrong:count}
     EX.arcPair(container, input, output, opts) -> wrapper  (input → output; opts as arcGrid + labels [a,b])
     EX.gridsEqual(a, b) -> bool
   Tooltip
     EX.tooltip.show(html, evtOrXY) / .move(evtOrXY) / .hide()
     EX.tooltip.attach(el, htmlOrFn) — hover + focus + tap (tap toggles)
   Colours for JS charts (prefer CSS vars in SVG attributes: fill="var(--ink)")
     EX.colors.get('accent') -> '#2F5F98' (current theme)  ; EX.colors.all() ; EX.colors.ramp(t in 0..1)
     re-read automatically; EX.on('theme', fn) fires after any theme change
   Events (cross-figure linking)
     EX.on(evt, fn) -> unsubscribe fn ; EX.off(evt, fn) ; EX.emit(evt, payload)
     Standard events: 'select-run' {run, source}  'select-node' {run, node, source}
                      'select-task' {task, set, source}  'theme' {theme}  'hash' {section, params}
     EX.state — last selection {run, node, task}; EX.select(kind, payload) sets state + emits.
   Figures
     EX.mount(name, initFn)  initFn(node, ctx) may return a Promise. Runs once when
         .mount[data-fig=name] exists. Errors (sync or async) render a quiet inline message.
         ctx = {name, figure (the <figure>), panel, width(), onResize(fn), setStatus(text), EX}
     EX.figures — registry {name: {status:'pending'|'ready'|'error', error}}
   Hash routing (ASCII names only)
     EX.hash.get() -> {section, params}      e.g. "#tree?run=source_s1&node=3"
     EX.hash.set(section, params, {replace=true, scroll=false})
     EX.hash.param(key)
   DOM helpers
     EX.h(tag, attrs, parent, text)   HTML element
     EX.s(tag, attrs, parent, text)   SVG element
     EX.esc(str)                      HTML-escape
     EX.scrollHint(scrollEl, {hint:'scroll →'}) — right-edge fade + muted hint for wide content
     EX.seg(container, options[{value,label}], value, onChange, {label, mono}) -> {set(v), el}
     EX.selectBox(container, options, value, onChange, {label, mono}) -> <select>
     EX.reduceMotion (bool) ; EX.dur(ms) -> 0 when reduced motion
     EX.uid(prefix)
   ===================================================================== */
(function(){
  'use strict';
  var EX = window.EX = window.EX || {};
  var doc = document, root = doc.documentElement;
  var SVGNS = 'http://www.w3.org/2000/svg';

  /* ---------------- DOM helpers ---------------- */
  function setAttrs(e, attrs){
    if(!attrs) return;
    for(var k in attrs){
      var v = attrs[k];
      if(v === undefined || v === null || v === false) continue;
      if(k === 'class') e.setAttribute('class', v);
      else if(k === 'style' && typeof v === 'object'){ for(var s in v) e.style[s] = v[s]; }
      else if(k === 'html') e.innerHTML = v;
      else if(k.slice(0,2) === 'on' && typeof v === 'function') e.addEventListener(k.slice(2), v);
      else e.setAttribute(k, v === true ? '' : v);
    }
  }
  EX.h = function(tag, attrs, parent, text){
    var e = doc.createElement(tag); setAttrs(e, attrs);
    if(text != null) e.textContent = text;
    if(parent) parent.appendChild(e);
    return e;
  };
  EX.s = function(tag, attrs, parent, text){
    var e = doc.createElementNS(SVGNS, tag); setAttrs(e, attrs);
    if(text != null) e.textContent = text;
    if(parent) parent.appendChild(e);
    return e;
  };
  EX.esc = function(s){
    return String(s == null ? '' : s).replace(/[&<>"']/g, function(c){
      return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];
    });
  };
  var _uid = 0;
  EX.uid = function(p){ return (p || 'ex') + '-' + (++_uid); };

  /* ---------------- motion ---------------- */
  var rm = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : null;
  EX.reduceMotion = !!(rm && rm.matches);
  if(rm && rm.addEventListener) rm.addEventListener('change', function(e){ EX.reduceMotion = e.matches; });
  EX.dur = function(ms){ return EX.reduceMotion ? 0 : (ms == null ? 180 : ms); };

  /* ---------------- event bus ---------------- */
  var handlers = {};
  EX.on = function(evt, fn){
    (handlers[evt] = handlers[evt] || []).push(fn);
    return function(){ EX.off(evt, fn); };
  };
  EX.off = function(evt, fn){
    var l = handlers[evt]; if(!l) return;
    var i = l.indexOf(fn); if(i >= 0) l.splice(i, 1);
  };
  EX.emit = function(evt, payload){
    (handlers[evt] || []).slice().forEach(function(fn){
      try { fn(payload); } catch(err){ console.error('[EX] handler for "' + evt + '" failed', err); }
    });
  };
  EX.state = { run: null, node: null, task: null };
  EX.select = function(kind, payload){
    payload = payload || {};
    if(kind === 'run'){ EX.state.run = payload.run; EX.emit('select-run', payload); }
    else if(kind === 'node'){ EX.state.run = payload.run; EX.state.node = payload.node; EX.emit('select-node', payload); }
    else if(kind === 'task'){ EX.state.task = payload.task; EX.emit('select-task', payload); }
  };

  /* ---------------- data ---------------- */
  var cache = {};
  EX.load = function(name){
    name = String(name).replace(/\.json$/, '');
    if(!cache[name]){
      cache[name] = fetch('data/' + name + '.json').then(function(r){
        if(!r.ok) throw new Error('data/' + name + '.json: HTTP ' + r.status);
        return r.json();
      });
      cache[name].catch(function(){ delete cache[name]; });
    }
    return cache[name];
  };
  EX.loadAll = function(names){ return Promise.all(names.map(EX.load)); };

  /* ---------------- formatting ---------------- */
  var MINUS = '−';
  function fx(x, d){ var s = Number(x).toFixed(d); if(/^-0(\.0+)?$/.test(s)) s = s.slice(1); return s; }
  function signed(x, d){
    d = d == null ? 1 : d;
    var s = fx(Math.abs(x), d);
    var zero = Number(s) === 0;
    return (zero ? '' : (x < 0 ? MINUS : '+')) + s;
  }
  EX.fmt = {
    MINUS: MINUS,
    pct: function(x, d){ if(x == null || isNaN(x)) return '—'; return fx(x * 100, d == null ? 1 : d) + '%'; },
    pctRaw: function(v, d){ if(v == null || isNaN(v)) return '—'; return fx(v, d == null ? 1 : d) + '%'; },
    pts: function(x, d){ if(x == null || isNaN(x)) return '—'; return signed(x * 100, d); },
    ptsU: function(x, d){ return EX.fmt.pts(x, d) + ' points'; },
    ci: function(lo, hi, d){ return '[' + signed(lo * 100, d) + ', ' + signed(hi * 100, d) + ']'; },
    ciPct: function(lo, hi, d){ return '[' + EX.fmt.pct(lo, d) + ', ' + EX.fmt.pct(hi, d) + ']'; },
    signed: signed,
    num: function(x, d){ if(x == null || isNaN(x)) return '—'; return fx(x, d == null ? 1 : d); },
    int: function(n){ if(n == null || isNaN(n)) return '—'; return Math.round(n).toLocaleString('en-US'); },
    tokens: function(n){
      if(n == null || isNaN(n)) return '—';
      var a = Math.abs(n);
      if(a >= 1e6) return fx(n / 1e6, a >= 1e7 ? 1 : 2) + 'M';
      if(a >= 1e3) return fx(n / 1e3, a >= 1e5 ? 0 : 1) + 'k';
      return String(Math.round(n));
    },
    usd: function(x, d){ if(x == null || isNaN(x)) return '—'; return (x < 0 ? MINUS : '') + '$' + Math.abs(x).toFixed(d == null ? 2 : d); },
    secs: function(s){ if(s == null) return '—'; if(s < 90) return Math.round(s) + ' s'; if(s < 5400) return fx(s / 60, 1) + ' min'; return fx(s / 3600, 1) + ' h'; }
  };

  /* ---------------- runs & terms ---------------- */
  EX.GROUP_ORDER = ['B0', 'xhigh', 'I0', 'Ig', 'g20', 'g40'];
  EX.GROUP_LABEL = {
    B0: 'B0 · two plain attempts', xhigh: 'A₀ at xhigh effort',
    I0: 'I₀ · original coach', Ig: 'I_g · evolved coach',
    g20: 'Extension · gen 20 coach', g40: 'Extension · gen 40 coach', source: 'Source run'
  };
  EX.runGroup = function(run){
    if(!run) return null;
    if(/^B0/.test(run)) return 'B0';
    if(run === 'xhigh') return 'xhigh';
    if(/^payoff_I0_/.test(run)) return 'I0';
    if(/^payoff_Ig_/.test(run)) return 'Ig';
    if(/^ext_.*_g20$/.test(run)) return 'g20';
    if(/^ext_.*_g40$/.test(run)) return 'g40';
    if(/^source_/.test(run)) return 'source';
    return null;
  };
  EX.runLabel = function(run, opts){
    var short = opts && opts.short, m;
    if((m = /^B0_rep(\d)$/.exec(run))) return short ? 'B0 rep ' + m[1] : 'B0, rep ' + m[1];
    if(run === 'xhigh') return short ? 'xhigh' : 'A₀ at xhigh';
    if((m = /^payoff_I0_(\d)$/.exec(run))) return short ? 'I₀ #' + m[1] : 'I₀ run ' + m[1];
    if((m = /^payoff_Ig_source_(s\d)$/.exec(run))) return short ? 'I_g ' + m[1] : 'I_g from ' + m[1];
    if((m = /^ext_source_(s\d)_g(\d+)$/.exec(run))) return short ? 'g' + m[2] + ' ' + m[1] : 'gen-' + m[2] + ' coach from ' + m[1];
    if((m = /^source_(s\d)$/.exec(run))) return short ? m[1] : 'source run ' + m[1];
    return run;
  };

  /* ---------------- colours ---------------- */
  var TOKENS = ['bg','panel','panel-strong','ink','ink-2','ink-muted','rule','rule-strong','accent','accent-hover',
    'accent-pressed','accent-wash','correct','wrong','ramp-0','ramp-1','ramp-2','ramp-3','ramp-4','code-bg'];
  var colorCache = null;
  function readColors(){
    var cs = getComputedStyle(root), o = {};
    TOKENS.forEach(function(t){ o[t] = cs.getPropertyValue('--' + t).trim(); });
    colorCache = o; return o;
  }
  EX.colors = {
    get: function(t){ return (colorCache || readColors())[t]; },
    all: function(){ return Object.assign({}, colorCache || readColors()); },
    ramp: function(t){ var i = Math.max(0, Math.min(4, Math.round(t * 4))); return EX.colors.get('ramp-' + i); },
    refresh: readColors
  };

  /* ---------------- theme ---------------- */
  var THEME_KEY = 'ex-theme';
  function storedTheme(){ try { return localStorage.getItem(THEME_KEY) || 'auto'; } catch(e){ return 'auto'; } }
  EX.theme = {
    get: function(){ return root.getAttribute('data-theme') || 'auto'; },
    effective: function(){
      var t = root.getAttribute('data-theme');
      if(t === 'light' || t === 'dark') return t;
      return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    },
    set: function(t){
      if(t === 'light' || t === 'dark') root.setAttribute('data-theme', t); else root.removeAttribute('data-theme');
      try { localStorage.setItem(THEME_KEY, t); } catch(e){}
      readColors();
      EX.emit('theme', { theme: EX.theme.effective(), setting: t });
    }
  };
  (function(){ var t = storedTheme(); if(t === 'light' || t === 'dark') root.setAttribute('data-theme', t); })();
  if(window.matchMedia){
    var mq = window.matchMedia('(prefers-color-scheme: dark)');
    var onMq = function(){ readColors(); EX.emit('theme', { theme: EX.theme.effective(), setting: EX.theme.get() }); };
    if(mq.addEventListener) mq.addEventListener('change', onMq); else if(mq.addListener) mq.addListener(onMq);
  }

  /* ---------------- tooltip ---------------- */
  var tipEl = null, tipPinnedBy = null;
  function tip(){ if(!tipEl){ tipEl = EX.h('div', { 'class': 'ex-tip', role: 'tooltip', 'aria-hidden': 'true' }, doc.body); } return tipEl; }
  function xy(e){
    if(!e) return null;
    if(e.touches && e.touches[0]) return { x: e.touches[0].clientX, y: e.touches[0].clientY };
    if(e.clientX != null && !(e.clientX === 0 && e.clientY === 0 && e.target && e.target.getBoundingClientRect)) return { x: e.clientX, y: e.clientY };
    if(e.target && e.target.getBoundingClientRect){ var r = e.target.getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top }; }
    if(e.getBoundingClientRect){ var r2 = e.getBoundingClientRect(); return { x: r2.left + r2.width / 2, y: r2.top }; }
    if(e.x != null) return { x: e.x, y: e.y };
    return null;
  }
  EX.tooltip = {
    show: function(html, e){ var t = tip(); t.innerHTML = html; t.classList.add('on'); EX.tooltip.move(e); },
    move: function(e){
      var p = xy(e); if(!p || !tipEl) return;
      var t = tipEl, w = t.offsetWidth, hgt = t.offsetHeight, vw = root.clientWidth, vh = window.innerHeight;
      var x = p.x + 14, y = p.y - hgt - 12;
      if(x + w > vw - 8) x = Math.max(8, p.x - w - 14);
      if(y < 8) y = Math.min(vh - hgt - 8, p.y + 18);
      t.style.transform = 'none';
      t.style.left = Math.round(x) + 'px'; t.style.top = Math.round(y) + 'px';
    },
    hide: function(){ if(tipEl){ tipEl.classList.remove('on'); } tipPinnedBy = null; },
    attach: function(el, content){
      var get = function(){ return typeof content === 'function' ? content(el) : content; };
      el.addEventListener('mouseenter', function(e){ EX.tooltip.show(get(), e); });
      el.addEventListener('mousemove', function(e){ EX.tooltip.move(e); });
      el.addEventListener('mouseleave', function(){ EX.tooltip.hide(); });
      el.addEventListener('focus', function(){ EX.tooltip.show(get(), el); });
      el.addEventListener('blur', function(){ EX.tooltip.hide(); });
      el.addEventListener('touchstart', function(e){
        if(tipPinnedBy === el){ EX.tooltip.hide(); return; }
        EX.tooltip.show(get(), e); tipPinnedBy = el;
      }, { passive: true });
    }
  };
  window.addEventListener('scroll', function(){ if(tipEl && tipEl.classList.contains('on')) EX.tooltip.hide(); }, { passive: true });
  doc.addEventListener('keydown', function(e){ if(e.key === 'Escape') EX.tooltip.hide(); });

  /* ---------------- ARC grids ---------------- */
  EX.ARC = ['#000000','#0074D9','#FF4136','#2ECC40','#FFDC00','#AAAAAA','#F012BE','#FF851B','#7FDBFF','#870C25'];
  EX.gridsEqual = function(a, b){
    if(!a || !b || a.length !== b.length) return false;
    for(var i = 0; i < a.length; i++){
      if(!a[i] || !b[i] || a[i].length !== b[i].length) return false;
      for(var j = 0; j < a[i].length; j++) if(a[i][j] !== b[i][j]) return false;
    }
    return true;
  };
  function isGrid(g){ return Array.isArray(g) && g.length > 0 && Array.isArray(g[0]) && g[0].length > 0; }
  function wrapLabel(container, label){
    if(!label) return container;
    var fig = EX.h('div', { 'class': 'arc-fig' }, container);
    EX.h('div', { 'class': 'arc-cap', html: label }, fig);
    return fig;
  }
  EX.arcGrid = function(container, grid, opts){
    opts = opts || {};
    var host = container ? wrapLabel(container, opts.label) : null;
    if(!isGrid(grid)){
      var sz = opts.emptySize || Math.min(opts.maxSize || 160, 96);
      var em = EX.h('div', { 'class': 'arc-empty', style: { width: sz + 'px', height: sz + 'px' } }, host, opts.emptyText || 'no answer');
      return em;
    }
    var h = grid.length, w = grid[0].length;
    var gap = opts.gap == null ? 1 : opts.gap;
    var cell = opts.cell;
    if(!cell){
      var maxSize = opts.maxSize || 160;
      cell = Math.floor((maxSize - gap) / Math.max(w, h));
      cell = Math.max(opts.minCell || 2, Math.min(opts.maxCell || 24, cell));
    }
    var W = w * cell + gap, H = h * cell + gap;
    var svg = EX.s('svg', { 'class': 'arc' + (opts.className ? ' ' + opts.className : ''), width: W, height: H,
      viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': opts.title || (h + ' by ' + w + ' grid') });
    EX.s('rect', { 'class': 'arc-bg', x: 0, y: 0, width: W, height: H }, svg);
    var cells = [];
    for(var r = 0; r < h; r++){
      cells.push([]);
      for(var c = 0; c < w; c++){
        var v = grid[r][c];
        var rect = EX.s('rect', { x: c * cell + gap, y: r * cell + gap, width: cell - gap, height: cell - gap,
          fill: EX.ARC[v] || '#AAAAAA', 'data-r': r, 'data-c': c }, svg);
        cells[r].push(rect);
      }
    }
    var wrong = 0;
    var truth = opts.diffAgainst;
    if(isGrid(truth)){
      if(truth.length !== h || truth[0].length !== w){
        wrong = -1;
        EX.s('rect', { 'class': 'arc-wrong', x: 1, y: 1, width: W - 2, height: H - 2, 'stroke-dasharray': '4 3' }, svg);
        svg.setAttribute('aria-label', (opts.title || 'grid') + ': wrong size (' + h + '×' + w + ' vs ' + truth.length + '×' + truth[0].length + ')');
      } else {
        var sw = cell >= 8 ? 2 : 1.25, inset = sw / 2 + (gap ? 0.5 : 0);
        for(var r2 = 0; r2 < h; r2++) for(var c2 = 0; c2 < w; c2++){
          if(grid[r2][c2] !== truth[r2][c2]){
            wrong++;
            EX.s('rect', { 'class': 'arc-wrong', x: c2 * cell + gap + inset - 0.5, y: r2 * cell + gap + inset - 0.5,
              width: Math.max(1, cell - gap - 2 * inset + 1), height: Math.max(1, cell - gap - 2 * inset + 1), 'stroke-width': sw }, svg);
          }
        }
        if(wrong) svg.setAttribute('aria-label', (opts.title || 'grid') + ': ' + wrong + ' wrong cell' + (wrong > 1 ? 's' : ''));
      }
    }
    (opts.highlight || []).forEach(function(p){
      EX.s('rect', { 'class': 'arc-hl', x: p[1] * cell + gap, y: p[0] * cell + gap, width: cell - gap, height: cell - gap }, svg);
    });
    if(opts.onCell){
      svg.style.cursor = 'pointer';
      svg.addEventListener('click', function(e){
        var t = e.target; if(t.getAttribute('data-r') == null) return;
        var rr = +t.getAttribute('data-r'), cc = +t.getAttribute('data-c');
        opts.onCell(rr, cc, grid[rr][cc], e);
      });
    }
    svg.__arc = { cell: cell, w: w, h: h, wrong: wrong, cells: cells,
      setCell: function(r, c, v){ grid[r][c] = v; cells[r][c].setAttribute('fill', EX.ARC[v]); } };
    if(host) host.appendChild(svg);
    return svg;
  };
  EX.arcPair = function(container, input, output, opts){
    opts = opts || {};
    var labels = opts.labels || [null, null];
    var outer = wrapLabel(container, opts.label);
    var pair = EX.h('div', { 'class': 'arc-pair' }, outer);
    var o1 = Object.assign({}, opts, { label: labels[0], diffAgainst: null });
    var o2 = Object.assign({}, opts, { label: labels[1] });
    if(opts.sameScale !== false && isGrid(input) && isGrid(output) && !opts.cell){
      var m = Math.max(input.length, input[0].length, output.length, output[0].length);
      var c = Math.max(opts.minCell || 2, Math.min(opts.maxCell || 24, Math.floor(((opts.maxSize || 160) - 1) / m)));
      o1.cell = o2.cell = c;
    }
    EX.arcGrid(pair, input, o1);
    EX.h('span', { 'class': 'arc-arrow', 'aria-hidden': 'true' }, pair, '→');
    EX.arcGrid(pair, output, o2);
    return outer;
  };

  /* ---------------- small UI builders ---------------- */
  EX.seg = function(container, options, value, onChange, o){
    o = o || {};
    var wrap = EX.h('span', { 'class': 'seg-wrap', style: { display: 'inline-flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' } }, container);
    if(o.label) EX.h('span', { 'class': 'control-label' }, wrap, o.label);
    var seg = EX.h('span', { 'class': 'seg' + (o.mono ? ' mono' : ''), role: 'group', 'aria-label': o.label || o.ariaLabel || 'options' }, wrap);
    var btns = options.map(function(opt){
      var b = EX.h('button', { type: 'button', 'aria-pressed': String(opt.value === value), 'data-opt': opt.value, title: opt.title }, seg, opt.label);
      b.addEventListener('click', function(){ api.set(opt.value); if(onChange) onChange(opt.value); });
      return b;
    });
    var api = { el: wrap, set: function(v){ value = v; btns.forEach(function(b){ b.setAttribute('aria-pressed', String(b.getAttribute('data-opt') === String(v))); }); }, get: function(){ return value; } };
    return api;
  };
  EX.selectBox = function(container, options, value, onChange, o){
    o = o || {};
    var lab = EX.h('label', { style: { display: 'inline-flex', alignItems: 'center', gap: '8px' } }, container);
    if(o.label) EX.h('span', { 'class': 'control-label' }, lab, o.label);
    var sel = EX.h('select', { 'class': 'select' + (o.mono ? ' mono' : '') }, lab);
    options.forEach(function(opt){
      if(opt.group){
        var g = EX.h('optgroup', { label: opt.group }, sel);
        opt.options.forEach(function(op){ var e = EX.h('option', { value: op.value }, g, op.label); if(op.value === value) e.selected = true; });
      } else { var e = EX.h('option', { value: opt.value }, sel, opt.label); if(opt.value === value) e.selected = true; }
    });
    sel.addEventListener('change', function(){ if(onChange) onChange(sel.value); });
    return sel;
  };
  EX.scrollHint = function(scrollEl, o){
    o = o || {};
    var wrap = scrollEl.parentNode;
    if(!wrap.classList || !wrap.classList.contains('scroll-wrap')){
      wrap = doc.createElement('div'); wrap.className = 'scroll-wrap';
      scrollEl.parentNode.insertBefore(wrap, scrollEl); wrap.appendChild(scrollEl);
    }
    var hint = wrap.nextElementSibling && wrap.nextElementSibling.classList.contains('scroll-hint') ? wrap.nextElementSibling : null;
    if(!hint){ hint = doc.createElement('div'); hint.className = 'scroll-hint'; hint.textContent = o.hint || 'scroll →'; wrap.parentNode.insertBefore(hint, wrap.nextSibling); }
    scrollEl.classList.add('scroll-x');
    function upd(){
      var over = scrollEl.scrollWidth > scrollEl.clientWidth + 2;
      wrap.classList.toggle('has-overflow', over);
      wrap.classList.toggle('at-end', scrollEl.scrollLeft + scrollEl.clientWidth >= scrollEl.scrollWidth - 2);
    }
    scrollEl.addEventListener('scroll', upd, { passive: true });
    if(window.ResizeObserver) new ResizeObserver(upd).observe(scrollEl);
    upd();
    return { update: upd, scrollTo: function(x){ scrollEl.scrollLeft = Math.max(0, x - scrollEl.clientWidth / 2); upd(); } };
  };

  /* ---------------- hash routing ---------------- */
  EX.hash = {
    get: function(){
      var raw = (location.hash || '').replace(/^#/, '');
      var q = raw.indexOf('?'), section = q >= 0 ? raw.slice(0, q) : raw, params = {};
      if(q >= 0) raw.slice(q + 1).split('&').forEach(function(kv){
        if(!kv) return; var i = kv.indexOf('=');
        var k = decodeURIComponent(i >= 0 ? kv.slice(0, i) : kv), v = i >= 0 ? decodeURIComponent(kv.slice(i + 1)) : '';
        params[k] = v;
      });
      return { section: section, params: params };
    },
    set: function(section, params, o){
      o = o || {};
      var qs = Object.keys(params || {}).filter(function(k){ return params[k] != null && params[k] !== ''; })
        .map(function(k){ return encodeURIComponent(k) + '=' + encodeURIComponent(params[k]); }).join('&');
      var h = '#' + (section || '') + (qs ? '?' + qs : '');
      if(h === location.hash) return;
      try {
        if(o.replace === false) history.pushState(null, '', h); else history.replaceState(null, '', h);
      } catch(e){}
      if(o.scroll){ var el = doc.getElementById(section); if(el) el.scrollIntoView({ behavior: EX.reduceMotion ? 'auto' : 'smooth' }); }
    },
    param: function(k){ return EX.hash.get().params[k]; }
  };
  window.addEventListener('hashchange', function(){ EX.emit('hash', EX.hash.get()); });

  /* ---------------- figure registry ---------------- */
  EX.figures = {};
  var pendingInits = {};
  function figureOf(node){ return node.closest ? node.closest('figure') : null; }
  function showError(node, name, err){
    console.error('[EX] figure "' + name + '" failed:', err);
    EX.figures[name] = { status: 'error', error: err };
    node.classList.remove('is-loading'); node.classList.add('is-error');
    node.innerHTML = '';
    var box = EX.h('div', { 'class': 'mount-error', role: 'status' }, node);
    EX.h('b', null, box, 'This figure could not be drawn. ');
    EX.h('span', null, box, 'The text around it still holds; reloading the page may help. ');
    EX.h('code', null, box, String(err && err.message || err));
  }
  function runInit(name, fn){
    var node = doc.querySelector('.mount[data-fig="' + name + '"]');
    if(!node){ pendingInits[name] = fn; return false; }
    if(EX.figures[name] && EX.figures[name].status !== 'pending') return true;
    EX.figures[name] = { status: 'pending' };
    node.classList.add('is-loading');
    var status = node.querySelector('.mount-status');
    var resizeFns = [];
    var ctx = {
      name: name, EX: EX, node: node, figure: figureOf(node),
      panel: node.closest ? node.closest('.fig-panel') : null,
      width: function(){ return node.clientWidth; },
      setStatus: function(t){ var s = node.querySelector('.mount-status'); if(s) s.textContent = t; },
      onResize: function(fn){ resizeFns.push(fn); }
    };
    if(window.ResizeObserver){
      var lastW = -1, raf = 0;
      new ResizeObserver(function(){
        var w = node.clientWidth; if(w === lastW) return; lastW = w;
        cancelAnimationFrame(raf);
        raf = requestAnimationFrame(function(){ resizeFns.forEach(function(f){ try { f(w); } catch(e){ console.error(e); } }); });
      }).observe(node);
    }
    var done = function(){
      if(EX.figures[name].status === 'error') return;
      EX.figures[name] = { status: 'ready' };
      node.classList.remove('is-loading'); node.classList.add('is-ready');
      var st = node.querySelector(':scope > .mount-status'); if(st) st.remove();
      EX.emit('figure-ready', { name: name });
    };
    try {
      var r = fn(node, ctx);
      if(r && typeof r.then === 'function') r.then(done, function(err){ showError(node, name, err); });
      else done();
    } catch(err){ showError(node, name, err); }
    return true;
  }
  EX.mount = function(name, fn){
    if(doc.readyState === 'loading') { pendingInits[name] = fn; }
    else runInit(name, fn);
  };
  function flushPending(){
    Object.keys(pendingInits).forEach(function(name){
      var fn = pendingInits[name]; delete pendingInits[name]; runInit(name, fn);
    });
    // any mount that never got a module: say so quietly
    setTimeout(function(){
      doc.querySelectorAll('.mount[data-fig]').forEach(function(n){
        var name = n.getAttribute('data-fig');
        if(!EX.figures[name]){ var s = n.querySelector('.mount-status'); if(s) s.textContent = 'This interactive figure is not available.'; }
      });
    }, 4000);
  }

  /* ---------------- bound values in prose ----------------
     <span data-v="pct:B0.mean">29.3%</span>   — static text is the fallback;
     core replaces it from summary.json (+ EX.derived) and warns on mismatch.
     formats: pct pct0 pts ptsU pp ci ciPct usd int tokens raw num
     <span data-bar="spend.by_role.task" data-of="spend.total"> gets width = share */
  EX.derive = function(S){
    var d = {};
    var se = S.self_edit || {}, g = 0, n = 0;
    Object.keys(se).forEach(function(k){ g += se[k].self_edit_gens; n += se[k].gens; });
    d.selfEditGens = g; d.totalGens = n;
    d.xhighGain = S.xhigh.score - S.B0.mean;
    d.nI0 = Object.keys(S.I0_runs).length; d.nIg = Object.keys(S.Ig_runs).length;
    d.metaTokI0 = S.tokens_by_arm.I0.meta_tokens_per_iteration; d.metaTokIg = S.tokens_by_arm.Ig.meta_tokens_per_iteration;
    d.taskTokI0 = S.tokens_by_arm.I0.task_tokens_per_task_eval; d.taskTokIg = S.tokens_by_arm.Ig.task_tokens_per_task_eval;
    d.B0min = Math.min.apply(null, S.B0.reps); d.B0max = Math.max.apply(null, S.B0.reps);
    return d;
  };
  function getPath(o, path){
    return path.split('.').reduce(function(a, k){ return a == null ? undefined : a[k]; }, o);
  }
  function fmtBound(f, v){
    switch(f){
      case 'pct': return EX.fmt.pct(v, 1);
      case 'pct0': return EX.fmt.pct(v, 0);
      case 'pts': return EX.fmt.pts(v, 1);
      case 'ptsU': return EX.fmt.ptsU(v, 1);
      case 'ci': return EX.fmt.ci(v.lo, v.hi, 1);
      case 'ciPct': return EX.fmt.ciPct(v.lo, v.hi, 1);
      case 'usd': return EX.fmt.usd(v, 2);
      case 'int': return EX.fmt.int(v);
      case 'tokens': return EX.fmt.tokens(v);
      case 'num': return EX.fmt.num(v, 1);
      case 'pp': return EX.fmt.num(Math.abs(v) * 100, 1);
      default: return String(v);
    }
  }
  EX.bindValues = function(scope){
    var nodes = (scope || doc).querySelectorAll('[data-v]');
    if(!nodes.length) return Promise.resolve();
    return EX.load('summary').then(function(S){
      var src = Object.assign({}, S, { derived: EX.derive(S) });
      nodes.forEach(function(n){
        var spec = n.getAttribute('data-v'), i = spec.indexOf(':');
        var f = i >= 0 ? spec.slice(0, i) : 'raw', path = i >= 0 ? spec.slice(i + 1) : spec;
        var v = getPath(src, path);
        if(v === undefined){ console.warn('[EX] bound value not found:', spec); return; }
        var txt = fmtBound(f, v);
        if(n.textContent.trim() !== txt) console.warn('[EX] prose value "' + n.textContent.trim() + '" replaced by data value "' + txt + '" (' + spec + ')');
        n.textContent = txt;
      });
      (scope || doc).querySelectorAll('[data-bar]').forEach(function(n){
        var v = getPath(src, n.getAttribute('data-bar')), of = getPath(src, n.getAttribute('data-of'));
        if(typeof v === 'number' && typeof of === 'number' && of > 0) n.style.width = (100 * v / of).toFixed(2) + '%';
      });
    }).catch(function(e){ console.warn('[EX] could not bind values', e); });
  };

  /* ---------------- theme toggle + boot ---------------- */
  function buildThemeToggle(){
    var host = doc.querySelector('[data-theme-toggle]'); if(!host) return;
    host.innerHTML = '';
    EX.seg(host, [{ value: 'auto', label: 'Auto' }, { value: 'light', label: 'Light' }, { value: 'dark', label: 'Dark' }],
      storedTheme(), function(v){ EX.theme.set(v); }, { label: 'Theme' });
  }
  function boot(){
    readColors();
    buildThemeToggle();
    EX.bindValues();
    flushPending();
    // honour a deep link once figures have had a chance to lay out
    var h = EX.hash.get();
    if(h.section){
      var target = doc.getElementById(h.section);
      if(target){
        var tries = 0;
        var settle = function(){ var all = Object.keys(EX.figures).every(function(k){ return EX.figures[k].status !== 'pending'; });
          if(all || ++tries > 20){ target.scrollIntoView(); } else setTimeout(settle, 150); };
        setTimeout(settle, 150);
      }
    }
  }
  if(doc.readyState === 'loading') doc.addEventListener('DOMContentLoaded', boot); else boot();
})();
