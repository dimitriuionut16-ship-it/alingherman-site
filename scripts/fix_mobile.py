"""
Mobile-first fix for all pages on alingherman.com
"""
import re, glob, os

BASE = 'c:/Users/IONUT/Desktop/SITE-GHERAM-FULL/'

# ─────────────────────────────────────────────
# 1. INDEX.HTML — full hamburger nav + mobile
# ─────────────────────────────────────────────

INDEX_NAV_CSS = """
        /* ── NAV TOGGLE (hamburger) ── */
        .nav-toggle {
            display: none;
            flex-direction: column;
            justify-content: space-between;
            width: 22px; height: 16px;
            background: none; border: none;
            cursor: pointer; padding: 0; z-index: 1100;
            flex-shrink: 0;
        }
        .nav-toggle span {
            display: block; width: 100%; height: 2px;
            background: var(--burgundy);
            transition: all 0.3s ease;
            transform-origin: center;
        }
        .nav-toggle.open span:nth-child(1) {
            transform: translateY(7px) rotate(45deg);
        }
        .nav-toggle.open span:nth-child(2) {
            transform: translateY(-7px) rotate(-45deg);
        }

        /* ── MOBILE BREAKPOINTS ── */
        @media (max-width: 900px) {
            .nav-content { padding: 18px 32px; }
            .nav-links { gap: 28px; }
        }

        @media (max-width: 768px) {
            /* show hamburger, hide links */
            .nav-toggle { display: flex; }
            .nav-content { padding: 16px 24px; }
            .nav-links {
                position: fixed;
                inset: 0;
                background: rgba(253,251,247,0.98);
                backdrop-filter: blur(20px);
                flex-direction: column;
                align-items: center;
                justify-content: center;
                gap: 36px;
                z-index: 1050;
                opacity: 0;
                pointer-events: none;
                transition: opacity 0.3s ease;
            }
            .nav-links.open {
                opacity: 1;
                pointer-events: all;
            }
            .nav-links a {
                font-size: 18px;
                letter-spacing: 1px;
                color: var(--burgundy);
            }

            /* hero */
            .hero { padding: 100px 24px 64px; min-height: 90vh; }
            .hero-title { font-size: clamp(34px, 10vw, 56px) !important; }
            .hero-text { font-size: 15px; padding: 0 8px; }
            .hero-cta { flex-direction: column; align-items: center; gap: 12px; }
            .btn-primary, .btn-secondary {
                width: 100%; max-width: 280px;
                text-align: center; display: block;
            }

            /* sections */
            section { padding: 80px 0; }
            .container-fluid, .container-narrow { padding: 0 24px; }
            .section-title { font-size: clamp(30px, 7vw, 52px) !important; }
            .section-label { font-size: 10px; }

            /* about */
            .about-grid { grid-template-columns: 1fr; gap: 40px; }
            .about-stats { flex-direction: column; gap: 28px; }
            .stat-number { font-size: 36px; }

            /* work cards */
            .work-grid { grid-template-columns: 1fr; gap: 16px; }
            .work-card { padding: 24px; }

            /* instruments */
            .instruments-showcase { grid-template-columns: 1fr; gap: 40px; }

            /* contact */
            .contact-grid { grid-template-columns: 1fr; gap: 40px; }
            .form-row { grid-template-columns: 1fr; }

            /* footer */
            .footer-content { flex-direction: column; gap: 16px; text-align: center; }
            .footer-center { justify-content: center; }
        }

        @media (max-width: 480px) {
            .nav-content { padding: 14px 20px; }
            .hero { padding: 90px 20px 56px; }
            .container-fluid, .container-narrow { padding: 0 20px; }
            .btn-primary, .btn-secondary { padding: 14px 24px; font-size: 13px; }
            .work-card { padding: 20px; }
            .section-title { font-size: clamp(26px, 8vw, 40px) !important; }
        }
"""

INDEX_HAMBURGER_JS = """
        // ── HAMBURGER MENU ──
        (function() {
            var toggle = document.getElementById('navToggle');
            var links  = document.querySelector('.nav-links');
            if (!toggle || !links) return;
            toggle.addEventListener('click', function() {
                toggle.classList.toggle('open');
                links.classList.toggle('open');
                document.body.style.overflow = links.classList.contains('open') ? 'hidden' : '';
            });
            links.querySelectorAll('a').forEach(function(a) {
                a.addEventListener('click', function() {
                    toggle.classList.remove('open');
                    links.classList.remove('open');
                    document.body.style.overflow = '';
                });
            });
        })();
"""

def fix_index():
    path = BASE + 'index.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace the single existing media query with full mobile CSS
    old_mq = re.search(
        r'\s*@media \(max-width: 968px\) \{.*?\}\s*(?=\.cat-link)',
        content, re.DOTALL
    )
    if old_mq:
        content = content[:old_mq.start()] + '\n' + INDEX_NAV_CSS + '\n        ' + content[old_mq.end():]
        print('index.html: replaced media query')
    else:
        # Append before </style>
        content = content.replace('    </style>', INDEX_NAV_CSS + '\n    </style>', 1)
        print('index.html: appended mobile CSS')

    # Add hamburger JS before closing </script> of the main script block
    if 'HAMBURGER MENU' not in content:
        content = content.replace(
            "    window.addEventListener('pageshow'",
            INDEX_HAMBURGER_JS + "\n    window.addEventListener('pageshow'"
        )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('index.html: DONE')


# ─────────────────────────────────────────────
# 2. COMPOSITIONS PAGES
# ─────────────────────────────────────────────

