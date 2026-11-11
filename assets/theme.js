/* KALO Gifts theme scripts. No dependencies. */
(function () {
  'use strict';

  /* mobile menu */
  var toggle = document.querySelector('[data-menu-toggle]');
  var nav = document.querySelector('[data-nav]');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open);
    });
  }

  /* product form: variant selection, price, quantity, gallery */
  var form = document.querySelector('[data-product-form]');
  if (form) {
    var json = document.querySelector('[data-product-json]');
    var product = json ? JSON.parse(json.textContent) : null;
    var idInput = form.querySelector('[name=id]');
    var priceEl = document.querySelector('[data-price]');
    var btn = form.querySelector('[data-add]');
    var fmt = new Intl.NumberFormat('en-IN', { style: 'currency', currency: (window.Shopify && Shopify.currency && Shopify.currency.active) || 'INR', maximumFractionDigits: 0 });

    var update = function () {
      if (!product) return;
      var chosen = [];
      form.querySelectorAll('.opt').forEach(function (g) {
        var c = g.querySelector('input:checked');
        chosen.push(c ? c.value : null);
      });
      var v = product.variants.find(function (x) {
        return x.options.every(function (o, i) { return chosen[i] === null || chosen[i] === o; });
      });
      if (!v) { if (btn) { btn.disabled = true; btn.querySelector('span').textContent = 'Unavailable'; } return; }
      idInput.value = v.id;
      if (priceEl) priceEl.textContent = fmt.format(v.price / 100);
      if (btn) {
        btn.disabled = !v.available;
        btn.querySelector('span').textContent = v.available ? 'Add to bag' : 'Sold out';
      }
      var wa = document.querySelector('[data-wa]');
      if (wa) {
        var msg = "Hi KALO! I'd like to customise: " + wa.getAttribute('data-wa-title') +
          (product.variants.length > 1 ? ' (' + v.options.join(', ') + ')' : '') + ' ' + wa.getAttribute('data-wa-url');
        wa.href = 'https://wa.me/' + wa.getAttribute('data-wa') + '?text=' + encodeURIComponent(msg);
      }
      var url = new URL(location.href);
      url.searchParams.set('variant', v.id);
      history.replaceState({}, '', url);
    };
    form.addEventListener('change', update);
    update();

    var q = form.querySelector('[data-qty]');
    form.querySelectorAll('[data-step]').forEach(function (b) {
      b.addEventListener('click', function () {
        var n = Math.max(1, (parseInt(q.value, 10) || 1) + parseInt(b.getAttribute('data-step'), 10));
        q.value = n;
      });
    });

  }

  document.querySelectorAll('[data-thumb]').forEach(function (b) {
    b.addEventListener('click', function () {
      var main = document.querySelector('.pdp .gallery .frame img');
      if (main) { main.src = b.getAttribute('data-src'); main.removeAttribute('srcset'); }
    });
  });

  /* handwritten gift card add-on: adds the card as a second line in the bag */
  var gcBox = document.querySelector('[data-gc]');
  if (form && gcBox) {
    var gcToggle = gcBox.querySelector('[data-gc-toggle]');
    var gcBody = gcBox.querySelector('[data-gc-body]');
    var gcText = gcBox.querySelector('[data-gc-text]');
    var gcCount = gcBox.querySelector('[data-gc-count]');
    gcToggle.addEventListener('change', function () { gcBody.hidden = !gcToggle.checked; if (gcToggle.checked) gcText.focus(); });
    gcText.addEventListener('input', function () { gcCount.textContent = gcText.value.length; });
    form.addEventListener('submit', function (e) {
      if (!gcToggle.checked) return;
      e.preventDefault();
      var msg = gcText.value.trim();
      if (!msg) { gcText.focus(); gcText.setCustomValidity('Write your message, or untick the gift card.'); gcText.reportValidity(); gcText.setCustomValidity(''); return; }
      var qty = Math.max(1, parseInt(form.querySelector('[name=quantity]').value, 10) || 1);
      var title = document.querySelector('.pdp h1').textContent.trim();
      fetch('/products/' + gcBox.getAttribute('data-gc-handle') + '.js')
        .then(function (r) { return r.json(); })
        .then(function (gc) {
          return fetch('/cart/add.js', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ items: [
              { id: Number(idInput.value), quantity: qty },
              { id: gc.variants[0].id, quantity: qty, properties: { 'Message': msg, 'For': title } }
            ] })
          });
        })
        .then(function (r) { if (!r.ok) throw new Error('add failed'); window.location.href = '/cart'; })
        .catch(function () { form.submit(); });
    });
  }

  /* snowfall */
  var snow = document.querySelector('[data-snow]');
  if (snow && !(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches)) {
    var sctx = snow.getContext('2d'), W = 0, H = 0, flakes = [], raf = 0, t = 0;
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var seed = function () {
      var n = Math.round(Math.min(80, Math.max(26, W / 18)));
      flakes = [];
      for (var i = 0; i < n; i++) {
        flakes.push({ x: Math.random() * W, y: Math.random() * H, r: Math.random() * 2.2 + 0.9,
          v: Math.random() * 0.8 + 0.4, p: Math.random() * 6.28, a: Math.random() * 0.4 + 0.6 });
      }
    };
    var resize = function () {
      W = window.innerWidth; H = window.innerHeight;
      snow.width = W * dpr; snow.height = H * dpr;
      sctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      seed();
    };
    var draw = function () {
      t += 0.01;
      sctx.clearRect(0, 0, W, H);
      sctx.lineWidth = 0.7;
      sctx.strokeStyle = 'rgba(15,61,46,0.28)';
      for (var i = 0; i < flakes.length; i++) {
        var f = flakes[i];
        f.y += f.v; f.x += Math.sin(t + f.p) * 0.35;
        if (f.y > H + 5) { f.y = -5; f.x = Math.random() * W; }
        if (f.x > W + 5) f.x = -5; else if (f.x < -5) f.x = W + 5;
        sctx.beginPath();
        sctx.fillStyle = 'rgba(255,255,255,' + f.a + ')';
        sctx.arc(f.x, f.y, f.r, 0, 6.2832);
        sctx.fill(); sctx.stroke();
      }
      raf = requestAnimationFrame(draw);
    };
    resize();
    window.addEventListener('resize', resize);
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) cancelAnimationFrame(raf); else raf = requestAnimationFrame(draw);
    });
    raf = requestAnimationFrame(draw);
  }
})();
