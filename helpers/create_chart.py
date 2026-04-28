#!/usr/bin/env python3
"""
Chart & Diagram Creator for Presentations
Usage:
    python create_chart.py --type bar --title "Revenue 2024" \
        --data '{"labels":["Q1","Q2","Q3","Q4"],"values":[120,150,180,210]}' \
        --colors '["1E2761","CADCFC","00D4FF"]' \
        --output ./output/charts/slide_3.png --style dark --dpi 200

    python create_chart.py --type pie --title "Market Share" \
        --data '{"labels":["Company A","Company B","Other"],"values":[45,35,20]}' \
        --output ./output/charts/slide_5.png

    python create_chart.py --type process --title "Workflow" \
        --data '{"steps":["Research","Outline","Design","Review","Publish"]}' \
        --output ./output/charts/slide_7.png

Supported types: bar, hbar, line, pie, donut, area, comparison, process, timeline, funnel
"""

import argparse
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np


# ── Default Styles ──

STYLES = {
    "dark": {
        "bg": "#0D1117",
        "text": "#E6EDF3",
        "grid": "#21262D",
        "muted": "#8B949E",
    },
    "light": {
        "bg": "#FFFFFF",
        "text": "#1E293B",
        "grid": "#E2E8F0",
        "muted": "#94A3B8",
    },
}

DEFAULT_COLORS = ["#1E2761", "#CADCFC", "#00D4FF", "#F96167", "#F9E795", "#2C5F2D"]


def validate_data(data, chart_type):
    """Check that required keys exist for each chart type. Exit with clear message if not."""
    requirements = {
        "bar": ["labels", "values"],
        "hbar": ["labels", "values"],
        "line": ["labels"],  # needs either "values" or "series"
        "pie": ["labels", "values"],
        "donut": ["labels", "values"],
        "area": ["labels"],  # needs either "values" or "series"
        "comparison": ["labels", "series"],
        "process": ["steps"],
        "timeline": ["events"],
        "funnel": ["labels", "values"],
    }
    required = requirements.get(chart_type, [])
    missing = [key for key in required if key not in data]
    if missing:
        print(f"ERROR: Chart type '{chart_type}' requires these keys in --data: {missing}",
              file=sys.stderr)
        print(f"Got keys: {list(data.keys())}", file=sys.stderr)
        sys.exit(1)
    # Special check for line/area: need either "values" or "series"
    if chart_type in ("line", "area") and "values" not in data and "series" not in data:
        print(f"ERROR: Chart type '{chart_type}' requires either 'values' or 'series' in --data",
              file=sys.stderr)
        sys.exit(1)


def hex_to_color(h):
    """Convert '1E2761' or '#1E2761' to matplotlib color."""
    h = h.strip().lstrip("#")
    return f"#{h}"


def setup_style(style_name, fig, ax):
    """Apply dark/light style to figure and axes."""
    s = STYLES.get(style_name, STYLES["light"])
    fig.patch.set_facecolor(s["bg"])
    ax.set_facecolor(s["bg"])
    ax.tick_params(colors=s["muted"], labelsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_color(s["grid"])
    ax.spines["left"].set_color(s["grid"])
    ax.title.set_color(s["text"])
    ax.xaxis.label.set_color(s["muted"])
    ax.yaxis.label.set_color(s["muted"])
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_color(s["muted"])
    return s


def create_bar(data, title, colors, style_name, output, dpi, horizontal=False):
    labels = data["labels"]
    values = data["values"]
    fig, ax = plt.subplots(figsize=(10, 6))
    s = setup_style(style_name, fig, ax)
    bar_colors = [hex_to_color(c) for c in colors[:len(labels)]]
    while len(bar_colors) < len(labels):
        bar_colors.append(bar_colors[-1])

    if horizontal:
        bars = ax.barh(labels, values, color=bar_colors, height=0.6, edgecolor="none")
        ax.set_xlabel("")
        for bar, val in zip(bars, values):
            ax.text(bar.get_width() + max(values)*0.02, bar.get_y() + bar.get_height()/2,
                    f"{val:,.0f}" if isinstance(val, (int, float)) else str(val),
                    va="center", color=s["text"], fontsize=11, fontweight="bold")
    else:
        bars = ax.bar(labels, values, color=bar_colors, width=0.6, edgecolor="none")
        ax.set_ylabel("")
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.02,
                    f"{val:,.0f}" if isinstance(val, (int, float)) else str(val),
                    ha="center", color=s["text"], fontsize=11, fontweight="bold")

    ax.set_title(title, fontsize=16, fontweight="bold", pad=15)
    ax.grid(axis="y" if not horizontal else "x", color=s["grid"], linewidth=0.5, alpha=0.5)
    plt.tight_layout()
    fig.savefig(output, dpi=dpi, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"OK: {output}")


