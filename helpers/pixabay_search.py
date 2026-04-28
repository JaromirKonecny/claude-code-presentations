#!/usr/bin/env python3
"""
Pixabay Image Search & Download Helper
Usage:
    python pixabay_search.py --query "artificial intelligence" --output ./output/images/slide_1.jpg
    python pixabay_search.py --query "teamwork office" --output ./img.jpg --min-width 1920 --orientation horizontal
    python pixabay_search.py --query "data visualization" --list-only  (shows results without downloading)
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.parse
import urllib.error


def load_dotenv(filepath=".env"):
    """Load key=value pairs from .env file into os.environ."""
    # Search in current dir, then parent dirs up to 3 levels
    for _ in range(4):
        if os.path.isfile(filepath):
            with open(filepath) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        os.environ.setdefault(key.strip(), value.strip())
            return
        filepath = os.path.join("..", filepath)


load_dotenv()


PIXABAY_API_URL = "https://pixabay.com/api/"


def search_images(query, api_key, orientation="horizontal", min_width=1280,
                  image_type="photo", per_page=5, category=None):
    """Search Pixabay for images. Returns list of image results."""
    params = {
        "key": api_key,
        "q": query,
        "image_type": image_type,
        "orientation": orientation,
        "min_width": min_width,
        "per_page": per_page,
        "safesearch": "true",
        "editors_choice": "false",
    }
    if category:
        params["category"] = category

    url = f"{PIXABAY_API_URL}?{urllib.parse.urlencode(params)}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "PresentationWorkflow/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"ERROR: Pixabay API returned {e.code}: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"ERROR: Could not reach Pixabay API: {e.reason}", file=sys.stderr)
        sys.exit(1)

    if data.get("totalHits", 0) == 0:
        print(f"WARNING: No images found for '{query}'", file=sys.stderr)
        return []

    results = []
    for hit in data.get("hits", []):
        results.append({
            "id": hit["id"],
            "tags": hit.get("tags", ""),
            "url_large": hit.get("largeImageURL", ""),
            "url_web": hit.get("webformatURL", ""),
            "url_preview": hit.get("previewURL", ""),
            "width": hit.get("imageWidth", 0),
            "height": hit.get("imageHeight", 0),
            "user": hit.get("user", ""),
            "page_url": hit.get("pageURL", ""),
        })

    return results


def download_image(url, output_path):
    """Download image from URL to output_path."""
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "PresentationWorkflow/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            with open(output_path, "wb") as f:
                f.write(resp.read())
        print(f"OK: Downloaded to {output_path}")
        return True
    except Exception as e:
        print(f"ERROR: Download failed: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Search and download Pixabay images")
    parser.add_argument("--query", required=True, help="Search query (English recommended)")
    parser.add_argument("--output", default=None, help="Output file path for downloaded image")
    parser.add_argument("--orientation", default="horizontal",
                        choices=["horizontal", "vertical", "all"])
    parser.add_argument("--min-width", type=int, default=1280)
    parser.add_argument("--image-type", default="photo",
                        choices=["photo", "illustration", "vector", "all"])
    parser.add_argument("--category", default=None,
                        help="Category filter: backgrounds, fashion, nature, science, "
                             "education, feelings, health, people, religion, places, "
                             "animals, industry, computer, food, sports, transportation, "
                             "travel, buildings, business, music")
    parser.add_argument("--per-page", type=int, default=5)
    parser.add_argument("--pick", type=int, default=1,
                        help="Which result to download (1=first, 2=second, ...)")
    parser.add_argument("--list-only", action="store_true",
                        help="Only list results, don't download")
    parser.add_argument("--json", action="store_true",
                        help="Output results as JSON")

    args = parser.parse_args()

    api_key = os.environ.get("PIXABAY_API_KEY", "")
    if not api_key:
        print("ERROR: PIXABAY_API_KEY environment variable not set.", file=sys.stderr)
        print("Get a free key at https://pixabay.com/api/docs/", file=sys.stderr)
        sys.exit(1)

    results = search_images(
        query=args.query,
        api_key=api_key,
        orientation=args.orientation,
        min_width=args.min_width,
        image_type=args.image_type,
        per_page=args.per_page,
        category=args.category,
    )

    if not results:
        sys.exit(1)

    if args.json:
        print(json.dumps(results, indent=2))
        return

    if args.list_only:
        for i, r in enumerate(results, 1):
            print(f"  [{i}] {r['width']}x{r['height']}  tags: {r['tags']}")
            print(f"      URL: {r['url_large']}")
            print(f"      by: {r['user']}  |  {r['page_url']}")
        return

    # Download
    pick_idx = args.pick - 1
    if pick_idx >= len(results):
        print(f"WARNING: Only {len(results)} results, picking first.", file=sys.stderr)
        pick_idx = 0

    chosen = results[pick_idx]
    output_path = args.output or f"pixabay_{chosen['id']}.jpg"

    print(f"Downloading: {chosen['width']}x{chosen['height']}  tags: {chosen['tags']}")
    success = download_image(chosen["url_large"], output_path)

    if success:
        # Write attribution info
        attr_path = output_path + ".attribution.txt"
        with open(attr_path, "w") as f:
            f.write(f"Image ID: {chosen['id']}\n")
            f.write(f"Author: {chosen['user']}\n")
            f.write(f"Source: {chosen['page_url']}\n")
            f.write(f"License: Pixabay Content License (free for commercial use)\n")
        print(f"Attribution saved to {attr_path}")


if __name__ == "__main__":
    main()
