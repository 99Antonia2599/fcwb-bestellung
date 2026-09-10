# FCWB Materialbestellung – Notiz zur Übergabe (Stand 09.09.2026)

## Zugang
- App: https://99antonia2599.github.io/fcwb-bestellung/
- Code: https://github.com/99Antonia2599/fcwb-bestellung (GitHub-Account 99Antonia2599, Antonia)
- Datenbank: Supabase-Projekt `fcwb-bestellung`, Organisation `FC Weinfelden-Buerglen`, Region Frankfurt, Free-Plan.
  Läuft auf Antonias Supabase-Account. Übertragung an den Verein per «Transfer project» möglich.

## Was sich gegenüber Erols letzter Version geändert hat
- Firebase ist ersetzt durch Supabase. Tabellen `orders` und `teams`: eine Zeile pro Bestellung bzw. Team,
  damit gleichzeitige Änderungen verschiedener Personen sich nicht überschreiben. Live-Sync über Supabase Realtime.
  Die Tabelle `meta` aus der ersten Version wird nicht mehr genutzt.
  Die zwei Testbestellungen aus Firebase sind nicht übernommen, die neue Datenbank startet leer.
- Neues Design (Blau/Gold, neue Schrift, Karten), Funktionen unverändert.
- Produktbilder: 105 Artikel mit Originalfoto vom 11teamsports-Shop (weisser Hintergrund),
  13 Artikel mit Erols Bild aus der PDF-Liste, auf Weiss gelegt,
  1 Artikel (Challenge VI Goalie-Trikot Damen) behält den dunklen Hintergrund.
  Zuordnung Artikelnummer → Bild in `imgmap.txt`.
- Überzieher = Roly «Ajax» 0417, Farbcodes 221 Neongelb, 222 Neongrün, 223 Neonorange, 228 Neonpink.

## Ablauf
Bestellung abschliessen → Status «Auszulösen» → ausführende Person bestellt im 11teamsports-Clubshop
(PDF/Excel als Vorlage) → «✔ Bei 11teamsports bestellt» → Geliefert → Bedruckt → Abholbereit → Übergeben → Archiv.

## Passwort
Startseite fragt ein Passwort ab (aktuell «FCWB1914», gemerkt pro Gerät). Es liegt nur als Prüfsumme im Code,
ist aber kein echter Schutz: Wer den Code liest, kann es umgehen. Ändern: Build mit FCWB_PASSWORD=neuesPasswort.

## WhatsApp
Keine Handynummern mehr in der App. «WhatsApp öffnen» startet WhatsApp mit vorausgefülltem Text, Chat oder Gruppe wählt man selbst.

## E-Mail bei neuer Bestellung
Datenbank-Webhook `notify_order_mail` (INSERT + UPDATE auf `orders`) → Edge Function `notify-order` → Mail.
Versand über Gmail-SMTP mit Erols Konto erolgencoglu84@gmail.com (Secrets GMAIL_USER, GMAIL_APP_PASSWORD); damit sind
beliebige Empfänger möglich. Empfänger in MAIL_TO (kommagetrennt). Resend (RESEND_API_KEY, MAIL_FROM) bleibt als
Rückfall, sendet aber ohne Domain nur an antonia.alber@modelgroup.com. Quellcode: `edge_notify_order.ts`.
Mail bei: neuer Bestellung; Änderung des Gesamtstatus (niedrigste Stufe über alle Positionen); Archivierung.
Wappen ist als eingebettete Anlage (CID) in der Mail, weil Outlook externe Bilder blockiert.

## Supabase-Wecker
GitHub Action `.github/workflows/supabase-wecker.yml` fragt alle 2 Tage die Datenbank an (gegen die 7-Tage-Pause
im Free-Plan) und committet sein Laufdatum (gegen die 60-Tage-Abschaltung von GitHub-Zeitplänen). Bei Fehlschlag
mailt GitHub die Repo-Inhaberin.

## Offen / bekannt
- Supabase Free-Plan pausiert das Projekt nach 7 Tagen ohne Zugriff; im Dashboard wieder starten.
- Wer den Link hat, kann Bestellungen lesen und ändern (bewusst so für das 6-Personen-Tool).

## Neu bauen nach Änderungen
`python build.py <SUPABASE_URL> <PUBLISHABLE_KEY>` erzeugt `index.html` aus `../index_7.html`
(Erols Original), `adapter.js`, `design.css` und `images.json`. Danach `git push`, GitHub Pages aktualisiert sich.
