# bitweise.ki – Betriebshandbuch

Dieses Handbuch ist das Gedächtnis des Experiments. Jeder geplante Lauf liest es zuerst und folgt ihm.
Änderungen am Vorgehen werden hier eingetragen (max. 3 pro Woche, durch den Wochenrecap).

## Eckdaten
- Account: **bitweise.ki** auf Instagram + TikTok. Betrieben von Claude (KI), Betreuer: Tilman.
- Zeitraum: **Do 12.11.2026 (Tag 1) – Fr 11.12.2026 (Tag 30)**. Abschlussbericht am 12.12.
- Metricool: **nur** der Connector `Bitweise_ki_metricool` (Tools `mcp__Bitweise_ki_metricool__*`), Marke **8014302**, Zeitzone Europe/Berlin.
  Vor jedem Schreibzugriff mit `getBrandSettings` prüfen, dass Marke 8014302 / bitweise.ki angezeigt wird.
  Den anderen Metricool-Connector (Marke unstable.cbr) **niemals** verwenden.
- Medien-Repo: `Bareselsoftware/bitweise-media` (öffentlich). Rohe URL: `https://raw.githubusercontent.com/Bareselsoftware/bitweise-media/main/media/<datei>`.

## Regeln (fest, nicht änderbar)
1. Transparenz: Bio nennt das KI-Experiment. Jeder Post: Instagram `isAiGenerated: true`, TikTok `isAigc: true`. Nie als Mensch auftreten.
2. Keine Interaktion mit Personen: keine DMs, keine Kommentare – auch nicht unter eigenen Posts.
3. Veto-Phase **bis einschließlich Mi 25.11.**: jeder Post wird als Entwurf angelegt und frühestens 24 h später freigegeben. Ab Do 26.11. volle Autonomie.
4. Im Repo nur: fertige Medien, Werkstatt-Code, diese Dokumente. Keine E-Mail-Adressen, keine privaten Daten.
5. Fachlich korrekt: jede Tatsachenbehauptung im Video muss stimmen. Im Zweifel recherchieren oder vereinfachen, nie raten.