def create_line(data, title, colors, style_name, output, dpi):
    labels = data["labels"]
    fig, ax = plt.subplots(figsize=(10, 6))
    s = setup_style(style_name, fig, ax)

    # Support multiple series
    if "series" in data:
        for i, series in enumerate(data["series"]):
            c = hex_to_color(colors[i % len(colors)])
            ax.plot(labels, series["values"], marker="o", linewidth=2.5,
                    markersize=6, color=c, label=series.get("name", f"Series {i+1}"))
        ax.legend(facecolor=s["bg"], edgecolor=s["grid"], labelcolor=s["text"])
    else:
        c = hex_to_color(colors[0])
        ax.plot(labels, data["values"], marker="o", linewidth=2.5, markersize=6, color=c)

    ax.set_title(title, fontsize=16, fontweight="bold", pad=15)
    ax.grid(color=s["grid"], linewidth=0.5, alpha=0.5)
    plt.xticks(rotation=45 if len(labels) > 6 else 0, ha="right" if len(labels) > 6 else "center")
    plt.tight_layout()
    fig.savefig(output, dpi=dpi, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"OK: {output}")


def create_pie(data, title, colors, style_name, output, dpi, donut=False):
    labels = data["labels"]
    values = data["values"]
    fig, ax = plt.subplots(figsize=(8, 8))
    s = setup_style(style_name, fig, ax)
    pie_colors = [hex_to_color(c) for c in colors[:len(labels)]]
    while len(pie_colors) < len(labels):
        pie_colors.extend([hex_to_color(c) for c in DEFAULT_COLORS])
    pie_colors = pie_colors[:len(labels)]

    wedgeprops = {"edgecolor": s["bg"], "linewidth": 2}
    if donut:
        wedgeprops["width"] = 0.4

    wedges, texts, autotexts = ax.pie(
        values, labels=None, autopct="%1.0f%%", colors=pie_colors,
        wedgeprops=wedgeprops, pctdistance=0.75 if donut else 0.6,
        startangle=90
    )
    # Choose text color per segment based on background brightness
    for t, segment_color in zip(autotexts, pie_colors):
        t.set_fontsize(12)
        t.set_fontweight("bold")
        # Calculate brightness of segment color (luminance formula)
        hex_clean = segment_color.lstrip("#")
        r, g, b = int(hex_clean[0:2], 16), int(hex_clean[2:4], 16), int(hex_clean[4:6], 16)
        brightness = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        t.set_color("#000000" if brightness > 0.6 else "#FFFFFF")

    ax.legend(wedges, labels, loc="center left", bbox_to_anchor=(1, 0.5),
              facecolor=s["bg"], edgecolor=s["grid"], labelcolor=s["text"], fontsize=11)

    ax.set_title(title, fontsize=16, fontweight="bold", pad=20, color=s["text"])
    ax.axis("equal")
    plt.tight_layout()
    fig.savefig(output, dpi=dpi, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"OK: {output}")


def create_process(data, title, colors, style_name, output, dpi):
    """Create a horizontal process/flow diagram."""
    steps = data["steps"]
    n = len(steps)
    fig, ax = plt.subplots(figsize=(max(12, n * 2.5), 4))
    s = setup_style(style_name, fig, ax)
    ax.set_xlim(-0.5, n * 2.5 + 0.5)
    ax.set_ylim(-1, 2.5)
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")
    ax.set_title(title, fontsize=16, fontweight="bold", pad=20, color=s["text"])

    for i, step in enumerate(steps):
        x = i * 2.5 + 0.5
        c = hex_to_color(colors[i % len(colors)])
        # Circle with number
        circle = plt.Circle((x + 0.5, 1.2), 0.35, color=c, zorder=3)
        ax.add_patch(circle)
        ax.text(x + 0.5, 1.2, str(i + 1), ha="center", va="center",
                fontsize=14, fontweight="bold", color="#FFFFFF", zorder=4)
        # Label below
        ax.text(x + 0.5, 0.3, step, ha="center", va="center",
                fontsize=11, color=s["text"], wrap=True,
                bbox=dict(boxstyle="round,pad=0.3", facecolor=s["bg"],
                          edgecolor=s["grid"], linewidth=0.5))
        # Arrow
        if i < n - 1:
            ax.annotate("", xy=(x + 1.5, 1.2), xytext=(x + 0.9, 1.2),
                        arrowprops=dict(arrowstyle="->", color=s["muted"], lw=2))

    plt.tight_layout()
    fig.savefig(output, dpi=dpi, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"OK: {output}")


