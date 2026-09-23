# FCWB Materialbestellung – Notiz zur Übergabe (Stand 22.09.2026)

## Zugang
- App: https://fcwb-shop.ch (GitHub Pages, Domain bei IONOS registriert)
  Die alte Adresse https://99antonia2599.github.io/fcwb-bestellung/ bleibt parallel erreichbar,
  solange GitHub Pages laeuft.
- Code: https://github.com/99Antonia2599/fcwb-bestellung (GitHub-Account 99Antonia2599, Antonia)
- Datenbank: Supabase-Projekt `fcwb-bestellung`, Organisation `FC Weinfelden-Buerglen`, Region Frankfurt, Free-Plan.
  Läuft auf Antonias Supabase-Account. Übertragung an den Verein per «Transfer project» möglich.
- Anmeldung in der App: gemeinsames Vereinskonto `bestellung@fcwb.ch`. Das Passwort kennen die
  sechs Personen, die bestellen; es steht **nicht** im Code, sondern nur in Supabase.

## Anmeldung und Schutz der Daten
Die Startseite fragt ein Passwort ab. Geprüft wird es von Supabase Auth, nicht im Browser.
Ohne gültige Anmeldung gibt die Datenbank nichts heraus und nimmt nichts an – die Maske ist
also echter Zugangsschutz.

Das hängt an zwei Dingen, die zusammengehören:
- `supabase_setup.sql` beschränkt die Tabellen `orders` und `teams` per Row Level Security auf
  das angemeldete Vereinskonto. Der Schlüssel, der in der Seite steht (`sb_publishable_…`), ist
  öffentlich und kann für sich allein nichts.
- `login.js` meldet mit der eingegebenen Eingabe bei Supabase an, `adapter.js` wartet mit Laden,
  Live-Sync und Speichern auf diese Anmeldung.

Die Anmeldung bleibt pro Gerät gemerkt und erneuert sich selbst. Unten rechts gibt es
«Abmelden», um ein Gerät wieder zu lösen.

**Passwort ändern:** Supabase-Dashboard → Authentication → Users → beim Konto `bestellung@fcwb.ch`
auf «Reset password» bzw. das Passwort neu setzen. Kein neuer Build nötig, die Seite bleibt wie sie ist.

**Mailadresse des Kontos ändern:** an drei Stellen anpassen, sonst kommt niemand mehr rein –
in Supabase beim Konto selbst, in `supabase_setup.sql` (zweimal, in beiden Policies, danach
das SQL neu ausführen) und beim Bauen über `FCWB_LOGIN_EMAIL` bzw. das dritte Argument.

**Wichtig in Supabase:** unter Authentication → Sign In / Providers die freie Registrierung
ausgeschaltet lassen. Zur Sicherheit prüfen die Policies zusätzlich die Mailadresse, ein
selbst angelegtes Konto käme also ohnehin nicht durch.

## Veröffentlichung
Veröffentlicht wird **nur der Ordner `docs/`**, und darin liegt nur die fertige `index.html`.
Alles andere im Repo – diese Notiz, `images.json`, `imgmap.txt`, die Build-Skripte – bleibt
damit vom Netz fern. `build.py` schreibt direkt dorthin.

Der Ordner heisst `docs`, weil GitHub Pages ausser dem Hauptordner nur diesen Namen anbietet
(Settings → Pages → Folder: `/docs`). Andere Anbieter akzeptieren jeden Namen.

`docs/CNAME` enthaelt die Domain `fcwb-shop.ch`. Die Datei muss dort liegen bleiben, sonst faellt
die Seite auf die github.io-Adresse zurueck. `build.py` schreibt nur `docs/index.html` und laesst
sie in Ruhe.

DNS bei IONOS: vier A-Records auf `@` (185.199.108-111.153), kein AAAA-Record. Die Mail-Eintraege
derselben Domain (MX, SPF, DKIM, DMARC, autodiscover) gehoeren zum Postfach und duerfen nicht
geloescht werden.

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
- Seit 22.09.2026: echte Anmeldung statt der früheren Passwortabfrage im Browser (siehe oben),
  Veröffentlichung nur noch aus `docs/`.

