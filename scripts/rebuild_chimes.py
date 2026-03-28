import re

# Read metal-cans CSS
with open('c:/Users/IONUT/Desktop/SITE-GHERAM-FULL/metal-cans-chimes.html', 'r', encoding='utf-8') as f:
    cans = f.read()

CSS = re.search(r'<style>(.*?)</style>', cans, re.DOTALL).group(1)

ICON_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/></svg>'
PREV_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 19l-7-7 7-7"/></svg>'
NEXT_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 5l7 7-7 7"/></svg>'
BACK_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 12H5M12 5l-7 7 7 7"/></svg>'

JS = """
    const gallery = document.querySelectorAll('.gallery-section .photo-item img');
    const lbImages = [];
    const lbCaptions = [];
    gallery.forEach(img => lbImages.push(img.src));
    document.querySelectorAll('.gallery-section .photo-caption').forEach(c => lbCaptions.push(c.textContent.trim()));
    let lbIdx = 0;
    function openLightbox(i) {
        lbIdx = i;
        document.getElementById('lb-img').src = lbImages[i];
        document.getElementById('lb-cap').textContent = lbCaptions[i] || '';
        document.getElementById('lb-counter').textContent = (i+1) + ' / ' + lbImages.length;
        document.getElementById('lightbox').classList.add('open');
        document.body.style.overflow = 'hidden';
    }
    function closeLightbox() {
        document.getElementById('lightbox').classList.remove('open');
        document.body.style.overflow = '';
    }
    function lbNav(dir) {
        lbIdx = (lbIdx + dir + lbImages.length) % lbImages.length;
        document.getElementById('lb-img').src = lbImages[lbIdx];
        document.getElementById('lb-cap').textContent = lbCaptions[lbIdx] || '';
        document.getElementById('lb-counter').textContent = (lbIdx+1) + ' / ' + lbImages.length;
    }
    document.addEventListener('keydown', e => {
        if (!document.getElementById('lightbox').classList.contains('open')) return;
        if (e.key === 'Escape') closeLightbox();
        if (e.key === 'ArrowLeft') lbNav(-1);
        if (e.key === 'ArrowRight') lbNav(1);
    });
"""

