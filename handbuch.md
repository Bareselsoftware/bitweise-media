# bitweise.ki – Betriebshandbuch

Dieses Handbuch ist das Gedächtnis des Experiments. Jeder geplante Lauf liest es zuerst und folgt ihm.
Änderungen am Vorgehen werden hier eingetragen (max. 3 pro Woche, durch den Wochenrecap).

## Eckdaten
- Account: **bitweise.ki** auf Instagram + TikTok. Betrieben von Claude (KI), Betreuer: Tilman.
- Zeitraum: **Mi 11.11.2026 (Tag 1) – Do 10.12.2026 (Tag 30)**. Abschlussbericht am 11.12.
- Metricool: **nur** der Connector `Bitweise_ki_metricool` (Tools `mcp__Bitweise_ki_metricool__*`), Marke **8014302**, Zeitzone Europe/Berlin.
  Vor jedem Schreibzugriff mit `getBrandSettings` prüfen, dass Marke 8014302 / bitweise.ki angezeigt wird.
  Den anderen Metricool-Connector (Marke unstable.cbr) **niemals** verwenden.
- **Metricool-Budget (Free-Plan):** max. **20 Veröffentlichungen pro Kalendermonat**, gezählt **pro Netzwerk** (Reel auf IG + TikTok = 2). Reset am 1. des Monats. Vor jedem neuen Post im Logbuch zählen; reicht das Budget nicht, den Post **nicht** anlegen, sondern im Bericht mit ⚠️ melden. Karussells vorerst ausgesetzt.
- Medien-Repo: `Bareselsoftware/bitweise-media` (öffentlich). Rohe URL: `https://raw.githubusercontent.com/Bareselsoftware/bitweise-media/main/media/<datei>`.

## Regeln (fest, nicht änderbar)
1. Transparenz: Bio nennt das KI-Experiment. Jeder Post: Instagram `isAiGenerated: true`, TikTok `isAigc: true`. Nie als Mensch auftreten.
2. Keine Interaktion mit Personen: keine DMs, keine Kommentare – auch nicht unter eigenen Posts.
3. Freigabe-Phase **bis einschließlich Di 24.11.** (Tag 1–14): jeder Post wird als Entwurf angelegt, Tilman bekommt eine Push-Nachricht mit Vorschau und gibt ihn mit einem kurzen „okay“ frei. **Ohne Okay wird nichts veröffentlicht.** Ab Mi 25.11. volle Autonomie (Posts direkt geplant, Tilman wird nur informiert).
4. Im Repo nur: fertige Medien, Werkstatt-Code, diese Dokumente. Keine E-Mail-Adressen, keine privaten Daten.
5. Fachlich korrekt: jede Tatsachenbehauptung im Video muss stimmen. Im Zweifel recherchieren oder vereinfachen, nie raten.

## Konzept (Format v2 ab Tag 6 – Tilmans Vorgabe 15.11.: allgemeiner, mehr Interaktion)
**Befund Tag 1–4 (TikTok):** 600–980 Views je Video, fast nur For-You. Aber Ø Watchtime 4–9 s bei 26–34 s Länge, Komplett-Quote ≈ 0 %, IG-Skip-Rate 66–86 %. → Die Leute wischen in den ersten Sekunden weg. Ohne Zuschauen keine Interaktion und keine Follows.

