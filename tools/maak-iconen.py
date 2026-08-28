#!/usr/bin/env python3
"""
Zet de icoon-PNG's om naar SVG-vormen voor de sprite in index.html.

Nodig: pip install pillow numpy scikit-image
Draaien:  python3 tools/maak-iconen.py

Waarom
------
PNG's van 512 px worden op een scherm met hoge resolutie alsnog zachtjes wazig.
SVG blijft altijd scherp en kost samen maar ~9 kB.

Hoe
---
Van elk PNG wordt de zichtbare vorm omgezet in lijnen (contouren), die daarna
worden vereenvoudigd zodat het pad kort blijft. De witte delen in deze iconen
zijn DOORZICHTIG in het origineel, geen wit. Daarom staat er
fill-rule="evenodd" op: dan worden de binnenste contouren als gat behandeld.

Het resultaat wordt naar tools/icons-sprite.svg geschreven. Kopieer de blokken
die je nodig hebt over de bestaande <symbol id="i-...">-blokken in index.html.
"""
from PIL import Image
import numpy as np
from skimage import measure
import os

HIER = os.path.dirname(os.path.abspath(__file__))
BRON = os.path.join(HIER, "..", "bronbestanden", "iconen")
UIT = os.path.join(HIER, "icons-sprite.svg")

# bestandsnaam -> id dat in index.html gebruikt wordt
ICONEN = [
    ("chevrons-omlaag.png", "i-chevrons"),
    ("vinkje-badge.png",    "i-check-badge"),
    ("baret.png",           "i-cap"),
    ("mail.png",            "i-mail"),
    ("medaille.png",        "i-medal"),
    ("github.png",          "i-github"),
    ("linkedin.png",        "i-linkedin"),
]
NAUWKEURIGHEID = 0.9   # lager = nauwkeuriger maar een langer pad


def vereenvoudig(punten, eps):
    """Douglas-Peucker: gooit punten weg die de vorm niet veranderen."""
    if len(punten) < 3:
        return punten
    a, b = punten[0], punten[-1]
    ab = b - a
    lengte = np.hypot(*ab)
    if lengte < 1e-9:
        afstand = np.hypot(*(punten - a).T)
    else:
        rel = punten - a
        afstand = np.abs(ab[0] * rel[:, 1] - ab[1] * rel[:, 0]) / lengte
    i = int(afstand.argmax())
    if afstand[i] <= eps:
        return np.array([a, b])
    return np.vstack([vereenvoudig(punten[:i + 1], eps)[:-1],
                      vereenvoudig(punten[i:], eps)])


def naar_pad(masker, eps, formaat):
    opgevuld = np.pad(masker.astype(float), 1)
    stukken = []
    for contour in measure.find_contours(opgevuld, 0.5):
        if len(contour) < 8:
            continue
        contour = contour - 1.0
        punten = np.stack([contour[:, 1], contour[:, 0]], axis=1)   # rij,kolom -> x,y
        if np.hypot(*(punten[0] - punten[-1])) < 1e-6:
            punten = punten[:-1]
        vorm = vereenvoudig(punten, eps)
        if len(vorm) < 3:
            continue
        opp = 0.5 * abs(np.dot(vorm[:, 0], np.roll(vorm[:, 1], -1))
                        - np.dot(vorm[:, 1], np.roll(vorm[:, 0], -1)))
        if opp < (formaat * formaat) * 0.0004:      # snippertjes overslaan
            continue
        stukken.append((opp, "M" + " L".join("%.1f %.1f" % (x, y) for x, y in vorm) + "Z"))
    stukken.sort(key=lambda t: -t[0])
    return " ".join(d for _, d in stukken)


regels = []
for bestand, naam in ICONEN:
    im = Image.open(os.path.join(BRON, bestand)).convert("RGBA")
    arr = np.asarray(im).astype(int)
    formaat = im.size[0]
    zichtbaar = arr[..., 3] > 128
    pad = naar_pad(zichtbaar, NAUWKEURIGHEID, formaat)
    regels.append('  <symbol id="%s" viewBox="0 0 %d %d">' % (naam, formaat, formaat))
    regels.append('    <path fill="currentColor" fill-rule="evenodd" d="%s"/>' % pad)
    regels.append('  </symbol>')
    print("%-15s viewBox %d, pad %d tekens" % (naam, formaat, len(pad)))

with open(UIT, "w") as f:
    f.write("\n".join(regels))
print("\nGeschreven naar tools/icons-sprite.svg")
print("Kopieer de <symbol>-blokken die je nodig hebt naar index.html.")
