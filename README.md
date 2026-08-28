# Portfolio — Tess Kollof

Mijn portfolio: **https://tejuko.github.io/2026Portfolio/**

Dit is een "gewone" website: geen frameworks, geen installatie, geen build-stap.
Je opent een bestand, verandert iets, slaat op, en ververst je browser.

> **Kom je hier na een tijdje terug?** Lees dan
> [PROJECT-GESCHIEDENIS.md](PROJECT-GESCHIEDENIS.md). Daar staat waarom de site
> is zoals hij is, wat er al geprobeerd en afgekeurd is, en waar de originele
> bestanden staan. Dit bestand gaat alleen over *hoe* je iets aanpast.

---

## Even snel: hoe pas ik iets aan?

1. Open de map in je editor (VS Code bijvoorbeeld).
2. Open `index.html`, `styles.css` of `main.js` en verander wat je wil.
3. Dubbelklik `index.html` om het lokaal in je browser te bekijken.
4. Tevreden? Dan online zetten:

```bash
git add -A
git commit -m "korte omschrijving van wat je veranderde"
git push
```

Wacht daarna ~1 minuut. GitHub zet het automatisch live. Zie je je wijziging
niet? Doe een **harde verversing**: `Cmd + Shift + R`.

---

## Welk bestand doet wat?

| Bestand | Wat er in staat |
|---|---|
| `index.html` | Alle **tekst** en de opbouw van de pagina. Hier verander je woorden, links en projecten. |
| `styles.css` | Alle **vormgeving**: kleuren, formaten, afstanden, schaduwen, animaties. |
| `main.js` | De **bewegende dingen**: het Portfolio-effect, het menu, de projectenrij. |
| `assets/img/` | De foto's en projectbeelden. |
| `assets/CV_Tess_Kollof.pdf` | Je cv, waar de knop "Download cv" naartoe linkt. |
| `.nojekyll` | Een leeg bestandje dat GitHub nodig heeft. Niet weghalen. |
| `bronbestanden/` | De **originelen**: het Figma-ontwerp, screenshots van de prototypes, de icoon-PNG's en je foto's op volle resolutie. De site gebruikt deze map niet, hij staat er zodat je later niets kwijt bent. |
| `tools/` | Hulpscripts: een nieuw project toevoegen, de beelden en iconen opnieuw maken, en een controle op afgesneden verlopen. |

---

## De dingen die je het vaakst wil aanpassen

### De regel "Laten we samenwerken!"
Dat is een link naar het contactgedeelte. Hij ziet er bewust uit als gewone
tekst; alleen als je eroverheen gaat wisselt de kleur. In `index.html` staat hij
als `<p class="about__closer"><a href="#contact">...`. Wil je hem naar iets
anders laten wijzen, verander dan die `href`.

### Een tekst veranderen
Zoek in `index.html` naar de tekst zoals die op de site staat en typ hem over.
Verder hoef je niets te doen.

### Een kleur veranderen
Alle kleuren staan **bovenaan** `styles.css`, in het blokje dat begint met
`:root {`. Verander daar één regel en de hele site gaat mee:

```css
:root{
  --cream:     #FFF7F0;   /* de achtergrond van de pagina */
  --pink-100:  #FFE3E1;   /* zacht roze, o.a. de projectkaarten */
  --hero-top:  #FE97A5;   /* het roze bovenaan de pagina */
  --rose:      #EB5E71;   /* de knoppen */
  --rose-deep: #D8465D;   /* tekst op het roze, zoals het menu */
  --magenta:   #ED3E78;   /* de iconen */
  --ink:       #1B1215;   /* gewone tekst */
}
```

Verander een kleur **alleen hier**, niet op tien plekken verderop in het bestand.

### Een project toevoegen — stap voor stap

Het lastigste is het beeld: de kaarten hebben een **vierkant** beeldvlak en dat
moet helemaal gevuld zijn, anders krijg je witte randen. Daarvoor is een script
dat het werk voor je doet. Je hoeft niets van code te snappen.

#### Stap 1 — eenmalig: Python-pakketten installeren

Alleen de eerste keer:

```bash
pip install pillow numpy
```

#### Stap 2 — maak een afbeelding van je project

Een screenshot van je ontwerp of je website. **Elk formaat mag**: liggend,
staand of vierkant. Snij wel de lege ruimte om je ontwerp weg, zodat alleen je
ontwerp overblijft.

#### Stap 3 — laat het script het beeld maken

```bash
python3 tools/nieuw-project.py pad/naar/jouw-screenshot.png "Naam van het project"
```

Bijvoorbeeld:

```bash
python3 tools/nieuw-project.py ~/Desktop/mijn-app.png "Mijn App"
```

Het script maakt er een vierkant beeld van dat het kader precies vult:

