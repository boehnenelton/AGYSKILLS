#!/usr/bin/env python3
"""
File:          tweet_thread_composer.py
Description:   Layer 5 Technical Tweet Thread Composer & Character Budget Auditor.
               Drafts, validates, and serializes 5-to-8 tweet engineering threads
               with strict 280-character budget validation, media preset mapping,
               and automated triggering of publication-tweet-automator for visual cards.
Version:       1.0.0
Date Created:  2026-10-25
Author:        Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID: 9c1e2f3a-4b5c-6d7e-8f9a-0b1c2d3e4f5a
"""

import argparse
import json
import logging
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

if sys.version_info < (3, 10):
    sys.stderr.write("tweet_thread_composer requires Python 3.10 or newer.\n")
    sys.exit(1)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [tweet_composer]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger("tweet_thread_composer")

CHAR_LIMIT: int = 280
URL_CHAR_EQUIVALENT: int = 23
URL_REGEX = re.compile(r"https?://\S+")

TWEET_AUTOMATOR_SCRIPT = Path(
    "/data/data/com.termux/files/home/.gemini/config/skills/publication-tweet-automator/scripts/tweet_canvas_generator.py"
)


def calculate_twitter_char_length(text: str) -> int:
    """Calculates Twitter/X effective character length considering 23-char URLs."""
    urls = URL_REGEX.findall(text)
    text_without_urls = URL_REGEX.sub("", text)
    return len(text_without_urls) + (len(urls) * URL_CHAR_EQUIVALENT)


def validate_thread_data(tweets: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
    """Validates thread parts against 280-character budget and sequencing."""
    errors = []
    if len(tweets) < 2 or len(tweets) > 12:
        errors.append(f"Thread length ({len(tweets)}) is outside recommended 2-12 range.")

    for idx, tw in enumerate(tweets, start=1):
        raw_text = tw.get("text", "")
        if not raw_text:
            errors.append(f"Tweet {idx} has empty text.")
            continue

        eff_len = calculate_twitter_char_length(raw_text)
        tw["effective_char_count"] = eff_len
        if eff_len > CHAR_LIMIT:
            errors.append(f"Tweet {idx} exceeds {CHAR_LIMIT} chars (actual: {eff_len}).")

    return len(errors) == 0, errors


def export_thread_markdown(
    project_name: str,
    tweets: List[Dict[str, Any]],
    output_path: Path
) -> None:
    """Exports structured thread to copy-pasteable Markdown file."""
    lines = [
        f"# Technical Launch Thread: {project_name}",
        "",
        f"**Total Tweets:** {len(tweets)}  ",
        "**Character Budget Standard:** <= 280 characters per tweet  ",
        "",
        "---",
        ""
    ]

    for idx, tw in enumerate(tweets, start=1):
        eff_len = calculate_twitter_char_length(tw.get("text", ""))
        lines.append(f"### Tweet {idx}/{len(tweets)} ({eff_len}/280 chars)")
        lines.append(tw.get("text", ""))
        lines.append("")
        if tw.get("media_preset"):
            preset = tw.get("media_preset")
            media_file = tw.get("media_filename", f"tweet_{idx}_{preset}.png")
            lines.append(f"> 🖼️ **Attached Visual ({preset}):** `{media_file}`")
            lines.append("")
        lines.append("---")
        lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    logger.info(f"Rendered thread Markdown to: {output_path}")


def trigger_media_generation(
    tweets: List[Dict[str, Any]],
    tweet_dir: Path,
    prompt_file: str = "tweet_thread.md"
) -> int:
    """Invokes publication-tweet-automator for any tweet specifying a media preset."""
    if not TWEET_AUTOMATOR_SCRIPT.exists():
        logger.warning(f"Tweet automator script not found at {TWEET_AUTOMATOR_SCRIPT}. Skipping media.")
        return 0

    generated_count = 0
    for idx, tw in enumerate(tweets, start=1):
        preset = tw.get("media_preset")
        if not preset:
            continue

        template = tw.get("canvas_template")
        media_name = tw.get("media_filename")
        seek = float(tw.get("seek_progress", 0.5))

        cmd = [
            sys.executable,
            str(TWEET_AUTOMATOR_SCRIPT),
            "--preset", str(preset),
            "--seek", str(seek),
            "--tweet-dir", str(tweet_dir),
            "--prompt-file", prompt_file,
            "--tweet-number", str(idx)
        ]
        if template:
            cmd.extend(["--template", str(template)])
        if media_name:
            cmd.extend(["--output", str(media_name)])

        logger.info(f"Generating visual asset for Tweet {idx} ({preset})...")
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            generated_count += 1
            logger.info(f"Tweet {idx} asset successfully generated.")
        else:
            logger.error(f"Asset generation failed for Tweet {idx}:\n{res.stderr}")

    return generated_count


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Technical Tweet Thread Composer & Character Budget Auditor"
    )
    parser.add_argument(
        "--input",
        type=Path,
        help="JSON file containing tweet thread array: [{'text': '...', 'media_preset': '...'}]"
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        help="Target Markdown file to write rendered thread cards to"
    )
    parser.add_argument(
        "--generate-media",
        action="store_true",
        help="Automatically trigger publication-tweet-automator for tweets with media presets"
    )
    parser.add_argument(
        "--tweet-dir",
        type=Path,
        default=Path("/data/data/com.termux/files/home/generate/prompts/tweet/images"),
        help="Destination directory for generated tweet images"
    )
    parser.add_argument(
        "--project-name",
        type=str,
        default="Software Project",
        help="Name of software project under announcement"
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not args.input or not args.input.exists():
        logger.error("Please supply a valid --input JSON file with thread definitions.")
        sys.exit(1)

    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
    except Exception as exc:
        logger.error(f"Failed to parse input JSON: {exc}")
        sys.exit(1)

    tweets = data if isinstance(data, list) else data.get("tweets", [])
    valid, errors = validate_thread_data(tweets)

    for tw in tweets:
        idx = tweets.index(tw) + 1
        logger.info(f"Tweet {idx}: {tw['effective_char_count']}/280 chars | Media: {tw.get('media_preset', 'None')}")

    if not valid:
        logger.error("Thread validation failed with errors:")
        for err in errors:
            logger.error(f"  - {err}")
        sys.exit(1)

    logger.info(f"Thread validation PASSED ({len(tweets)} tweets, all within 280 chars).")

    if args.output_md:
        export_thread_markdown(args.project_name, tweets, args.output_md)

    if args.generate_media:
        gen_cnt = trigger_media_generation(tweets, args.tweet_dir, args.input.name)
        logger.info(f"Completed media generation for {gen_cnt} visual assets.")


if __name__ == "__main__":
    main()
