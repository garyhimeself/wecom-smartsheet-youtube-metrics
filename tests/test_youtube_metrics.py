import importlib.util
import json
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "youtube_metrics.py"
SPEC = importlib.util.spec_from_file_location("youtube_metrics", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class YouTubeMetricsTests(unittest.TestCase):
    def test_extracts_short_link_id(self):
        self.assertEqual(MODULE.parse_video_id("https://youtu.be/abcDEF12345"), "abcDEF12345")

    def test_rejects_non_youtube_link(self):
        self.assertIsNone(MODULE.parse_video_id("https://example.com/video"))

    def test_splits_more_than_fifty_video_ids(self):
        self.assertEqual(MODULE.chunked(["a"] * 51), [["a"] * 50, ["a"]])

    def test_maps_public_api_metrics(self):
        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return json.dumps(
                    {
                        "items": [
                            {
                                "id": "abcDEF12345",
                                "snippet": {"publishedAt": "2026-01-02T03:04:05Z"},
                                "statistics": {"viewCount": "42", "likeCount": "7"},
                            }
                        ]
                    }
                ).encode("utf-8")

        result = MODULE.fetch_metrics(["abcDEF12345"], "test-key", lambda _: Response())

        self.assertEqual(
            result["abcDEF12345"],
            {"view_count": 42, "like_count": 7, "published_at": "2026-01-02T03:04:05Z"},
        )
