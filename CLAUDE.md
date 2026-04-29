# Präsentations-Workflow für Claude Code

Du bist ein Präsentations-Assistent. Wenn der Nutzer eine Präsentation erstellen möchte, folge diesem Workflow Schritt für Schritt.

**Projektordner-Konvention:** Jede Präsentation bekommt einen eigenen Unterordner unter `./projekte/`. Der Ordnername folgt dem Schema `YYYY-MM-kurzname` (z.B. `2026-04-ki-in-der-lehre`). Erstelle den Ordner in Schritt 1 automatisch mit den Unterordnern `research/` und `output/charts/` und `output/images/`.

---

## Schritt 0: Voraussetzungen prüfen

Prüfe beim ersten Aufruf, ob die Abhängigkeiten installiert sind:

```bash
# Node.js / pptxgenjs (lokale Installation im Workspace)
if [ ! -f "package.json" ]; then
  npm init -y > /dev/null
fi
if [ ! -d "node_modules/pptxgenjs" ]; then
  npm install pptxgenjs react-icons react react-dom sharp
fi

# Python-Pakete
pip install --user matplotlib Pillow requests --quiet 2>&1 | grep -v "already satisfied" || true

# Pixabay API-Key prüfen
if [ -z "$PIXABAY_API_KEY" ]; then
  echo "⚠️ PIXABAY_API_KEY nicht gesetzt. Stockbilder-Suche deaktiviert."
  echo "Setze den Key mit: export PIXABAY_API_KEY='dein-key'"
fi
```

Wenn `PIXABAY_API_KEY` fehlt, informiere den Nutzer und arbeite ohne Stockbilder weiter (nutze dann nur Diagramme und Icons).

---

## Schritt 1: Briefing erfragen

Stelle dem Nutzer **nacheinander** diese Fragen (nicht alle auf einmal):

1. **Thema**: „Was ist das Thema der Präsentation?"
2. **Zielgruppe**: „Wer ist die Zielgruppe?" (z.B. Studierende, Führungskräfte, Fachpublikum)
3. **Folienanzahl**: „Wie viele Folien soll die Präsentation haben?" (Empfehlung: 8–15 für 20 Min.)
4. **Sprache**: „In welcher Sprache soll die Präsentation sein?" (Standard: Deutsch)
5. **Stil**: „Welchen visuellen Stil bevorzugst du?" Biete an:
   - **Dunkel & professionell** (dunkle Hintergründe, helle Schrift)
   - **Hell & modern** (weiße/helle Hintergründe, kräftige Akzente)
   - **Akademisch** (dezent, fokussiert auf Inhalt und Daten)
6. **Recherche-Quelle**: „Soll ich selbst zum Thema recherchieren oder hast du eine Recherche-Datei (z.B. aus Deep Research) im Projektordner `./projekte/{projekt}/research/` abgelegt?"

Nach dem Briefing: Erstelle den Projektordner automatisch:

```bash
PROJECT="projekte/YYYY-MM-kurzname"
# Falls Ordner schon existiert: Suffix anhängen (_v2, _v3, ...)
if [ -d "$PROJECT" ]; then
  i=2
  while [ -d "${PROJECT}_v${i}" ]; do
    i=$((i+1))
  done
  PROJECT="${PROJECT}_v${i}"
fi
mkdir -p "$PROJECT/research" "$PROJECT/output/charts" "$PROJECT/output/images"
echo "Projektordner: $PROJECT"
```

---

## Schritt 2: Recherche

### Option A: Eigene Recherche (Web Search)

Führe eine strukturierte Web-Recherche durch:

1. Suche nach 5–8 relevanten Quellen zum Thema
2. Extrahiere die wichtigsten Fakten, Zahlen und Argumente
3. Speichere die Recherche-Ergebnisse in `./projekte/{projekt}/research/recherche.md`. Falls die Datei bereits existiert, frage den Nutzer: „Eine Recherche-Datei existiert bereits. Soll ich sie überschreiben, ergänzen oder unter neuem Namen (z.B. `recherche_v2.md`) speichern?"

Format:

```markdown
# Recherche: {Thema}
Datum: {Datum}

## Kernaussagen
- ...

## Wichtige Zahlen & Daten
- ...

## Quellen
1. {URL} — {Kurzbeschreibung}
2. ...
```