def create_comparison(data, title, colors, style_name, output, dpi):
    """Create a grouped bar chart for comparison."""
    labels = data["labels"]
    fig, ax = plt.subplots(figsize=(10, 6))
    s = setup_style(style_name, fig, ax)

    x = np.arange(len(labels))
    n_groups = len(data["series"])
    width = 0.7 / n_groups

    for i, series in enumerate(data["series"]):
        c = hex_to_color(colors[i % len(colors)])
        offset = (i - n_groups / 2 + 0.5) * width
        bars = ax.bar(x + offset, series["values"], width, color=c,
                      label=series.get("name", f"Group {i+1}"), edgecolor="none")

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_title(title, fontsize=16, fontweight="bold", pad=15)
    ax.legend(facecolor=s["bg"], edgecolor=s["grid"], labelcolor=s["text"])
    ax.grid(axis="y", color=s["grid"], linewidth=0.5, alpha=0.5)
    plt.tight_layout()
    fig.savefig(output, dpi=dpi, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"OK: {output}")


def create_timeline(data, title, colors, style_name, output, dpi):
    """Create a horizontal timeline."""
    events = data["events"]  # [{"date": "2023", "label": "Event A"}, ...]
    n = len(events)
    fig, ax = plt.subplots(figsize=(max(12, n * 2), 4))
    s = setup_style(style_name, fig, ax)
    ax.axis("off")
    ax.set_title(title, fontsize=16, fontweight="bold", pad=20, color=s["text"])

    y_line = 1.5
    ax.plot([0, n + 0.5], [y_line, y_line], color=s["muted"], linewidth=2, zorder=1)

    for i, event in enumerate(events):
        x = i + 0.75
        c = hex_to_color(colors[i % len(colors)])
        ax.plot(x, y_line, "o", markersize=14, color=c, zorder=3)
        # Alternate above/below
        if i % 2 == 0:
            y_text, y_date = y_line + 0.6, y_line + 0.3
            va = "bottom"
        else:
            y_text, y_date = y_line - 0.6, y_line - 0.3
            va = "top"
        ax.text(x, y_date, event.get("date", ""), ha="center", va=va,
                fontsize=9, color=s["muted"], fontweight="bold")
        ax.text(x, y_text, event.get("label", ""), ha="center", va=va,
                fontsize=10, color=s["text"])

    ax.set_xlim(-0.2, n + 0.7)
    ax.set_ylim(0, 3)
    plt.tight_layout()
    fig.savefig(output, dpi=dpi, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"OK: {output}")


def create_funnel(data, title, colors, style_name, output, dpi):
    """Create a funnel chart."""
    labels = data["labels"]
    values = data["values"]
    n = len(labels)
    fig, ax = plt.subplots(figsize=(8, 6))
    s = setup_style(style_name, fig, ax)
    ax.axis("off")
    ax.set_title(title, fontsize=16, fontweight="bold", pad=15, color=s["text"])

    max_val = max(values)
    min_width_for_inside_label = 3.0  # threshold: below this, put label outside
    for i in range(n):
        width = max(values[i] / max_val * 6, 0.8)  # minimum bar width 0.8
        c = hex_to_color(colors[i % len(colors)])
        y = n - i - 1
        rect = FancyBboxPatch(
            (5 - width / 2, y * 1.1), width, 0.9,
            boxstyle="round,pad=0.05", facecolor=c, edgecolor="none"
        )
        ax.add_patch(rect)
        label_text = f"{labels[i]}  ({values[i]:,.0f})"
        if width >= min_width_for_inside_label:
            # Label fits inside bar
            ax.text(5, y * 1.1 + 0.45, label_text,
                    ha="center", va="center", fontsize=12, color="#FFFFFF", fontweight="bold")
        else:
            # Label goes to the right of the bar
            ax.text(5 + width / 2 + 0.2, y * 1.1 + 0.45, label_text,
                    ha="left", va="center", fontsize=11, color=s["text"], fontweight="bold")

    ax.set_xlim(0, 12)
    ax.set_ylim(-0.5, n * 1.1 + 0.5)
    plt.tight_layout()
    fig.savefig(output, dpi=dpi, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"OK: {output}")


