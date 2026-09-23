# FCWB Materialbestellung – Notiz zur Übergabe (Stand 23.09.2026)

## Zugang
- App: https://fcwb-shop.ch (GitHub Pages, Domain bei IONOS registriert)
  Die alte Adresse https://99antonia2599.github.io/fcwb-bestellung/ bleibt parallel erreichbar,
  solange GitHub Pages laeuft.
- Code: https://github.com/99Antonia2599/fcwb-bestellung (GitHub-Account 99Antonia2599, Antonia)
- Datenbank: Supabase-Projekt `fcwb-bestellung`, Organisation `FC Weinfelden-Buerglen`, Region Frankfurt, Free-Plan.
  Läuft auf Antonias Supabase-Account. Übertragung an den Verein per «Transfer project» möglich.
- Anmeldung in der App: gemeinsames Vereinskonto `bestellung@fcwb-shop.ch`. Das Passwort kennen die
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

**Passwort ändern:** Supabase-Dashboard → Authentication → Users → beim Konto `bestellung@fcwb-shop.ch`
auf «Reset password» bzw. das Passwort neu setzen. Kein neuer Build nötig, die Seite bleibt wie sie ist.

**Mailadresse des Kontos ändern:** an drei Stellen anpassen, sonst kommt niemand mehr rein –
in Supabase beim Konto selbst, in `supabase_setup.sql` (zweimal, in beiden Policies, danach
das SQL neu ausführen) und beim Bauen über `FCWB_LOGIN_EMAIL` bzw. das dritte Argument.

**Wichtig in Supabase:** unter Authentication → Sign In / Providers, Abschnitt «User Signups»,
muss «Allow new users to sign up» ausgeschaltet bleiben – nicht beim Anbieter «Email» selbst,
der bleibt aktiviert. Zur Sicherheit prüfen die Policies zusätzlich die Mailadresse, ein
selbst angelegtes Konto käme also ohnehin nicht durch.

Das Konto wurde am 23.09.2026 angelegt und per «Auto Confirm User» bestätigt. Es ging keine
Bestätigungsmail raus, weil hinter der Adresse bewusst kein Postfach liegt – sie ist nur
Benutzername. Passwort neu setzen geht deshalb ausschliesslich über das Dashboard.

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
Datenbank-Webhook `notify_order_mail` (INSERT, UPDATE und DELETE auf `orders`) → Edge Function
`notify-order` → Mail. Am 23.09.2026 über `pg_trigger` geprüft: alle drei Ereignisse aktiv.
Versand über Gmail-SMTP mit Erols privatem Konto (Adresse und App-Passwort stehen in den Supabase-Secrets
`GMAIL_USER` und `GMAIL_APP_PASSWORD`); damit sind beliebige Empfänger möglich. Resend
(`RESEND_API_KEY`, `MAIL_FROM`) bleibt als Rückfall, sendet aber ohne eigene Domain nur an die dort
verifizierte Adresse. Quellcode: `edge_notify_order.ts`.

Mail bei: neuer Bestellung; Mengenänderung oder Storno; **jedem Stufenwechsel einer Position**;
Löschung; Archivierung.

Der Stufenwechsel wird **je Position** verglichen. Früher zählte nur der Gesamtstatus, also das Minimum
über alle Positionen – bei einer Teillieferung ging deshalb keine Mail raus, solange eine einzige
Position zurückhing, obwohl der Rest längst da war. Seit 23.09.2026 meldet jede Änderung, und die Mail
listet auf, welche Positionen gewechselt haben und wohin.

Eine Mail entsteht pro **Speichervorgang**, nicht pro Position: Wer über das Dropdown «Status für die
ganze Bestellung» alle auf einmal setzt, löst eine einzige Mail aus. Wer zehn Positionen einzeln
anklickt, löst zehn aus. Bei grossen Bestellungen also besser das Dropdown nehmen.

**Wer was bekommt** (Adressen stehen in Secrets, nicht im Code – das Repo ist öffentlich):

