import re
from pathlib import Path

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
        return mo * 100 + d
    m = re.search(r"([A-Za-z]+)\s*(\d{4})?", t)
    if m:
        mo = month_map.get(m.group(1), 0)
        return mo * 100 + 1
    m = re.search(r"(\d{1,2})", t)
    if m:
        return int(m.group(1))
    return 0


def find_matching_div(s, start_idx):
    open_tag = re.compile(r'<\s*div\b', re.IGNORECASE)
    close_tag = re.compile(r'<\s*/\s*div\b', re.IGNORECASE)

    # find first > after start_idx
    gt = s.find('>', start_idx)
    if gt == -1:
        return -1
    idx = gt + 1
    depth = 1
    while depth > 0:
        # look for next <div or </div>
        next_open = open_tag.search(s, idx)
        next_close = close_tag.search(s, idx)
        if not next_close:
            return -1
        if next_open and next_open.start() < next_close.start():
            # found nested open
            # ensure it's not the same start tag (position >=idx should be okay)
            depth += 1
            # move idx after > of this tag
            gt2 = s.find('>', next_open.end())
            if gt2 == -1:
                return -1
            idx = gt2 + 1
            continue
        # close tag wins
        depth -= 1
        gt2 = s.find('>', next_close.end())
        if gt2 == -1:
            return -1
        idx = gt2 + 1
    return idx


def reorder_calendar_in_file(path):
    content = Path(path).read_text(encoding='utf-8')
    parts = re.split(r'(?=<!--\s*\d{4}\s*-->)', content)
    if len(parts) == 1:
        return False
    prefix = parts[0]
    new_parts = [prefix]

    for chunk in parts[1:]:
        start = chunk.find('<div class="year-section"')
        if start == -1:
            new_parts.append(chunk)
            continue
        end = find_matching_div(chunk, start)
        if end == -1:
            new_parts.append(chunk)
            continue

        year_section = chunk[start:end]
        head = year_section[:year_section.find('<div class="event"')] if '<div class="event"' in year_section else year_section
        if '<div class="event"' not in year_section:
            new_parts.append(chunk)
            continue

        events_area = year_section[year_section.find('<div class="event"'):]

        # Find all event blocks with positions
        events = []
        idx = 0
        while True:
            ev_start = events_area.find('<div class="event"', idx)
            if ev_start == -1:
                break
            ev_end = find_matching_div(events_area, ev_start)
            if ev_end == -1:
                break
            events.append(events_area[ev_start:ev_end])
            idx = ev_end

        tail = events_area[idx:]

        if not events:
            new_parts.append(chunk)
            continue

        def event_score(ev):
            m = re.search(r'<div class="event-date">(.*?)</div>', ev, re.DOTALL)
            date = m.group(1).strip() if m else ''
            return parse_score(date)

        sorted_events = sorted(events, key=event_score, reverse=True)
        reordered_year_section = head + ''.join(sorted_events) + tail
        new_parts.append(chunk[:start] + reordered_year_section + chunk[end:])

    new_content = ''.join(new_parts)
    Path(path).write_text(new_content, encoding='utf-8')
    return True

for fn in ["pressbook-timeline-updated.html", "pressbook-timeline.html"]:
    ok = reorder_calendar_in_file(fn)
    print(f"{fn}: {'updated' if ok else 'skipped'}")

# debug check
for d in ['3rd June','6th June','9th October','January – February','1st August','2nd August','27th September']:
    print(d, parse_score(d))
