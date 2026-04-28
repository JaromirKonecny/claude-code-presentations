# Anleitung: Präsentationen erstellen mit Claude Code

**Autor:** Prof. Dr. Jaromir Konecny & Claude Opus 4.7
**Stand:** April 2026
**Zielgruppe:** Menschen ohne Programmierkenntnisse
**Betriebssystem:** Windows 10/11

---

## Was ist das hier?

Dieses Projekt ermöglicht es dir, mit Hilfe von KI (Claude Code) professionelle PowerPoint-Präsentationen automatisch erstellen zu lassen. Du gibst ein Thema an, Claude Code recherchiert, erstellt eine Gliederung, baut Diagramme und sucht passende Bilder — und am Ende bekommst du eine fertige .pptx-Datei.

Du musst dafür **nicht programmieren können**. Du musst nur einmalig ein paar Programme installieren und danach mit Claude Code in natürlicher Sprache kommunizieren.

---

## Begriffe, die du kennen musst

| Begriff | Erklärung |
|---------|-----------|
| **Terminal / PowerShell** | Das Textfenster in Windows, in dem du Befehle eintippen kannst. Öffnen: Windows-Taste drücken, „PowerShell" tippen, Enter. |
| **Node.js** | Eine Laufzeitumgebung für JavaScript. Wird benötigt, weil die Bibliothek, die PowerPoint-Dateien erzeugt (`pptxgenjs`), in JavaScript geschrieben ist. |
| **npm** | Node Package Manager. Ein Programm, das zusammen mit Node.js installiert wird. Damit installierst du JavaScript-Bibliotheken. Vergleich: npm ist für JavaScript das, was pip für Python ist. |
| **pip** | Der Paketmanager für Python. Damit installierst du Python-Bibliotheken wie matplotlib. |
| **pptxgenjs** | Eine JavaScript-Bibliothek, die PowerPoint-Dateien (.pptx) erzeugt. Sie produziert deutlich schönere Ergebnisse als vergleichbare Python-Bibliotheken. |
| **matplotlib** | Eine Python-Bibliothek für Diagramme (Balken, Linien, Kreisdiagramme usw.). Die Diagramme werden als Bilder (PNG) gespeichert und in die Präsentation eingebettet. |
| **API** | Application Programming Interface — eine Schnittstelle, über die Programme miteinander kommunizieren. Die Pixabay-API erlaubt es, automatisch Bilder zu suchen und herunterzuladen. |
| **API-Key** | Ein persönlicher Schlüssel (wie ein Passwort), der dich bei einer API identifiziert. Jeder braucht seinen eigenen Key. **Teile deinen Key niemals öffentlich.** |
| **Umgebungsvariable** | Ein Wert, der im Betriebssystem gespeichert ist und von Programmen gelesen werden kann. Der Pixabay-API-Key wird als Umgebungsvariable gesetzt, damit die Scripts ihn finden. |
| **.env-Datei** | Eine einfache Textdatei, in der Umgebungsvariablen gespeichert werden (z.B. API-Keys). Sie wird nicht auf GitHub hochgeladen, damit dein Key privat bleibt. |
| **Workspace** | Der Ordner, in dem du mit Claude Code arbeitest (Projektordner). Claude Code liest beim Start die Datei `CLAUDE.md` aus diesem Ordner und weiß dadurch, was es tun soll. |
| **CLAUDE.md** | Eine Anweisungsdatei für Claude Code. Sie beschreibt den gesamten Workflow Schritt für Schritt. Claude Code liest sie automatisch und befolgt die Anweisungen. |
| **Claude Code** | Ein KI-Werkzeug von Anthropic, das direkt im Terminal arbeitet. Es kann Dateien lesen, Befehle ausführen, Code schreiben und im Internet recherchieren. |
| **Git for Windows** | Eine Windows-Version von Git, die Versionsverwaltung über die Kommandozeile, Git Bash und zusätzliche Integrationswerkzeuge ermöglicht. |


