"""
Performance & mobile-first improvements:
- Meta tags, OG, Schema.org on index.html
- Nav hamburger: translateX approach (mobile-first)
- loading=lazy on all external images
- manifest.json link
- prefers-reduced-motion
"""
import re, glob, os

BASE = 'c:/Users/IONUT/Desktop/SITE-GHERAM-FULL/'

# ──────────────────────────────────────────────
# 1. INDEX.HTML — meta tags + OG + schema + nav
# ──────────────────────────────────────────────

META_BLOCK = """    <meta name="description" content="Alin Gherman — contemporary composer. Compositions for percussion, orchestra, electronic music, instrumental theatre, and film.">
    <meta name="author" content="Alin Gherman">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://alingherman.com/">

    <!-- Open Graph -->
    <meta property="og:title" content="Alin Gherman — Contemporary Composer">
    <meta property="og:description" content="Compositions for percussion, orchestra, electronic music, instrumental theatre, and film.">
    <meta property="og:image" content="https://alingherman.com/pianist-tanar-color-1997.webp">
    <meta property="og:url" content="https://alingherman.com/">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="Alin Gherman">

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Alin Gherman — Contemporary Composer">
    <meta name="twitter:description" content="Compositions for percussion, orchestra, electronic music, instrumental theatre, and film.">
    <meta name="twitter:image" content="https://alingherman.com/pianist-tanar-color-1997.webp">

    <!-- PWA -->
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#6B1B3D">
    <link rel="apple-touch-icon" href="/favicon.png">

    <!-- Schema.org -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Person",
      "name": "Alin Gherman",
      "jobTitle": "Contemporary Composer",
      "url": "https://alingherman.com",
      "image": "https://alingherman.com/pianist-tanar-color-1997.webp",
      "sameAs": [
        "https://www.youtube.com/@AlinGherman",
        "https://soundcloud.com/alingherman",
        "https://alingherman.bandcamp.com"
      ],
      "knowsAbout": ["Contemporary Music", "Percussion", "Electronic Music", "Film Music", "Instrumental Theatre", "Orchestra"]
    }
    </script>"""

