/* Lightbox — click any content image to view full size */
(function () {
  // Skip if page already has its own custom lightbox (avoid ID/handler conflicts)
  if (document.getElementById('lb-img') || document.getElementById('lightbox')) return;

  var RO = (document.documentElement.lang || "").toLowerCase().indexOf("ro") === 0;
  var T = RO ? { viewer: "Vizualizare imagine", close: "Închide vizualizarea imaginii" } : { viewer: "Image viewer", close: "Close image viewer" };

  // Build overlay once
  var overlay = document.createElement('div');
  overlay.id = 'lb-overlay';
  overlay.setAttribute('role', 'dialog');
  overlay.setAttribute('aria-modal', 'true');
  overlay.setAttribute('aria-label', T.viewer);
  overlay.innerHTML =
    '<div id="lb-wrap">' +
      '<img id="lb-img-global" alt="">' +
      '<button type="button" id="lb-close" aria-label="' + T.close + '">&times;</button>' +
    '</div>';
  document.body.appendChild(overlay);

  var lbImg = document.getElementById('lb-img-global');
  var closeBtn = document.getElementById('lb-close');
  var lastFocus = null;
  var style = document.createElement('style');
  style.textContent =
    '#lb-overlay{display:none;position:fixed;inset:0;z-index:9999;background:rgba(0,0,0,.85);' +
    'justify-content:center;align-items:center;cursor:zoom-out;}' +
    '#lb-overlay.show{display:flex;}' +
    '#lb-wrap{position:relative;max-width:92vw;max-height:92vh;}' +
    '#lb-img-global{max-width:92vw;max-height:92vh;object-fit:contain;border-radius:4px;box-shadow:0 0 40px rgba(0,0,0,.5);}' +
    '#lb-close{position:fixed;top:18px;right:24px;background:none;border:none;color:#fff;' +
    'font-size:40px;cursor:pointer;line-height:1;z-index:10000;font-weight:300;min-width:44px;min-height:44px;}' +
    '#lb-close:hover{opacity:.7;}' +
    '#lb-close:focus-visible{outline:2px solid #fff;outline-offset:2px;}' +
    'img[data-lb-bound]{cursor:zoom-in;}' +
    'img[data-lb-bound]:focus-visible{outline:2px solid #6B1B3D;outline-offset:3px;}';
  document.head.appendChild(style);

  function open(img) {
    lastFocus = document.activeElement;
    // the src attribute always points to the largest file (srcset only serves the in-page display)
    lbImg.src = img.getAttribute('data-full') || img.src;
    lbImg.alt = img.alt || '';
    overlay.classList.add('show');
    closeBtn.focus();
  }
  function close() {
    if (!overlay.classList.contains('show')) return;
    overlay.classList.remove('show');
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  // Close on click overlay or button
  overlay.addEventListener('click', close);

  // Close on Escape; keep focus inside the dialog
  document.addEventListener('keydown', function (e) {
    if (!overlay.classList.contains('show')) return;
    if (e.key === 'Escape') close();
    else if (e.key === 'Tab') { e.preventDefault(); closeBtn.focus(); }
  });

  // Attach to all content images (skip logos, icons, tiny images, paypal)
  function attach() {
    var imgs = document.querySelectorAll('img');
    for (var i = 0; i < imgs.length; i++) {
      var img = imgs[i];
      // Skip small images, SVGs, paypal logo, favicons
      if (img.naturalWidth && img.naturalWidth < 80) continue;
      if (img.height && img.height < 50) continue;
      if (img.src && img.src.indexOf('paypal') !== -1) continue;
      if (img.src && img.src.indexOf('favicon') !== -1) continue;
      if (img.id === 'lb-img-global') continue;
      if (getComputedStyle(img).pointerEvents === 'none') continue;
      if (img.closest('.nav') || img.closest('footer') || img.closest('.footer') || img.closest('a, button')) continue;
      if (img.dataset.lbBound) continue;
      img.dataset.lbBound = '1';
      if (!img.hasAttribute('tabindex')) img.setAttribute('tabindex', '0');
      img.addEventListener('click', function (e) {
        e.preventDefault();
        open(this);
      });
      img.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(this); }
      });
    }
  }

  // Run after DOM and also after lazy images load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', attach);
  } else {
    attach();
  }
  window.addEventListener('load', attach);
})();