---
## Voraussetzungen
- Claude Pro/Max
- Internet
- Windows
---

## Schritt 1: Programme installieren

### 1.1 Node.js installieren
Node.js wird nicht für Claude Code selbst benötigt, aber für die Bibliothek pptxgenjs, die die PowerPoint-Dateien erzeugt.

1. Gehe auf https://nodejs.org/
2. Lade die **LTS-Version** herunter (linker Button, markiert mit „Latest LTS - Long Term Support")
3. Installiere mit den Standardeinstellungen
4. Prüfe die Installation — öffne PowerShell und tippe:

```powershell
node --version
npm --version
```

Wenn jeweils eine Versionsnummer erscheint (z.B. `v22.15.0` und `11.11.0`), hat es geklappt.

**Was ist passiert?** Du hast Node.js installiert. npm wurde automatisch mitinstalliert — es gehört zu Node.js.

### 1.2 Python installieren

Falls du Python noch nicht hast:

1. Gehe auf https://www.python.org/downloads/
2. Lade die neueste Version herunter
3. **Wichtig:** Setze beim Installieren den Haken bei **„Add Python to PATH"**
4. Prüfe:

```powershell
python --version
pip --version
```

### 1.3 Claude Code installieren

Falls du Claude Code noch nicht hast (Voraussetzung: Claude Pro oder Max):

1. Installiere Git for Windows: https://git-scm.com/downloads/win
2. Öffne PowerShell und führe aus:
```powershell
irm https://claude.ai/install.ps1 | iex
```
3. Prüfe: 
```powershell
claude --version
```

---

## Schritt 2: Projekt einrichten

### 2.1 Projektordner anlegen

Erstelle einen Ordner auf deinem Rechner, z.B.:

```
C:\Users\DEIN-NAME\presentation-workflow\
```

### 2.2 Projektdateien hineinkopieren

Kopiere diese Dateien in den Ordner (du bekommst sie von deinem Dozenten oder aus dem Kurs-Repository):

```
presentation-workflow/
├── CLAUDE.md
├── helpers/
│   ├── pixabay_search.py
│   └── create_chart.py
└── projekte/
```

### 2.3 JavaScript-Bibliotheken installieren

Öffne PowerShell und navigiere in den Ordner:

```powershell
cd C:\Users\DEIN-NAME\presentation-workflow
```

Dann installiere die benötigten Bibliotheken:

```powershell
npm init -y
npm install pptxgenjs react-icons react react-dom sharp
```

npm init -y erstellt eine package.json-Datei im aktuellen Ordner. npm install installiert die Pakete in einen node_modules-Unterordner direkt im Workspace. Damit findet Node.js die Pakete automatisch.

**Was passiert hier?** Du installierst fünf Pakete:

| Paket | Zweck |
|-------|-------|
| `pptxgenjs` | Erzeugt PowerPoint-Dateien |
| `react-icons` | Sammlung von tausenden Icons (Symbole) |
| `react`, `react-dom` | Werden von react-icons benötigt |
| `sharp` | Konvertiert Icons in Bilder (PNG), die PowerPoint versteht |

### 2.4 Python-Bibliotheken installieren

```powershell
pip install matplotlib Pillow requests
```

| Paket | Zweck |
|-------|-------|
| `matplotlib` | Erstellt Diagramme (Balken, Linien, Kreise usw.) |
| `Pillow` | Verarbeitet Bilder |
| `requests` | Ermöglicht Internetanfragen (für die Pixabay-Bildersuche) |

---

## Schritt 3: Pixabay-Bildersuche einrichten (optional)

Dieser Schritt ist optional. Ohne Pixabay funktioniert der Workflow trotzdem — es werden dann nur Diagramme und Icons verwendet, keine Stockfotos.

### 3.1 Pixabay-Account erstellen

1. Gehe auf https://pixabay.com/ und klicke auf **„Join"**
2. Registriere dich kostenlos (E-Mail-Adresse genügt)

### 3.2 API-Key kopieren

1. Gehe auf https://pixabay.com/api/docs/
2. Melde dich an (falls nicht schon eingeloggt)
3. Dein API-Key wird oben auf der Seite im Bereich **„Parameters"** neben **„key"** angezeigt (eine lange Zeichenkette mit Buchstaben, Zahlen und Bindestrichen)
4. Kopiere diesen Key

**Wichtig:** Dein API-Key ist persönlich, wie ein Passwort. Teile ihn nicht in Chats, Screenshots oder öffentlichen Dokumenten.

### 3.3 .env-Datei erstellen

1. Öffne Notepad++ (oder einen anderen Texteditor)
2. Tippe genau diese eine Zeile ein (ersetze den Beispiel-Key durch deinen echten Key):

```
PIXABAY_API_KEY=12345678-abcdef1234567890abcdef123
```

3. Speichere die Datei als `.env` in deinem `presentation-workflow/`-Ordner
4. **Achtung beim Speichern:** Stelle den Dateityp auf **„All types (\*.\*)"**, sonst speichert Notepad++ die Datei als `.env.txt`

Dein Ordner sieht jetzt so aus:

```
presentation-workflow/
├── .env                    ← Neu! Enthält deinen API-Key
├── CLAUDE.md
├── helpers/
│   ├── pixabay_search.py
│   └── create_chart.py
└── projekte/
```

**Pixabay-Lizenz:** Bilder von Pixabay dürfen in der Regel kostenlos für private und kommerzielle Zwecke genutzt, kopiert, bearbeitet und in eigene Projekte eingebunden werden; eine Namensnennung ist nicht erforderlich, aber erwünscht. Nicht erlaubt ist unter anderem der unveränderte Weiterverkauf bzw. die Weiterverbreitung als eigenständige Datei sowie eine rechtswidrige, irreführende oder herabwürdigende Nutzung; bei erkennbaren Personen, Marken oder geschützten Objekten sollten zusätzliche Rechte geprüft werden. (Quelle: https://pixabay.com/service/license-summary/) 

---

## Schritt 4: Erste Präsentation erstellen

### 4.1 Claude Code starten

Öffne PowerShell, navigiere in den Projektordner und starte Claude Code:

```powershell
cd C:\Users\DEIN-NAME\presentation-workflow
claude
```

### 4.2 Präsentation anfordern

Tippe einfach:

```
Erstelle eine Präsentation
```

Claude Code liest automatisch die CLAUDE.md und führt dich durch den Workflow. Er wird dich nacheinander fragen:

1. **Thema** — Worüber soll die Präsentation sein?
2. **Zielgruppe** — Für wen ist sie? (Studierende, Fachpublikum, Führungskräfte...)
3. **Folienanzahl** — Wie viele Folien? (Empfehlung: 8–15 für eine 20-Minuten-Präsentation)
4. **Sprache** — Deutsch, Englisch oder andere?
5. **Stil** — Dunkel & professionell, hell & modern oder akademisch?
6. **Recherche** — Soll Claude Code selbst recherchieren oder hast du eine eigene Recherche-Datei?

### 4.3 Ablauf nach dem Briefing

Claude Code arbeitet dann diese Schritte ab:

**Recherche** → Claude Code sucht im Internet nach Informationen zu deinem Thema und zeigt dir eine Zusammenfassung.

**Gliederung** → Claude Code erstellt eine Folien-Gliederung und schlägt für jede Folie vor, welche Art von Grafik am besten passt:

| Kürzel | Bedeutung | Beispiel |
|--------|-----------|---------|
| CHART | Daten-Diagramm | Balkendiagramm mit Marktanteilen |
| DIAGRAM | Prozess-Darstellung | Ablaufdiagramm eines Workflows |
| STOCKIMAGE | Foto von Pixabay | Stimmungsbild „Teamwork" |
| ICON | Symbol | Glühbirne für „Idee" |
| TABLE | Tabelle | Vergleichstabelle |

Du kannst die Gliederung ändern, bevor er weitermacht.

**Farbpalette** → Claude Code schlägt Farben vor, die zum Thema passen. Du kannst sie anpassen.

**Erstellung** → Claude Code baut die Diagramme, lädt Bilder herunter und erstellt die .pptx-Datei.

**Prüfung** → Claude Code prüft die Präsentation auf Fehler und zeigt dir das Ergebnis.

### 4.4 Ergebnis

Die fertige Präsentation liegt in:

```
presentation-workflow/projekte/YYYY-MM-kurzname/output/presentation.pptx
```

Öffne sie mit PowerPoint oder LibreOffice Impress. Falls du nichts davon installiert hast: PowerPoint Online (kostenlos mit Microsoft-Account) oder LibreOffice (kostenlos zum Download).

---

## Eigene Recherche verwenden (z.B. aus Deep Research)

Wenn du eine eigene Recherche hast (z.B. aus Claude Deep Research, ChatGPT Deep Research oder einer anderen Quelle):

1. Speichere sie als Markdown-Datei (.md) oder Textdatei (.txt)
2. Lege sie in den Research-Ordner deines Projekts:

```
presentation-workflow/projekte/YYYY-MM-kurzname/research/recherche.md
```

3. Sage Claude Code bei der Recherche-Frage: **„Ich habe eine eigene Recherche-Datei im Research-Ordner."**

Claude Code liest die Datei dann ein und nutzt sie als Grundlage.

---

## Häufige Probleme

### „npm wird nicht erkannt"

Node.js ist nicht installiert oder nicht im PATH. Installiere Node.js neu (Schritt 1.1) und starte PowerShell danach neu.

### „pip wird nicht erkannt"

Python ist nicht im PATH. Installiere Python neu und setze dabei den Haken bei **„Add Python to PATH"**.

### „PIXABAY_API_KEY nicht gesetzt"

Die .env-Datei fehlt, liegt im falschen Ordner, oder heißt `.env.txt` statt `.env`. Prüfe:

```powershell
Get-ChildItem -Hidden .env
```

Wenn die Datei da ist, aber der Fehler trotzdem kommt: Öffne sie und prüfe, ob der Key korrekt eingetragen ist (keine Anführungszeichen, keine Leerzeichen um das `=`).

### Keine Stockbilder trotz API-Key

Prüfe, ob dein Key funktioniert — öffne diese URL im Browser (ersetze `DEIN-KEY`):

```
https://pixabay.com/api/?key=DEIN-KEY&q=flower&per_page=3
```

Wenn du eine JSON-Antwort mit Bilddaten siehst, funktioniert der Key.

### Die Präsentation sieht anders aus als erwartet

Sage Claude Code einfach, was dir nicht gefällt:

- „Die Schrift auf Folie 3 ist zu klein"
- „Ich hätte gern ein anderes Bild auf Folie 5"
- „Die Farben gefallen mir nicht, nimm lieber Blautöne"

Claude Code passt die Präsentation an und erstellt sie neu.

---

## Zusammenfassung: Was wurde installiert und warum?

| Programm/Paket | Typ | Zweck |
|---------------|-----|-------|
| Node.js | Laufzeitumgebung | Führt JavaScript-Programme aus |
| npm | Paketmanager | Installiert JavaScript-Bibliotheken |
| pptxgenjs | JavaScript-Bibliothek | Erzeugt PowerPoint-Dateien |
| react-icons + sharp | JavaScript-Bibliotheken | Stellt Icons als Bilder bereit |
| Python | Programmiersprache | Führt Python-Scripts aus |
| pip | Paketmanager | Installiert Python-Bibliotheken |
| matplotlib | Python-Bibliothek | Erstellt Diagramme |
| Pillow | Python-Bibliothek | Verarbeitet Bilder |
| requests | Python-Bibliothek | Kommuniziert mit der Pixabay-API |
| Claude Code | KI-Werkzeug | Steuert den gesamten Workflow |