| Secret | Wer | Wann |
|---|---|---|
| `MAIL_INTERN` | Erol, Roberto | jede Mail |
| `MAIL_BESTELLER` | JSON Name→Adresse | der Besteller der jeweiligen Bestellung, jede Mail |
| `MAIL_SHOP` | Shopkontakte | nur Auslösung, Mengenänderung, Storno, Löschung |
| `MAIL_CC` | Antonia | jede Mail, im CC |
| `MAIL_TO` | – | nur noch Rückfall, falls `MAIL_INTERN` leer ist |

Die Namen in `MAIL_BESTELLER` müssen exakt dem Dropdown in der App entsprechen:
`Roberto, Francis, Erol, Muriel, Rami, Joelle`. Ein Tippfehler heisst stillschweigend: Besteller
bekommt keine Mail. Doppelte Adressen fallen raus, wer schon Empfänger ist, steht nicht nochmal im CC.
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
- Der öffentliche Supabase-Schlüssel stand von Anfang an in der Seite und in der Git-Historie. Das ist so
  vorgesehen, aber er lässt sich nicht zurückholen; der Schutz liegt deshalb allein bei den Policies.
  Bis zum 23.09.2026 waren diese offen, das heisst die Bestelldaten waren in dieser Zeit öffentlich les- und
  änderbar. Hinweise auf einen Zugriff gibt es keine (das Repo hatte keine Sterne, Forks oder Klone).
  Seit dem 23.09.2026 greifen `orders_auth` und `teams_auth`; eine Abfrage mit dem öffentlichen Schlüssel
  ohne Anmeldung liefert seither eine leere Liste. Genau diese Abfrage eignet sich als Kontrolle, falls
  jemand die Policies später anfasst.
- Bei Statuswechseln entsteht eine Mail pro Speichervorgang. Wer viele Positionen einzeln abhakt, löst
  entsprechend viele Mails aus; das Dropdown «Status für die ganze Bestellung» erzeugt eine einzige.
  Angedacht und bewusst zurückgestellt: Häkchen pro Position plus «markierte auf Stufe X setzen», damit
  sich eine Teillieferung in einem Schritt abhaken liesse – ein Speichervorgang, eine Mail. Ein Knopf
  «jetzt melden» wurde verworfen: Wer ihn vergisst, meldet nie etwas.
- Supabase Free-Plan pausiert das Projekt nach 7 Tagen ohne Zugriff; im Dashboard wieder starten.
- Repo, Supabase-Projekt, Domain und Absenderkonto laufen auf Privatpersonen. Bei einem Wechsel im Vorstand
  sollte das dem Verein gehören.

## Neu bauen nach Änderungen
`python build.py <SUPABASE_URL> <PUBLISHABLE_KEY> [LOGIN_EMAIL]` erzeugt `docs/index.html` aus
`index_7.html` (Erols Original), `adapter.js`, `design.css` und `images.json`. Ohne drittes Argument
wird `bestellung@fcwb-shop.ch` eingesetzt. Danach `git push`, die veröffentlichte Seite aktualisiert sich.
Der Build braucht Pillow (`pip install Pillow`).

`index_7.html` liegt seit 23.09.2026 im Repo und wurde dabei um zwei Dinge erleichtert, die nicht in ein
öffentliches Repository gehören: den API-Schlüssel des stillgelegten Firebase-Projekts `fcwb-bestellungen`
und die sieben privaten Handynummern in `Gg={…}`. Am Build ändert das nichts – `build.py` schneidet den
Firebase-Block ohnehin heraus und `no_phones` ersetzt den Nummernblock durch `Gg={}`. Nachgewiesen: Ein
Build aus dieser Vorlage ergibt eine Datei, die sich von der veröffentlichten nur im Zeitstempel `Qg`
unterscheidet, den `patches.seedversion` bei jedem Lauf neu setzt. Sonst byte-identisch.
