import os
import base64
import mimetypes
import urllib.parse

pages = {
    'dan43': {
        'title': 'Dance — under impending rain — opus 78c',
        'scoreLinks': [{'label': 'Score (locked)', 'url': 'http://home.scarlet.be/bucovina/scores/Dance-under_impending_rain-by_Alin_Gherman_tempv1.1%28secured%29.pdf'}],
        'codeImage': 'codes/dan43.jpg'
    },
    'cym32': {
        'title': 'Cymbals Vitamins — opus 78b',
        'scoreLinks': [{'label': 'Score (locked)', 'url': 'http://home.scarlet.be/bucovina/scores/Cymbals_Vitamins_by_Alin_Gherman_%28secured%29.pdf'}],
        'codeImage': 'codes/cym32.jpg'
    },
    'mou1322': {
        'title': 'Mouvements (v1) — for voice + instruments',
        'scoreLinks': [{'label': 'Score (locked)', 'url': 'http://home.scarlet.be/bucovina/scores/Mouvements_%28v1%29_by_Alin_GHERMAN_%28secured%29.pdf'}],
        'codeImage': 'codes/mou1322.jpg'
    },
    'vla2214': {
        'title': 'VLAN! pour soprano/tenor',
        'scoreLinks': [{'label': 'Score for Soprano/Tenor (locked)', 'url': 'http://home.scarlet.be/bucovina/scores/VLAN!_pour_soprano_tenor_by_Alin_GHERMAN_v3(secured).pdf'}],
        'codeImage': 'codes/vla2214.jpg'
    },
    'bri27': {
        'title': 'Bright challenge fanfare (v1)',
        'scoreLinks': [{'label': 'Score (locked)', 'url': 'http://home.scarlet.be/gherman/scores/Bright_challenge_fanfare_%28v1%29_by_Alin_GHERMAN_%28secured%29.pdf'}],
        'codeImage': 'codes/bri27.jpeg'
    },
    'pot1616': {
        'title': 'Pot-pourri v5.2 & vCHAMBER',
        'scoreLinks': [
            {'label': 'Symphonic version (locked)', 'url': 'http://home.scarlet.be/gherman/scores/Pot-pourri_%28v5.2%29_by_Alin_GHERMAN_%28secured%29.pdf'},
            {'label': 'Chamber version (locked)', 'url': 'http://home.scarlet.be/gherman/scores/Pot-pourri_%28vCHAMBER_Lausanne_2009_PREtemp1_by_Alin_GHERMAN_%28secured%29.pdf'}
        ],
        'codeImage': 'codes/pot1616.jpg'
    },
    'rel181': {
        'title': 'Relations lumineuses (v1)',
        'scoreLinks': [{'label': 'Score (locked)', 'url': 'http://home.scarlet.be/bucovina/scores/Relations_lumineuses_%28v1%29_by_Alin_GHERMAN.pdf'}],
        'codeImage': 'codes/rel181.jpeg'
    },
    'his1820': {
        'title': 'Histoire 1 (v1)',
        'scoreLinks': [{'label': 'Score (locked)', 'url': 'http://home.scarlet.be/bucovina/scores/Histoire1%28v1%29byAlinGHERMAN%28secured%29.pdf'}],
        'codeImage': 'codes/his1820.jpeg'
    },
    'his2820': {
        'title': 'Histoire 2 (v1)',
        'scoreLinks': [{'label': 'Score (locked)', 'url': 'http://home.scarlet.be/bucovina/scores/Histoire2%28v1%29byAlinGHERMAN%28secured%29.pdf'}],
        'codeImage': 'codes/his2820.jpeg'
    },
    'gra79': {
        'title': 'Grains, fleur et son envol',
        'scoreLinks': [{'label': 'Score + parts (locked)', 'url': 'http://home.scarlet.be/bucovina/scores/Grains,fleur_et_son_envol_%28+parts%29_by_Alin_GHERMAN%28secured%29%28v3%29.pdf'}],
        'codeImage': 'codes/gra79.jpeg'
    },
    'mou1320': {
        'title': 'Mouth and strings (v2)',
        'scoreLinks': [{'label': 'Score (locked)', 'url': 'http://home.scarlet.be/gherman/scores/Mouth_and_strings_%28v2%29_by_Alin_GHERMAN_%28secured%29.pdf'}],
        'codeImage': 'codes/mou1320.jpeg'
    },
    'ful612': {
        'title': 'Full bright fanfare',
        'scoreLinks': [{'label': 'Score+Parts (locked)', 'url': 'http://home.scarlet.be/gherman/scores/Full_bright_fanfare_by_Alin_Gherman_%28v1%29_Score+Parts_%28secured%29.pdf'}],
        'codeImage': 'codes/ful612.jpeg'
    },
    'fol63': {
        'title': 'FOLCLOR v.3color',
        'scoreLinks': [{'label': 'Score (locked)', 'url': 'http://home.scarlet.be/bucovina/scores/FOLCLOR_by_Alin_GHERMAN_(v.3color)(secured).pdf'}],
        'codeImage': 'codes/fol63.jpeg'
    },
    'int95': {
        'title': 'Intermede instrumental',
        'scoreLinks': [{'label': 'Score + parts (locked)', 'url': 'http://home.scarlet.be/gherman/scores/Intermede_intrumental_%28tempv2.2%29_by_Alin_Gherman_%28score+parts%29.pdf'}],
        'codeImage': 'codes/int95.jpeg'
    },
    'hel812': {
        'title': 'HELLO temp 3.1 + 3.3',
        'scoreLinks': [
            {'label': 'Score (v3.1/B.Cl.) (locked)', 'url': 'http://home.scarlet.be/bucovina/scores/HELLO_temp3.1_by_Alin_Gherman%28secured%29.pdf'},
            {'label': 'Score (v3.3/Horn) (locked)', 'url': 'http://home.scarlet.be/bucovina/scores/HELLO_temp3.3+COR_by_Alin_Gherman%28secured%29.pdf'}
        ],
        'codeImage': 'codes/hel812.jpeg'
    },
    'kla1122': {
        'title': 'Klavierstuck v1/v2',
        'scoreLinks': [
            {'label': 'Score (v1 short) (locked)', 'url': 'http://home.scarlet.be/bucovina/scores/Klavierstuck_%28v1%29_by_Alin_GHERMAN_%28secured%29.pdf'},
            {'label': 'Score (v2 full) (locked)', 'url': 'http://home.scarlet.be/gherman/scores/Klavierstuck_%28v2temp%29_by_Alin_GHERMAN_%28secured%29.pdf'}
        ],
        'codeImage': 'codes/kla1122.jpeg'
    },
    'min139': {'title': 'Minimistic 139', 'scoreLinks': [], 'codeImage': 'codes/min139.jpeg'},
    'pri1612': {'title': 'Prilude (v2.2)', 'scoreLinks': [{'label': 'Score (locked)', 'url': 'http://home.scarlet.be/bucovina/scores/Prilude_by_Alin%20GHERMAN%28v2.2%29%28secured%29.pdf'}], 'codeImage': 'codes/pri1612.jpeg'},
    'div45': {'title': 'Divertimento 45', 'scoreLinks': [], 'codeImage': 'codes/div45.jpeg'},
    'don414': {
        'title': 'Donna Odokia v1',
        'scoreLinks': [
            {'label': 'Score in German (locked)', 'url': 'http://home.scarlet.be/gherman/scores/Donna_Odokia_%28v1german%29_by_Alin_GHERMAN_%28secured%29.pdf'},
            {'label': 'Score in French (locked)', 'url': 'http://home.scarlet.be/gherman/scores/Donna_Odokia_%28v1french%29_by_Alin_GHERMAN_%28secured%29.pdf'}
        ],
        'codeImage': 'codes/don414.jpeg'
    },
    'ori157': {'title': 'Origines (Conductor)', 'scoreLinks': [{'label': 'Score (locked)', 'url': 'http://home.scarlet.be/gherman/scores/Origines_%28Conductor%29_%28v2-2006%29_by_Alin_Gherman_%28secured%29.pdf'}], 'codeImage': 'codes/ori157.jpeg'},
    'tar201': {'title': 'Taraf in the graveyard', 'scoreLinks': [{'label': 'Score (locked)', 'url': 'http://home.scarlet.be/gherman/scores/Taraf_in_the_graveyard_%28v2.1%29_by_Alin_GHERMAN_%28secured%29.pdf'}], 'codeImage': 'codes/tar201jpeg.jpg'},
    'poe1619': {'title': 'Poesie perdue', 'scoreLinks': [{'label': 'Score + parts (locked)', 'url': 'http://home.scarlet.be/gherman/scores/Poesie_perdue_%28v.3.1%29_by_Alin_GHERMAN_%28secured%29.pdf'}], 'codeImage': 'codes/poe1619.jpeg'},
    'add15': {'title': 'Addendum exitum', 'scoreLinks': [{'label': 'Score (locked)', 'url': 'http://home.scarlet.be/gherman/scores/Addendum_exitum_%28v1%29_by_Alin_GHERMAN_%28secured%29.pdf'}], 'codeImage': 'codes/add15.jpeg'},
    'opo1522': {'title': 'Opo 1522', 'scoreLinks': [], 'codeImage': 'codes/opo1522.jpeg'},
    'err51': {'title': 'Errances (v3)', 'scoreLinks': [{'label': 'Score (locked)', 'url': 'http://home.scarlet.be/gherman/scores/Errances_%28v3%29_by_Alin_GHERMAN_%28secured%29.pdf'}], 'codeImage': 'codes/err51.jpeg'},
    'pla1625': {'title': 'Play song (v4)', 'scoreLinks': [{'label': 'Score (locked)', 'url': 'http://home.scarlet.be/bucovina/scores/Play_song_%28v4%29_by_Alin_GHERMAN_%28secured%29.pdf'}], 'codeImage': 'codes/pla1625.jpeg'},
    'ari13': {'title': 'Ariciul', 'scoreLinks': [{'label': 'Score (locked)', 'url': 'http://home.scarlet.be/bucovina/scores/Ariciul_%28v3%29_by_Alin_GHERMAN_%28secured%29.pdf'}], 'codeImage': 'codes/ari13.jpeg'},
    'vib2218': {'title': 'Vibrations (Score + parts)', 'scoreLinks': [{'label': 'Score + parts (locked)', 'url': 'http://home.scarlet.be/bucovina/scores/Vibrations%28Score+parts%29ByAlinGherman%28v1%29%28secured%29.pdf'}], 'codeImage': 'codes/vib2218.jpeg'},
    'met131': {'title': 'Metal spirits I+II', 'scoreLinks': [{'label': 'Score (locked)', 'url': 'http://home.scarlet.be/bucovina/scores/Metal%20_spirits_I+II_%28v1%29_by_Alin_GHERMAN.pdf'}], 'codeImage': 'codes/met131.jpeg'},
    'hau820': {'title': 'Haute Tension', 'scoreLinks': [{'label': 'Score (locked)', 'url': 'http://home.scarlet.be/bucovina/scores/HauteTension%28v1%29byAlinGHERMAN%28secured%29.pdf'}], 'codeImage': 'codes/hau820.jpeg'},
    'caf35': {'title': 'Cafemelange', 'scoreLinks': [{'label': 'Score (locked)', 'url': 'http://home.scarlet.be/bucovina/scores/CafemelangebyAlinGherman%28v1%29%28secured%29.pdf'}], 'codeImage': 'codes/caf35.jpeg'}
}

