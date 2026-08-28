# Portfolio — Tess Kollof (2026)

Persoonlijk portfolio. Statische site, geen build-stap: HTML + CSS + vanilla JS.

**Live:** https://tejuko.github.io/2026Portfolio/

## Bestanden

| Bestand      | Wat het doet |
|--------------|--------------|
| `index.html` | De hele pagina + een inline SVG-sprite met alle iconen en swirls |
| `styles.css` | Alle styling. Kleuren staan bovenaan als CSS-variabelen in `:root` |
| `main.js`    | Hero-effect, navigatie, scroll-reveal, parallax, projectenrail |
| `assets/img` | Foto's en projectbeelden (jpg + webp) |

## Projectbeelden

De thumbnails zijn verse screenshots van de echte prototypes en de live site
(niet de oude, aan de zijkanten afgekapte PNG's). Elk beeld staat compleet en op
ware verhouding op een vlak in een kleur uit het project zelf, zodat het
vierkante kader helemaal gevuld is zonder dat er iets wordt afgesneden.

Let op bij het opnieuw maken: Adobe XD-prototypes hebben **WebGL** nodig. In een
headless browser lukt dat alleen met `--enable-unsafe-swiftshader --use-gl=angle
--use-angle=swiftshader`; zonder die vlaggen krijg je "There was a problem
displaying this prototype".

## Hero-effect

`Portfolio` is geen tekst maar een canvas. `main.js` zet het woord op een
onzichtbaar canvas, leest per rastercel uit of daar letter zit en maakt van elke
cel een blokje met een eigen kleur uit het roze verloop. De blokjes vliegen bij
het laden naar hun plek en worden daarna weggedrukt door je muis, met een veer
die ze terugtrekt.

## Zelf aanpassen

- **Kleuren** → `:root` bovenaan `styles.css`
- **Projecten** → de `<li class="card">`-blokken in `index.html`
- **Skills in de lopende balk** → de twee `.marquee__group`-blokken (houd ze identiek, anders hapert de loop)
- **Swirls verplaatsen** → de `.deco--*`-regels in `styles.css` (`top`/`left`/`width`)
- **Nieuwe foto** → zet hem in `assets/img/` en pas het `<picture>`-blok aan

## Toegankelijkheid

Alle animaties staan uit bij `prefers-reduced-motion: reduce`. Decoratieve SVG's
zijn `aria-hidden`, de pixelhero heeft een tekstalternatief.
