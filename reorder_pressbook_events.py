import re
from pathlib import Path
from bs4 import BeautifulSoup

month_map = {
    'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,'July':7,'August':8,'September':9,'October':10,'November':11,'December':12,
    'Jan':1,'Feb':2,'Mar':3,'Apr':4,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12
}

def parse_score(text):
    t = text.strip()
    if not t:
        return 0
    if '–' in t or '-' in t:
        sep = '–' if '–' in t else '-'
        parts = [p.strip() for p in t.split(sep) if p.strip()]
        scores = [parse_score(p) for p in parts]
        return max(scores) if scores else 0

    m = re.search(r"(\d{1,2})(?:st|nd|rd|th)?\s+([A-Za-z]+)", t)
    if m:
        d = int(m.group(1))
        mo = month_map.get(m.group(2), 0)
        return mo*100 + d

    m = re.search(r"([A-Za-z]+)\s*(\d{4})?", t)
    if m:
        mo = month_map.get(m.group(1), 0)
        return mo*100 + 1

    m = re.search(r"(\d{1,2})", t)
    if m:
        return int(m.group(1))

    return 0

for fn in ["pressbook-timeline-updated.html", "pressbook-timeline.html"]:
    path = Path(fn)
    text = path.read_text(encoding='utf-8')
    soup = BeautifulSoup(text, 'html.parser')

    for year in soup.select('.year-section'):
        # take top-level event divs only
        events = [child for child in year.find_all('div', class_='event', recursive=False)]
        if not events:
            continue

        scores = []
        for e in events:
            date_div = e.find('div', class_='event-date')
            score = parse_score(date_div.get_text(strip=True)) if date_div else 0
            scores.append((score, e))

        new_order = [e for _, e in sorted(scores, key=lambda x: x[0], reverse=True)]

        for e in events:
            e.extract()

        for e in new_order:
            year.append('\n')
            year.append(e)

    path.write_text(str(soup), encoding='utf-8')
    print(f'Updated {fn}')

# debug values
print('debug')
for d in ['3rd June','6th June','9th October','January – February','1st August','2nd August','27th September']:
    print(d, parse_score(d))