def image_to_data_uri(path):
    if os.path.exists(path):
        mime_type, _ = mimetypes.guess_type(path)
        if not mime_type:
            mime_type = 'application/octet-stream'
        with open(path, 'rb') as f:
            raw = f.read()
        return f'data:{mime_type};base64,{base64.b64encode(raw).decode("utf-8")}'
    return None


def local_score_url(url):
    try:
        parsed = urllib.parse.urlparse(url)
        name = os.path.basename(parsed.path)
        if not name:
            return None
        decoded_name = decode_score_name(name)
        candidate = os.path.join('scores', decoded_name)
        if os.path.exists(candidate):
            return candidate
    except Exception:
        pass
    return None


def normalize_name(name):
    # Case-insensitive, strip spaces and extensions in matching
    base = os.path.splitext(name)[0]
    return ''.join(ch for ch in base.lower() if ch.isalnum())


def decode_score_name(name):
    return urllib.parse.unquote(name)


def ensure_score_files_exists():
    available = [f for f in os.listdir('scores') if f.lower().endswith('.pdf')]
    normalized_map = {normalize_name(decode_score_name(f)): f for f in available}

    for code, entry in pages.items():
        for link in entry.get('scoreLinks', []):
            url = link.get('url', '')
            basename = os.path.basename(urllib.parse.urlparse(url).path)
            if not basename:
                continue

            desired_name = decode_score_name(basename)
            desired_path = os.path.join('scores', desired_name)

            if os.path.exists(desired_path):
                continue

            normalized_target = normalize_name(desired_name)

            if normalized_target in normalized_map:
                source_file = normalized_map[normalized_target]
                source_path = os.path.join('scores', source_file)
                if os.path.exists(source_path):
                    try:
                        if source_file != desired_name:
                            os.rename(source_path, desired_path)
                            print(f'Renamed local score: {source_file} -> {desired_name}')
                        else:
                            print(f'Found local score (already correct): {source_file}')
                    except Exception as e:
                        print(f'Failed rename {source_file}: {e}')
            else:
                # fuzzy match on normalized keys
                from difflib import get_close_matches
                close = get_close_matches(normalized_target, normalized_map.keys(), n=1, cutoff=0.75)
                if close:
                    source_file = normalized_map[close[0]]
                    source_path = os.path.join('scores', source_file)
                    if os.path.exists(source_path):
                        try:
                            if source_file != desired_name:
                                os.rename(source_path, desired_path)
                                print(f'Renamed local score (fuzzy): {source_file} -> {desired_name}')
                            else:
                                print(f'Found local score (already correct): {source_file}')
                        except Exception as e:
                            print(f'Failed rename {source_file}: {e}')


