# Projectgeschiedenis en overdracht

Dit document bestaat zodat je (of iemand anders) later kan achterhalen **waarom**
de site is zoals hij is. De `README.md` legt uit *hoe* je dingen aanpast; dit
bestand legt uit *waarom* het zo geworden is en welke dingen al geprobeerd en
afgekeurd zijn.

Gemaakt op 28 augustus 2026, in één werksessie, samen met Claude Code.

---

## 0. Als je op een nieuwe laptop begint

Je hebt niets bijzonders nodig. Geen installatie, geen frameworks.

```bash
git clone https://github.com/tejuko/2026Portfolio.git
cd 2026Portfolio
open index.html          # of dubbelklik het bestand
```

Wil je de scripts in `tools/` gebruiken, dan heb je Python nodig met drie pakketten:

```bash
pip install pillow numpy scikit-image
```

### Belangrijke waarschuwingen

- **De site staat op de GitHub-account `tejuko`.** Zeg je die account op, dan gaat
  https://tejuko.github.io/2026Portfolio/ offline. De code blijft bestaan zolang
  je een kopie hebt (een `git clone` is een volledige kopie, inclusief alle
  geschiedenis). Wil je de site behouden, verhuis de repo dan naar een account
  die blijft bestaan en zet GitHub Pages daar opnieuw aan.
- **De Adobe XD-links kunnen verdwijnen.** Twee projectknoppen ("Bekijk" bij
  Boekenzoeker en HEMA) wijzen naar prototypes op xd.adobe.com. Adobe bouwt XD af.
  Als die links ooit stoppen, staan de screenshots van die ontwerpen nog wel in
  `bronbestanden/projecten/`.
- **De Figma-link** waarop dit ontwerp is gebaseerd:
  https://www.figma.com/design/IBc1NhlmeDsNU4RWnDNnDC/Untitled?node-id=0-1
  Een afbeelding van dat ontwerp staat veilig in `bronbestanden/ontwerp/`, dus
  ook als het Figma-bestand verdwijnt weet je nog hoe het bedoeld was.
- **De oude portfolio** staat op https://github.com/tejuko/Portfolio_Tess_Kollof
  en is niet aangeraakt. De originele foto's daaruit zijn gekopieerd naar
  `bronbestanden/`, dus die repo is niet meer nodig.

---

## 1. Wat er in de repo staat

```
index.html                 de hele pagina + een inline SVG-sprite met alle iconen
styles.css                 alle vormgeving; kleuren staan bovenaan in :root
main.js                    hero-effect, menu, scroll-reveal, projectenrij
assets/img/                de beelden die de site gebruikt (jpg + webp)
assets/CV_Tess_Kollof.pdf  je cv

bronbestanden/             de ORIGINELEN, niet gebruikt door de site
  ontwerp/                 het Figma-ontwerp als afbeelding
  projecten/               screenshots van de echte prototypes en de live site
  iconen/                  de icoon-PNG's, bron voor de SVG's in index.html
  tess-*-origineel.*       je foto's op volledige resolutie

tools/                     scripts om de beelden en iconen opnieuw te maken
README.md                  hoe je dingen aanpast
PROJECT-GESCHIEDENIS.md    dit bestand
.nojekyll                  leeg bestandje dat GitHub Pages nodig heeft
```

`bronbestanden/` en `tools/` worden **niet** door de site gebruikt. Ze staan er
alleen zodat je later niets hoeft te reconstrueren.

---

## 2. Het uitgangspunt

- **Oude portfolio:** https://tejuko.github.io/Portfolio_Tess_Kollof/ — die vond
  je niet indrukwekkend genoeg.
- **Nieuw ontwerp:** gemaakt in Figma, roze verloop-hero, cream pagina, zachte
  roze kaarten. Zie `bronbestanden/ontwerp/`.
- **Extra wensen bovenop het ontwerp:** een cool effect in de hero, en schattige
  graphics en swirls rondom de pagina.

Uit het Figma-bestand kwamen exacte maten: frame 1440 breed, projectkaart 271×380
met een beeldvlak van 221×265, badge-pil 377×85 met een cirkel van 110, contactpil
434×48. Je kleurenpalet heet daar **"Rosé Garden"**: `#FE95A2`, `#EB5D70`,
`#B3D531`, `#407516`, `#B2E0EF`. De roze tinten in `styles.css` komen daaruit.

**Fonts:** Space Grotesk voor koppen, Manrope voor tekst. Beide van Google Fonts.
Het ontwerp gebruikte een pixelachtig lettertype voor de koppen; dat is opgelost
door het woordmerk in de hero écht uit blokjes op te bouwen in plaats van een
pixelfont te gebruiken.

