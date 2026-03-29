import re, os

BASE = 'c:/Users/IONUT/Desktop/SITE-GHERAM-FULL/'

# Score name + fixed random suffix (not sequential, not guessable)
PAGES = {
    'thankyadd15.html':  ('Addendum exitum',              '8374'),
    'thankyari13.html':  ('Ariciul',                      '2951'),
    'thankybri27.html':  ('Bright challenge fanfare',     '6082'),
    'thankycaf35.html':  ('Cafemelange',                  '4719'),
    'thankycym32.html':  ('Cymbals Vitamins',             '3867'),
    'thankydan43.html':  ('Dance under impending rain',   '9143'),
    'thankydiv45.html':  ('Divertimento',                 '5230'),
    'thankydon414.html': ('Donna Odokia',                 '7416'),
    'thankyerr51.html':  ('Errances',                     '1895'),
    'thankyfol63.html':  ('FOLCLOR',                      '6347'),
    'thankyful612.html': ('Full bright fanfare',          '2068'),
    'thankygra79.html':  ('Grains fleur et son envol',    '8521'),
    'thankyhau820.html': ('Haute Tension',                '4903'),
    'thankyhel812.html': ('HELLO',                        '7264'),
    'thankyhis1820.html':('Histoire 1',                   '3759'),
    'thankyhis2820.html':('Histoire 2',                   '9031'),
    'thankyint95.html':  ('Intermede instrumental',       '5847'),
    'thankykla1122.html':('Klavierstuck',                 '2493'),
    'thankymet131.html': ('Metal spirits',                '6715'),
    'thankymin139.html': ('Minimes apocalypse',           '8042'),
    'thankymou1320.html':('Mouth and strings',            '3176'),
    'thankymou1322.html':('Mouvements',                   '7589'),
    'thankyopo1522.html':('O poveste',                    '4268'),
    'thankyori157.html': ('Origines',                     '9374'),
    'thankypla1625.html':('Play song',                    '1853'),
    'thankypoe1619.html':('Poesie perdue',                '6490'),
    'thankypot1616.html':('Pot-pourri',                   '3027'),
    'thankypri1612.html':('Prilude',                      '8631'),
    'thankyrel181.html': ('Relations lumineuses',         '5142'),
    'thankytar201.html': ('Taraf in the graveyard',       '7908'),
    'thankyvib2218.html':('Vibrations',                   '2364'),
    'thankyvla2214.html':('VLAN',                         '9517'),
}

for fname, (title, suffix) in PAGES.items():
    path = BASE + fname
    if not os.path.exists(path):
        print(f'MISSING: {fname}')
        continue
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    new_title = f'{title} · {suffix}'
    c = re.sub(r'<title>[^<]*</title>', f'<title>{new_title}</title>', c)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f'{fname}: title = "{new_title}"')

print('\nDone!')