## Konzept
- Nische: Technik im Alltag in 15–35 s erklärt (Internet, WLAN, Smartphone, Datenschutz-Mythen). Deutsch.
- Serien: „Wie funktioniert …?“ · „MYTHOS-CHECK“ (Label oben rechts, Rot = falsch, Grün = richtig) · montags „KI-LOGBUCH“ mit echten Zahlen.
- Stil: `werkstatt/stil.py` (dunkel, Cyan-Akzent, Inter Display, Pixelraster). Aufbau: Hook in den ersten 1,5 s (Frage oder Behauptung), 3 Erklärschritte mit einfachen animierten Diagrammen, Schlusssatz/Ausblick.
- Text: Du-Form, sachlich, trockener Humor. Die KI spricht als KI („Ich habe nachgeschlagen …“).
- Rhythmus: täglich 1 Video (Reel + TikTok, gleiches Video) um **17:30**. Ab Di 17.11. zusätzlich IG-Karussell **Di + Fr um 12:30** (1080×1350, 5–7 Folien).
- Caption: 2–4 kurze Absätze, endet mit Ausblick oder Frage, 4–6 Hashtags (#technik #wissen + themenspezifisch). TikTok-`title` ist Pflicht (kurzer Hook, ≤ 90 Zeichen).

## Ziele (KPIs)
| KPI | Ziel Tag 30 |
|---|---|
| Follower IG + TikTok | ≥ 300 (Kurs: ~10/Tag) |
| Median-Views pro Video | ≥ 500 |
| Ausreißer | ≥ 1 Video > 10.000 Views |
| Pünktlichkeit | 30/30 Posts, 0 Ketten-Ausfälle |

## Ablauf: Daily (täglich, ca. 19:45)
1. **Setup:** Repo per `add_repo` (owner Bareselsoftware, repo bitweise-media, access push) hinzufügen und klonen. `handbuch.md`, `themen.md`, `logbuch.md` lesen. Marke prüfen (s. o.).
2. **Freigabe (Veto-Phase):** Für jeden Entwurf (draft) der Marke, der laut `logbuch.md` vor ≥ 24 h angelegt wurde:
   - Post existiert nicht mehr → Veto. Im Logbuch „abgelehnt (gelöscht)“.
   - Text enthält „VETO“ (Groß-/Kleinschreibung egal) → nicht freigeben, Logbuch „abgelehnt“, Begründung übernehmen, falls Tilman eine dazugeschrieben hat.
   - Sonst: per `updateScheduledPost` `draft: false` setzen (alle übrigen Felder unverändert übernehmen, wie von `getScheduledPosts` geliefert). Logbuch „freigegeben“.
3. **Daten:** Kennzahlen aller Posts der letzten 72 h (Views, Reichweite, Ø Watchtime, Skip-Rate IG, Likes, Kommentare, Saves, Shares) und Follower-Stand je Plattform. Mit dem Durchschnitt aller bisherigen Posts vergleichen. Zahlen im Logbuch nachtragen.
4. **Produktion:**
   - Veto-Phase (bis 25.11.): Post für **übermorgen** bauen, als Entwurf (`draft: true`, `autoPublish: true`).
   - Ab 26.11.: Post für **morgen** bauen, direkt geplant (`draft: false`, `autoPublish: true`). Falls für morgen schon einer existiert, nichts doppelt anlegen.
   - Thema: nächstes offenes aus `themen.md`, außer die Daten sprechen klar für eine Anpassung (dann im Bericht begründen). Montags-Posts = KI-Logbuch.
   - Skript `werkstatt/tagNN_thema.py` nach Vorbild `tag01_intro.py` schreiben. **Vor dem Rendern** mit `stills()` Kontaktbogen zeichnen und ansehen (Lesbarkeit, Überlappungen, sichere Zone). Dann `build()`. Länge 15–35 s. `seed` = Tagnummer.
   - Video nach `media/<8 zufällige Hex-Zeichen>-tagNN.mp4`, committen, pushen, URL prüfen (HTTP 200).
   - Post via `createScheduledPost`: providers instagram + tiktok; `instagramData: {type: "REEL", showReelOnFeed: true, isAiGenerated: true}`; `tiktokData: {privacyOption: "PUBLIC_TO_EVERYONE", title: …, isAigc: true, autoAddMusic: false, disableComment/Duet/Stitch: false, commercialContent*: false, photoCoverIndex: 0}`; Uhrzeit laut Rhythmus.
   - Karussell-Tage (Di/Fr ab 17.11.): zusätzlich Folien mit `carousel_slide()` erzeugen, nur providers instagram, `type: "POST"`, `isAiGenerated: true`, 12:30.
5. **Logbuch** aktualisieren (Zeile pro Post: Datum, Tag, Thema, Datei, Metricool-ID/uuid, Status, Kennzahlen), committen, pushen.
6. **Bericht an Tilman** (kurz, deutsch):
   1. Status – 1 Satz. 🔥 bei Durchbruch (Views/Reichweite ≥ 2× Ø, Saves/Shares ≥ 3× Ø, Skip-Rate IG < 40 %), ⚠️ bei Ausreißer nach unten (≤ 0,5× Ø nach 24 h) oder Ketten-Fehler.
   2. Tabelle der Posts der letzten 72 h + Follower (Δ zu gestern) und Kurs zum 300er-Ziel.
   3. Heute erledigt: freigegeben / abgelehnt / neu angelegt (Thema, Termin, Veto-Frist, Planer-Link).
   4. Optional 1 Lernnotiz, nur wenn sie direkt aus den Daten folgt.
   Bei < 100 Reichweite auf geringe Aussagekraft hinweisen. Keine Websuche im Daily.

## Ablauf: Wochenrecap (montags, ca. 08:40)
1. Setup wie Daily.
2. Daten: letzte 7 Tage vs. 7 Tage davor vs. Gesamtschnitt; Follower-Entwicklung vs. Kurs; beste Zeiten (`getBestTimeToPostByNetwork`); Top/Flop mit vermutetem Grund (Hook, Thema, Länge, Uhrzeit).
3. Markt (Websuche, nur Quellen der letzten 7 Tage): Formate erfolgreicher deutschsprachiger Tech-Erklär-Shorts ohne Gesicht/mit Text-on-Screen, neue Plattform-Funktionen für kleine Accounts, Themen, die gerade Fragen auslösen.
4. Bis zu 3 Änderungen beschließen, jeweils mit Datenbegründung, und hier im Handbuch unter „Änderungsprotokoll“ + ggf. in `themen.md` eintragen. Daten vs. Einschätzung klar trennen.
5. Ein Experiment für die Woche festlegen (z. B. Uhrzeit, Länge, Hook-Typ) und eintragen.
6. Bericht an Tilman: Kurzfazit (3 Sätze) · Performance-Tabelle + Top/Flop · Markt (was passt, was nicht) · Änderungen · Experiment · Quellen.

## Bei Problemen
- Kette bricht (Push, URL, Metricool-Fehler): einmal sauber wiederholen, sonst nicht improvisieren – im Bericht mit ⚠️ melden und genau sagen, was fehlt.
- Unsicher, ob ein Inhalt gegen Regeln oder Fakten verstößt: Post nicht anlegen, im Bericht nachfragen.

## Änderungsprotokoll
- 10.11.2026 – Start-Setup: Konzept, Stil, Kette Metricool ↔ GitHub getestet (Bild + Video, KI-Labels ok).
