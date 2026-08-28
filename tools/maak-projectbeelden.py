#!/usr/bin/env python3
"""
Maakt de projectbeelden voor de kaarten.

Nodig: pip install pillow numpy
Draaien:  python3 tools/maak-projectbeelden.py

Wat het doet
------------
De kaarten hebben een VIERKANT beeldvlak. De ontwerpen van Tess zijn dat niet:
Boekenzoeker is 4:3, HEMA is 2:1 en Bakje Plant is een smalle mobiele pagina.

Voor de liggende ontwerpen blijft de volle breedte staan en wordt er boven en
onder bijgevuld met de MEDIAAN-kleur van de buitenste beeldrijen. Dat is precies
de achtergrondkleur van het ontwerp zelf, dus je ziet de vulling niet.
De mediaan (en niet het gemiddelde) omdat er een logo in de hoek kan staan; dat
mag de kleur niet vervuilen.

Bakje Plant is staand en wordt vierkant vanaf de bovenkant gesneden.
"""
from PIL import Image
import numpy as np
import os

HIER = os.path.dirname(os.path.abspath(__file__))
BRON = os.path.join(HIER, "..", "bronbestanden", "projecten")
DOEL = os.path.join(HIER, "..", "assets", "img")
FORMAAT = 900          # de kaarten tonen dit op ~280 px, 900 is ruim genoeg voor retina


def randkleur(arr, kant, diepte=4):
    band = arr[:diepte] if kant == "boven" else arr[-diepte:]
    return np.median(band.reshape(-1, 3), axis=0).astype(np.uint8)


def maak_vierkant(pad):
    im = Image.open(pad).convert("RGB")
    arr = np.asarray(im)
    hoogte, breedte, _ = arr.shape

    if hoogte >= breedte:
        # staand (mobiele pagina): vierkant vanaf de bovenkant
        return im.crop((0, 0, breedte, breedte))

    # liggend: volle breedte houden, boven en onder bijvullen
    vulling = breedte - hoogte
    boven_px = vulling // 2
    onder_px = vulling - boven_px
    boven = np.tile(randkleur(arr, "boven"), (boven_px, breedte, 1))
    onder = np.tile(randkleur(arr, "onder"), (onder_px, breedte, 1))
    return Image.fromarray(np.vstack([boven, arr, onder]))


BESTANDEN = [
    ("boekenzoeker-artboard.png", "project-boekenzoeker"),
    ("bakjeplant-mobiel.png",     "project-bakjeplant"),
    ("hema-artboard.png",         "project-hemacupcakes"),
]

for bron, naam in BESTANDEN:
    im = maak_vierkant(os.path.join(BRON, bron)).resize((FORMAAT, FORMAAT), Image.LANCZOS)
    jpg = os.path.join(DOEL, naam + ".jpg")
    webp = os.path.join(DOEL, naam + ".webp")
    im.save(jpg, quality=88, optimize=True, progressive=True)
    im.save(webp, quality=84, method=6)
    print("%-24s %3d kB jpg / %3d kB webp" % (naam, os.path.getsize(jpg) // 1024,
                                              os.path.getsize(webp) // 1024))
print("\nKlaar. De bestanden staan in assets/img/ en worden al door index.html gebruikt.")
