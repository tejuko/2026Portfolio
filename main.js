/* =========================================================
   Tess Kollof — Portfolio 2026
   ========================================================= */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* -------------------------------------------------------
     1. Hero: "Portfolio" als pixelwolk op canvas
     ------------------------------------------------------- */
  function initWordmark() {
    var canvas = document.getElementById('wordmark');
    if (!canvas) return;
    var ctx = canvas.getContext('2d');
    if (!ctx) return;

    var TEXT = 'Portfolio';
    // wit linksboven naar zacht roze rechtsonder. Dit is het verloop van de
    // eerste versie: geen bordeaux, want dat werd te donker.
    var COLOR_TOP = [255, 255, 255];   // wit, linksboven
    var COLOR_BOT = [222, 66, 89];     // #DE4259, rechtsonder

    // Het verloop staat als 64 kleuren klaar in een lijst. Per beeldje zoeken we
    // per blokje alleen een nummer op; dat is snel genoeg voor duizenden blokjes.
    var STEPS_N = 64;
    var PALETTE = (function () {
      var out = [];
      for (var i = 0; i < STEPS_N; i++) {
        var t = i / (STEPS_N - 1);
        out.push('rgb(' +
          Math.round(COLOR_TOP[0] + (COLOR_BOT[0] - COLOR_TOP[0]) * t) + ',' +
          Math.round(COLOR_TOP[1] + (COLOR_BOT[1] - COLOR_TOP[1]) * t) + ',' +
          Math.round(COLOR_TOP[2] + (COLOR_BOT[2] - COLOR_TOP[2]) * t) + ')');
      }
      return out;
    })();
    // De kleurgolf. SHIFT_DOWN is hoeveel lichter het mag worden, SHIFT_UP
    // hoeveel dieper. Vooral naar dieper, zodat het nooit slechter leesbaar
    // wordt dan de rusttoestand.
    var SHIFT_DOWN  = 0.07;
    var SHIFT_UP    = 0.34;
    var SHIFT_SPEED = 0.00075;   // hoger = snellere golf
    var SHIFT_LENGTH = 0.0055;   // hoger = kortere golf, meer banen tegelijk

    var W = 0, H = 0, dpr = 1, cellSize = 8, drawSize = 7;
    var cells = [];
    var pointer = { x: -9999, y: -9999, on: false };
    var running = false, visible = true, rafId = 0;
    var startTime = 0, introDone = false;

    function lerp(a, b, t) { return a + (b - a) * t; }

    function build() {
      var rect = canvas.getBoundingClientRect();
      if (rect.width < 2 || rect.height < 2) return false;

      dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = Math.round(rect.width);
      H = Math.round(rect.height);
      canvas.width = Math.round(W * dpr);
      canvas.height = Math.round(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      // 1a. tekst op een offscreen canvas zetten en uitlezen
      var off = document.createElement('canvas');
      off.width = W;
      off.height = H;
      var octx = off.getContext('2d');
      octx.textAlign = 'center';
      octx.textBaseline = 'middle';

      var maxW = W * (W < 620 ? 0.95 : 0.9);
      var size = H * 0.92;
      for (var i = 0; i < 24; i++) {
        octx.font = '700 ' + size + 'px "Space Grotesk", system-ui, sans-serif';
        var m = octx.measureText(TEXT).width;
        if (m <= maxW) break;
        size = size * (maxW / m) * 0.995;
      }
      octx.font = '700 ' + size + 'px "Space Grotesk", system-ui, sans-serif';
      octx.fillStyle = '#000';
      octx.fillText(TEXT, W / 2, H * 0.52);

      var data;
      try {
        data = octx.getImageData(0, 0, W, H).data;
      } catch (e) {
        return false;
      }

      // 1b. raster aftasten -> pixelblokjes
      cellSize = Math.max(4, Math.round(W / 130));
      var gap = Math.max(1, Math.round(cellSize * 0.16));
      drawSize = cellSize - gap;

      cells = [];
      var minX = W, maxX = 0, minY = H, maxY = 0;
      var hits = [];
      for (var y = 0; y < H; y += cellSize) {
        for (var x = 0; x < W; x += cellSize) {
          var sx = Math.min(W - 1, x + (cellSize >> 1));
          var sy = Math.min(H - 1, y + (cellSize >> 1));
          if (data[(sy * W + sx) * 4 + 3] > 130) {
            hits.push([x, y]);
            if (x < minX) minX = x;
            if (x > maxX) maxX = x;
            if (y < minY) minY = y;
            if (y > maxY) maxY = y;
          }
        }
      }
      var spanX = Math.max(1, maxX - minX);
      var spanY = Math.max(1, maxY - minY);

      for (var k = 0; k < hits.length; k++) {
        var hx = hits[k][0], hy = hits[k][1];
        var nx = (hx - minX) / spanX;
        var ny = (hy - minY) / spanY;
        var base = Math.min(1, Math.max(0, ny * 0.7 + nx * 0.3 + (Math.random() - 0.5) * 0.1));
        // machtsverheffing duwt het verloop sneller naar verzadigd roze, zodat er
        // minder blokjes in de vage middenzone vallen
        var t = Math.pow(base, 0.78);
        cells.push({
          tx: hx, ty: hy,
          x: hx, y: hy,
          vx: 0, vy: 0,
          // startpositie van de intro: vanaf buiten het beeld naar binnen
          ox: hx + (Math.random() - 0.5) * W * 1.1,
          oy: hy + (Math.random() - 0.5) * H * 2.6,
          delay: nx * 340 + Math.random() * 260,
          wob: Math.random() * Math.PI * 2,
          // plek in het verloop (0 = wit, 1 = diep roze) en de eigen fase van de
          // kleurgolf, zodat die diagonaal over het woord loopt
          bt: t,
          phase: (hx + hy) * SHIFT_LENGTH
        });
      }
      return cells.length > 0;
    }

    function paint(now) {
      ctx.clearRect(0, 0, W, H);

      var intro = 1;
      var t = now - startTime;

      for (var i = 0; i < cells.length; i++) {
        var c = cells[i];
        var px, py, s = drawSize;

        if (!introDone) {
          var p = Math.min(1, Math.max(0, (t - c.delay) / 900));
          var e = 1 - Math.pow(1 - p, 3);          // easeOutCubic
          px = lerp(c.ox, c.tx, e);
          py = lerp(c.oy, c.ty, e);
          s = drawSize * (0.2 + 0.8 * e);
          c.x = px; c.y = py;
          if (p < 1) intro = 0;
        } else {
          // veerkracht terug naar huis
          c.vx += (c.tx - c.x) * 0.058;
          c.vy += (c.ty - c.y) * 0.058;

          if (pointer.on) {
            var dx = c.x - pointer.x;
            var dy = c.y - pointer.y;
            var d2 = dx * dx + dy * dy;
            var R = Math.max(90, W * 0.14);
            if (d2 < R * R) {
              var d = Math.sqrt(d2) || 0.001;
              var f = (1 - d / R);
              var push = f * f * 5.4;
              c.vx += (dx / d) * push;
              c.vy += (dy / d) * push;
            }
          }

          c.vx *= 0.87;
          c.vy *= 0.87;
          c.x += c.vx;
          c.y += c.vy;

          // rustige golf die van links naar rechts loopt (per kolom, niet per blokje,
          // anders valt het woord uiteen in ruis)
          var wave = Math.sin(now * 0.0016 + c.tx * 0.016) * 1.2;
          px = c.x;
          py = c.y + wave;

          var speed = Math.abs(c.vx) + Math.abs(c.vy);
          s = drawSize * (1 + Math.min(0.55, speed * 0.05));
        }

        // De kleuren schuiven heen en weer door het verloop. Daardoor is elk
        // blokje steeds even donker genoeg om te lezen, zonder dat het woord
        // als geheel donkerder wordt.
        var shift = 0;
        if (!reduceMotion) {
          var w01 = Math.sin(now * SHIFT_SPEED - c.phase) * 0.5 + 0.5;   // 0..1
          shift = w01 * (SHIFT_DOWN + SHIFT_UP) - SHIFT_DOWN;
        }
        var ti = Math.round((c.bt + shift) * (STEPS_N - 1));
        if (ti < 0) ti = 0; else if (ti > STEPS_N - 1) ti = STEPS_N - 1;
        ctx.fillStyle = PALETTE[ti];
        var off = (s - drawSize) / 2;
        ctx.fillRect(px - off, py - off, s, s);
      }

      if (!introDone && intro === 1) introDone = true;
    }

    function frame(now) {
      rafId = 0;
      if (!running) return;
      paint(now);
      if (visible) rafId = requestAnimationFrame(frame);
    }

    function start(withIntro) {
      if (running || !cells.length) return;
      running = true;
      startTime = performance.now();
      introDone = !withIntro;
      if (!rafId) rafId = requestAnimationFrame(frame);
    }

    function stop() {
      running = false;
      if (rafId) { cancelAnimationFrame(rafId); rafId = 0; }
    }

    function staticPaint() {
      ctx.clearRect(0, 0, W, H);
      for (var i = 0; i < cells.length; i++) {
        var c = cells[i];
        ctx.fillStyle = PALETTE[Math.round(c.bt * (STEPS_N - 1))];
        ctx.fillRect(c.tx, c.ty, drawSize, drawSize);
      }
    }

    function setup(animate) {
      if (!build()) return;
      if (reduceMotion) { staticPaint(); return; }
      stop();
      // na een resize opnieuw opbouwen zonder de intro nog eens te spelen
      start(!!animate);
    }

    // pointer
    function movePointer(clientX, clientY) {
      var r = canvas.getBoundingClientRect();
      pointer.x = clientX - r.left;
      pointer.y = clientY - r.top;
      pointer.on = true;
    }
    if (!reduceMotion) {
      window.addEventListener('mousemove', function (e) {
        var r = canvas.getBoundingClientRect();
        var pad = 140;
        if (e.clientX > r.left - pad && e.clientX < r.right + pad &&
            e.clientY > r.top - pad && e.clientY < r.bottom + pad) {
          movePointer(e.clientX, e.clientY);
        } else {
          pointer.on = false;
        }
      }, { passive: true });
      canvas.addEventListener('touchmove', function (e) {
        if (e.touches && e.touches[0]) movePointer(e.touches[0].clientX, e.touches[0].clientY);
      }, { passive: true });
      canvas.addEventListener('touchend', function () { pointer.on = false; }, { passive: true });
      window.addEventListener('mouseout', function () { pointer.on = false; }, { passive: true });
    }

    // alleen tekenen als het in beeld is
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        visible = entries[0].isIntersecting;
        if (visible && !reduceMotion) { if (!rafId && running) rafId = requestAnimationFrame(frame); }
      }, { threshold: 0 }).observe(canvas);
    }
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) { if (rafId) { cancelAnimationFrame(rafId); rafId = 0; } }
      else if (running && visible) { if (!rafId) rafId = requestAnimationFrame(frame); }
    });

    // opbouwen zodra het lettertype er is
    var kick = function () { setup(true); };
    if (document.fonts && document.fonts.load) {
      document.fonts.load('700 100px "Space Grotesk"').then(kick, kick);
    } else {
      kick();
    }
    // vangnet als fonts.ready blijft hangen
    setTimeout(function () { if (!cells.length) setup(true); }, 1800);

    var rt;
    var lastW = window.innerWidth;
    window.addEventListener('resize', function () {
      if (window.innerWidth === lastW && Math.abs(canvas.getBoundingClientRect().width - W) < 2) return;
      lastW = window.innerWidth;
      clearTimeout(rt);
      rt = setTimeout(function () { setup(false); }, 180);
    });
  }

  /* -------------------------------------------------------
     2. Navigatie
     ------------------------------------------------------- */
  function initNav() {
    var nav = document.getElementById('nav');
    var burger = document.getElementById('burger');
    var menu = document.getElementById('mobilemenu');

    var onScroll = function () {
      if (nav) nav.classList.toggle('is-stuck', window.scrollY > 24);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });

    if (burger && menu) {
      var setOpen = function (open) {
        burger.setAttribute('aria-expanded', open ? 'true' : 'false');
        burger.querySelector('.sr-only').textContent = open ? 'Menu sluiten' : 'Menu openen';
        document.body.classList.toggle('menu-open', open);
        if (open) menu.removeAttribute('inert'); else menu.setAttribute('inert', '');
      };
      burger.addEventListener('click', function () {
        setOpen(burger.getAttribute('aria-expanded') !== 'true');
      });
      menu.addEventListener('click', function (e) {
        if (e.target.closest('a')) setOpen(false);
      });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && document.body.classList.contains('menu-open')) setOpen(false);
      });
    }

    // actieve link
    var links = Array.prototype.slice.call(document.querySelectorAll('[data-navlink]'));
    var map = {};
    links.forEach(function (a) {
      var id = a.getAttribute('href').slice(1);
      var sec = document.getElementById(id);
      if (sec) map[id] = a;
    });
    var ids = Object.keys(map);
    if (ids.length && 'IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) {
            links.forEach(function (l) { l.classList.remove('is-active'); });
            map[en.target.id].classList.add('is-active');
          }
        });
      }, { rootMargin: '-45% 0px -50% 0px', threshold: 0 });
      ids.forEach(function (id) { io.observe(document.getElementById(id)); });
    }
  }

  /* -------------------------------------------------------
     3. Reveal bij scrollen
     ------------------------------------------------------- */
  function initReveal() {
    var items = document.querySelectorAll('[data-reveal]');
    if (!items.length) return;
    if (reduceMotion || !('IntersectionObserver' in window)) {
      items.forEach(function (el) { el.classList.add('is-in'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add('is-in');
          io.unobserve(en.target);
        }
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
  }

  /* -------------------------------------------------------
     4. Parallax voor de swirls
     ------------------------------------------------------- */
  function initParallax() {
    if (reduceMotion) return;
    var els = Array.prototype.slice.call(document.querySelectorAll('[data-speed]'));
    if (!els.length) return;
    var ticking = false;

    var update = function () {
      ticking = false;
      var mid = window.scrollY + window.innerHeight / 2;
      for (var i = 0; i < els.length; i++) {
        var el = els[i];
        var host = el.parentElement;
        var rect = host.getBoundingClientRect();
        var hostMid = window.scrollY + rect.top + rect.height / 2;
        var offset = (mid - hostMid) * parseFloat(el.dataset.speed);
        if (offset > 70) offset = 70; else if (offset < -70) offset = -70;
        el.style.transform = 'translate3d(0,' + offset.toFixed(1) + 'px,0)';
      }
    };
    var onScroll = function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    };
    update();
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
  }

  /* -------------------------------------------------------
     5. Projectenrail: slepen + pijlen
     ------------------------------------------------------- */
  function initRail() {
    var rail = document.getElementById('rail');
    if (!rail) return;
    var prev = document.querySelector('[data-rail="prev"]');
    var next = document.querySelector('[data-rail="next"]');

    var step = function () {
      var card = rail.querySelector('.card');
      var gap = 20;
      return card ? card.getBoundingClientRect().width + gap : rail.clientWidth * 0.8;
    };

    var sync = function () {
      var max = rail.scrollWidth - rail.clientWidth - 2;
      if (prev) prev.disabled = rail.scrollLeft <= 2;
      if (next) next.disabled = rail.scrollLeft >= max;
    };

    if (prev) prev.addEventListener('click', function () { rail.scrollBy({ left: -step(), behavior: reduceMotion ? 'auto' : 'smooth' }); });
    if (next) next.addEventListener('click', function () { rail.scrollBy({ left: step(), behavior: reduceMotion ? 'auto' : 'smooth' }); });
    rail.addEventListener('scroll', sync, { passive: true });
    window.addEventListener('resize', sync);
    sync();

    // slepen met de muis
    var down = false, moved = false, startX = 0, startLeft = 0;
    rail.addEventListener('pointerdown', function (e) {
      if (e.pointerType !== 'mouse') return;
      down = true; moved = false;
      startX = e.clientX;
      startLeft = rail.scrollLeft;
    });
    rail.addEventListener('pointermove', function (e) {
      if (!down) return;
      var dx = e.clientX - startX;
      if (!moved && Math.abs(dx) > 6) { moved = true; rail.classList.add('is-dragging'); }
      if (moved) { rail.scrollLeft = startLeft - dx; e.preventDefault(); }
    });
    var end = function () {
      down = false;
      if (moved) setTimeout(function () { rail.classList.remove('is-dragging'); }, 0);
      moved = false;
    };
    rail.addEventListener('pointerup', end);
    rail.addEventListener('pointercancel', end);
    rail.addEventListener('pointerleave', end);
  }

  /* -------------------------------------------------------
     6. Kleine dingen
     ------------------------------------------------------- */
  function initMisc() {
    var y = document.getElementById('year');
    if (y) y.textContent = new Date().getFullYear();
  }

  /* ------------------------------------------------------- */
  function boot() {
    initNav();
    initReveal();
    initParallax();
    initRail();
    initMisc();
    initWordmark();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
