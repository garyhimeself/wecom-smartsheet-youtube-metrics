"""Read public YouTube metrics without modifying any external system."""

from __future__ import annotations

import argparse
import json
import os
import re
from collections.abc import Callable
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import urlopen


VIDEO_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")


def parse_video_id(url: str) -> str | None:
    """Extract a public YouTube video ID from a supported URL."""
    parsed = urlparse(url)
    host = parsed.netloc.lower().removeprefix("www.")
    candidate: str | None = None
    if host == "youtu.be":
        candidate = parsed.path.strip("/").split("/")[0]
    elif host in {"youtube.com", "m.youtube.com", "music.youtube.com"}:
        parts = [part for part in parsed.path.split("/") if part]
        if parsed.path == "/watch":
            candidate = parse_qs(parsed.query).get("v", [None])[0]
        elif len(parts) >= 2 and parts[0] in {"shorts", "embed"}:
            candidate = parts[1]
    return candidate if candidate and VIDEO_ID.fullmatch(candidate) else None


def chunked(items: list[str], size: int = 50) -> list[list[str]]:
    """Split IDs into YouTube Data API request batches."""
    if size <= 0:
        raise ValueError("size must be greater than zero")
    return [items[index : index + size] for index in range(0, len(items), size)]


def fetch_metrics(
    video_ids: list[str], api_key: str, opener: Callable = urlopen
) -> dict[str, dict]:
    """Return public view count, like count, and publication time by video ID."""
    metrics: dict[str, dict] = {}
    for batch in chunked(video_ids):
        query = urlencode(
            {"part": "snippet,statistics", "id": ",".join(batch), "key": api_key}
        )
        with opener(f"https://www.googleapis.com/youtube/v3/videos?{query}") as response:
            payload = json.loads(response.read().decode("utf-8"))
        for item in payload.get("items", []):
            statistics = item.get("statistics", {})
            view_count = statistics.get("viewCount")
            if item.get("id") and view_count is not None:
                metrics[item["id"]] = {
                    "view_count": int(view_count),
                    "like_count": int(statistics["likeCount"])
                    if statistics.get("likeCount") is not None
                    else None,
                    "published_at": item.get("snippet", {}).get("publishedAt"),
                }
    return metrics


def load_local_api_key(env_file: Path) -> str:
    """Load only YOUTUBE_API_KEY from a local, untracked .env file."""
    key = os.environ.get("YOUTUBE_API_KEY", "").strip()
    if key:
        return key
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            if line.startswith("YOUTUBE_API_KEY="):
                return line.split("=", 1)[1].strip()
    raise RuntimeError("Set YOUTUBE_API_KEY in the environment or local .env file.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect public YouTube video metrics.")
    parser.add_argument("--url", action="append", required=True, help="Public YouTube URL")
    parser.add_argument("--env-file", type=Path, default=Path(__file__).parents[1] / ".env")
    args = parser.parse_args()

    ids = [video_id for url in args.url if (video_id := parse_video_id(url))]
    result = fetch_metrics(ids, load_local_api_key(args.env_file))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