NAV_CSS_MOBILE_FIRST = """
        /* ── NAV TOGGLE — MOBILE FIRST ── */
        .nav-toggle {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            width: 24px; height: 18px;
            background: none; border: none;
            cursor: pointer; padding: 0;
            z-index: 1100; flex-shrink: 0;
            min-width: 44px; min-height: 44px;
            align-items: center; justify-content: center;
        }
        .nav-toggle span {
            display: block; width: 22px; height: 2px;
            background: var(--burgundy);
            transition: transform 0.35s cubic-bezier(0.16,1,0.3,1),
                        opacity 0.25s ease;
            transform-origin: center;
        }
        .nav-toggle.open span:nth-child(1) {
            transform: translateY(8px) rotate(45deg);
        }
        .nav-toggle.open span:nth-child(2) {
            transform: translateY(-8px) rotate(-45deg);
        }

        /* MOBILE NAV — fullscreen overlay */
        .nav-links {
            position: fixed;
            inset: 0;
            background: rgba(253,251,247,0.98);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 2rem;
            z-index: 1050;
            transform: translateX(100%);
            transition: transform 0.4s cubic-bezier(0.16,1,0.3,1);
        }
        .nav-links.open {
            transform: translateX(0);
        }
        .nav-links a {
            font-size: 1.25rem;
            letter-spacing: 0.5px;
            color: var(--burgundy);
            padding: 0.5rem 1rem;
            min-height: 44px;
            display: flex;
            align-items: center;
        }

        /* TABLET+ — inline nav */
        @media (min-width: 900px) {
            .nav-toggle { display: none; }
            .nav-links {
                position: static;
                flex-direction: row;
                gap: 2.5rem;
                background: none;
                backdrop-filter: none;
                -webkit-backdrop-filter: none;
                transform: none;
                z-index: auto;
                transition: none;
            }
            .nav-links a {
                font-size: 0.875rem;
                letter-spacing: 0.5px;
                color: var(--text-dark);
                padding: 0;
                min-height: auto;
            }
        }

        /* ── MOBILE LAYOUT ── */
        @media (max-width: 899px) {
            .nav-content { padding: 1rem 1.5rem; }
            .hero { padding: 6rem 1.5rem 3.5rem; min-height: 90svh; }
            .hero-title { font-size: clamp(2rem, 9vw, 3.5rem) !important; }
            .hero-text { font-size: 0.9375rem; }
            .hero-cta { flex-direction: column; align-items: center; gap: 0.75rem; }
            .btn-primary, .btn-secondary {
                width: 100%; max-width: 280px;
                text-align: center; display: block;
                min-height: 44px; display: flex; align-items: center; justify-content: center;
            }
            section { padding: 4rem 0; }
            .container-fluid, .container-narrow { padding: 0 1.5rem; }
            .section-title { font-size: clamp(1.75rem, 7vw, 3rem) !important; }
            .about-grid, .instruments-showcase, .contact-grid {
                grid-template-columns: 1fr; gap: 2.5rem;
            }
            .about-stats { flex-direction: column; gap: 1.5rem; }
            .work-grid { grid-template-columns: 1fr; gap: 1rem; }
            .form-row { grid-template-columns: 1fr; }
            .footer-content { flex-direction: column; gap: 1rem; text-align: center; }
            .footer-center { justify-content: center; }
            .about-stats { padding-top: 2rem; margin-top: 2rem; }
        }

        @media (max-width: 480px) {
            .nav-content { padding: 0.875rem 1.25rem; }
            .container-fluid, .container-narrow { padding: 0 1.25rem; }
            .hero { padding: 5.5rem 1.25rem 3rem; }
            .section-title { font-size: clamp(1.5rem, 8vw, 2.5rem) !important; }
        }

        /* ── REDUCE MOTION ── */
        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after {
                animation-duration: 0.01ms !important;
                transition-duration: 0.01ms !important;
            }
        }
"""

HAMBURGER_JS = """
        // ── HAMBURGER MENU — mobile-first ──
        (function() {
            var toggle = document.getElementById('navToggle');
            var menu   = document.querySelector('.nav-links');
            if (!toggle || !menu) return;
            function closeMenu() {
                toggle.classList.remove('open');
                menu.classList.remove('open');
                toggle.setAttribute('aria-expanded', 'false');
                document.body.style.overflow = '';
            }
            toggle.addEventListener('click', function() {
                var isOpen = menu.classList.contains('open');
                if (isOpen) {
                    closeMenu();
                } else {
                    toggle.classList.add('open');
                    menu.classList.add('open');
                    toggle.setAttribute('aria-expanded', 'true');
                    document.body.style.overflow = 'hidden';
                }
            });
            menu.querySelectorAll('a').forEach(function(a) {
                a.addEventListener('click', closeMenu);
            });
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape') closeMenu();
            });
        })();
"""

def fix_index():
    path = BASE + 'index.html'
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # 1. Add meta block after <title> line if not already present
    if 'og:title' not in c:
        c = c.replace(
            '    <link rel="preconnect" href="https://fonts.googleapis.com">',
            META_BLOCK + '\n    <link rel="preconnect" href="https://fonts.googleapis.com">'
        )
        print('index.html: meta/OG/schema added')

    # 2. Add aria-label to nav toggle button
    c = c.replace(
        '<button class="nav-toggle" id="navToggle">',
        '<button class="nav-toggle" id="navToggle" aria-label="Menu" aria-expanded="false">'
    )

    # 3. Replace ALL previous mobile CSS (both old media queries and the ones added by fix_mobile.py)
    # Remove the old nav-toggle CSS block added previously and the media queries we added
    # Strategy: find and replace the section between "/* ── NAV TOGGLE" and end of last @media block
    pattern = r'/\* ── NAV TOGGLE.*?@media \(max-width: 480px\) \{.*?\}\s*'
    match = re.search(pattern, c, re.DOTALL)
    if match:
        c = c[:match.start()] + NAV_CSS_MOBILE_FIRST + c[match.end():]
        print('index.html: nav CSS replaced with mobile-first version')
    else:
        # Try appending before </style>
        if 'MOBILE FIRST' not in c:
            c = c.replace('    </style>', NAV_CSS_MOBILE_FIRST + '\n    </style>', 1)
            print('index.html: nav CSS appended')

    # 4. Add/replace hamburger JS
    if 'HAMBURGER MENU — mobile-first' not in c:
        # Remove old hamburger JS if present
        old_pattern = r'// ── HAMBURGER MENU ──.*?\}\)\(\);'
        c = re.sub(old_pattern, '', c, flags=re.DOTALL)
        # Add new one before window.addEventListener pageshow
        c = c.replace(
            "    window.addEventListener('pageshow'",
            HAMBURGER_JS + "\n    window.addEventListener('pageshow'"
        )
        print('index.html: hamburger JS updated')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print('index.html: DONE')