| Jouw beeld | Wat het script doet |
|---|---|
| Liggend | De volle breedte blijft staan. Boven en onder wordt bijgevuld met de achtergrondkleur van je eigen ontwerp, dus je ziet die vulling niet. |
| Staand | Er wordt een vierkant vanaf de bovenkant gesneden. |
| Vierkant | Blijft zoals het is. |

Het zet een `.jpg` en een `.webp` in `assets/img/`.

#### Stap 4 — plak het stukje HTML

Het script **print zelf het stukje HTML** dat je nodig hebt, met de juiste
bestandsnamen er al in. Kopieer dat.

Open `index.html`, zoek op `<li class="card card--more"` (dat is de laatste
kaart, die met "de rest staat op GitHub") en plak jouw blok er **net boven**.

#### Stap 5 — vul de vier stukken in HOOFDLETTERS in

In het geplakte blok staan vier plekken die je moet vervangen:

| Wat er staat | Wat jij invult |
|---|---|
| `alt="OMSCHRIJF HIER..."` | Kort wat er op het beeld staat. Dit leest een screenreader voor. |
| `SCHRIJF HIER EEN OF TWEE REGELS...` | De omschrijving die op de kaart komt. |
| `href="HTTPS://LINK-NAAR-JE-PROJECT"` | Waar de knop "Bekijk" naartoe gaat. |
| `ZOIETS ALS: FIGMA ONTWERP` | Het labeltje onder de knop. |