---

## 3. Het hero-effect, en waarom het zo werkt

Het woord "Portfolio" is geen tekst maar een tekening op een `<canvas>`. In
`main.js`, functie `initWordmark()`:

1. Het woord wordt op een onzichtbaar canvas geschreven.
2. Daar gaat een raster over. Per vakje: zit hier letter, ja of nee?
3. Elk "ja" wordt een blokje met een kleur uit het roze verloop.
4. Bij het laden vliegen de blokjes van buiten het beeld naar hun plek.
5. Daarna duwt je muis ze weg, met een veer die ze terugtrekt.
6. Er schuift continu een **kleurgolf** door de letters.

### De kleurgolf is de belangrijkste vondst

Het lichte verloop (wit → `#DE4259`) is mooi maar slecht leesbaar: witte blokjes
op een licht-roze lucht. Er zijn veel dingen geprobeerd om dat op te lossen. Wat
uiteindelijk werkte was **jouw eigen idee**: de kleuren laten bewegen. Er reist
een golf door het verloop, waardoor elk deel van het woord om de paar seconden
diep genoeg van kleur is om te lezen — zonder dat het geheel donkerder wordt.

De golf is met opzet **asymmetrisch**: hij gaat veel verder naar dieper
(`SHIFT_UP = 0.46`) dan naar lichter (`SHIFT_DOWN = 0.06`). Daardoor wordt het
nooit slechter leesbaar dan in rust.

Voor de snelheid staat het verloop klaar als lijst van 64 kleuren. Per beeldje
wordt per blokje alleen een nummer opgezocht in die lijst, in plaats van elke
kleur opnieuw te berekenen.

### Niet meer proberen: dit is al afgekeurd

| Wat | Waarom afgekeurd |
|---|---|
| Verzadigd verloop (`#FE95A2` → bordeaux) | "ik mis de mooie gradient nu" |
| Bordeaux als eindkleur (`#C91E3C`) | "die donkerse roze kleur vind ik niet mooi" |
| S-curve op het verloop | zette te veel blokjes in de diepste tint, oogde donker |
| Fijner raster + gemiddelde bedekking per cel meten | "de kwaliteit is achteruitgegaan" |
| Kleinere ruimte tussen de blokjes + grotere tekst | idem, hoorde bij dezelfde poging |
| Een halo-schaduw om elk blokje | idem |
| Een gradient die de muis volgt over de hele pagina | "wel vet, maar hoeft niet" |

**Vaste waarden waar je niet aan moet zitten** tenzij je het bewust anders wil:
`COLOR_TOP` wit, `COLOR_BOT` `[222, 66, 89]`, raster `Math.round(W / 130)` met
16% ruimte ertussen, één meting in het midden van elk vakje, verloopkromme
`Math.pow(base, 0.78)`.

### Als je toch aan het raster gaat zitten

Bekijk het resultaat dan met animaties **uit**, anders kijk je naar een half
beeldje van de golf en lijken de letters kapot terwijl ze prima zijn. In Chrome:
DevTools → `Cmd+Shift+P` → typ "reduced motion" → "Emulate
prefers-reduced-motion".

---

## 4. De projectbeelden: het lastigste onderdeel

Er zijn **drie echte projecten**: Boekenzoeker, Bakje Plant en HEMA Cupcakes.
(`project-1.png` t/m `project-3.png` in de oude repo zijn stockplaatjes uit een
template, geen werk van jou. Niet gebruiken.)

Het probleem: de drie ontwerpen hebben totaal verschillende verhoudingen —
Boekenzoeker 4:3, HEMA 2:1, en Bakje Plant is een smalle mobiele pagina (0,46).
Geen enkel kader vult die alle drie zonder iets af te snijden of witruimte over
te houden.

Ook waren de oude PNG's in de vorige portfolio al **aan de zijkanten afgekapt**:
bij Boekenzoeker miste het Gemeente Amsterdam-logo en de helft van de kop, bij
HEMA het hele rode HEMA-logo. Daarom zijn er verse screenshots gemaakt van de
echte prototypes en de live site. Die staan in `bronbestanden/projecten/`.

### De werkende oplossing

Een vast **vierkant** beeldvlak met ronde hoeken. De liggende ontwerpen houden
hun volle breedte en worden boven en onder bijgevuld met de **mediaan-kleur van
de buitenste beeldrijen**. Dat is exact de achtergrondkleur van het ontwerp, dus
de vulling is onzichtbaar. Bakje Plant wordt vierkant vanaf de bovenkant gesneden.

