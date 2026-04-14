import time
import random
import json
from json import JSONDecodeError
from pathlib import Path
from ddgs import DDGS

def search_images(query, region="uk-en", max_results=50, attempts=10, base_sleep=0.5):
    for attempt in range(attempts):
        try:
            with DDGS(timeout=20) as ddgs:
                results = list(ddgs.images(query, region=region, max_results=max_results))
                if results:
                    return results
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")

            sleep_time = base_sleep ** attempt + random.uniform(0, 1)
            print(f"Retrying in {sleep_time:.1f}s...")
            time.sleep(sleep_time)

    raise RuntimeError(f"Failed to fetch images after {attempts} attempts")

def load_seen_urls(cache_file="seen_urls.json"):
    if Path(cache_file).exists():
        try:
            print(f"Loading cached URLs from {cache_file}")
            return set(json.loads(Path(cache_file).read_text()))
        except JSONDecodeError:
            print("cache file exists but is empty")
            return set()
    print("Path does not exist, creating new file...")
    return set()

def save_seen_urls(seen_urls, cache_file="seen_urls.json"):
    if not Path(cache_file).exists():
        open(cache_file, "w")

    Path(cache_file).write_text(json.dumps(list(seen_urls)))

def collect_images(query, region="uk-en", target=100, attempts=10, cache_file="seen_urls.json"):
    seen_urls = load_seen_urls(cache_file)
    collected_images = []

    while len(collected_images) < target:
        results = search_images(query, region, max_results=target * 2, attempts=attempts, base_sleep=0.5)
        new_results = [r for r in results if r["image"] not in seen_urls]

        for r in new_results:
            collected_images.append(r)
            seen_urls.add(r["image"])

        save_seen_urls(seen_urls, cache_file)

        if not new_results:
            break

    return collected_images