#!/usr/bin/env python3
"""
Controleert of er ergens een gloed of verloop hard wordt afgesneden.

Waarom dit bestaat
------------------
Op deze site zitten een paar zachte roze wolken (achter de badges, achter de
projectkaarten en rond Contact). Als zo'n wolk groter is dan het gedeelte waar
hij in staat, wordt hij op de rand recht afgekapt en zie je een streep of een
rechthoek op de pagina. Dat is drie keer gebeurd tijdens het bouwen en met het
oog niet altijd goed te zien.

Dit script verbergt ALLE inhoud en rendert alleen de wolken. Elke plotselinge
kleursprong die dan overblijft is per definitie een afgesneden verloop.

Nodig
-----
    pip install pillow numpy websocket-client
En Google Chrome moet geinstalleerd zijn.

Gebruik
-------
Start eerst een lokale server in de projectmap:

    python3 -m http.server 8931

En draai dan in een tweede terminal:

    python3 tools/controleer-gloeden.py

Je wil zien: "schoon: geen enkele harde rand" op elke breedte.
Krijg je wel een melding, kijk dan in de bijbehorende `-gloed-<breedte>.png` die
het script naast zichzelf neerzet: daar zie je precies waar de streep zit.
"""
import base64
import json
import os
import subprocess
import time
import urllib.request

import numpy as np
import websocket
from PIL import Image

URL = "http://localhost:8931/"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT = 9477
BREEDTES = [(1907, 1000), (1440, 900), (768, 1024), (390, 844)]
DREMPEL = 6          # som van de rgb-verschillen tussen twee opeenvolgende rijen
HIER = os.path.dirname(os.path.abspath(__file__))

# Alles onzichtbaar, behalve de lagen die de verlopen tekenen.
CSS = """
  body *, body::before, body::after { visibility: hidden !important; }
  .hero__sky, .hero__glow,
  .contact::before, .projects::before, .badges::before { visibility: visible !important; }
"""


def start_chrome():
    profiel = os.path.join(HIER, ".chrome-controle")
    os.makedirs(profiel, exist_ok=True)
    proces = subprocess.Popen(
        [CHROME, "--headless=new", f"--remote-debugging-port={PORT}",
         f"--user-data-dir={profiel}", "--no-first-run", "--no-default-browser-check",
         "--hide-scrollbars", "--remote-allow-origins=*", "--disable-gpu", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(80):
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=1)
            return proces
        except Exception:
            time.sleep(0.3)
    raise SystemExit("Chrome start niet. Staat het pad naar Chrome goed?")


class Browser:
    def __init__(self):
        tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json"))
        adres = [t for t in tabs if t["type"] == "page"][0]["webSocketDebuggerUrl"]
        self.ws = websocket.create_connection(adres, timeout=90)
        self.n = 0

    def stuur(self, methode, **params):
        self.n += 1
        self.ws.send(json.dumps({"id": self.n, "method": methode, "params": params}))
        while True:
            antwoord = json.loads(self.ws.recv())
            if antwoord.get("id") == self.n:
                if "error" in antwoord:
                    raise RuntimeError(f"{methode}: {antwoord['error']}")
                return antwoord.get("result", {})


def main():
    try:
        urllib.request.urlopen(URL, timeout=3)
    except Exception:
        raise SystemExit("Geen server op %s. Start eerst: python3 -m http.server 8931" % URL)

    proces = start_chrome()
    alles_schoon = True
    try:
        b = Browser()
        for breedte, hoogte in BREEDTES:
            b.stuur("Network.enable")
            b.stuur("Network.setCacheDisabled", cacheDisabled=True)
            b.stuur("Emulation.setEmulatedMedia",
                    features=[{"name": "prefers-reduced-motion", "value": "reduce"}])
            b.stuur("Emulation.setDeviceMetricsOverride", width=breedte, height=hoogte,
                    deviceScaleFactor=1, mobile=(breedte < 500),
                    screenWidth=breedte, screenHeight=hoogte)
            b.stuur("Page.enable")
            b.stuur("Page.navigate", url=URL)
            time.sleep(4)
            b.stuur("Runtime.evaluate", expression=
                    "var s=document.createElement('style');"
                    "s.textContent=%r;document.head.appendChild(s);" % CSS)
            time.sleep(1.2)

            secties = json.loads(b.stuur("Runtime.evaluate", returnByValue=True, expression="""
                JSON.stringify(Array.from(document.querySelectorAll('section,.marqueewrap,footer'))
                  .map(function(e){var r=e.getBoundingClientRect();
                    return [e.className.toString().split(' ')[0] || e.tagName.toLowerCase(),
                            Math.round(r.top + scrollY), Math.round(r.height)];}))
            """)["result"]["value"])

            def welk_gedeelte(y):
                treffers = [naam for naam, top, hg in secties if top <= y <= top + hg]
                return treffers[-1] if treffers else "buiten alle gedeeltes"

            maten = b.stuur("Page.getLayoutMetrics")
            pb = int(maten["cssContentSize"]["width"])
            ph = int(maten["cssContentSize"]["height"])
            plaatje = b.stuur("Page.captureScreenshot", format="png",
                              clip={"x": 0, "y": 0, "width": pb, "height": ph, "scale": 1},
                              captureBeyondViewport=True)
            pad = os.path.join(HIER, "-gloed-%d.png" % breedte)
            with open(pad, "wb") as f:
                f.write(base64.b64decode(plaatje["data"]))

            arr = np.asarray(Image.open(pad).convert("RGB")).astype(int)
            per_rij = np.abs(np.diff(arr.mean(axis=1), axis=0)).sum(axis=1)
            per_kolom = np.abs(np.diff(arr.mean(axis=0), axis=0)).sum(axis=1)

            print("%4d px breed (pagina %d hoog)" % (breedte, ph))
            gevonden = False
            for y in np.where(per_rij > DREMPEL)[0]:
                print("   HORIZONTALE streep op y=%d (sprong %.1f) in %s"
                      % (y, per_rij[y], welk_gedeelte(y)))
                gevonden = True
            for x in np.where(per_kolom > DREMPEL)[0]:
                print("   VERTICALE streep op x=%d (sprong %.1f)" % (x, per_kolom[x]))
                gevonden = True
            if not gevonden:
                print("   schoon: geen enkele harde rand")
            else:
                alles_schoon = False
                print("   zie %s" % os.path.relpath(pad))
    finally:
        proces.terminate()

    print()
    print("ALLES SCHOON" if alles_schoon else "ER ZIJN AFGESNEDEN VERLOPEN, zie hierboven")


if __name__ == "__main__":
    main()