Mediaan en niet gemiddelde, omdat er een logo in de hoek kan staan dat de kleur
anders vervuilt.

Opnieuw maken: `python3 tools/maak-projectbeelden.py`

### Ook hier al afgekeurd

| Wat | Waarom |
|---|---|
| `object-fit: contain` in een 4:5 kader | "te veel witte randen boven en onder" |
| Vierkant snijden zonder bijvullen | snijdt koppen en logo's af |
| De buitenste beeldrij uitrekken als vulling | die rij is niet egaal → strepen |
| Een gekleurd verloopvlak achter het beeld | "kan het niet net als bij mijn oude portfolio" |

---

## 5. De iconen

Je leverde ze zelf aan als PNG's van 512 px. Ze zijn omgezet naar SVG, omdat
PNG's op een scherm met hoge resolutie alsnog zacht worden. De hele set kost
samen ~9 kB en blijft scherp op elke zoom.

Belangrijk detail: de witte delen in die PNG's zijn **doorzichtig**, geen wit.
Daarom staat er `fill-rule="evenodd"` op elk pad — dan worden de binnenste
contouren als gat behandeld. De kleur komt via `currentColor`, dus je kunt hem
in CSS zetten.

Opnieuw maken: `python3 tools/maak-iconen.py`, daarna de `<symbol>`-blokken
overzetten naar `index.html`.

Waar ze staan: medaille bij Ervaring, baret bij Educatie, mail/LinkedIn/GitHub in
de contactpil, de dubbele chevron bij de scroll-hint onder de hero, de
vinkje-badge bij het label "Adobe XD prototype", en de GitHub-mark bij "Code op
GitHub".

---

## 6. Vormgevingsafspraken die zijn vastgelegd

- **Tekst op het roze verloop** is `--rose-deep` (`#D8465D`). Zowel het menu in
  ruststand als de tagline onder het woordmerk. Wit is daar onleesbaar, en het
  diepere `#A81E3C` is afgekeurd.
- **Vuistregel voor hovers:** opvallend mag, donker niet. Een subtiele
  kleurwissel is te onopvallend, maar een donkere of verzadigde vlak is te zwaar
  voor de zachte vibe. Wat werkt is de glaspil die verend opduikt.
- **Menu-hover:** een zachte glaspil duikt op, de tekst rolt omhoog naar een
  kopie in magenta, en er verschijnt een sparkle op de hoek. Wit-transparant op
  de roze hero, zacht roze op de cream balk.
- **Actieve sectie in het menu:** dezelfde tekstkleur als de rest, met een fijn
  randje. Sta je bovenaan in de hero, dan is er niets gemarkeerd — dat is opzet.
  Een afwijkende kleur voor de actieve link is afgekeurd.
- **Knoppen:** diagonaal verloop, lichtrand bovenop, een glans die bij hover in
  een schuine baan overheen glijdt, en een verende lift. Géén extra ring of
  border bij hover (afgekeurd). De tweede knop is glas.
- **De skillbalk** moet van rand tot rand doorlopen en over de hero uitsteken.
  Dus geen randmasker en ruim breder dan het venster, zodat de schuine uiteinden
  buiten beeld vallen.
- **Het hoi!-label** blijft de simpele magenta pil. Een cream ring eromheen is
  afgekeurd. Het label staat op `rotate: 0deg` omdat de foto eronder al schuin
  staat; dubbel roteren maakt tekst wazig.

---

## 7. Technische valkuilen die al een keer misgingen

Deze staan hier zodat je ze niet opnieuw hoeft te ontdekken.

**Gloeden en verlopen mogen nooit hard aflopen op een rand.**
Gebruik `radial-gradient(closest-side, ...)` met een laatste kleurstop op `100%`.
Zet je daar een percentage in dat groter is dan de afstand tot de rand, dan zie
je een rechthoek op de pagina. Dit ging twee keer mis: bij de kleurwolk achter de
badges, en bij de gloed rondom Contact.

**Een gloed moet in zijn eigen doos passen, of het gedeelte moet hem laten
doorlopen.** Bij Contact was de gloed 1478 px hoog in een gedeelte van 449 px met
`overflow: hidden` — die werd recht afgekapt. Nu staat er
`overflow-x: clip; overflow-y: visible` en staat de gloed op `z-index: -1`, zodat
hij achter de omliggende inhoud doorloopt.

