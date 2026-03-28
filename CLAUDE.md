# CLAUDE.md — alingherman.com

## Despre proiect

Site-ul personal al compozitorului **Alin Gherman** — portofoliu de compoziții, catalog de instrumente inventate, pressbook și link-uri. Site static multi-pagină (HTML/CSS/JS), fără framework, deployat pe **Netlify**.

## Stack tehnic

- **HTML5 / CSS3 / Vanilla JS** — fiecare pagină e un fișier `.html` independent
- **Fonturi**: Google Fonts — `Instrument Serif` (headings), `Inter` (body text)
- **Imagini**: fișiere externe în folder-ul rădăcină (NU base64 inline, cu excepția cazurilor deja existente)
- **Deploy**: Netlify (auto-deploy din GitHub)
- **CMS planificat**: GitHub-based, pentru ca Gherman să poată edita singur conținut
- **Vânzare partituri PDF**: Payhip (0% comision platformă, no-code setup)

## Design system — CULORI

```css
--burgundy:    #6B1B3D;   /* culoare primară, headings, accente */
--turquoise:   #14B8A6;   /* culoare secundară, hover states, butoane */
--cream:       #FDFBF7;   /* background principal */
--text-dark:   #2D2D2D;   /* text body */
--text-light:  #6B7280;   /* text secundar / muted */
```

### Reguli culori
- Burgundy = headings, titluri secțiuni, decorațiuni SVG
- Turquoise = hover pe link-uri, butoane CTA, elemente interactive
- Cream = background body pe toate paginile
- NU folosi alte culori fără aprobare explicită

## Design system — TIPOGRAFIE

```css
h1, h2, h3    → font-family: 'Instrument Serif', serif;
body, p, span  → font-family: 'Inter', sans-serif;
```

## Design system — ELEMENTE VIZUALE

- **Waveform SVG decorations** — linii ondulate SVG folosite ca separatoare și elemente decorative
- **Work cards** — carduri expandabile pe rânduri pentru listarea compozițiilor
- **Footer** — ÎNTOTDEAUNA în afara containerului `max-width`, full-width

## Structura fișierelor

```
/
├── index.html                    # Homepage
├── compositions/
│   ├── solo.html                 # Compoziții solo
│   ├── duos.html                 # Duouri
│   ├── ensembles.html            # Ansambluri
│   ├── orchestra.html            # Orchestră
│   ├── opera.html                # Operă
│   ├── organ.html                # Orgă
│   ├── brass.html                # Alamă
│   ├── percussion.html           # Percuție (PAGINA REFERINȚĂ pentru layout)
│   ├── instrumental-theatre.html # Teatru instrumental
│   ├── film-dance-media.html     # Film / dans / media
│   ├── electronic.html           # Electronică
│   └── computer.html             # Computer music
├── instruments/
│   ├── metal-cans-chimes.html
│   ├── metal-spoons-chimes.html
│   ├── wood-chimes.html
│   ├── glass-chimes.html
│   └── metal-tubes-chimes.html
├── my-links.html                 # Pagina My Links
├── pressbook.html                # Timeline pressbook (1994–2006+)
├── images/                       # Toate imaginile proiectului
├── styles.css                    # CSS global (dacă există)
└── CLAUDE.md                     # Acest fișier
```

## ⚠️ REGULI STRICTE — NU ÎNCĂLCA NICIODATĂ

### 1. Container margin
```
NU modifica NICIODATĂ `.container` margin independent.
Dacă trebuie ajustat spacing, folosește padding sau wrapper divs.
```

### 2. Body flex layout
```
TOATE paginile de compoziții TREBUIE să aibă exact același body flex layout
ca pagina de percuție (percussion.html). Aceasta este PAGINA REFERINȚĂ.
Copiază structura body/main/footer exact de acolo.
```

### 3. Footer placement
```
Footer-ul este ÎNTOTDEAUNA în afara oricărui container cu max-width.
Footer = full-width, sticky bottom.
```

### 4. Imagini
```
Preferă ÎNTOTDEAUNA fișiere externe pentru imagini noi.
NU converti la base64 decât dacă e cerut explicit.
Imaginile stau în folderul /images/ sau în root (structură flat).
```

### 5. Consistență între pagini
```
Când modifici o pagină de compoziții, verifică că:
- Header-ul e identic cu celelalte pagini
- Navigația e identică
- Footer-ul e identic
- Font imports sunt identice
- Color scheme e identică
```

## Convenții de cod

### HTML
- Semantic HTML5 (`<header>`, `<main>`, `<footer>`, `<section>`, `<article>`)
- Clase descriptive în română sau engleză (consistent per pagină)
- Fiecare pagină include propriile `<style>` în `<head>` (inline CSS)
- Meta tags complete: description, viewport, charset UTF-8, lang="ro" sau lang="en"

### CSS
- Mobile-first responsive design
- Breakpoints: 768px (tablet), 1024px (desktop)
- Tranziții smooth pe hover states (0.3s ease)
- Box-shadow subtle pe carduri: `0 2px 8px rgba(0,0,0,0.08)`

### Work cards (carduri compoziții)
- Fiecare lucrare = un card expandabil
- Click pe card → expandează detalii (anul, instrumentație, durată, note program)
- Rânduri de carduri — responsive grid
- Hover effect: ușoară ridicare (translateY) + shadow increase

## Pagini speciale

### Homepage (index.html)
- Hero section cu numele compozitorului
- Secțiuni: despre, compoziții (preview), instrumente (preview), contact
- Waveform SVG decorations între secțiuni

### Pressbook (pressbook.html)
- Format timeline vertical
- Perioada acoperită: 1994–2006+
- Fiecare intrare: an, eveniment, descriere
- Design: linie verticală cu puncte/noduri pe fiecare an

### My Links (my-links.html)
- Pagină tip Linktree
- Link-uri externe către platforme (YouTube, SoundCloud, academia, etc.)

### Instrumente inventate
- Fiecare instrument = pagină dedicată cu:
  - Poze ale instrumentului
  - Descriere
  - Cum e construit
  - Cum sună (link audio dacă disponibil)
  - Compoziții care îl folosesc

## Deployment

```bash
# Site-ul se deployază automat pe Netlify la push pe main
git add .
git commit -m "descriere modificare"
git push origin main
# Netlify detectează push-ul și face build automat
```

## Workflow de lucru

1. Deschide proiectul în terminal: `cd ~/projects/alingherman`
2. Rulează `claude` pentru a începe sesiunea
3. Descrie ce pagină/secțiune trebuie modificată
4. Claude Code citește fișierele relevante, face modificări
5. Testează local (deschide HTML în browser)
6. Commit + push → live pe Netlify

## Tone of voice (conținut site)

- Academic dar accesibil
- Bilingv: română pentru publicul local, engleză pentru internațional
- Descrieri compoziții: poetice dar informative
- NU folosi limbaj informal sau emoji pe site