def create_area(data, title, colors, style_name, output, dpi):
    """Create an area chart."""
    labels = data["labels"]
    fig, ax = plt.subplots(figsize=(10, 6))
    s = setup_style(style_name, fig, ax)

    x = range(len(labels))
    if "series" in data:
        for i, series in enumerate(data["series"]):
            c = hex_to_color(colors[i % len(colors)])
            ax.fill_between(x, series["values"], alpha=0.3, color=c)
            ax.plot(x, series["values"], linewidth=2, color=c,
                    label=series.get("name", f"Series {i+1}"))
        ax.legend(facecolor=s["bg"], edgecolor=s["grid"], labelcolor=s["text"])
    else:
        c = hex_to_color(colors[0])
        ax.fill_between(x, data["values"], alpha=0.3, color=c)
        ax.plot(x, data["values"], linewidth=2, color=c)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45 if len(labels) > 6 else 0,
                        ha="right" if len(labels) > 6 else "center")
    ax.set_title(title, fontsize=16, fontweight="bold", pad=15)
    ax.grid(color=s["grid"], linewidth=0.5, alpha=0.5)
    plt.tight_layout()
    fig.savefig(output, dpi=dpi, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"OK: {output}")


# ── Main ──

CHART_TYPES = {
    "bar": lambda d, t, c, s, o, dpi: create_bar(d, t, c, s, o, dpi, horizontal=False),
    "hbar": lambda d, t, c, s, o, dpi: create_bar(d, t, c, s, o, dpi, horizontal=True),
    "line": create_line,
    "pie": lambda d, t, c, s, o, dpi: create_pie(d, t, c, s, o, dpi, donut=False),
    "donut": lambda d, t, c, s, o, dpi: create_pie(d, t, c, s, o, dpi, donut=True),
    "area": create_area,
    "comparison": create_comparison,
    "process": create_process,
    "timeline": create_timeline,
    "funnel": create_funnel,
}


def main():
    parser = argparse.ArgumentParser(description="Create charts and diagrams for presentations")
    parser.add_argument("--type", required=True, choices=list(CHART_TYPES.keys()))
    parser.add_argument("--title", required=True)
    parser.add_argument("--data", required=True, help="JSON string with chart data")
    parser.add_argument("--colors", default=None, help="JSON array of hex colors (without #)")
    parser.add_argument("--output", required=True)
    parser.add_argument("--style", default="light", choices=["dark", "light"])
    parser.add_argument("--dpi", type=int, default=200)

    args = parser.parse_args()

    try:
        data = json.loads(args.data)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON data: {e}", file=sys.stderr)
        sys.exit(1)

    if args.colors:
        try:
            colors = json.loads(args.colors)
        except json.JSONDecodeError:
            colors = DEFAULT_COLORS
    else:
        colors = [c.lstrip("#") for c in DEFAULT_COLORS]

    validate_data(data, args.type)

    # Convert string values to floats where possible
    def coerce_numbers(d):
        if isinstance(d, dict):
            for k, v in d.items():
                if k == "values" and isinstance(v, list):
                    try:
                        d[k] = [float(x) for x in v]
                    except (ValueError, TypeError):
                        print(f"ERROR: 'values' must be numbers, got: {v}", file=sys.stderr)
                        sys.exit(1)
                elif isinstance(v, (dict, list)):
                    coerce_numbers(v)
        elif isinstance(d, list):
            for item in d:
                coerce_numbers(item)
    coerce_numbers(data)

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)

    chart_fn = CHART_TYPES[args.type]
    chart_fn(data, args.title, colors, args.style, args.output, args.dpi)


if __name__ == "__main__":
    main()