**En dan gaat het aan de andere kant mis.** Zodra de gloed mag doorlopen, loopt hij
ook voorbij het einde van de pagina — onder Contact zit alleen de footer, zo'n
80 px. Gemeten reikte hij 130 tot 235 px voorbij het documenteinde, afhankelijk
van de schermbreedte, en daar werd hij weer recht afgekapt. Oplossing: het
middelpunt op `top: 38%` in plaats van 50% en de hoogte terug naar `130%`. De
overloop gaat nu naar boven, waar het projectengedeelte zit, en aan de onderkant
is de gloed uitgefade met 66 tot 101 px marge. Nagemeten op 320, 390, 768, 1440
en 1907 px breed.

Wil je hier iets veranderen, meet dan of de onderkant nog binnen de pagina valt.
Je kunt dat controleren door in de browserconsole te kijken of
`contactTop + sectieHoogte * 0.38 + gloedHoogte / 2` kleiner is dan
`document.documentElement.scrollHeight`.

**`overflow-x: clip` met `overflow-y: visible`** is de truc voor de gekantelde
skillbalk. Zonder die combinatie wordt de pagina breder dan het venster.

**Een menu dat de actieve sectie markeert moet ook het verlaten opvangen.**
Reageer je alleen op binnenkomst, dan blijft de laatste markering staan als je
terugscrollt naar boven. En onderaan de pagina past het laatste gedeelte niet
meer in het meetvenster, dus daar is een aparte controle op "bijna beneden" nodig.

**Draai tekst niet twee keer.** Het hoi!-label stond op 8 graden binnen een foto
die al schuin stond. Twee rotaties samen laten elke letter tussen de pixels
vallen en dat ziet wazig uit.

**Adobe XD-prototypes hebben WebGL nodig.** Krijg je "There was a problem
displaying this prototype", dan is de link niet stuk.

**Bakje Plant screenshotten kan alleen op telefoonformaat.** Op een breed venster
rekt de site uit.

**Screenshots maken van een gescrollde pagina:** een uitsnede rekent in
documentcoördinaten, niet in venstercöordinaten. Op een gescrollde pagina valt de
uitsnede dan naast de vastgezette menubalk en lijkt die leeg. Dat is geen bug.

---

## 8. Wat er is getest

Bij elke wijziging is nagekeken op **320, 390, 768, 1440 en 1920 px** breed:
geen horizontale overloop, geen JavaScript-fouten, geen mislukte bestanden, geen
gebroken beelden. Ook is elke keer de versie met "minder beweging" gecontroleerd.

De navigatie is getest op 1280, 1440 en 1907 px: bovenaan niets gemarkeerd, dan
Ervaring, Projecten, Contact, en weer niets bij terugscrollen.

---

## 9. Ideeën die nog openstaan

Niets hiervan is nodig, het zijn losse gedachten:

- De projectkaarten hebben nu allemaal dezelfde opbouw. Een uitgebreidere
  casepagina per project (proces, keuzes, resultaat) zou het portfolio sterker
  maken dan alleen een screenshot en een link.
- Er staat nu een vierde kaart met "de rest staat op GitHub". Zodra je meer
  projecten hebt, kan die eruit.
- De skillbalk noemt Adobe XD. Als je daarvan afstapt, is dat een van de eerste
  dingen om te vervangen.
- De site is nu Nederlands. De oude portfolio had een taalwissel (NL/EN); die is
  niet meegenomen.

---

## 10. Commitgeschiedenis

De volgorde waarin het is gebouwd. Elke commit heeft een uitgebreide beschrijving
met de reden erachter; `git log` laat die zien.

| Commit | Wat |
|---|---|
| `8bf08c0` | Eerste, lege commit met alleen een README |
| `a11bba2` | Het hele portfolio: pixelhero, projectenrij, swirls |
| `f614b19` | Hero leesbaarder, banner van rand tot rand, betere projectbeelden |
| `2551d05` | Lichte gradient terug in de hero, leesbaar menu met rollende hover |
| `6fc7f01` | Woordmerk terug naar het roze van de eerste versie |
| `4f19fdc` | Menu-hover in de stijl van de site: zachte glaspil met sparkle |
| `65ad5eb` | Eigen iconen, glasbadges, menukleur gelijk aan de tagline |
| `1586c98` | Actieve menulink met randje, fancy knoppen, glaskaarten |
| `82d64ff` | Kleurgolf in de hero, drie dingen teruggedraaid, README voor beginners |
| `a0ba737` | Golf duidelijker, geen actieve markering in de hero, hoi-label scherp |
| `a4d5159` | Contactgloed loopt over, gelijke labelkleuren, menu springt op Contact |

Wil je zien wat er precies in een commit is veranderd:

```bash
git show a4d5159
```

Wil je terug naar een oudere versie van één bestand:

```bash
git checkout 6fc7f01 -- main.js
```
