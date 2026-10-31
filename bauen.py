"""Baut die öffentliche Quellenseite des Kanals (GitHub Pages, ErikFink/buddha-und-psychologie).

Eingabe: quellen.json, ein Eintrag pro Beitrag (neuester zuerst angezeigt): Frage, Lehrtexte mit
Fundstelle und Link, Studien mit Angabe, Kurzbeschreibung und DOI-Link, Bildnachweis; für Hinweise
auf Podcastfolgen statt Lehrtexten und Studien der Abschnitt „anhoeren“ (Titel, Link, Kurzbeschreibung).
Ausgabe: index.html und profilbild.png in diesem Ordner, der zugleich das Git-Repository ist.

Nach jedem neuen Beitrag: Eintrag in quellen.json ergänzen, dieses Skript laufen lassen, committen
und pushen (`git -C Instagram\\quellenseite push`).
Aufruf: .venv\\Scripts\\python.exe Instagram\\quellenseite\\bauen.py
"""

import html
import json
from pathlib import Path

from PIL import Image

HIER = Path(__file__).parent
PROFILBILD = HIER.parent / "profilbild" / "final" / "profilbild.png"

KOPF = """<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Buddha &amp; Psychologie · Quellen</title>
<meta name="description" content="Lehrtexte und Studien zu den Beiträgen von @buddha.und.psychologie">
<style>
  :root { --lapis: #1e2a78; --tief: #172061; --gold: #dab060; --hell: #f6efe2; --leise: #c9c3d9; }
  * { box-sizing: border-box; }
  body { margin: 0; background: var(--lapis); color: var(--hell); font: 16px/1.55 Georgia, "Times New Roman", serif; }
  main { max-width: 680px; margin: 0 auto; padding: 32px 16px 56px; }
  header { text-align: center; margin-bottom: 28px; }
  header img { width: 112px; height: 112px; border-radius: 50%; display: block; margin: 0 auto 14px; }
  h1 { font-weight: 400; font-size: 26px; margin: 0; color: var(--gold); }
  .unter { color: var(--leise); margin: 6px 0 0; font-size: 15px; }
  article { background: var(--tief); border-radius: 14px; padding: 18px 18px 14px; margin-top: 16px; }
  h2 { font-weight: 400; font-size: 21px; margin: 0 0 2px; color: var(--gold); }
  .datum { color: var(--leise); font-size: 13px; margin: 0 0 12px; font-family: -apple-system, "Segoe UI", Arial, sans-serif; }
  h3 { font-size: 13px; letter-spacing: .06em; text-transform: uppercase; color: var(--leise); margin: 14px 0 6px;
       font-family: -apple-system, "Segoe UI", Arial, sans-serif; font-weight: 600; }
  ul { list-style: none; padding: 0; margin: 0; }
  li { margin: 0 0 10px; }
  a { color: var(--hell); text-decoration-color: var(--gold); text-underline-offset: 3px; }
  .was { color: var(--leise); font-size: 14px; display: block; }
  .bilder { color: var(--leise); font-size: 13px; margin-top: 10px; }
  footer { color: var(--leise); font-size: 13px; text-align: center; margin-top: 32px; }
</style>
</head>
<body>
<main>
<header>
  <img src="profilbild.png" alt="Profilbild Buddha &amp; Psychologie">
  <h1>Buddha &amp; Psychologie</h1>
  <p class="unter">Lehrtexte und Studien zu jedem Beitrag</p>
</header>
"""

FUSS = """<footer>@buddha.und.psychologie · Dr. sc. med. Erik Fink</footer>
</main>
</body>
</html>
"""


def e(t):
    return html.escape(t, quote=True)


def eintrag(b):
    teile = [f'<article>\n  <h2>{e(b["frage"])}</h2>\n  <p class="datum">{e(b["datum"])}</p>']
    if b.get("lehrtexte"):
        teile.append("  <h3>Lehrtexte</h3>\n  <ul>")
        for t in b["lehrtexte"]:
            teile.append(f'    <li><a href="{e(t["link"])}">{e(t["wer"])}, {e(t["titel"])}</a>'
                         f'<span class="was">{e(t["fundstelle"])} · {e(t["uebersetzung"])}</span></li>')
        teile.append("  </ul>")
    if b.get("studien"):
        teile.append("  <h3>Studien</h3>\n  <ul>")
        for s in b["studien"]:
            teile.append(f'    <li><a href="{e(s["link"])}">{e(s["angabe"])}</a><span class="was">{e(s["was"])}</span></li>')
        teile.append("  </ul>")
    if b.get("anhoeren"):   # Beiträge ohne Lehrtext, etwa ein Hinweis auf eine Podcastfolge
        teile.append("  <h3>Zum Anhören</h3>\n  <ul>")
        for a in b["anhoeren"]:
            teile.append(f'    <li><a href="{e(a["link"])}">{e(a["titel"])}</a><span class="was">{e(a["was"])}</span></li>')
        teile.append("  </ul>")
    if b.get("bilder"):
        teile.append(f'  <p class="bilder">Bilder: {e(b["bilder"])}</p>')
    teile.append("</article>")
    return "\n".join(teile)


def main():
    beitraege = json.loads((HIER / "quellen.json").read_text(encoding="utf-8"))
    beitraege.sort(key=lambda b: b["datum"], reverse=True)
    seite = KOPF + "\n".join(eintrag(b) for b in beitraege) + "\n" + FUSS
    (HIER / "index.html").write_text(seite, encoding="utf-8")
    Image.open(PROFILBILD).convert("RGB").resize((240, 240), Image.LANCZOS).save(HIER / "profilbild.png")
    print("fertig:", len(beitraege), "Beiträge")


if __name__ == "__main__":
    main()