Wil je onder de knop een **link** in plaats van een labeltje (zoals "Code op
GitHub" bij Bakje Plant)? Het script print onderaan de regel die je daarvoor in
de plaats zet.

#### Stap 6 — kijken en online zetten

Dubbelklik `index.html` om het te bekijken. Klopt het?

```bash
git add -A
git commit -m "Project Mijn App toegevoegd"
git push
```

Na ongeveer een minuut staat het live.

#### Even opletten

- De kaarten staan in een **rij die je horizontaal kunt schuiven**. Je kunt dus
  zoveel projecten toevoegen als je wil; er komt automatisch een schuifbalk bij.
- Heb je genoeg projecten, dan kun je de laatste kaart met "de rest staat op
  GitHub" weghalen. Dat is het hele blok `<li class="card card--more">`.
- Een project **aanpassen** in plaats van toevoegen: zoek de titel in
  `index.html` en verander de tekst eromheen. Je hebt het script alleen nodig
  als je ook een nieuw beeld wil.

### De lopende balk met skills
Zoek naar `marquee__group`. Dat blok staat er **twee keer**, precies hetzelfde.
Dat moet zo: daardoor loopt de balk rond zonder te haperen. Pas je iets aan, pas
het dan in **beide** blokken aan.

### Iets dat schuin staat wordt wazig
Draai tekst niet twee keer. De foto bij Over mij staat al schuin (`rotate` op
`.about__photo`), dus het `hoi!`-label daarbinnen staat zelf op `rotate: 0deg`.
Zet je daar weer een hoek in, dan valt de tekst tussen de pixels en wordt hij
wazig.

### De krullen en sterretjes verplaatsen
Zoek in `styles.css` naar `.deco--`. Elke krul heeft zo'n regel met `top`,
`left`/`right` en `width`. Verander die getallen om hem te verplaatsen of te
vergroten.

---

## Het Portfolio-effect in de hero

Het woord "Portfolio" is geen tekst maar een **tekening op een canvas**, opgebouwd
uit honderden kleine blokjes. Wat `main.js` doet:

1. Het schrijft het woord op een onzichtbaar vlak.
2. Het legt daar een raster over en kijkt per vakje: zit hier letter, ja of nee?
3. Elk "ja" wordt een blokje met een eigen kleur uit het roze verloop.
4. Bij het laden vliegen de blokjes van buiten het beeld naar hun plek.
5. Daarna duwt je muis ze weg, met een veer die ze terugtrekt.
6. En er schuift continu een **kleurgolf** door de letters, zodat elk deel
   steeds even diep genoeg van kleur is om goed te lezen.

### Draaiknoppen (bovenaan `initWordmark` in `main.js`)

| Naam | Wat het doet |
|---|---|
| `TEXT` | Welk woord er staat. |
| `COLOR_TOP` | De kleur linksboven, als `[rood, groen, blauw]`. Nu wit. |
| `COLOR_BOT` | De kleur rechtsonder. Nu `#DE4259`. |
| `SHIFT_UP` | Hoeveel **dieper** de kleurgolf gaat. Hoger = beter leesbaar. |
| `SHIFT_DOWN` | Hoeveel **lichter** de golf gaat. Houd dit laag. |
| `SHIFT_SPEED` | Hoe snel de golf reist. Hoger = sneller. |
| `SHIFT_LENGTH` | Hoe lang de golf is. Hoger = kortere golf, meer banen tegelijk. |
| `SHIFT_TILT` | Hoe schuin de golf staat. `0` is kaarsrecht, hoger is schuiner. |

Wil je de golf **duidelijker** zien? Zet `SHIFT_UP` hoger. Wil je meer banen
tegelijk over het woord? Zet `SHIFT_LENGTH` hoger.

**Let op:** ga je aan het raster zitten (`cellSize`, `drawSize`), bekijk het
resultaat dan met animaties **uit**. Anders kijk je naar een half beeldje van de
beweging en lijken de letters kapot terwijl ze prima zijn. In Chrome: DevTools →
`Cmd+Shift+P` → typ "reduced motion" → "Emulate prefers-reduced-motion".

---

## Het glaseffect

De badges bij Over mij, de projectkaarten en de tweede knop zijn "glas". Dat is
drie dingen bij elkaar:

1. Een half doorschijnende achtergrond (`rgba(...)` met een getal onder de 1).
2. `backdrop-filter: blur(...)`, dat vervaagt wat erachter zit.
3. Een lichtrandje langs de bovenkant (`inset 0 1px 0 rgba(255,255,255,...)`).

Belangrijk: op een egale achtergrond zie je van glas niets. Daarom staat er
achter de badges en achter de projectenrij een zachte kleurwolk waar het glas
iets van kan tonen.

Die wolken gebruiken `radial-gradient(closest-side, ...)`. Dat woord
`closest-side` zorgt ervoor dat de gloed altijd netjes naar doorzichtig uitloopt
en nooit met een harde rand afbreekt. **Verander dat niet in een percentage** —
dan krijg je een zichtbare rechthoek op de pagina.

Tweede valkuil met gloeden: de doos van de gloed moet **binnen** het gedeelte
passen, of het gedeelte moet hem laten doorlopen. Bij Contact staat daarom
`overflow-x: clip; overflow-y: visible` en staat de gloed op `z-index: -1`. Zo
loopt hij achter de inhoud van de gedeeltes erboven en eronder door, in plaats
van er recht afgekapt te worden. Zet je daar `overflow: hidden`, dan krijg je een
harde streep terug.

Derde valkuil, en die is makkelijk te missen: onder het contactgedeelte zit alleen
de footer, dus daar is nog maar ~80 px ruimte. Loopt de gloed verder dan het
einde van de pagina, dan wordt hij daar alsnog afgekapt. Daarom staat het
middelpunt op `top: 38%` in plaats van 50% en is de hoogte `130%`: de overloop
gaat vooral naar boven, waar het projectengedeelte zit. **Maak je die hoogte
groter, controleer dan of de onderkant nog binnen de pagina valt.**

Vierde valkuil: **zet een gloed nooit in een element dat moet scrollen.** De
projectenrij (`.rail`) heeft `overflow` nodig om horizontaal te kunnen schuiven,
en dat kapt de gloed recht af. Daarom staat die gloed op `.projects`, het
gedeelte eromheen.

Vijfde valkuil, in datzelfde element: die rij kapt **ook de schaduwen onder de
kaarten** af. Daarom heeft `.rail` een ruime `padding-bottom` van `3.75rem`.
Maak je die kleiner, of geef je de kaarten een grotere schaduw, dan komt de
streep terug.

### Zelf controleren

Twijfel je of een verloop ergens wordt afgesneden? Er is een script dat dat voor
je nakijkt. Zie [`tools/controleer-gloeden.py`](tools/controleer-gloeden.py) — het
verbergt alle inhoud, rendert alleen de wolken en meldt elke harde streep. Je wil
"ALLES SCHOON" zien.

---

## Projectbeelden opnieuw maken

De beelden komen uit verse screenshots van de echte prototypes en de live site.
Twee dingen om te weten als je dat opnieuw doet:

- **Adobe XD-prototypes hebben WebGL nodig.** In een normale browser werkt dat.
  Krijg je "There was a problem displaying this prototype", dan is het dus niet
  je link die stuk is.
- **Bakje Plant is een mobiele site.** Screenshot die op telefoonformaat; op een
  breed venster rekt hij uit.

Zijn je ontwerpen niet vierkant? Houd dan de volle breedte en vul boven en onder
bij met de achtergrondkleur van het ontwerp zelf. Dan ziet niemand de vulling.

---

## Toegankelijkheid

Dit zit erin, dus houd het erin als je iets toevoegt:

- Alle animaties gaan uit als iemand in zijn systeem "minder beweging" aan heeft
  staan (het blok `@media (prefers-reduced-motion: reduce)` onderaan `styles.css`).
- Krullen en sterretjes hebben `aria-hidden="true"`, zodat een screenreader ze
  overslaat.
- Het menu markeert de sectie waar je bent met een randje. Sta je bovenaan in de
  hero, dan is er geen sectie gemarkeerd. Dat is opzet.
- Elke `<img>` heeft een `alt=` met een omschrijving.
- Het Portfolio-canvas heeft een verborgen tekstversie, zodat een screenreader
  weet wat er staat.
