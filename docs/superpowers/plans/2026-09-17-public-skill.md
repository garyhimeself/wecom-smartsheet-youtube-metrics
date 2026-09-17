# WeCom SmartSheet YouTube Metrics Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a reusable Skill that safely reads YouTube links from WeCom SmartSheets and, after explicit approval, writes verified public video metrics back to mapped fields.

**Architecture:** A concise `SKILL.md` routes the agent through WeCom authorization, schema inspection, deterministic YouTube API collection, row-level preview, approval-gated update, and read-back verification. A Python helper handles public YouTube URL normalization and batches video IDs in groups of 50; no credential or spreadsheet identifier is stored in the repository.

**Tech Stack:** Codex Agent Skills format, Python standard library, YouTube Data API v3, WeCom CLI.

## Global Constraints

- Never commit `.env`, API keys, Webhook URLs, bot secrets, or spreadsheet URLs.
- Only update explicitly mapped metric fields after a user approves the displayed row-level preview.
- Use YouTube `videos.list` with `snippet,statistics`; preserve unavailable videos and unsupported links without overwriting cells.
- WeCom CLI is the default existing-record update path; use Webhook only when its documented constraints permit it.

---

### Task 1: Write and verify the metric collector

**Files:**
- Create: `tests/test_youtube_metrics.py`
- Create: `scripts/youtube_metrics.py`

**Interfaces:**
- Produces: `parse_video_id(url: str) -> str | None`
- Produces: `fetch_metrics(video_ids: list[str], api_key: str, opener) -> dict[str, dict]`

- [ ] **Step 1: Write failing tests**

```python
assert parse_video_id("https://youtu.be/abcDEF12345") == "abcDEF12345"
assert parse_video_id("https://example.com/video") is None
assert fetch_metrics(["abcDEF12345"], "key", fake_opener)["abcDEF12345"]["view_count"] == 42
```

- [ ] **Step 2: Run tests and verify failure**

Run: `python -m unittest tests/test_youtube_metrics.py -v`

Expected: FAIL because `scripts/youtube_metrics.py` does not exist.

- [ ] **Step 3: Implement only URL parsing, 50-ID batching, and read-only API response mapping**

- [ ] **Step 4: Run tests and verify pass**

Run: `python -m unittest tests/test_youtube_metrics.py -v`

Expected: PASS.

### Task 2: Create the public Skill package

**Files:**
- Create: `SKILL.md`
- Create: `README.md`
- Create: `.env.example`
- Create: `.gitignore`
- Create: `LICENSE`

**Interfaces:**
- Consumes: a WeCom SmartSheet link, mapped field names, and local `YOUTUBE_API_KEY`.
- Produces: an approval-required update preview and a verified update report.

- [ ] **Step 1: Write the Skill with required authority boundaries and the exact read-preview-confirm-write-verify workflow**
- [ ] **Step 2: Write concise initialization instructions for non-technical marketers**
- [ ] **Step 3: Add blank configuration template, secret exclusions, and MIT license**
- [ ] **Step 4: Run the Skill validator and secret scan**

### Task 3: Publish safely

**Files:**
- Modify: all repository files only if validation identifies a concrete issue.

- [ ] **Step 1: Verify tests, syntax, validator, and secret scan pass**
- [ ] **Step 2: Inspect the staged public diff for credentials, private links, and internal identifiers**
- [ ] **Step 3: Create the public GitHub repository and push the verified initial commit**
