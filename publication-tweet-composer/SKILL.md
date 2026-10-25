---
name: publication-tweet-composer
description: >-
  Plan, structure, draft, and audit technical Twitter/X threads (5-8 tweets) and promotional tweet decks adhering to strict 280-character budget ceilings, high-signal engineering hook structures, URL slot calculations, and automated canvas media pairing. Use when drafting viral launch threads for software repositories, auditing tweet drafts for character overflow, mapping tweets to Twitter-optimized canvas media cards, or generating copy-pasteable social media release packs. Do NOT use for raw SVG canvas image rendering (use publication-tweet-automator), multi-page technical manuals (use code-manual-builder), or long-form technical blog posts (use publication-blog-post-writer).
---

# publication-tweet-composer (Layer 5 Technical Tweet Thread & Social Media Architect)

- **Target Architecture**: Cross-Platform (Termux Android, Linux, macOS)
- **Architectural Tier**: Layer 5 (L5) Domain Use Cases, Blueprints & Writers
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
- **RELATIONAL_ID**: `4e2a1b3c-5d6f-7a8b-9c0d-1e2f3a4b5c6d`
- **Version**: `1.0.0`
- **Downstream Collaborator**: `publication-tweet-automator` (Layer 3 Media Automation)

---

## 1. When to Use & When NOT to Use

### Use This Skill When:
- Composing multi-part technical announcement threads (5 to 8 tweets) from repository source code, README files, or release manifests (`bejson_project.json`).
- Auditing tweet copy to guarantee every individual tweet strictly satisfies the 280-character limit (with 23-character t.co URL reservation).
- Structuring engineering hook archetypes: The Bold Technical Claim, The Flawed Consensus Attack, The Hard Benchmark Drop, or The Code Walkthrough.
- Assigning visual media presets (`landscape`, `square`, `banner`, `portrait`, `icon`) and linking them directly to `publication-tweet-automator`.
- Exporting copy-pasteable social release markdown documents with attached image previews.

### When NOT to Use:
- Do NOT use for headless Playwright canvas image rendering and disk copying (use `publication-tweet-automator`).
- Do NOT use for authoring 4-part long-form technical blog articles (use `publication-blog-post-writer`).
- Do NOT use for compiling multi-page HTML documentation websites or e-books (use `code-manual-builder`).
- Do NOT use for single-page editorial HTML layouts (use `publication-html-builder`).

---

## 2. Technical Thread Architecture & Narrative Pacing

The skill enforces a disciplined 6-part narrative arc designed to maximize developer engagement and technical credibility:

```
[Tweet 1: Hook & Scope] -> [Tweet 2: Flawed Consensus] -> [Tweet 3: Architecture]
           |                                                       |
     (16:9 Landscape)                                        (2:1 Banner)
           v                                                       v
[Tweet 4: Hard Benchmarks] -> [Tweet 5: Terminal Quickstart] -> [Tweet 6: CTA & Links]
           |                                                       |
     (1:1 Square Cube)                                      (Repo URL + Tags)
```

1. **Tweet 1 (The Hook & Scope)**: Introduce the software name and the single most provocative engineering innovation in the opening sentence. Attach a 16:9 Landscape Card (`1200x675` px).
2. **Tweet 2 (The Flawed Consensus)**: Attack legacy industry bloat (e.g., repeating JSON keys, cloud lock-in, sluggish runtimes).
3. **Tweet 3 (Under the Hood)**: Dissect core mechanics: event loops, atomic operations, in-memory caches, or AST parsers. Attach a 2:1 Banner (`1200x600` px).
4. **Tweet 4 (Hard Benchmarks)**: Present empirical data: token savings, memory footprints, passing test counts. Attach a 1:1 Square Cube Spotlight (`800x800` px).
5. **Tweet 5 (Developer Quickstart)**: Provide a copy-pasteable 2-line terminal command or API invocation.
6. **Tweet 6 (CTA & Links)**: Link to the repository, credit creator Elton Boehnen, and include technical hashtags (#DevTools #OpenSource #SystemsProgramming).

---

## 3. Character Budgeting & URL Slot Rules

- **Hard Limit**: 280 characters per tweet.
- **Link Budget**: Every URL occupies exactly 23 characters under Twitter/X t.co wrapping, regardless of raw string length.
- **Target Body Budget**: Draft tweets to 220-250 characters to prevent cramped text and allow flexible hashtag tuning.

---

## 4. Operational Execution via CLI

The composer is driven by `scripts/tweet_thread_composer.py`:

### Step 1: Validate Thread Character Budgets
```bash
python3 scripts/tweet_thread_composer.py \
    --input drafts/newagent_launch_thread.json \
    --project-name "NewAgent"
```

### Step 2: Validate and Export Rendered Markdown
```bash
python3 scripts/tweet_thread_composer.py \
    --input drafts/newagent_launch_thread.json \
    --project-name "NewAgent" \
    --output-md /data/data/com.termux/files/home/generate/prompts/tweet/NewAgent_Launch_Thread.md
```

### Step 3: End-to-End Pipeline (Draft + Image Generation)
Validate thread text and automatically invoke `publication-tweet-automator` to generate and copy all attached canvas images:
```bash
python3 scripts/tweet_thread_composer.py \
    --input drafts/newagent_launch_thread.json \
    --project-name "NewAgent" \
    --output-md /data/data/com.termux/files/home/generate/prompts/tweet/NewAgent_Launch_Thread.md \
    --generate-media \
    --tweet-dir /data/data/com.termux/files/home/generate/prompts/tweet/images
```

---

## 5. Headless agy Execution Protocol

When invoking via Antigravity CLI, enforce `--sandbox` isolation:

```bash
agy --sandbox -p "Compose a 6-tweet technical launch thread for repository /storage/emulated/0/Admin/Dev/Repos/NewAgent, validate all tweets under 280 characters, and export to ~/generate/prompts/tweet/NewAgent_Thread.md"
```

Negative Constraints: Zero conversational filler. Do not exceed 280 characters per tweet.

---

## 6. BEJSON Manifest Integration (Format 104a)

Thread structures map to BEJSON 104a schemas in `assets/tweet_thread_template.104a.bejson`:

```json
{
  "Format": "BEJSON",
  "Format_Version": "104a",
  "Format_Creator": "Elton Boehnen",
  "Records_Type": ["TweetThreadRecord"],
  "Fields": [
    {"name": "thread_id",       "type": "string"},
    {"name": "project_name",    "type": "string"},
    {"name": "tweet_index",     "type": "integer"},
    {"name": "tweet_role",      "type": "string"},
    {"name": "tweet_text",      "type": "string"},
    {"name": "char_count",      "type": "integer"},
    {"name": "media_preset",    "type": "string"},
    {"name": "canvas_template", "type": "string"},
    {"name": "media_filename",  "type": "string"},
    {"name": "status",          "type": "string"}
  ],
  "Values": []
}
```

In runtime operations, fields are accessed dynamically via `field_map`:
```python
field_map = {f["name"]: idx for idx, f in enumerate(doc["Fields"])}
tweet_text = row[field_map["tweet_text"]]
```