COMPOSITIONS_MOBILE_CSS = """
        /* ── MOBILE ── */
        @media (max-width: 768px) {
            .nav-content { padding: 14px 24px; }
            .back-btn { padding: 8px 16px; font-size: 11px; }
            .hero { padding: 100px 24px 48px; min-height: auto; }
            .hero-title { font-size: clamp(28px, 8vw, 48px) !important; }
            .hero-subtitle { font-size: 14px; }
            .container { padding: 0 24px; }
            .works-grid { gap: 12px; }
            .work-row { padding: 20px 0; }
            .work-header { flex-direction: column; align-items: flex-start; gap: 8px; }
            .work-title { font-size: 18px; }
            .work-meta { flex-direction: column; gap: 4px; }
            .multi-show-dropdown { min-width: auto; width: 100%; max-width: 100%; }
            .waveform-bg { display: none; }
            section { padding: 60px 0; }
        }
        @media (max-width: 480px) {
            .hero { padding: 88px 20px 40px; }
            .container { padding: 0 20px; }
            .work-title { font-size: 16px; }
        }
"""

def fix_compositions():
    files = glob.glob(BASE + 'compositions-*.html')
    for path in files:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'MOBILE' in content:
            print(f'{os.path.basename(path)}: already has mobile CSS, skipping')
            continue
        # Replace minimal existing media query or append
        old = re.search(r'@media\s*\(max-width:\s*768px\)\s*\{[^}]*\}', content)
        if old:
            content = content[:old.start()] + COMPOSITIONS_MOBILE_CSS + content[old.end():]
        else:
            content = content.replace('    </style>', COMPOSITIONS_MOBILE_CSS + '\n    </style>', 1)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'{os.path.basename(path)}: DONE')


# ─────────────────────────────────────────────
# 3. CHIMES PAGES — improve existing mobile CSS
# ─────────────────────────────────────────────

CHIMES_EXTRA_MOBILE = """
        @media (max-width: 768px) {
            .nav-content { padding: 14px 24px; }
            .back-btn { padding: 8px 16px; font-size: 11px; }
            .hero { min-height: 60vh; }
            .hero-title { font-size: clamp(32px, 9vw, 60px) !important; }
            .hero-sub { font-size: clamp(13px, 3vw, 18px); }
            .hero-strip { flex-direction: row; }
            .hero-eyebrow { font-size: 10px; letter-spacing: 3px; }
            .description-section { padding: 48px 0; }
            .gallery-section { padding: 48px 0; }
            .used-section { padding: 48px 0; }
            .gallery-header { margin-bottom: 28px; }
            .gallery-title { font-size: 24px; }
            .photo-grid-2 { grid-template-columns: 1fr; }
        }
        @media (max-width: 480px) {
            .nav-content { padding: 12px 16px; }
            .container, .container-narrow { padding: 0 16px; }
            .hero-title { font-size: clamp(28px, 10vw, 48px) !important; }
            .desc-grid { gap: 32px; }
            .used-work { font-size: 17px; }
        }
"""

def fix_chimes():
    files = [
        'metal-cans-chimes.html', 'metal-spoons-chimes.html',
        'wood-chimes.html', 'glass-chimes.html',
        'metal-tubes-chimes.html', 'stone-chimes.html',
    ]
    for fname in files:
        path = BASE + fname
        if not os.path.exists(path):
            continue
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'max-width: 768px' in content and 'max-width: 480px' in content:
            print(f'{fname}: already has 480px breakpoint, skipping')
            continue
        content = content.replace('    </style>', CHIMES_EXTRA_MOBILE + '\n    </style>', 1)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'{fname}: DONE')


# ─────────────────────────────────────────────
# 4. OTHER PAGES (pressbook, links, support, portraits, photos)
# ─────────────────────────────────────────────

OTHER_MOBILE_CSS = """
        /* ── MOBILE ── */
        @media (max-width: 768px) {
            .nav-content { padding: 14px 24px !important; }
            .back-btn { padding: 8px 16px; font-size: 11px; }
            .container, .container-narrow { padding: 0 24px !important; }
            .hero { padding: 100px 24px 48px !important; min-height: auto !important; }
            .hero-title { font-size: clamp(28px, 8vw, 48px) !important; }
            .footer-content { flex-direction: column !important; gap: 12px !important; text-align: center !important; }
            section { padding: 60px 0 !important; }
        }
        @media (max-width: 480px) {
            .nav-content { padding: 12px 16px !important; }
            .container, .container-narrow { padding: 0 16px !important; }
        }
"""

OTHER_FILES = [
    'links.html', 'support.html',
    'pressbook-timeline.html', 'pressbook-timeline-updated.html',
    'portraits.html', 'photos-composers.html',
    'photos-miscellaneous.html', 'photos-performers-recent.html',
    'press-photos.html', 'purpleritual.html',
]

def fix_others():
    for fname in OTHER_FILES:
        path = BASE + fname
        if not os.path.exists(path):
            continue
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'max-width: 480px' in content:
            print(f'{fname}: already has 480px, skipping')
            continue
        # Replace existing minimal media query or append
        old = re.search(r'@media\s*\(max-width:\s*768px\)\s*\{[^}]*\}', content)
        if old:
            content = content[:old.start()] + OTHER_MOBILE_CSS + content[old.end():]
        else:
            content = content.replace('    </style>', OTHER_MOBILE_CSS + '\n    </style>', 1)
            if '</style>' not in content:
                content = content.replace('</style>', OTHER_MOBILE_CSS + '\n    </style>', 1)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'{fname}: DONE')


# ─────────────────────────────────────────────
# RUN ALL
# ─────────────────────────────────────────────
print('=== Fixing index.html ===')
fix_index()

print('\n=== Fixing compositions pages ===')
fix_compositions()

print('\n=== Fixing chimes pages ===')
fix_chimes()

print('\n=== Fixing other pages ===')
fix_others()

print('\nAll done!')
