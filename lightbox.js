/* Lightbox — click any content image to view full size */
(function () {
  // Skip if page already has its own custom lightbox (avoid ID/handler conflicts)
  if (document.getElementById('lb-img') || document.getElementById('lightbox')) return;

  // Build overlay once
  var overlay = document.createElement('div');
  overlay.id = 'lb-overlay';
  overlay.innerHTML =
    '<div id="lb-wrap">' +
      '<img id="lb-img-global" alt="">' +
      '<button id="lb-close" aria-label="Close">&times;</button>' +
    '</div>';
  document.body.appendChild(overlay);

  var lbImg = document.getElementById('lb-img-global');
  var style = document.createElement('style');
  style.textContent =
    '#lb-overlay{display:none;position:fixed;inset:0;z-index:9999;background:rgba(0,0,0,.85);' +
    'justify-content:center;align-items:center;cursor:zoom-out;}' +
    '#lb-overlay.show{display:flex;}' +
    '#lb-wrap{position:relative;max-width:92vw;max-height:92vh;}' +
    '#lb-img-global{max-width:92vw;max-height:92vh;object-fit:contain;border-radius:4px;box-shadow:0 0 40px rgba(0,0,0,.5);}' +
    '#lb-close{position:fixed;top:18px;right:24px;background:none;border:none;color:#fff;' +
    'font-size:40px;cursor:pointer;line-height:1;z-index:10000;font-weight:300;}' +
    '#lb-close:hover{opacity:.7;}';
  document.head.appendChild(style);

  // Close on click overlay or button
  overlay.addEventListener('click', function () { overlay.classList.remove('show'); });

  // Close on Escape
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') overlay.classList.remove('show');
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
      if (img.closest('.nav') || img.closest('footer') || img.closest('.footer')) continue;
      if (img.dataset.lbBound) continue;
      img.dataset.lbBound = '1';
      img.style.cursor = 'default';
      img.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        lbImg.src = this.src;
        overlay.classList.add('show');
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