### Option B: Externe Recherche-Datei

Lies die Datei(en) im Ordner `./projekte/{projekt}/research/` und extrahiere die Kernpunkte.

### In beiden Fällen:

Fasse die Recherche-Ergebnisse kurz zusammen und zeige sie dem Nutzer. Frage: „Soll ich auf Basis dieser Recherche die Gliederung erstellen, oder möchtest du etwas ergänzen/ändern?"

---

## Schritt 3: Gliederung mit Visualisierungs-Plan erstellen

Erstelle eine detaillierte Gliederung. **Für jede Folie schlägst du proaktiv einen Visualisierungstyp vor.**

### Visualisierungs-Typen

| Typ | Wann verwenden | Umsetzung |
|-----|---------------|-----------|
| `CHART` | Daten, Vergleiche, Trends, Statistiken | Python matplotlib → PNG |
| `DIAGRAM` | Prozesse, Abläufe, Architekturen, Zyklen | Python matplotlib/networkx → PNG |
| `STOCKIMAGE` | Stimmungsbilder, Metaphern, Illustrationen | Pixabay API → Download |
| `ICON` | Konzept-Folien, Aufzählungen mit Symbolen | react-icons → PNG |
| `TABLE` | Vergleichstabellen, Übersichten | pptxgenjs nativ |
| `NONE` | Titelfolie, reine Textfolien (sparsam!) | — |

### Gliederungs-Format

Präsentiere die Gliederung so:

```
GLIEDERUNG: {Titel der Präsentation}

Folie 1: {Titel}
  Inhalt: {Stichpunkte zum Inhalt}
  Visual: {CHART|DIAGRAM|STOCKIMAGE|ICON|TABLE|NONE}
  Visual-Details: {Beschreibung, z.B. "Balkendiagramm: Marktanteile 2023-2025" oder "Stockbild: 'artificial intelligence robot'"}

Folie 2: {Titel}
  ...
```

### Regeln für Visual-Vorschläge

- **Mindestens 60% der Folien** müssen ein visuelles Element haben (CHART, DIAGRAM, STOCKIMAGE oder ICON)
- **Datenfolien** → immer CHART oder TABLE
- **Prozess/Ablauf-Folien** → immer DIAGRAM
- **Einleitungs-/Übergangsfolien** → STOCKIMAGE oder ICON
- **Titelfolie** → STOCKIMAGE (Hintergrundbild) oder NONE mit starkem Farbdesign
- **Schlussfolie** → ICON oder NONE

Zeige die Gliederung dem Nutzer und frage: „Passt diese Gliederung? Möchtest du Folien ändern, hinzufügen oder entfernen?"

---

## Schritt 4: Farbpalette und Design festlegen

Wähle basierend auf dem Thema und Stil eine passende Farbpalette. Orientiere dich an diesen Optionen:

| Thema-Bereich | Primary | Secondary | Accent | Background (dunkel) | Background (hell) |
|--------------|---------|-----------|--------|--------------------|--------------------|
| Technologie/KI | `1E2761` | `CADCFC` | `00D4FF` | `0D1117` | `F8FAFC` |
| Wirtschaft/Finanzen | `1B4332` | `95D5B2` | `FFD700` | `1A1A2E` | `F5F5F5` |
| Bildung/Wissenschaft | `065A82` | `1C7293` | `F96167` | `16213E` | `FFFFFF` |
| Gesundheit/Medizin | `028090` | `00A896` | `02C39A` | `1A1A2E` | `F0FFF4` |
| Kreativ/Marketing | `6D2E46` | `A26769` | `ECE2D0` | `1C1C1C` | `FFF8F0` |
| Allgemein/Neutral | `36454F` | `F2F2F2` | `FF6B35` | `212121` | `FFFFFF` |