def make_fallback_svg_code(code):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="480" height="140" viewBox="0 0 480 140">
        <rect width="100%" height="100%" fill="#FDFBF7" stroke="#6B1B3D" stroke-width="2" rx="10"/>
        <text x="50%" y="45%" font-family="Inter, sans-serif" font-size="20" fill="#6B1B3D" text-anchor="middle" dominant-baseline="middle">Code {code}</text>
        <text x="50%" y="75%" font-family="Inter, sans-serif" font-size="13" fill="#1F2937" text-anchor="middle" dominant-baseline="middle">Image does not exist locally; embedded placeholder</text>
    </svg>'''
    encoded = base64.b64encode(svg.encode('utf-8')).decode('utf-8')
    return f'data:image/svg+xml;base64,{encoded}'

base_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>thank-you-page ##INDEX##</title>
    <meta name="description" content="Thank you page for ##TITLE## (code ##CODE##).">
    <link rel="icon" href="/favicon.png" type="image/x-icon">
    <link rel="shortcut icon" href="/favicon.png" type="image/x-icon">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        *{margin:0;padding:0;box-sizing:border-box;}
        :root{--white:#FFFFFF;--cream:#FDFBF7;--burgundy:#6B1B3D;--turquoise:#14B8A6;--grey:#6B7280;--grey-light:#E5E7EB;--text-dark:#1F2937;}
        body{font-family:'Inter',sans-serif;background:var(--cream);color:var(--text-dark);line-height:1.6;font-weight:300;min-height:100vh;display:flex;flex-direction:column;}
        .nav{position:fixed;top:0;left:0;right:0;background:rgba(253,251,247,0.96);backdrop-filter:blur(20px);border-bottom:3px solid var(--burgundy);z-index:1000;}
        .nav-content{max-width:1400px;margin:0 auto;padding:16px 40px;display:flex;justify-content:space-between;align-items:center;}
        .nav-logo{font-size:14px;font-weight:600;letter-spacing:2px;color:var(--burgundy);text-decoration:none;}
        .nav-links{display:flex;gap:14px;}
        .nav-links a{font-size:12px;font-weight:500;color:var(--text-dark);text-decoration:none;letter-spacing:0.5px;}
        .nav-links a:hover{color:var(--burgundy);}
        .hero{padding:120px 40px 30px;max-width:900px;margin:0 auto;text-align:center;}
        .hero-label{display:block;font-size:11px;font-weight:500;letter-spacing:3px;text-transform:uppercase;color:var(--turquoise);margin-bottom:10px;}
        .hero-title{font-family:'Instrument Serif',serif;font-size:clamp(24px,6vw,44px);color:var(--burgundy);margin:0;}
        .hero-subtitle{font-size:14px;line-height:1.8;color:var(--grey);margin-top:12px;max-width:680px;margin-left:auto;margin-right:auto;}
        .hero-divider{width:40px;height:2px;background:var(--burgundy);margin:22px auto 0;}
        .main{flex:1;padding:20px 40px 40px;max-width:900px;margin:0 auto;width:100%;}
        .card{background:var(--white);border:1px solid var(--grey-light);box-shadow:0 3px 12px rgba(0,0,0,0.08);border-radius:10px;padding:26px;}
        .card h1{font-family:'Instrument Serif',serif;color:var(--burgundy);font-size:clamp(28px,5vw,42px);margin-bottom:14px;}
        .code-block{border:1px dashed var(--turquoise);border-radius:6px;padding:14px;display:inline-block;font-weight:600;color:var(--turquoise);}
        .links{display:flex;flex-wrap:wrap;gap:12px;margin:14px 0;}
        .link-btn{display:inline-flex;align-items:center;gap:8px;padding:10px 16px;border:1px solid var(--burgundy);border-radius:5px;color:var(--burgundy);font-weight:500;text-decoration:none;transition:0.25s;}
        .link-btn:hover{background:var(--burgundy);color:#fff;}
        .score-image{max-width:140px;max-height:90px;border:1px solid var(--grey-light);border-radius:6px;margin-top:18px;}
        .footer{padding:22px 40px;text-align:center;background:var(--burgundy);color:#fff;font-size:13px;}
        @media(max-width:768px){.nav-content,.main,.footer{padding-left:20px;padding-right:20px;}.main{padding-top:120px;}}
    </style>
</head>
<body>
    <nav class="nav">
        <div class="nav-content">
            <a href="index.html" class="nav-logo">ALIN GHERMAN</a>
            <div class="nav-links">
                <a href="index.html">Home</a>
                <a href="compositions-percussion.html">Compositions</a>
                <a href="support.html">Support</a>
                <a href="thank-you.html">Thank You</a>
            </div>
        </div>
    </nav>

    <div class="hero">
        <span class="hero-label">SECURED SCORE ACCESS</span>
        <h1 class="hero-title">Thank You</h1>
        <p class="hero-subtitle">You have premium access to your score now. The assigned code is shown below and the score links are ready to download.</p>
        <div class="hero-divider"></div>
    </div>

    <main class="main">
        <article class="card">
            <h1>##TITLE##</h1>
            <p>1. Click the score button(s) below to download the PDF locally in the folder <code>scores/</code>.</p>
            <p>2. Open the downloaded score and use this password code to unlock if required.</p>
            <p>3. Save the code somewhere safe; you can return to this page anytime.</p>
            <div class="links">##LINKS##</div>
            <p><strong>Code/password:</strong></p>
            <div class="code-block">##CODE##</div>
            ##IMAGE##
            <p style="margin-top:16px;">After closing this page your code will still remain here unless the browser cache is cleared. Keep a copy safe for future access.</p>
            <p><a class="link-btn" href="thank-you.html?id=##CODE##">View dynamic page for this code</a></p>
        </article>
    </main>

    <footer class="footer">© 2026 Alin Gherman — All rights reserved</footer>
</body>
</html>'''

