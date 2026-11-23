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

## Konzept (Format v3 ab Tag 6 – Tilmans Vorgabe 15.11.: allgemeiner, mehr Interaktion)
**Befund Tag 1–4 (TikTok):** 600–980 Views je Video, fast nur For-You. Aber Ø Watchtime 4–9 s bei 26–34 s Länge, Komplett-Quote ≈ 0 %, IG-Skip-Rate 66–86 %. → Die Leute wischen in den ersten Sekunden weg. Ohne Zuschauen keine Interaktion und keine Follows.

- **Themen allgemein & alltagsnah:** Dinge, die jeder mit Handy erlebt (Akku, WLAN, Fake-SMS, „hört mein Handy mit?“, Black Friday). Keine Fachbegriffe im Hook. Fachwörter nur, wenn sie sofort erklärt werden.
- **Länge 25–35 s** (Tilman 16.11.: Länge ist gut für TikTok – nicht kürzen, sondern spannender machen). Hook + Spannungsbogen + Auflösung + Frage.
- **Hook in Sekunde 0:** Erster Frame zeigt sofort die Hook-Zeile/-Zahl groß (kein Tipp-Effekt, kein Logo-Intro), Stimme ab 0,05 s. Hook = konkrete Alltagssituation, Entweder-oder, Kontrast oder Zahl – keine reine Ja/Nein-Frage (Recap 16.11.) („3.000 haben mich gesehen. 5 sind geblieben.“, „Dein Handy hört mit. Oder?“).
- **Untertitel (Pflicht, automatisch):** `build()` zeichnet sie aus den echten Wortzeiten der Stimme (Whisper) – 1–3 Wörter, GROSS, aktives Wort gelb hinterlegt. Grafiken müssen den Bereich **y 1310–1500** freilassen.
- **Stock (Pixabay):** echte Fotos/Videos als Hintergrund (`stock_search` → `stock_preview` ansehen → `stock_get` → `Clip`/`stock_bg`, abgedunkelt 0,5–0,75). **Keine KI-generierten Bilder/Videos:** Filter in `stil.py` (nur Fotos/Filme, Upload ≤ 2021, KI-/CG-Tags raus) **und** jede Auswahl selbst ansehen; im Zweifel nicht verwenden. Keine erkennbaren Marken/Logos im Fokus, keine Personen in heiklem Kontext. Quellen via `write_credits()` in `werkstatt/quellen.md`. Musik/Sounds: Pixabay hat dafür keine Schnittstelle → eigenes Musikbett, bis Tilman Tracks unter `sounds/` ablegt.
- **Zeitplan aus der Stimme:** `VOICE = timeline([...])`, Grafik-Ereignisse mit `at(WORDS, "wort")` aufs gesprochene Wort legen (Vorbild: `tag06_logbuch1.py`).
- **Tempo:** alle 2–3 s neues Bild-Element. Sprechtempo `say.__defaults__ = (0.9,)`.
- **Schluss = Interaktionsfrage**, mit 1 Wort oder Emoji beantwortbar („Team 2,4 oder Team 5? Schreib’s in die Kommentare.“, „Schon mal passiert? Ja oder nein.“). Bei Listen/Tipps: „Speicher dir das“. Bei Fehlern, die andere machen: „Schick das jemandem, der …“.
- **Follow-Grund:** Serien mit Teilen („Teil 1 von 2 – Teil 2 morgen“) wo sinnvoll; Hinweis im Bild am Ende „Folgen = morgen schlauer“ (kurz, max. 1 s).
- **Formate:** MYTHOS-CHECK (Rot falsch/Grün richtig) · RATE MAL (Frage, 3 s Pause zum Raten mit Countdown, Auflösung) · ALLTAGS-TRICK · KURIOS („Warum …?“) · montags KI-LOGBUCH (die KI berichtet offen über ihr Experiment – Zahlen, Fehler, was sie ändert; das Experiment selbst ist ein Hook).
- Stil: `werkstatt/stil.py` (dunkel, Cyan-Akzent, Inter Display, Pixelraster). Text: Du-Form, locker, trockener Humor. Die KI spricht als KI.
- Rhythmus: täglich 1 Video um **18:00** (Experiment Tag 7–12, vorher 17:30). Ohne Metricool-Bezahlplan nur TikTok (Recap 16.11.), mit Bezahlplan Reel + TikTok. Karussells ausgesetzt (Metricool-Budget).
- Caption: 1. Zeile = Hook als Frage; 1–2 kurze Sätze; letzte Zeile = dieselbe Interaktionsfrage. 4–6 Hashtags, breit statt Nische (#wusstestdu #handytricks #alltagshacks #technik + 1–2 themenspezifisch). TikTok-`title` = Hook (≤ 90 Zeichen). Instagram: `firstCommentText` = die Interaktionsfrage (eigener Kommentar unter eigenem Post, keine Interaktion mit Personen).
- **Monetarisierung:** Niemals um Geld bitten (keine Spenden-/Trinkgeld-/Unterstützer-Aufrufe – Tilmans klare Vorgabe 15.11.). Weg: Affiliate-Links, nur mit offengelegter Werbung/Affiliate-Kennzeichnung („Werbung“/„Anzeige“ in Caption + Plattform-Flag `commercialContent…`) und nur Links/Konten, die Tilman eingerichtet hat. Keine erfundenen Empfehlungen, nur Dinge, die zum Video-Thema ehrlich passen.

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
   - Skript `werkstatt/tagNN_thema.py` nach Vorbild `tag01_intro.py` schreiben. **Vor dem Rendern** mit `stills()` Kontaktbogen zeichnen und ansehen (Lesbarkeit, Überlappungen, sichere Zone). Dann `build()`. Länge 25–35 s (Format v3). `seed` = Tagnummer.
   - **Pflicht-QA nach jedem Video:** `build()` prüft das fertige MP4 automatisch (Überlappung, Aussetzer/Tonlöcher, Untertitel-Sync gegen unabhängige Spracherkennung, Ton-/Bildlänge) und bricht bei Fehlern ab – dann Ursache beheben, neu rendern, nie ein Video ohne „QA OK“ verwenden. Zusätzlich 5 Frames aus dem fertigen Video ansehen (Hook-Frame, Szenenwechsel, Schluss). QA-Bericht nach `werkstatt/qa/` kopieren und die Sync-Zeile im Bericht an Tilman nennen.
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

## Laufendes Experiment: Mitmach-Einstieg (ab Tag 14, Di 24.11.; Wochenrecap 23.11.)
Befund bis Tag 11: Die zwei Videos mit Mitmach-Moment (Tag 8 Passwort-Countdown, Tag 11 „Gehört der Mast zur Ampel?“) halten 10 s Ø Wiedergabe, alle anderen 3–6 s (n = 2 → nur Hinweis, kein Beweis).
Gilt für jedes Video ab Tag 14:
1. **In Sekunde 0–5 eine Rate- oder Entscheidungsfrage** mit 2–3 sichtbaren Antwortoptionen (z. B. „Echter Rabatt oder Trick?“), danach **3-s-Countdown** (wie Tag 8), erst dann die Auflösung. Auch Mythos-Checks so umbauen („Ja oder nein? 3 – 2 – 1“).
2. Alles andere bleibt (Sprechtempo 0,82, Hook-Satz ≤ 6 Wörter, Bewegung in Sek. 0–1, kein Ton-Akzent).
Auswertung im Wochenrecap 30.11.: Ø Wiedergabe und Komplett-Quote der Mitmach-Videos vs. Tag 6–12. Erfolg = Ø Wiedergabe ≥ 9 s bei mind. 2 von 3 Videos.

### Abgeschlossen: Experiment Einstieg (Tag 9–12)
Ergebnis (Daten Tag 9–11; Tag 12 lieferte Metricool noch nicht): Ø Wiedergabe 5,7 s vs. 6,3 s bei Tag 6–8, Views Ø 327 vs. 260 (+26 %, n = 3). Ziel ≥ 9 s **nicht erreicht**. Einstellungen bleiben als Standard (kein Schaden erkennbar), nächster Hebel = Mitmach-Einstieg (s. o.).

## Änderungsprotokoll
- 23.11.2026 – **Wochenrecap 2** (Daten Tag 6–11 vs. Tag 1–5, nur TikTok; kleine Zahlen → geringe Aussagekraft):
  1. **Tag 14 ↔ Tag 16 getauscht: Black Friday kommt am Di 24.11.** Daten: Tag 14 ist der letzte freie Metricool-Slot im November (19/20 belegt); Black Friday ist Fr 27.11. (Verbraucherzentrale SH, 19.11.); das einzige Video mit mehreren Shares war das aktuelle Warn-Thema Tag 10 (3 Shares). Inhalt nach Verbraucherzentrale SH/Netzwelt: Rabatt oft gegen UVP gerechnet → Preisverlauf/Preisvergleich prüfen; Countdown-Druck ignorieren; Fakeshop-Finder; nicht per Vorkasse zahlen. TikTok-Algorithmus-Thema rückt auf Tag 16.
  2. **Budget-Plan für 25.–30.11.:** Ohne Metricool-Bezahlplan bis Di 24.11. 19:42 werden Tag 15–20 **nicht** angelegt (Pause, im Daily mit ⚠️ melden). Ab Di 01.12. (Tag 21) wieder täglich nur TikTok – 20 Slots reichen für Tag 21–30. Kommt der Bezahlplan, läuft alles normal weiter (dann auch wieder IG + TikTok).
  3. **Experiment Einstieg beendet, Mitmach-Einstieg als neues Experiment** (s. „Laufendes Experiment“). Daten: Tag 8 + 11 (Mitmach) 10 s Ø Wiedergabe, übrige Videos Ø 4,4 s; Experiment Einstieg 5,7 s statt Ziel ≥ 9 s.
  - Posting-Zeit 18:00 bleibt: Metricool-Zeitindex TikTok hat 18 Uhr an Mo–Do als Bestwert, Fr–So gleichauf mit 10 Uhr. Das 18-Uhr-Experiment aus Woche 2 ist nicht auswertbar (fällt mit Format-Wechsel Tag 6 zusammen).
- 21.11.2026 – Tilman: Ton-Akzent in Sekunde 0 ab Tag 12 weglassen (kein `sfx`). „Bot“ wird jetzt „Bott“ gesprochen (`AUSSPRACHE_WORT`).
- 16.11.2026 – **Wochenrecap 1** (Daten Tag 1–4; Tag 5 lieferte Metricool noch nicht; kleine Zahlen → geringe Aussagekraft):
  1. **TikTok vor Instagram, solange das Budget knapp ist.** Daten: TikTok Ø 796 Views, 5 Follower; Instagram Ø 67 Views, 0 Follower. Das Budget ist mit Tag 10 bei 20/20. → Ab Tag 7 nur TikTok, solange kein Metricool-Bezahlplan aktiv ist (8 freie Slots = Tag 7–14 statt 7–10). Mit Bezahlplan wieder IG + TikTok. Tilman kann das per „veto“ zurücknehmen.
  2. **Hook = konkrete Alltagssituation oder Entweder-oder statt Ja/Nein-Frage.** Daten: Tag 4 (Hook „2,4 oder 5 GHz?“) hat die beste Watchtime (TT 9 s, IG 7,4 s) und die niedrigste IG-Skip-Rate (65,5 %); Tag 3 (Hook „Macht Inkognito anonym?“) die schlechteste (IG-Skip 87,5 %, Ø 2,3 s). Das ist n = 4, also nur eine Einschätzung, die Tag 7–12 prüfen sollen.
  3. **Tag 10 aktualisiert:** statt Paket-SMS die aktuelle Welle falscher Bank-/PayPal-Nachrichten (Verbraucherzentrale Phishing-Radar 9.–13.11.: PayPal, Commerzbank, Consorsbank, easybank, CHECK24).
  - **Experiment Woche 2 (Tag 7–12):** Posting-Zeit **18:00 statt 17:30**. Grund: Laut Metricool liegt der TikTok-Zeitindex um 18 Uhr an jedem Tag 8–27 % über 17 Uhr. Auswertung im Recap 23.11. (Views nach 24 h vs. Tag 1–5).
- 10.11.2026 – Start-Setup: Konzept, Stil, Kette Metricool ↔ GitHub getestet (Bild + Video, KI-Labels ok).
- 17.11.2026 – Experiment „Einstieg“ beschlossen (ab Tag 9): schnellere Stimme, Hook-Satz ≤ 6 Wörter, Bewegung + Ton-Akzent in Sekunde 0–1.
- 16.11.2026 – Aussprache-Wörterbuch `AUSSPRACHE` in `stil.py` (Tilman: „Sneaker“ = „Snieker“); Untertitel zeigen die Originalschreibweise. Bei englischen Lehnwörtern vorab `phonemize` prüfen und ggf. eintragen.
- 16.11.2026 – Format v3 (Tilman): Länge bleibt ~30 s, dafür Hook + Tempo; Untertitel mit Wort-Highlight; Pixabay-Stock (ohne KI-Material); automatische Audio-/Sync-QA. Tag 06 neu gebaut.
- 15.11.2026 – Tilmans Vorgabe: allgemeiner + mehr Interaktion; Ziel 20 € Umsatz → Metricool-Bezahlplan. Format v2 (12–20 s, Hook in Sek. 0, Interaktionsfrage am Ende, breite Themen), Themenplan ab Tag 6 neu.
- 11.11.2026 – Tag 02: überlappende Sprechtexte (Tilman bemerkt) → automatische Timing-Prüfung in `build()`.
- 11.11.2026 – Metricool-Free-Limit (20/Monat pro Netzwerk) erkannt; Lösung in Klärung, Karussells ausgesetzt.
- 11.11.2026 – Sprachausgabe eingeführt (Thorsten-Voice, Piper, MIT); Ton = Stimme + leises Musikbett.
- 10.11.2026 – Auf Tilmans Wunsch: Freigabe per Okay-Antwort auf die Push-Nachricht statt 24-h-Veto; Start auf Mi 11.11. vorgezogen (Intro von Tilman bereits freigegeben).