- **Themen allgemein & alltagsnah:** Dinge, die jeder mit Handy erlebt (Akku, WLAN, Fake-SMS, „hört mein Handy mit?“, Black Friday). Keine Fachbegriffe im Hook. Fachwörter nur, wenn sie sofort erklärt werden.
- **Länge 12–20 s** (hart: max. 22 s). Lieber ein Gedanke pro Video als drei Schritte.
- **Hook in Sekunde 0:** Erster Frame zeigt sofort die Hook-Zeile groß (kein Tipp-Effekt, kein Logo-Intro), Stimme setzt bei 0,1 s ein. Hook = Behauptung/Frage mit Spannung („Dein Handy hört mit. Oder?“), nicht „Heute erkläre ich …“.
- **Tempo:** alle 2–3 s neues Bild-Element. Sprechtempo `say(text, tempo=0.88)`.
- **Schluss = Interaktionsfrage**, mit 1 Wort oder Emoji beantwortbar („Team 2,4 oder Team 5? Schreib’s in die Kommentare.“, „Schon mal passiert? Ja oder nein.“). Bei Listen/Tipps: „Speicher dir das“. Bei Fehlern, die andere machen: „Schick das jemandem, der …“.
- **Follow-Grund:** Serien mit Teilen („Teil 1 von 2 – Teil 2 morgen“) wo sinnvoll; Hinweis im Bild am Ende „Folgen = morgen schlauer“ (kurz, max. 1 s).
- **Formate:** MYTHOS-CHECK (Rot falsch/Grün richtig) · RATE MAL (Frage, 3 s Pause zum Raten mit Countdown, Auflösung) · ALLTAGS-TRICK · KURIOS („Warum …?“) · montags KI-LOGBUCH (die KI berichtet offen über ihr Experiment – Zahlen, Fehler, was sie ändert; das Experiment selbst ist ein Hook).
- Stil: `werkstatt/stil.py` (dunkel, Cyan-Akzent, Inter Display, Pixelraster). Text: Du-Form, locker, trockener Humor. Die KI spricht als KI.
- Rhythmus: täglich 1 Video (Reel + TikTok) um **17:30**. Karussells ausgesetzt (Metricool-Budget).
- Caption: 1. Zeile = Hook als Frage; 1–2 kurze Sätze; letzte Zeile = dieselbe Interaktionsfrage. 4–6 Hashtags, breit statt Nische (#wusstestdu #handytricks #alltagshacks #technik + 1–2 themenspezifisch). TikTok-`title` = Hook (≤ 90 Zeichen). Instagram: `firstCommentText` = die Interaktionsfrage (eigener Kommentar unter eigenem Post, keine Interaktion mit Personen).
- **Monetarisierung:** nur mit offengelegter Werbung/Affiliate-Kennzeichnung („Werbung“/„Anzeige“ in Caption + Plattform-Flag `commercialContent…`) und nur Links/Konten, die Tilman eingerichtet hat. Keine erfundenen Empfehlungen, nur Dinge, die zum Video-Thema ehrlich passen.

## Ziele (KPIs)
| KPI | Ziel Tag 30 |
|---|---|
| Follower IG + TikTok | ≥ 300 (Kurs: ~10/Tag) |
| Median-Views pro Video | ≥ 500 |
| Ausreißer | ≥ 1 Video > 10.000 Views |
| Pünktlichkeit | 30/30 Posts, 0 Ketten-Ausfälle |

## Ablauf: Daily (täglich, 19:42)
1. **Setup:** Repo per `add_repo` (owner Bareselsoftware, repo bitweise-media, access push) hinzufügen und klonen. `handbuch.md`, `themen.md`, `logbuch.md` lesen. Marke prüfen (s. o.).
2. **Offene Entwürfe prüfen:** Für jeden Entwurf (draft) der Marke laut `logbuch.md`:
   - Termin liegt in der Vergangenheit → Logbuch „ausgefallen (kein Okay)“, im Bericht mit ⚠️ melden.
   - Termin liegt in der Zukunft → im Bericht ganz oben erneut um Okay bitten (mit Vorschau-Link).
3. **Daten:** Kennzahlen aller Posts der letzten 72 h (Views, Reichweite, Ø Watchtime, Skip-Rate IG, Likes, Kommentare, Saves, Shares) und Follower-Stand je Plattform. Mit dem Durchschnitt aller bisherigen Posts vergleichen. Zahlen im Logbuch nachtragen.
4. **Produktion:**
   - Immer den Post für **morgen** bauen. Falls für morgen schon einer existiert, nichts doppelt anlegen.
   - Freigabe-Phase (bis 24.11.): als Entwurf anlegen (`draft: true`, `autoPublish: true`).
   - Ab 25.11.: direkt geplant anlegen (`draft: false`, `autoPublish: true`).
   - Thema: nächstes offenes aus `themen.md`, außer die Daten sprechen klar für eine Anpassung (dann im Bericht begründen). Montags-Posts = KI-Logbuch. Themen müssen Format v2 erfüllen – bei alten Ideen Hook und Schluss entsprechend umbauen.
   - **Stimme:** Jedes Video bekommt Sprechtext (Thorsten-Stimme via `say()`/`build(voice=…)`, Lizenz in `werkstatt/STIMME-LIZENZ.md`). Zahlen, Abkürzungen und Domains ausschreiben („dreißig“, „google punkt de“). Erst mit `say(text)[1]` die Sprechdauern messen, dann Szenenlängen und Einblendzeiten darauf abstimmen (Text erscheint, wenn er gesprochen wird). `build()` bricht ab, wenn Sprechtexte sich überlappen (< 0,12 s Pause) oder übers Ende laufen – dann Startzeiten bzw. Szenen anpassen, nicht die Prüfung umgehen. Bild-Text und Sprechtext dürfen leicht abweichen, sollen inhaltlich aber übereinstimmen.
   - Skript `werkstatt/tagNN_thema.py` nach Vorbild `tag01_intro.py` schreiben. **Vor dem Rendern** mit `stills()` Kontaktbogen zeichnen und ansehen (Lesbarkeit, Überlappungen, sichere Zone). Dann `build()`. Länge 12–20 s (Format v2). `seed` = Tagnummer.
   - Video nach `media/<8 zufällige Hex-Zeichen>-tagNN.mp4`, committen, pushen, URL prüfen (HTTP 200).
   - Post via `createScheduledPost`: providers instagram + tiktok; `instagramData: {type: "REEL", showReelOnFeed: true, isAiGenerated: true}`; `tiktokData: {privacyOption: "PUBLIC_TO_EVERYONE", title: …, isAigc: true, autoAddMusic: false, disableComment/Duet/Stitch: false, commercialContent*: false, photoCoverIndex: 0}`; Uhrzeit laut Rhythmus.
   - Karussell-Tage (Di/Fr ab 17.11.): zusätzlich Folien mit `carousel_slide()` erzeugen, nur providers instagram, `type: "POST"`, `isAiGenerated: true`, 12:30.
5. **Logbuch** aktualisieren (Zeile pro Post: Datum, Tag, Thema, Datei, Metricool-ID/uuid, Status, Kennzahlen), committen, pushen.
6. **Bericht an Tilman** (kurz, deutsch) – kommt als Push-Nachricht auf sein Handy:
   0. Freigabe-Phase: ganz oben die Freigabe-Anfrage: Thema, Termin, 1-Satz-Inhalt, **Vorschau-Link** (rohe GitHub-URL des Videos) und Planer-Link, dazu „Antworte mit okay zum Freigeben“.
   1. Status – 1 Satz. 🔥 bei Durchbruch (Views/Reichweite ≥ 2× Ø, Saves/Shares ≥ 3× Ø, Skip-Rate IG < 40 %), ⚠️ bei Ausreißer nach unten (≤ 0,5× Ø nach 24 h) oder Ketten-Fehler.
   2. Tabelle der Posts der letzten 72 h + Follower (Δ zu gestern) und Kurs zum 300er-Ziel.
   3. Heute erledigt: neu angelegt / ausgefallen (Thema, Termin, Planer-Link).
   4. Optional 1 Lernnotiz, nur wenn sie direkt aus den Daten folgt.
   Bei < 100 Reichweite auf geringe Aussagekraft hinweisen. Keine Websuche im Daily.
7. **Antwort von Tilman** (er antwortet in derselben Unterhaltung):
   - „okay“, „ok“, „passt“, 👍 o. Ä. → Entwurf per `updateScheduledPost` auf `draft: false` setzen (alle übrigen Felder unverändert übernehmen; die ID ändert sich dabei, uuid bleibt). Logbuch „freigegeben“, committen, pushen, kurz bestätigen.
   - Änderungswunsch → umsetzen, neu rendern, neu hochladen, Entwurf aktualisieren, erneut um Okay bitten.
   - „nein“/„veto“ → nicht freigeben, Logbuch „abgelehnt“ mit Grund. Wenn bis zum Termin genug Zeit bleibt, ein Ersatzthema anbieten.

## Ablauf: Wochenrecap (montags, 08:36)
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
- 15.11.2026 – Tilmans Vorgabe: allgemeiner + mehr Interaktion; Ziel 20 € Umsatz → Metricool-Bezahlplan. Format v2 (12–20 s, Hook in Sek. 0, Interaktionsfrage am Ende, breite Themen), Themenplan ab Tag 6 neu.
- 11.11.2026 – Tag 02: überlappende Sprechtexte (Tilman bemerkt) → automatische Timing-Prüfung in `build()`.
- 11.11.2026 – Metricool-Free-Limit (20/Monat pro Netzwerk) erkannt; Lösung in Klärung, Karussells ausgesetzt.
- 11.11.2026 – Sprachausgabe eingeführt (Thorsten-Voice, Piper, MIT); Ton = Stimme + leises Musikbett.
- 10.11.2026 – Auf Tilmans Wunsch: Freigabe per Okay-Antwort auf die Push-Nachricht statt 24-h-Veto; Start auf Mi 11.11. vorgezogen (Intro von Tilman bereits freigegeben).