# asigurăm că avem fișierele corespunzătoare în folderul scores/ înainte de a genera paginile
ensure_score_files_exists()

for i, (code, entry) in enumerate(pages.items(), start=1):
    title = entry.get('title', code)
    score_links = entry.get('scoreLinks', [])
    code_image = entry.get('codeImage', f'codes/{code}.jpeg')

    if score_links:
        def render_link(ln):
            local_href = local_score_url(ln.get('url', ''))
            if local_href:
                basename = os.path.basename(urllib.parse.urlparse(ln.get('url', '')).path) or code
                download_name = f"{code}-{basename}"
                return f'<a class="link-btn" href="{local_href}" download="{download_name}">{ln["label"]}</a>'
            return f'<span style="font-size:14px;color:#E11D48;">{ln["label"]}: PDF lipsă în folderul scores/</span>'
        links_section = ''.join([render_link(ln) for ln in score_links])
    else:
        links_section = '<div style="font-size:14px;color:#6B7280;">Nicio partitură locală disponibilă pentru acest cod.</div>'

    image_uri = image_to_data_uri(code_image)
    if not image_uri:
        image_uri = make_fallback_svg_code(code)

    image_section = f'<div><img src="{image_uri}" alt="Code {code}" class="score-image"></div>'

    page_index = i
    html = base_template.replace('##INDEX##', str(page_index)).replace('##TITLE##', title).replace('##CODE##', code).replace('##LINKS##', links_section).replace('##IMAGE##', image_section)

    fname = f'thanky{code}.html'
    with open(fname, 'w', encoding='utf-8') as out:
        out.write(html)
    print('created', fname)

print('done', len(pages))