# ──────────────────────────────────────────────
# 2. ALL HTML PAGES — loading=lazy on external images
# ──────────────────────────────────────────────

def add_lazy_loading():
    files = glob.glob(BASE + '*.html')
    count = 0
    for path in files:
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()

        original = c

        # Add loading=lazy and decoding=async to external img tags (not base64, not already lazy)
        def add_lazy(m):
            tag = m.group(0)
            src = re.search(r'src=["\']([^"\']+)["\']', tag)
            if not src:
                return tag
            src_val = src.group(1)
            # Skip base64
            if src_val.startswith('data:'):
                return tag
            # Skip if already lazy
            if 'loading=' in tag:
                return tag
            # Skip hero/first images (heuristic: if tag contains 'hero' class or is first in hero section)
            tag = tag.rstrip('>')
            if 'decoding=' not in tag:
                tag += ' decoding="async"'
            tag += ' loading="lazy">'
            return tag

        c = re.sub(r'<img[^>]+>', add_lazy, c)

        if c != original:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(c)
            count += 1

    print(f'lazy loading: updated {count} files')


# ──────────────────────────────────────────────
# 3. ALL PAGES — add manifest + theme-color to <head>
# ──────────────────────────────────────────────

MANIFEST_TAGS = '    <link rel="manifest" href="/manifest.json">\n    <meta name="theme-color" content="#6B1B3D">\n'

def add_manifest_to_all():
    files = glob.glob(BASE + '*.html')
    count = 0
    for path in files:
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        if 'manifest.json' in c:
            continue
        if '<link rel="preconnect"' in c:
            c = c.replace('<link rel="preconnect"', MANIFEST_TAGS + '    <link rel="preconnect"', 1)
        elif '</head>' in c:
            c = c.replace('</head>', MANIFEST_TAGS + '</head>', 1)
        else:
            continue
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
        count += 1
    print(f'manifest/theme-color: added to {count} files')


# ──────────────────────────────────────────────
# 4. COMPOSITIONS PAGES — mobile-first nav CSS fix
# ──────────────────────────────────────────────

BACK_BTN_MOBILE = """
        /* ── BACK BTN TOUCH TARGET ── */
        .back-btn {
            min-height: 44px;
            min-width: 44px;
            display: inline-flex;
            align-items: center;
        }
        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after {
                animation-duration: 0.01ms !important;
                transition-duration: 0.01ms !important;
            }
        }
"""

def fix_compositions_nav():
    files = glob.glob(BASE + 'compositions-*.html') + glob.glob(BASE + '*-chimes.html')
    count = 0
    for path in files:
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        if 'min-height: 44px' in c:
            continue
        c = c.replace('    </style>', BACK_BTN_MOBILE + '\n    </style>', 1)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
        count += 1
    print(f'touch targets: fixed in {count} files')


# ── RUN ──
print('=== index.html ===')
fix_index()

print('\n=== lazy loading ===')
add_lazy_loading()

print('\n=== manifest + theme-color ===')
add_manifest_to_all()

print('\n=== touch targets ===')
fix_compositions_nav()

print('\nAll done!')