## Ablauf
Bestellung abschliessen → Status «Auszulösen» → ausführende Person bestellt im 11teamsports-Clubshop
(PDF/Excel als Vorlage) → «✔ Bei 11teamsports bestellt» → Geliefert → Bedruckt → Abholbereit → Übergeben → Archiv.

## WhatsApp
Keine Handynummern mehr in der App. «WhatsApp öffnen» startet WhatsApp mit vorausgefülltem Text, Chat oder Gruppe wählt man selbst.

## E-Mail bei neuer Bestellung
Datenbank-Webhook `notify_order_mail` (INSERT + UPDATE auf `orders`) → Edge Function `notify-order` → Mail.
Versand über Gmail-SMTP mit Erols privatem Konto (Adresse und App-Passwort stehen in den Supabase-Secrets
`GMAIL_USER` und `GMAIL_APP_PASSWORD`); damit sind beliebige Empfänger möglich. Empfänger in `MAIL_TO`
(kommagetrennt). Resend (`RESEND_API_KEY`, `MAIL_FROM`) bleibt als Rückfall, sendet aber ohne eigene Domain
nur an die dort verifizierte Adresse. Quellcode: `edge_notify_order.ts`.
Mail bei: neuer Bestellung; Änderung des Gesamtstatus (niedrigste Stufe über alle Positionen); Archivierung.
Wappen ist als eingebettete Anlage (CID) in der Mail, weil Outlook externe Bilder blockiert; es macht rund
42 KB pro Mail aus, bei realistischem Betrieb also etwa 50 MB im Jahr.

Besser wäre mittelfristig ein Vereins-Mailkonto als Absender statt eines privaten – heute laufen die
gesendeten Mails im Ordner «Gesendet» von Erols privatem Gmail mit.

## Supabase-Wecker
GitHub Action `.github/workflows/supabase-wecker.yml` fragt alle 2 Tage die Datenbank an (gegen die 7-Tage-Pause
im Free-Plan) und committet sein Laufdatum (gegen die 60-Tage-Abschaltung von GitHub-Zeitplänen). Bei Fehlschlag
mailt GitHub die Repo-Inhaberin. Die Anfrage läuft mit dem öffentlichen Schlüssel und bekommt seit der
Umstellung keine Daten mehr zurück – geprüft wird nur, ob die Datenbank überhaupt antwortet.

## Offen / bekannt
- **Die Build-Quelle `index_7.html` liegt nicht im Repo.** `build.py` erwartet sie im übergeordneten Ordner
  (Erols Original). Solange sie nur auf einem privaten Rechner liegt, ist sie bei einem Geräteverlust weg und
  die App lässt sich nicht mehr neu bauen – übrig bliebe nur die fertige `docs/index.html`. Gehört ins Repo.
- Der öffentliche Supabase-Schlüssel stand von Anfang an in der Seite und in der Git-Historie. Das ist so
  vorgesehen, aber er lässt sich nicht zurückholen; der Schutz liegt deshalb allein bei den Policies.
  Bis zum 22.09.2026 waren diese offen, das heisst die Bestelldaten waren in dieser Zeit öffentlich les- und
  änderbar. Hinweise auf einen Zugriff gibt es keine (das Repo hatte keine Sterne, Forks oder Klone).
- Supabase Free-Plan pausiert das Projekt nach 7 Tagen ohne Zugriff; im Dashboard wieder starten.
- Repo, Supabase-Projekt, Domain und Absenderkonto laufen auf Privatpersonen. Bei einem Wechsel im Vorstand
  sollte das dem Verein gehören.

## Neu bauen nach Änderungen
`python build.py <SUPABASE_URL> <PUBLISHABLE_KEY> [LOGIN_EMAIL]` erzeugt `docs/index.html` aus `../index_7.html`
(Erols Original), `adapter.js`, `design.css` und `images.json`. Ohne drittes Argument wird `bestellung@fcwb.ch`
eingesetzt. Danach `git push`, die veröffentlichte Seite aktualisiert sich.
