# Verse screenshots van de prototypes maken

De bestanden in `bronbestanden/projecten/` zijn screenshots van de echte
prototypes en de live site. Wil je ze opnieuw maken (bijvoorbeeld omdat je een
ontwerp hebt bijgewerkt), dan gaat dat zo.

## Boekenzoeker en HEMA Cupcakes (Adobe XD)

- Boekenzoeker: https://xd.adobe.com/view/ed07539b-f12a-4488-a52a-48838edb302f-b854/?fullscreen&hints=off
- HEMA Cupcakes: https://xd.adobe.com/view/0b43d6d1-0e2c-48b5-a184-23f760993929-5e10/?fullscreen&hints=off

Open ze in een gewone browser en maak een schermafbeelding. Snij daarna de
witte ruimte om het artboard weg, zodat alleen het ontwerp overblijft.

**Let op:** XD-prototypes hebben **WebGL** nodig. Zie je "There was a problem
displaying this prototype", dan is je link niet stuk maar staat WebGL uit
(of je gebruikt een browser zonder grafische versnelling).

## Bakje Plant (live site)

https://tejuko.github.io/BakjePlant/index.html

Dit is een **mobiele** site. Screenshot hem op telefoonformaat (in Chrome:
DevTools openen met `F12`, dan het telefoon-icoontje, en kies iPhone). Op een
breed venster rekt de site uit en ziet het er verkeerd uit.

## Daarna

Zet de nieuwe bestanden in `bronbestanden/projecten/` onder dezelfde namen en
draai:

```bash
python3 tools/maak-projectbeelden.py
```
