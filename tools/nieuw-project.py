#!/usr/bin/env python3
"""
Maakt in een keer een kaartbeeld voor een nieuw project, en print het stukje
HTML dat je in index.html kunt plakken.

Nodig: pip install pillow numpy
Gebruik:

    python3 tools/nieuw-project.py mijn-screenshot.png "Naam van het project"

Je mag elk formaat aanleveren: liggend, staand of vierkant. Het script maakt er
een vierkant beeld van dat het kaartkader helemaal vult, zonder iets belangrijks
af te snijden:

- Liggend beeld  -> de volle breedte blijft staan, boven en onder wordt bijgevuld
                    met de achtergrondkleur van je eigen ontwerp. Die vulling zie
                    je niet.
- Staand beeld   -> er wordt een vierkant vanaf de bovenkant gesneden.
- Vierkant       -> blijft zoals het is.

Het schrijft een .jpg en een .webp naar assets/img/ en print daarna de HTML.
"""
import os
import re
import sys

import numpy as np
from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
DOEL = os.path.join(HIER, "..", "assets", "img")
FORMAAT = 900


def randkleur(arr, kant, diepte=4):
    """De mediaan-kleur van de buitenste beeldrijen: dat is de achtergrondkleur
    van het ontwerp. Mediaan en niet gemiddelde, want een logo in de hoek mag de
    kleur niet vervuilen."""
    band = arr[:diepte] if kant == "boven" else arr[-diepte:]
    return np.median(band.reshape(-1, 3), axis=0).astype(np.uint8)


def maak_vierkant(pad):
    im = Image.open(pad).convert("RGB")
    arr = np.asarray(im)
    hoogte, breedte, _ = arr.shape

    if hoogte == breedte:
        return im, "was al vierkant"
    if hoogte > breedte:
        return im.crop((0, 0, breedte, breedte)), "staand: vierkant vanaf de bovenkant gesneden"

    vulling = breedte - hoogte
    boven_px = vulling // 2
    onder_px = vulling - boven_px
    boven = np.tile(randkleur(arr, "boven"), (boven_px, breedte, 1))
    onder = np.tile(randkleur(arr, "onder"), (onder_px, breedte, 1))
    uitleg = "liggend: %d px boven en %d px onder bijgevuld met je eigen achtergrondkleur" % (
        boven_px, onder_px)
    return Image.fromarray(np.vstack([boven, arr, onder])), uitleg


def naar_bestandsnaam(titel):
    naam = titel.lower()
    for van, naar in [("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"), ("ë", "e"), ("ï", "i")]:
        naam = naam.replace(van, naar)
    naam = re.sub(r"[^a-z0-9]+", "-", naam).strip("-")
    return "project-" + (naam or "nieuw")


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        raise SystemExit("Geef een bestand en een projectnaam mee.")
    bron, titel = sys.argv[1], sys.argv[2]
    if not os.path.exists(bron):
        raise SystemExit("Bestand niet gevonden: %s" % bron)

    naam = naar_bestandsnaam(titel)
    im, uitleg = maak_vierkant(bron)
    im = im.resize((FORMAAT, FORMAAT), Image.LANCZOS)
    jpg = os.path.join(DOEL, naam + ".jpg")
    webp = os.path.join(DOEL, naam + ".webp")
    im.save(jpg, quality=88, optimize=True, progressive=True)
    im.save(webp, quality=84, method=6)

    print()
    print("Beeld gemaakt (%s)" % uitleg)
    print("   assets/img/%s.jpg   %3d kB" % (naam, os.path.getsize(jpg) // 1024))
    print("   assets/img/%s.webp  %3d kB" % (naam, os.path.getsize(webp) // 1024))
    print()
    print("-" * 70)
    print("Plak dit in index.html, net na de laatste </li> van een project")
    print("(zoek op:  <li class=\"card\"  )")
    print("-" * 70)
    print("""
        <li class="card" data-reveal>
          <div class="card__shot">
            <picture>
              <source srcset="assets/img/{n}.webp" type="image/webp">
              <img src="assets/img/{n}.jpg" alt="OMSCHRIJF HIER KORT WAT ER OP HET BEELD STAAT" width="900" height="900" loading="lazy" decoding="async">
            </picture>
          </div>
          <div class="card__body">
            <h3 class="card__title">{t}</h3>
            <p class="card__desc">SCHRIJF HIER EEN OF TWEE REGELS OVER HET PROJECT.</p>
            <a class="btn btn--primary btn--full" href="HTTPS://LINK-NAAR-JE-PROJECT" target="_blank" rel="noopener">
              Bekijk <svg aria-hidden="true"><use href="#i-external"></use></svg>
            </a>
            <span class="card__meta"><svg aria-hidden="true"><use href="#i-check-badge"></use></svg>ZOIETS ALS: FIGMA ONTWERP</span>
          </div>
        </li>
""".format(n=naam, t=titel))
    print("-" * 70)
    print("Vervang daarna de vier stukken in HOOFDLETTERS. Klaar!")
    print()
    print("Wil je onder de knop een link in plaats van een label, gebruik dan")
    print("in plaats van de <span class=\"card__meta\"> deze regel:")
    print('   <a class="card__link" href="HTTPS://..." target="_blank" rel="noopener">'
          '<svg aria-hidden="true"><use href="#i-github"></use></svg>Code op GitHub</a>')
    print()


if __name__ == "__main__":
    main()