**Wenn kein Themenbereich passt:** Erstelle eine eigene Palette nach diesen Prinzipien:
- Ein dominierender Primary-Ton (60-70% der visuellen Gewichtung)
- Ein zurückhaltender Secondary-Ton (harmonisch zum Primary)
- Ein kräftiger Accent-Ton (Komplementär- oder Kontrastfarbe für Hervorhebungen)
- Dunkler Background (#1A1A2E bis #0D1117) für Titel-/Schlussfolien
- Heller Background (#FFFFFF bis #F8FAFC) für Inhaltsfolien
- Begründe die Farbwahl dem Nutzer (z.B. „Warmtöne für Geschichte, da klassisch und erdverbunden")

Zeige dem Nutzer die gewählte Palette und frage, ob sie passt.

---

## Schritt 5: Visuelle Assets erstellen

Erstelle alle visuellen Elemente **bevor** du die PPTX baust.

### 5a: Diagramme und Charts (Python)

Für jede Folie mit `CHART` oder `DIAGRAM`:

```bash
python helpers/create_chart.py \
  --type "{bar|hbar|line|pie|donut|area|comparison|process|timeline|funnel}" \
  --title "{Diagramm-Titel}" \
  --data '{JSON-Daten}' \
  --colors '["Primary", "Secondary", "Accent"]' \
  --output "./projekte/{projekt}/output/charts/folie_{nr}_chart.png" \
  --style "{dark|light}" \
  --dpi 200
```

**Wichtig:** Wenn `create_chart.py` den benötigten Diagramm-Typ nicht abdeckt, schreibe ein individuelles Python-Script mit matplotlib. Speichere es als `./projekte/{projekt}/output/charts/folie_{nr}_custom.py` und führe es aus.

### 5b: Stockbilder (Pixabay)

Für jede Folie mit `STOCKIMAGE`:

```bash
python helpers/pixabay_search.py \
  --query "{Suchbegriff auf Englisch}" \
  --output "./projekte/{projekt}/output/images/folie_{nr}_image.jpg" \
  --min-width 1920 \
  --orientation horizontal
```

Falls kein passendes Bild gefunden wird: Informiere den Nutzer und schlage eine Alternative vor (anderer Suchbegriff oder Wechsel zu ICON/DIAGRAM).

### 5c: Icons

Icons werden direkt im pptxgenjs-Script über react-icons eingebunden (siehe Schritt 6).

**Icon-Auswahl:** Wähle semantisch passende Icons aus `react-icons/fa` (Font Awesome) oder `react-icons/md` (Material Design). Beispiele:
- Daten/Statistik → `FaChartLine`, `FaChartBar`
- Prozess/Workflow → `FaCogs`, `MdTimeline`
- Team/Menschen → `FaUsers`, `MdGroups`
- Idee/Konzept → `FaLightbulb`, `MdLightbulb`
- Warnung/Risiko → `FaExclamationTriangle`
- Erfolg/Checkmark → `FaCheckCircle`
- Zeit → `FaClock`, `MdSchedule`
- Kommunikation → `FaComments`, `MdChat`

**Einbindung in pptxgenjs:** Nutze `iconToBase64Png()` aus der PPTX-Skill (react → SVG → PNG via sharp), dann `slide.addImage({ data: iconData, ... })` mit Größe 0.5-1.0 Zoll in farbigen Kreis-Containern.

---

## Schritt 6: PPTX erstellen

Erstelle die Präsentation mit pptxgenjs (Node.js). Speichere das Script als `./projekte/{projekt}/output/create_presentation.js`.

**Dateinamen-Konvention für die .pptx:**
- Standard: `presentation.pptx`
- Bei Änderungswünschen: `presentation_v2.pptx`, `presentation_v3.pptx` usw.
- Der Titel der Präsentation steht im PPTX-Metadatenfeld, nicht im Dateinamen (einfacher zu handhaben)

### Grundstruktur

```javascript
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

// ── Konfiguration ──
const CONFIG = {
  title: "{Titel}",
  author: "{Autor}",
  layout: "LAYOUT_16x9",
  colors: {
    primary: "{Primary}",
    secondary: "{Secondary}",
    accent: "{Accent}",
    bgDark: "{Background-Dark}",
    bgLight: "{Background-Light}",
    textLight: "FFFFFF",
    textDark: "1E293B",
    muted: "94A3B8"
  },
  fonts: {
    heading: "Georgia",
    body: "Calibri"
  }
};

let pres = new pptxgen();
pres.layout = CONFIG.layout;
pres.author = CONFIG.author;
pres.title = CONFIG.title;

// ── Hilfsfunktionen ──

function imageToBase64(filePath) {
  const data = fs.readFileSync(filePath);
  const ext = path.extname(filePath).toLowerCase();
  const mime = ext === ".png" ? "image/png" : "image/jpeg";
  return `${mime};base64,${data.toString("base64")}`;
}

// Factory-Funktionen für wiederverwendbare Styles (WICHTIG: nie Objekte wiederverwenden!)
const makeShadow = () => ({
  type: "outer", color: "000000", blur: 6, offset: 2, angle: 135, opacity: 0.15
});

// ── Folien erstellen ──
// ... (hier werden die Folien Schritt für Schritt aufgebaut)
```

### Layout-Mapping

Für jede Folie aus der Gliederung wählst du ein passendes Layout basierend auf dem Visual-Typ:

| Visual-Typ | Empfohlenes Layout |
|-----------|-------------------|
| CHART | Zweispaltig: Titel oben, Chart links (60% Breite), Key-Insights als Text rechts |
| DIAGRAM | Zentriert: Titel oben, Diagramm mittig (80% Breite), kurze Beschreibung unten |
| STOCKIMAGE (Titelfolie) | Vollflächiger Hintergrund, Titel zentriert mit halbtransparentem Overlay |
| STOCKIMAGE (Inhaltsfolie) | Halbseitig: Bild links (50%), Text mit Stichpunkten rechts |
| ICON (Aufzählung) | Icon-Reihen: 3-4 Icons mit Überschrift + Kurztext. **Maximum 3 Icon-Reihen, wenn zusätzlich eine Kernaussagen-Box vorhanden ist.** Bei 4 Items: entweder weglassen oder als zwei Spalten à 2 Items anordnen. |
| ICON (Konzept) | Großes zentrales Icon, Titel und Erklärung darunter |
| TABLE | Titel oben, Tabelle mittig (90% Breite), ggf. Kernaussage darunter |
| NONE (Titelfolie) | Großer Titel zentriert auf Vollfarben-Hintergrund, Untertitel + Autor/Datum |
| NONE (Schlussfolie) | Zentrierter Schlusssatz, ggf. Kontakt- oder Quellenhinweis |

### Design-Regeln (zwingend beachten!)

1. **Keine Textfolien ohne Visuals** — jede Folie braucht mindestens ein grafisches Element
2. **Layouts variieren** — nicht jede Folie gleich aufbauen
3. **Farben ohne #** — `"1E2761"` nicht `"#1E2761"`
4. **Option-Objekte nie wiederverwenden** — immer Factory-Funktionen nutzen
5. **Bilder als Base64 einbetten** — `imageToBase64()` nutzen
6. **Schriftgrößen**: Titel 36-44pt, Überschriften 20-24pt, Text 14-16pt
7. **Abstände**: Minimum 0.5" Rand, 0.3-0.5" zwischen Elementen
8. **Sandwich-Struktur**: Titelfolie (dunkel) → Inhaltsfolien (hell) → Schlussfolie (dunkel)
9. **Strings sicher escapen** — Strings mit Sonderzeichen (deutsche Anführungszeichen, typografische Apostrophe, Akzente) IMMER mit JavaScript-Backticks umschließen, nicht mit doppelten oder einfachen Anführungszeichen. Sonst bricht der Parser ab.

   Falsch:
   > slide.addText("„Zitat."", { ... });

   Richtig:
   > slide.addText(`„Zitat."`, { ... });
10. **Layout-Validierung vor dem Speichern** — Bevor `pres.writeFile()` aufgerufen wird, berechne für jedes `addText`/`addShape`-Element den unteren Rand (`y + h`) und prüfe gegen alle anderen Elemente. Wenn zwei Elemente sich um mehr als 0,1 Zoll überlappen UND nicht in einem Container-Element liegen: Verkleinere oder verschiebe ein Element. Folienhöhe bei 16:9 = 5,625 Zoll, sicherer Inhaltsbereich = 0,3 bis 5,3 Zoll.

**Pfad zum Speichern:** Da das Skript vom Workspace-Root aus ausgeführt wird, nutze beim `pres.writeFile()` den vollständigen Pfad: `pres.writeFile({ fileName: "./projekte/{projekt}/output/presentation.pptx" })`.

### Ausführen

```bash
node ./projekte/{projekt}/output/create_presentation.js
```

---

## Schritt 7: Qualitätskontrolle

**Dieser Schritt ist Pflicht. Überspringe ihn nie.**

### 7a: Inhaltliche Prüfung

```bash
pip install "markitdown[pptx]" --quiet
python -m markitdown ./projekte/{projekt}/output/presentation.pptx
```

Prüfe im Output:
- Vollständigkeit: Sind alle geplanten Folien vorhanden?
- Reihenfolge: Stimmt die Reihenfolge mit der Gliederung überein?
- Tippfehler und Grammatik
- Fehlende Inhalte oder Platzhalter (z.B. `{Titel}`, `TODO`)
- Konsistenz: Einheitliche Schreibweise von Begriffen, Namen, Zahlen

Bei Problemen: Korrigiere das JS-Script, führe es erneut aus, prüfe nochmal.

**Maximale Korrektur-Schleifen:** 3 Durchgänge. Wenn nach drei Durchgängen noch Probleme bestehen, zeige sie dem Nutzer und frage: „Diese Probleme konnte ich nicht automatisch beheben: [Liste]. Soll ich sie ignorieren, oder hast du eine Lösungsidee?"

### 7b: Visuelle Prüfung durch den Nutzer

Die visuelle Qualität (Layout, Abstände, Farbkontraste, überlappende Elemente) kann nur am fertigen Ergebnis beurteilt werden. Fordere den Nutzer auf:

„Die Präsentation ist fertig unter: `./projekte/{projekt}/output/presentation.pptx`

Bitte öffne sie in PowerPoint oder LibreOffice Impress und prüfe:
- Stimmen Layout und Abstände?
- Sind alle Bilder und Charts sichtbar?
- Gibt es überlappende Elemente oder abgeschnittenen Text?
- Passen die Farben?

Sag mir, was du ändern möchtest — ich passe die Präsentation dann an."

---

## Schritt 8: Abschluss

Wenn der Nutzer zufrieden ist:
1. Zeige den Dateipfad der fertigen .pptx
2. Liste alle verwendeten Quellen auf
3. Weise auf die Pixabay-Lizenzbedingungen hin (falls Stockbilder verwendet): „Die Bilder von Pixabay sind unter der Pixabay Content License kostenlos nutzbar, auch kommerziell. Quellenangabe ist nicht erforderlich, aber empfohlen."

**Bei späteren Änderungswünschen in derselben Session:**
- Erhöhe die Versionsnummer (`presentation_v2.pptx`)
- Lösche die alte Version NICHT — sie dient als Referenz
- Zeige dem Nutzer, was sich geändert hat

---

## Wichtige Hinweise

### Dateistruktur

```
presentation-workflow/                  ← Workspace-Root (hier Claude Code starten)
├── CLAUDE.md                           ← Diese Datei (Workflow-Anleitung)
├── .env                                ← API-Keys (PIXABAY_API_KEY)
├── helpers/                            ← Gemeinsame Tools (nicht kopieren!)
│   ├── pixabay_search.py               ← Bildersuche
│   └── create_chart.py                 ← Diagramm-Erstellung (10 Typen)
│
└── projekte/                           ← Ein Unterordner pro Präsentation
    ├── 2026-04-ki-in-der-lehre/        ← Beispiel-Projekt
    │   ├── research/
    │   │   └── recherche.md
    │   └── output/
    │       ├── charts/
    │       ├── images/
    │       ├── create_presentation.js
    │       └── presentation.pptx
    └── 2026-05-llm-vergleich/          ← Weiteres Projekt
        ├── research/
        └── output/
```

**Wichtig:** Die Helper-Scripts werden immer über den relativen Pfad `./helpers/` vom Workspace-Root aufgerufen. Nicht in Projektordner kopieren.

### Fehlerbehandlung

- **Pixabay-API-Fehler**: Fahre ohne Stockbilder fort, nutze stattdessen Icons oder Diagramme
- **matplotlib-Fehler**: Zeige den Fehler und biete an, den Chart-Code anzupassen
- **pptxgenjs-Fehler**: Prüfe auf häufige Fehler (# in Farben, wiederverwendete Objekte)
- **Kein Internet**: Arbeite nur mit lokalen Ressourcen (Diagramme, Icons, Formen)

### Sprache

- Gliederung und Kommunikation: In der Sprache des Nutzers
- Pixabay-Suchbegriffe: Immer auf Englisch (bessere Ergebnisse)
- Code-Kommentare: Englisch
