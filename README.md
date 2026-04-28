# Presentation Workflow für Claude Code

Ein automatisierter Workflow, mit dem Claude Code (Desktop App) professionelle PowerPoint-Präsentationen erstellt — inklusive Recherche, Diagramme und Stockbilder.

## Features

- **Automatische Recherche** — Claude Code recherchiert selbst per Web Search oder liest eine externe Recherche-Datei ein (z.B. aus Deep Research)
- **Intelligente Visual-Vorschläge** — Für jede Folie wird automatisch der passende Visualisierungstyp vorgeschlagen: Chart, Diagramm, Stockbild, Icon oder Tabelle
- **Diagramme mit Python** — matplotlib-basierte Charts (Bar, Line, Pie, Donut, Area, Process, Timeline, Funnel, Comparison)
- **Stockbilder von Pixabay** — Automatische Bildersuche und Download über die kostenlose Pixabay API
- **Professionelles Design** — Themenspezifische Farbpaletten, Font-Pairings, Sandwich-Struktur (dunkel → hell → dunkel)
- **Integrierte QA** — Automatische Inhalts- und Visualprüfung

## Voraussetzungen

- [Claude Desktop App](https://claude.ai/download) mit Claude Code
- Node.js ≥ 18
- Python ≥ 3.10
- Pixabay API Key (kostenlos: https://pixabay.com/api/docs/)

## Installation

```bash
# 1. Repository klonen
git clone https://github.com/DEIN-USER/presentation-workflow.git
cd presentation-workflow

# 2. Node.js-Abhängigkeiten
npm install -g pptxgenjs react-icons react react-dom sharp

# 3. Python-Abhängigkeiten
pip install matplotlib Pillow requests

# 4. API Key konfigurieren
cp .env.example .env
# Trage deinen Pixabay API Key in .env ein
# Dann: export PIXABAY_API_KEY="dein-key"
```

## Verwendung

1. Öffne die Claude Desktop App
2. Navigiere in das Projektverzeichnis
3. Sage Claude Code: **„Erstelle eine Präsentation"**
4. Claude Code führt dich durch den Workflow:
   - Thema, Zielgruppe, Folienanzahl festlegen
   - Recherche-Quelle wählen
   - Gliederung mit Visual-Vorschlägen reviewen
   - Farbpalette bestätigen
   - Präsentation generieren und prüfen

## Projektstruktur

```
presentation-workflow/
├── CLAUDE.md              ← Workflow-Anleitung für Claude Code
├── README.md              ← Diese Datei
├── .env.example           ← API-Key-Template
├── helpers/
│   ├── pixabay_search.py  ← Bildersuche & Download
│   └── create_chart.py    ← Diagramm-Erstellung (10 Typen)
│
└── projekte/              ← Ein Unterordner pro Präsentation
    └── YYYY-MM-kurzname/
        ├── research/      ← Recherche-Dateien
        └── output/        ← Generierte Dateien
            ├── charts/    ← PNG-Diagramme
            ├── images/    ← Stockbilder
            └── *.pptx     ← Fertige Präsentation
```

## Chart-Typen

| Typ | Beschreibung | Daten-Format |
|-----|-------------|--------------|
| `bar` | Vertikales Balkendiagramm | `{"labels": [...], "values": [...]}` |
| `hbar` | Horizontales Balkendiagramm | `{"labels": [...], "values": [...]}` |
| `line` | Liniendiagramm | `{"labels": [...], "values": [...]}` oder mit `"series"` |
| `pie` | Kreisdiagramm | `{"labels": [...], "values": [...]}` |
| `donut` | Donut-Diagramm | `{"labels": [...], "values": [...]}` |
| `area` | Flächendiagramm | `{"labels": [...], "values": [...]}` |
| `comparison` | Gruppiertes Balkendiagramm | `{"labels": [...], "series": [{"name": "...", "values": [...]}]}` |
| `process` | Prozessdiagramm (Kreise + Pfeile) | `{"steps": ["Step 1", "Step 2", ...]}` |
| `timeline` | Zeitstrahl | `{"events": [{"date": "2024", "label": "Event A"}, ...]}` |
| `funnel` | Trichterdiagramm | `{"labels": [...], "values": [...]}` |

## Ohne Pixabay-Key

Der Workflow funktioniert auch ohne Pixabay-Key. In dem Fall werden statt Stockbildern automatisch Icons (react-icons) oder zusätzliche Diagramme verwendet.

## Lizenz

MIT

## Danksagung

- [pptxgenjs](https://github.com/nicepkg/pptxgenjs) — PPTX-Erstellung
- [Pixabay API](https://pixabay.com/api/docs/) — Kostenlose Stockbilder
- [react-icons](https://react-icons.github.io/react-icons/) — Icon-Bibliothek
- [matplotlib](https://matplotlib.org/) — Diagramme