def get_imgs(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    return re.findall(r'src="(data:[^"]+)"', content)

def photo_item(src, cap, extra_class='', idx=0):
    cls = ' ' + extra_class if extra_class else ''
    return (
        '                <div class="photo-item' + cls + '" onclick="openLightbox(' + str(idx) + ')">\n'
        '                    <img src="' + src + '" alt="' + cap.replace('&amp;','&').replace('&','&amp;') + '" loading="lazy">\n'
        '                    <div class="photo-caption">' + cap + '</div>\n'
        '                </div>'
    )

def make_strip_html(imgs, caps, gidxs):
    html = '        <div class="hero-strip">\n'
    for i, (src, cap) in enumerate(zip(imgs, caps)):
        gidx = gidxs[i]
        num = '0' + str(i+1) if i < 9 else str(i+1)
        html += (
            '            <div class="strip-img" onclick="openLightbox(' + str(gidx) + ')">\n'
            '                <img src="' + src + '" alt="' + cap.replace('"', '&quot;') + '" loading="lazy">\n'
            '                <div class="strip-icon">' + ICON_SVG + '</div>\n'
            '                <span class="strip-num">' + num + '</span>\n'
            '                <span class="strip-caption">' + cap + '</span>\n'
            '            </div>\n'
        )
    html += '        </div>'
    return html

def build_page(title, subtitle, eyebrow, meta_html, desc_html, gallery_html,
               used_works, thanks_text, footer_note, strip_html):
    used_html = '\n'.join('                <div class="used-work">' + w + '</div>' for w in used_works)
    return (
        '<!DOCTYPE html>\n'
        '<html lang="en">\n'
        '<head>\n'
        '    <meta charset="UTF-8">\n'
        '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '    <title>' + title + ' \u2014 Alin Gherman</title>\n'
        '    <link rel="icon" href="/favicon.png" type="image/x-icon">\n'
        '    <link rel="shortcut icon" href="/favicon.png" type="image/x-icon">\n'
        '    <link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '    <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">\n'
        '    <style>' + CSS + '</style>\n'
        '</head>\n'
        '<body>\n\n'
        '    <nav class="nav">\n'
        '        <div class="nav-content">\n'
        '            <a href="index.html" class="nav-logo">ALIN GHERMAN</a>\n'
        '            <a href="index.html#instruments" class="back-btn">\n'
        '                ' + BACK_SVG + '\n'
        '                Back to Instruments\n'
        '            </a>\n'
        '        </div>\n'
        '    </nav>\n\n'
        '    <div class="hero">\n'
        + strip_html + '\n'
        '        <div class="hero-text">\n'
        '            <span class="hero-eyebrow">' + eyebrow + '</span>\n'
        '            <h1 class="hero-title">' + title + '</h1>\n'
        '            <span class="hero-sub">' + subtitle + '</span>\n'
        '        </div>\n'
        '        <div class="hero-hint">Click to expand</div>\n'
        '        <div class="scroll-cue">\n'
        '            <div class="scroll-dot"></div>\n'
        '            <div class="scroll-dot"></div>\n'
        '            <div class="scroll-dot"></div>\n'
        '        </div>\n'
        '    </div>\n\n'
        '    <div class="lightbox" id="lightbox">\n'
        '        <button class="lightbox-close" onclick="closeLightbox()">&times;</button>\n'
        '        <button class="lightbox-prev" onclick="lbNav(-1)">' + PREV_SVG + '</button>\n'
        '        <img class="lightbox-img" id="lb-img" src="" alt="">\n'
        '        <button class="lightbox-next" onclick="lbNav(1)">' + NEXT_SVG + '</button>\n'
        '        <div class="lightbox-caption" id="lb-cap"></div>\n'
        '        <div class="lightbox-counter" id="lb-counter"></div>\n'
        '    </div>\n\n'
        '    <section class="description-section">\n'
        '        <div class="container">\n'
        '            <div class="desc-grid">\n'
        '                <div class="desc-meta">\n'
        '                    <span class="section-label">Specifications</span>\n'
        + meta_html + '\n'
        '                </div>\n'
        '                <div class="desc-text">\n'
        '                    <span class="section-label">About the instrument</span>\n'
        + desc_html + '\n'
        '                </div>\n'
        '            </div>\n'
        '        </div>\n'
        '    </section>\n\n'
        '    <section class="gallery-section">\n'
        '        <div class="container">\n'
        + gallery_html + '\n'
        '        </div>\n'
        '    </section>\n\n'
        '    <section class="used-section">\n'
        '        <div class="container-narrow">\n'
        '            <span class="used-label">Featured In</span>\n'
        '            <div class="used-works">\n'
        + used_html + '\n'
        '            </div>\n'
        '            <div class="thanks-block">' + thanks_text + '</div>\n'
        '        </div>\n'
        '    </section>\n\n'
        '    <footer class="footer">\n'
        '        <div class="container">\n'
        '            <div class="footer-content">\n'
        '                <span class="footer-brand">ALIN GHERMAN</span>\n'
        '                <span class="footer-note">' + footer_note + '</span>\n'
        '            </div>\n'
        '        </div>\n'
        '    </footer>\n\n'
        '<script>\n' + JS + '\n</script>\n'
        '</body>\n'
        '</html>'
    )

THANKS_HKB = 'Special thanks to <strong>Urs Gehbauer</strong> and <strong>Letizia Lenherr</strong> from the H.K.B. Workshop in Bern, Switzerland, for their kind assistance.'
EYEBROW = 'Custom Instruments \u2014 Percussion'

# ============================================================
# 1. WOOD CHIMES
# ============================================================
wood_imgs = get_imgs('c:/Users/IONUT/Desktop/SITE-GHERAM-FULL/wood-chimes.html')
wood_caps = [
    'Set B \u201cThe Queen\u201d \u2014 front, High, Medium-High',
    'Set B \u201cThe Queen\u201d \u2014 front, High',
    'Set B \u201cThe Queen\u201d \u2014 front right, High + Medium-Low',
    'Set B \u201cThe Queen\u201d \u2014 back, Low + Medium-Low',
    'Set B \u201cThe Queen\u201d \u2014 back, Low',
    'Set B \u201cThe Queen\u201d \u2014 back, Low (detail)',
    'Set A',
    'Set A',
    'Set A',
    'Set C',
]

wood_meta = (
    '                    <div class="meta-item">\n'
    '                        <div class="meta-label">Workshop</div>\n'
    '                        <div class="meta-value">H.K.B. Workshop<br>Bern, Switzerland<br><strong>May\u2013June 2009</strong></div>\n'
    '                    </div>\n'
    '                    <div class="meta-item">\n'
    '                        <div class="meta-label">Set A \u2014 34 tubes</div>\n'
    '                        <div class="meta-value">Mixed registers<br>Recommended for <em>Purple Ritual</em><br><strong>Acquired by CIP Geneva</strong><br>Available for rent</div>\n'
    '                    </div>\n'
    '                    <div class="meta-item">\n'
    '                        <div class="meta-label">Set B \u201cThe Queen\u201d \u2014 64 tubes</div>\n'
    '                        <div class="meta-value">4 Registers:<br><strong>Low \xb7 Medium-Low \xb7 Medium-High \xb7 High</strong></div>\n'
    '                    </div>\n'
    '                    <div class="meta-item">\n'
    '                        <div class="meta-label">Set C \u2014 9 pieces</div>\n'
    '                        <div class="meta-value">Mono register<br>Very dry impact sound &amp; small resonances</div>\n'
    '                    </div>\n'
    '                    <div class="meta-item">\n'
    '                        <div class="meta-label">Platform</div>\n'
    '                        <div class="meta-value">Natural wood</div>\n'
    '                    </div>\n'
    '                    <div class="meta-item">\n'
    '                        <div class="meta-label">Commissioned for</div>\n'
    '                        <div class="meta-value"><strong>Geneva International Music Competition</strong><br>\u201cPurple Ritual\u201d</div>\n'
    '                    </div>'
)

wood_desc = (
    '                    <p>Three sets of Wood Chimes were made by Alin Gherman at the H.K.B. workshop in Bern (Switzerland), May\u2013June 2009, especially for <em>Purple Ritual</em> \u2014 a multi-percussion piece commissioned by the Geneva International Music Competition.</p>\n'
    '                    <p><strong>Set A</strong> consists of 34 mixed wood tubes covering mixed registers. It is particularly recommended for <em>Purple Ritual</em> and has been acquired by the Centre International de Percussion (CIP) in Geneva, where it is available for rent.</p>\n'
    '                    <p><strong>Set B \u201cThe Queen\u201d</strong> is the largest and most complete set, featuring 64 mixed wood tubes across four registers: Low, Medium-Low, Medium-High, and High. Sets A and B were especially assembled to resonate as long as possible.</p>\n'
    '                    <p><strong>Set C</strong> features 9 pieces assembled to produce a very dry impact sound and small resonances \u2014 a distinct timbral counterpoint to Sets A and B.</p>\n'
    '                    <div class="highlight-box">\n'
    '                        <p>Quality hand-made manufacturing: all knots secured with hot glue, rounded ends, and 3 types of wires matched to tube sizes. The performer may freely choose which tubes to let ring \u2014 the density of the sound is freely controlled.</p>\n'
    '                    </div>'
)

wood_gallery = (
    '            <div class="gallery-header">\n'
    '                <span class="section-label">Photography</span>\n'
    '                <h2 class="gallery-title">Set B \u2014 \u201cThe Queen\u201d</h2>\n'
    '                <p class="gallery-subtitle">64 mixed wood tubes \xb7 4 registers \xb7 H.K.B. Studio, Bern</p>\n'
    '            </div>\n'
    '            <div class="photo-row photo-row-lp" style="margin-bottom:20px;">\n'
    + photo_item(wood_imgs[0], wood_caps[0], 'landscape', 0) + '\n'
    + photo_item(wood_imgs[1], wood_caps[1], 'portrait', 1) + '\n'
    '            </div>\n'
    '            <div class="photo-grid-3" style="margin-bottom:20px;">\n'
    + photo_item(wood_imgs[2], wood_caps[2], '', 2) + '\n'
    + photo_item(wood_imgs[3], wood_caps[3], '', 3) + '\n'
    + photo_item(wood_imgs[4], wood_caps[4], '', 4) + '\n'
    '            </div>\n'
    '            <div class="photo-grid-3" style="margin-bottom:48px;">\n'
    + photo_item(wood_imgs[5], wood_caps[5], '', 5) + '\n'
    '            </div>\n'
    '            <div class="gallery-header" style="margin-top:16px;">\n'
    '                <span class="section-label">Photography</span>\n'
    '                <h2 class="gallery-title">Set A</h2>\n'
    '                <p class="gallery-subtitle">34 mixed wood tubes \xb7 Mixed registers \xb7 Acquired by CIP Geneva</p>\n'
    '            </div>\n'
    '            <div class="photo-grid-3" style="margin-bottom:48px;">\n'
    + photo_item(wood_imgs[6], wood_caps[6], '', 6) + '\n'
    + photo_item(wood_imgs[7], wood_caps[7], '', 7) + '\n'
    + photo_item(wood_imgs[8], wood_caps[8], '', 8) + '\n'
    '            </div>\n'
    '            <div class="gallery-header" style="margin-top:16px;">\n'
    '                <span class="section-label">Photography</span>\n'
    '                <h2 class="gallery-title">Set C</h2>\n'
    '                <p class="gallery-subtitle">9 pieces \xb7 Mono register \xb7 Dry impact sound</p>\n'
    '            </div>\n'
    '            <div class="photo-grid-2">\n'
    + photo_item(wood_imgs[9], wood_caps[9], 'landscape', 9) + '\n'
    '            </div>'
)

wood_strip = make_strip_html(wood_imgs[:5], wood_caps[:5], [0,1,2,3,4])
wood_html = build_page('Wood Chimes', 'powerful instruments.', EYEBROW,
    wood_meta, wood_desc, wood_gallery,
    ['\u201cPurple Ritual\u201d \u2014 multi-percussion, Geneva International Music Competition',
     '\u201cEin Werktag\u201d \u2014 original soundtrack'],
    THANKS_HKB + ' All three sets.',
    'Wood Chimes \u2014 H.K.B. Workshop, Bern 2009',
    wood_strip)
with open('c:/Users/IONUT/Desktop/SITE-GHERAM-FULL/wood-chimes.html', 'w', encoding='utf-8') as f:
    f.write(wood_html)
print('wood-chimes.html: OK (' + str(len(wood_html)) + ' chars)')

# ============================================================
# 2. GLASS CHIMES
# ============================================================
glass_imgs = get_imgs('c:/Users/IONUT/Desktop/SITE-GHERAM-FULL/glass-chimes.html')
glass_caps = [
    'Set B \u2014 Medium register',
    'Set B \u2014 Low register',
    'Set A \u2014 front view, Low (left), Medium (centre) & High (right)',
    'Set B \u2014 front view, Low (left), Medium (centre) & High (right)',
]

glass_meta = (
    '                    <div class="meta-item">\n'
    '                        <div class="meta-label">Workshop</div>\n'
    '                        <div class="meta-value">H.K.B. Workshop<br>Bern, Switzerland<br><strong>May 2009</strong></div>\n'
    '                    </div>\n'
    '                    <div class="meta-item">\n'
    '                        <div class="meta-label">Composition</div>\n'
    '                        <div class="meta-value"><strong>37 light bulbs</strong> per set<br>old &amp; new glass bulbs</div>\n'
    '                    </div>\n'
    '                    <div class="meta-item">\n'
    '                        <div class="meta-label">Registers</div>\n'
    '                        <div class="meta-value"><strong>Low \xb7 Medium \xb7 High</strong><br>Low (left) \u2192 High (right)<br>3 independent registers per set</div>\n'
    '                    </div>\n'
    '                    <div class="meta-item">\n'
    '                        <div class="meta-label">Sets</div>\n'
    '                        <div class="set-tags">\n'
    '                            <div class="set-tag">\n'
    '                                <div class="tag-name">Set A \u2014 37 bulbs</div>\n'
    '                                <div class="tag-registers">\n'
    '                                    <div class="tag-reg">Low: <span>10 pieces</span></div>\n'
    '                                    <div class="tag-reg">Medium: <span>11 pieces</span></div>\n'
    '                                    <div class="tag-reg">High: <span>16 pieces</span></div>\n'
    '                                </div>\n'
    '                                <div class="tag-cip">Acquired by CIP Geneva \xb7 Available for rent</div>\n'
    '                            </div>\n'
    '                            <div class="set-tag">\n'
    '                                <div class="tag-name">Set B \u2014 37 bulbs</div>\n'
    '                                <div class="tag-registers">\n'
    '                                    <div class="tag-reg">Low: <span>12 pieces</span></div>\n'
    '                                    <div class="tag-reg">Medium: <span>11 pieces</span></div>\n'
    '                                    <div class="tag-reg">High: <span>14 pieces</span></div>\n'
    '                                </div>\n'
    '                            </div>\n'
    '                        </div>\n'
    '                    </div>\n'
    '                    <div class="meta-item">\n'
    '                        <div class="meta-label">Platform</div>\n'
    '                        <div class="meta-value">Natural wood</div>\n'
    '                    </div>\n'
    '                    <div class="meta-item">\n'
    '                        <div class="meta-label">Commissioned for</div>\n'
    '                        <div class="meta-value"><strong>Geneva International Music Competition</strong><br>\u201cPurple Ritual\u201d</div>\n'
    '                    </div>'
)

glass_desc = (
    '                    <p>Made by Alin Gherman at the H.K.B. workshop in Bern (Switzerland), May 2009, especially for <em>Purple Ritual</em> \u2014 a multi-percussion piece commissioned by the Geneva International Music Competition.</p>\n'
    '                    <p>Both sets A and B are composed of 37 light bulbs each, spanning three independent registers. Quality hand-made manufacturing: all knots secured with hot glue. The Glass Chimes were especially assembled in order to resonate very long.</p>\n'
    '                    <div class="highlight-box">\n'
    '                        <p>The white plastic wires are long enough to allow the performer to easily isolate any non-desired glass bulb on the wood platform \u2014 the performer may freely choose which sounds and pitches to let ring.</p>\n'
    '                    </div>\n'
    '                    <p style="margin-top:24px;">Set A has been acquired by the <strong>Centre International de Percussion (CIP)</strong> in Geneva, Switzerland, and is available for rent.</p>\n'
    '                    <p>The Glass Chimes were included in the instrumentation of <em>Purple Ritual</em> and <em>Metal Spirits I</em>, as well as in the original soundtrack of <em>Ein Werktag</em>.</p>'
)

glass_gallery = (
    '            <div class="gallery-header">\n'
    '                <span class="section-label">Photography</span>\n'
    '                <h2 class="gallery-title">Sets A &amp; B</h2>\n'
    '                <p class="gallery-subtitle">74 light bulbs total \xb7 Bern, May 2009</p>\n'
    '            </div>\n'
    '            <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px;">\n'
    + photo_item(glass_imgs[0], glass_caps[0], 'landscape', 0) + '\n'
    + photo_item(glass_imgs[1], glass_caps[1], 'portrait', 1) + '\n'
    '            </div>\n'
    '            <div class="photo-grid-2">\n'
    + photo_item(glass_imgs[2], glass_caps[2], 'landscape', 2) + '\n'
    + photo_item(glass_imgs[3], glass_caps[3], 'landscape', 3) + '\n'
    '            </div>'
)

glass_strip = make_strip_html(glass_imgs[:4], glass_caps[:4], [0,1,2,3])
glass_html = build_page('Glass Chimes', 'a very long resonating instrument.', EYEBROW,
    glass_meta, glass_desc, glass_gallery,
    ['\u201cPurple Ritual\u201d \u2014 multi-percussion, Geneva International Music Competition',
     '\u201cMetal Spirits I\u201d',
     '\u201cEin Werktag\u201d \u2014 original soundtrack'],
    THANKS_HKB + ' Both sets.',
    'Glass Chimes \u2014 H.K.B. Workshop, Bern 2009',
    glass_strip)
with open('c:/Users/IONUT/Desktop/SITE-GHERAM-FULL/glass-chimes.html', 'w', encoding='utf-8') as f:
    f.write(glass_html)
print('glass-chimes.html: OK (' + str(len(glass_html)) + ' chars)')

# ============================================================
# 3. METAL TUBES CHIMES
# ============================================================
tubes_imgs = get_imgs('c:/Users/IONUT/Desktop/SITE-GHERAM-FULL/metal-tubes-chimes.html')
tubes_caps = [
    'Natural light \u2014 full view',
    'Warm light \u2014 detail',
    'Platform \u2014 natural wood',
    'Wood frame \u2014 construction detail',
    'Spoon &amp; tubes \u2014 assembled',
    'Resonator detail',
    'Full instrument \u2014 H.K.B. Studio',
]
# Pad if needed
while len(tubes_caps) < len(tubes_imgs):
    tubes_caps.append('Detail')

tubes_meta = (
    '                    <div class="meta-item">\n'
    '                        <div class="meta-label">Workshop</div>\n'
    '                        <div class="meta-value">H.K.B. Workshop<br>Bern, Switzerland<br><strong>May 2009</strong></div>\n'
    '                    </div>\n'
    '                    <div class="meta-item">\n'
    '                        <div class="meta-label">Components</div>\n'
    '                        <div class="meta-value"><strong>12 tubes</strong> (solid &amp; hollowed)<br>1 huge spoon</div>\n'
    '                    </div>\n'
    '                    <div class="meta-item">\n'
    '                        <div class="meta-label">Registers</div>\n'
    '                        <div class="meta-value"><strong>Mixed</strong><br>Microtonal tuning</div>\n'
    '                    </div>\n'
    '                    <div class="meta-item">\n'
    '                        <div class="meta-label">Platform</div>\n'
    '                        <div class="meta-value">Natural wood<br>Extensible design</div>\n'
    '                    </div>\n'
    '                    <div class="meta-item">\n'
    '                        <div class="meta-label">Resonance</div>\n'
    '                        <div class="meta-value"><strong>Extremely long</strong></div>\n'
    '                    </div>\n'
    '                    <div class="meta-item">\n'
    '                        <div class="meta-label">Status</div>\n'
    '                        <div class="meta-value"><strong>Unique instrument</strong></div>\n'
    '                    </div>'
)

tubes_desc = (
    '                    <p>Made by Alin Gherman at the H.K.B. workshop in Bern (Switzerland), May 2009. A unique instrument composed of 12 tubes (solid &amp; hollowed) and 1 huge spoon, assembled on a platform of natural wood already prepared with holes for easy extension.</p>\n'
    '                    <p>Quality hand-made manufacturing: all knots secured with hot glue, resonant tubes and spoon, aesthetically assembled. Tuning: microtonal and slightly polarized, not based on any classified chord.</p>\n'
    '                    <div class="highlight-box">\n'
    '                        <p>These Metal Tubes chimes were especially assembled in order to resonate extremely long. The red-yellow plastic wires are long enough to allow the performer to easily isolate any non-desired tubes \u2014 the performer may choose which sounds and pitches to let ring freely.</p>\n'
    '                    </div>\n'
    '                    <p style="margin-top:24px;">The Metal Tubes Chimes were built as a continuation of the <em>\u201cPurple Ritual\u201d</em> chimes series, and were included in the instrumentation of the original soundtrack of <em>\u201cEin Werktag\u201d</em>.</p>'
)

n_tubes = len(tubes_imgs)
if n_tubes >= 7:
    tubes_gallery = (
        '            <div class="gallery-header">\n'
        '                <span class="section-label">Photography</span>\n'
        '                <h2 class="gallery-title">Instrument Gallery</h2>\n'
        '                <p class="gallery-subtitle">12 tubes + 1 huge spoon \xb7 H.K.B. Studio, Bern 2009</p>\n'
        '            </div>\n'
        '            <div class="photo-row photo-row-lp" style="margin-bottom:20px;">\n'
        + photo_item(tubes_imgs[0], tubes_caps[0], 'landscape', 0) + '\n'
        + photo_item(tubes_imgs[1], tubes_caps[1], 'portrait', 1) + '\n'
        '            </div>\n'
        '            <div class="photo-grid-3" style="margin-bottom:20px;">\n'
        + photo_item(tubes_imgs[2], tubes_caps[2], '', 2) + '\n'
        + photo_item(tubes_imgs[3], tubes_caps[3], '', 3) + '\n'
        + photo_item(tubes_imgs[4], tubes_caps[4], '', 4) + '\n'
        '            </div>\n'
        '            <div class="photo-grid-2">\n'
        + photo_item(tubes_imgs[5], tubes_caps[5], 'landscape', 5) + '\n'
        + photo_item(tubes_imgs[6], tubes_caps[6], 'landscape', 6) + '\n'
        '            </div>'
    )
else:
    tubes_gallery = (
        '            <div class="gallery-header">\n'
        '                <span class="section-label">Photography</span>\n'
        '                <h2 class="gallery-title">Instrument Gallery</h2>\n'
        '                <p class="gallery-subtitle">12 tubes + 1 huge spoon \xb7 H.K.B. Studio, Bern 2009</p>\n'
        '            </div>\n'
        '            <div class="photo-grid-2">\n'
        + '\n'.join(photo_item(tubes_imgs[i], tubes_caps[i], 'landscape', i) for i in range(n_tubes)) + '\n'
        '            </div>'
    )

tubes_strip = make_strip_html(tubes_imgs[:min(5, n_tubes)], tubes_caps[:min(5, n_tubes)], list(range(min(5, n_tubes))))
tubes_html = build_page('Metal Tubes Chimes', 'flexible &amp; extremely long resonating.', EYEBROW,
    tubes_meta, tubes_desc, tubes_gallery,
    ['\u201cEin Werktag\u201d \u2014 original soundtrack'],
    THANKS_HKB,
    'Metal Tubes Chimes \u2014 H.K.B. Workshop, Bern 2009',
    tubes_strip)
with open('c:/Users/IONUT/Desktop/SITE-GHERAM-FULL/metal-tubes-chimes.html', 'w', encoding='utf-8') as f:
    f.write(tubes_html)
print('metal-tubes-chimes.html: OK (' + str(len(tubes_html)) + ' chars)')

# ============================================================
# 4. STONE CHIMES
# ============================================================
stone_imgs = get_imgs('c:/Users/IONUT/Desktop/SITE-GHERAM-FULL/stone-chimes.html')
stone_caps = [
    'Set A \u2014 back, High, Medium',
    'Set A \u2014 front, Low',
    'Set A \u2014 left side, High, Medium &amp; Low',
    'Set B \u2014 stones before assembly',
    'Set B \u2014 top, manufacturing details',
    'Set B \u2014 front, Low',
    'Set B \u2014 front right, Low',
    'Set B \u2014 back right, High',
]
while len(stone_caps) < len(stone_imgs):
    stone_caps.append('Detail')

stone_meta = (
    '                    <div class="meta-item">\n'
    '                        <div class="meta-label">Workshop</div>\n'
    '                        <div class="meta-value">H.K.B. Workshop<br>Bern, Switzerland<br><strong>May\u2013June 2009</strong></div>\n'
    '                    </div>\n'
    '                    <div class="meta-item">\n'
    '                        <div class="meta-label">Set A \u2014 33 stones</div>\n'
    '                        <div class="meta-value">Registers: <strong>Low, Medium, High</strong><br>(higher pitch than Set B)</div>\n'
    '                    </div>\n'
    '                    <div class="meta-item">\n'
    '                        <div class="meta-label">Set B \u2014 45 stones</div>\n'
    '                        <div class="meta-value">Registers: <strong>Low, Medium, High</strong></div>\n'
    '                    </div>\n'
    '                    <div class="meta-item">\n'
    '                        <div class="meta-label">Platform</div>\n'
    '                        <div class="meta-value">Matted black painted wood</div>\n'
    '                    </div>\n'
    '                    <div class="meta-item">\n'
    '                        <div class="meta-label">Acquired by</div>\n'
    '                        <div class="meta-value"><strong>Centre International de Percussion (CIP)</strong><br>Geneva, Switzerland</div>\n'
    '                    </div>\n'
    '                    <div class="meta-item">\n'
    '                        <div class="meta-label">Commissioned for</div>\n'
    '                        <div class="meta-value"><strong>Geneva International Music Competition</strong><br>\u201cPurple Ritual\u201d</div>\n'
    '                    </div>'
)

stone_desc = (
    '                    <p>Set A and Set B were made by Alin Gherman at the H.K.B. workshop in Bern (Switzerland), May\u2013June 2009, especially for <em>Purple Ritual</em> \u2014 a multi-percussion piece commissioned by the Geneva International Music Competition.</p>\n'
    '                    <p>Set A is composed of <strong>33 stones</strong> collected from the river Aare in Bern, Switzerland. Set B consists of <strong>45 stones</strong>, also collected from the Aare. All stones were selected for their natural resonant qualities and assembled to resonate as long as possible.</p>\n'
    '                    <div class="highlight-box">\n'
    '                        <p>Quality hand-made manufacturing: all knots secured with hot glue, resonant stones aesthetically assembled. The stone colours may change depending on the lighting conditions.</p>\n'
    '                    </div>\n'
    '                    <p style="margin-top:24px;">Both sets are included in the instrumentation of <em>Purple Ritual</em> and <em>Metal Spirits I &amp; II</em>, as well as in the original soundtrack of <em>Ein Werktag</em>.</p>'
)

stone_gallery = (
    '            <div class="gallery-header">\n'
    '                <span class="section-label">Photography</span>\n'
    '                <h2 class="gallery-title">Set A</h2>\n'
    '                <p class="gallery-subtitle">33 stones \u2014 River Aare, Bern</p>\n'
    '            </div>\n'
    '            <div class="photo-row photo-row-lp" style="margin-bottom:20px;">\n'
    + photo_item(stone_imgs[0], stone_caps[0], 'landscape', 0) + '\n'
    + photo_item(stone_imgs[1], stone_caps[1], 'portrait', 1) + '\n'
    '            </div>\n'
    '            <div class="photo-grid-2" style="margin-bottom:48px;">\n'
    + photo_item(stone_imgs[2], stone_caps[2], 'landscape', 2) + '\n'
    '            </div>\n'
    '            <div class="gallery-header" style="margin-top:16px;">\n'
    '                <span class="section-label">Photography</span>\n'
    '                <h2 class="gallery-title">Set B</h2>\n'
    '                <p class="gallery-subtitle">45 stones \u2014 River Aare, Bern</p>\n'
    '            </div>\n'
    '            <div class="photo-grid-3" style="margin-bottom:20px;">\n'
    + photo_item(stone_imgs[3], stone_caps[3], '', 3) + '\n'
    + photo_item(stone_imgs[4], stone_caps[4], '', 4) + '\n'
    + photo_item(stone_imgs[5], stone_caps[5], '', 5) + '\n'
    '            </div>\n'
    '            <div class="photo-grid-2">\n'
    + photo_item(stone_imgs[6], stone_caps[6], 'landscape', 6) + '\n'
    + photo_item(stone_imgs[7], stone_caps[7], 'landscape', 7) + '\n'
    '            </div>'
)

stone_strip = make_strip_html(stone_imgs[:5], stone_caps[:5], [0,1,2,3,4])
stone_html = build_page('Stone Chimes', 'unique instruments.', EYEBROW,
    stone_meta, stone_desc, stone_gallery,
    ['\u201cPurple Ritual\u201d \u2014 multi-percussion, Geneva International Music Competition',
     '\u201cMetal Spirits I &amp; II\u201d',
     '\u201cEin Werktag\u201d \u2014 original soundtrack'],
    THANKS_HKB + ' Both sets.',
    'Stone Chimes \u2014 H.K.B. Workshop, Bern 2009',
    stone_strip)
with open('c:/Users/IONUT/Desktop/SITE-GHERAM-FULL/stone-chimes.html', 'w', encoding='utf-8') as f:
    f.write(stone_html)
print('stone-chimes.html: OK (' + str(len(stone_html)) + ' chars)')

# ============================================================
# 5. METAL SPOONS CHIMES (only 1 external image available)
# ============================================================
spoons_img = 'metal-spoons-forks-chimes.webp'

spoons_meta = (
    '                    <div class="meta-item">\n'
    '                        <div class="meta-label">Workshop</div>\n'
    '                        <div class="meta-value">H.K.B. Workshop<br>Bern, Switzerland<br><strong>July 2009</strong></div>\n'
    '                    </div>\n'
    '                    <div class="meta-item">\n'
    '                        <div class="meta-label">Composition</div>\n'
    '                        <div class="meta-value"><strong>43 pieces</strong><br>old &amp; new spoons, forks<br>&amp; coffee spoons</div>\n'
    '                    </div>\n'
    '                    <div class="meta-item">\n'
    '                        <div class="meta-label">Registers</div>\n'
    '                        <div class="meta-value"><strong>Low \xb7 Medium \xb7 High</strong><br>Low (left) \u2192 High (right)</div>\n'
    '                    </div>\n'
    '                    <div class="meta-item">\n'
    '                        <div class="meta-label">Platform</div>\n'
    '                        <div class="meta-value">Wood painted in black<br>Sides painted in <strong>gold</strong></div>\n'
    '                    </div>\n'
    '                    <div class="meta-item">\n'
    '                        <div class="meta-label">Status</div>\n'
    '                        <div class="meta-value"><strong>Unique instrument</strong></div>\n'
    '                    </div>'
)

spoons_desc = (
    '                    <p>Made by Alin Gherman at the H.K.B. workshop in Bern (Switzerland) in July 2009. This unique instrument is composed of 43 old and new spoons, forks and coffee spoons, spanning three registers \u2014 Low, Medium and High \u2014 arranged from left to right on a black wood platform with gold-painted sides.</p>\n'
    '                    <p>Quality hand-made manufacturing: all knots secured with hot glue. The Metal Spoons Chimes were especially assembled in order to resonate very long.</p>\n'
    '                    <div class="highlight-box">\n'
    '                        <p>The black plastic wires are long enough to allow the performer to easily isolate any non-desired spoons or forks on the wood platform \u2014 the performer may freely choose which sounds and pitches to let ring.</p>\n'
    '                    </div>'
)

spoons_gallery = (
    '            <div class="gallery-header">\n'
    '                <span class="section-label">Photography</span>\n'
    '                <h2 class="gallery-title">Instrument Gallery</h2>\n'
    '                <p class="gallery-subtitle">43 spoons, forks &amp; coffee spoons \xb7 H.K.B. Studio, Bern 2009</p>\n'
    '            </div>\n'
    '            <div class="photo-row photo-row-lp">\n'
    '                <div class="photo-item landscape" onclick="openLightbox(0)">\n'
    '                    <img src="' + spoons_img + '" alt="Metal Spoons &amp; Forks Chimes" loading="lazy">\n'
    '                    <div class="photo-caption">Spoons, forks &amp; coffee spoons \u2014 full view</div>\n'
    '                </div>\n'
    '            </div>'
)

spoons_strip = (
    '        <div class="hero-strip">\n'
    '            <div class="strip-img" onclick="openLightbox(0)">\n'
    '                <img src="' + spoons_img + '" alt="Full view" loading="lazy">\n'
    '                <div class="strip-icon">' + ICON_SVG + '</div>\n'
    '                <span class="strip-num">01</span>\n'
    '                <span class="strip-caption">Full view</span>\n'
    '            </div>\n'
    '            <div class="strip-img" onclick="openLightbox(0)">\n'
    '                <img src="' + spoons_img + '" alt="Low register" loading="lazy">\n'
    '                <div class="strip-icon">' + ICON_SVG + '</div>\n'
    '                <span class="strip-num">02</span>\n'
    '                <span class="strip-caption">Low register</span>\n'
    '            </div>\n'
    '            <div class="strip-img" onclick="openLightbox(0)">\n'
    '                <img src="' + spoons_img + '" alt="Spoons detail" loading="lazy">\n'
    '                <div class="strip-icon">' + ICON_SVG + '</div>\n'
    '                <span class="strip-num">03</span>\n'
    '                <span class="strip-caption">Spoons detail</span>\n'
    '            </div>\n'
    '        </div>'
)

spoons_html = build_page('Metal Spoons Chimes', 'a flexible and unique instrument.', EYEBROW,
    spoons_meta, spoons_desc, spoons_gallery,
    ['\u201cMetal Spirits I\u201d',
     '\u201cEin Werktag\u201d \u2014 original soundtrack'],
    THANKS_HKB,
    'Metal Spoons Chimes \u2014 H.K.B. Workshop, Bern 2009',
    spoons_strip)
with open('c:/Users/IONUT/Desktop/SITE-GHERAM-FULL/metal-spoons-chimes.html', 'w', encoding='utf-8') as f:
    f.write(spoons_html)
print('metal-spoons-chimes.html: OK (' + str(len(spoons_html)) + ' chars)')

print('\nAll 5 chimes pages rebuilt successfully!')
