#!/usr/bin/env python3
"""
Tool:            compose_template_plan.py
Skill:           template-plan-composer (Layer 5)
Description:     Composes exhaustive, taxonomy-aware template architecture plans and scaffolds
                 required template suites for site archetypes (blog, docs, video hub, portfolio, etc.).
Version:         1.0.0
Release_Version: 300
Date Created:    2026-10-24
Author:          Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
Format_Creator:  Elton Boehnen
RELATIONAL_ID:   b84e2a10-4f3d-4c8e-a91b-6d0e8c5a2f30
"""

import os
import sys
import json
import logging
import argparse
from pathlib import Path
from typing import Any, Dict, List, Optional

VERSION = "1.0.0"
RELEASE_VERSION = "300"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
app_logger = logging.getLogger("compose_template_plan")

# Canonical Domain Archetype Catalog
ARCHETYPE_BLUEPRINT_ROSTER: Dict[str, Dict[str, Any]] = {
    "blog": {
        "archetype_id": "blog",
        "display_name": "Editorial Blog & Magazine",
        "primary_entity_prefixes": ["blog_", "post_", "cat_", "author_", "comment_", "tag_"],
        "templates": [
            {
                "template_key": "home_master_index",
                "filename": "index.html",
                "semantic_role": "Portal Landing Page & Latest Post Stream",
                "bound_prefixes": ["post_", "cat_", "author_"],
                "target_layers": [1, 2, 4],
                "views": ["Hero Featured Post", "Category Filter Bar", "Latest Posts 8-Lane Grid", "Author Byline Badges"],
                "forms": ["Newsletter Subscription Input", "Quick Search Input"]
            },
            {
                "template_key": "post_single_view",
                "filename": "post.html",
                "semantic_role": "Single Article & Long-Form Reading View",
                "bound_prefixes": ["post_", "author_", "cat_", "tag_"],
                "target_layers": [1, 2, 4],
                "views": ["Hero Header & Metadata Bar", "Prose Body Container", "Tags List", "Sequential Next/Prev Navigation"],
                "forms": ["Social Share Action Buttons"]
            },
            {
                "template_key": "content_page",
                "filename": "page.html",
                "semantic_role": "Static Standalone Content Page (About, Terms, Privacy)",
                "bound_prefixes": ["page_", "author_"],
                "target_layers": [1, 2, 4],
                "views": ["Page Title Bar", "Document Prose Body", "Structured Spec Table"],
                "forms": []
            },
            {
                "template_key": "category_tag_feed",
                "filename": "feed.html",
                "semantic_role": "Category & Tag Filtered Post Archive Feed",
                "bound_prefixes": ["cat_", "post_", "tag_"],
                "target_layers": [1, 2, 4],
                "views": ["Hierarchical Breadcrumb Bar", "Active Category Banner", "Sorted Post Stream", "Paging Controls"],
                "forms": ["Sort Order Dropdown"]
            },
            {
                "template_key": "author_profile",
                "filename": "author.html",
                "semantic_role": "Author Profile & Published Works Showcase",
                "bound_prefixes": ["author_", "post_"],
                "target_layers": [1, 2, 4],
                "views": ["Author Bio Card & Avatar", "Published Articles Metric Readout", "Author Post Archive List"],
                "forms": []
            },
            {
                "template_key": "contact_inquiry",
                "filename": "contact.html",
                "semantic_role": "Contact & Reader Inquiry Interface",
                "bound_prefixes": ["inquiry_"],
                "target_layers": [1, 2, 4],
                "views": ["Contact Info Details", "Response Time Telemetry Badge"],
                "forms": ["Inquiry Form (Name, Email, Subject Select, Message Textarea, Submit Action)"]
            },
            {
                "template_key": "comments_discussion_feed",
                "filename": "comments.html",
                "semantic_role": "Threaded Discussion & Reader Feedback Component",
                "bound_prefixes": ["comment_", "post_"],
                "target_layers": [1, 2, 3],
                "views": ["Comment Count Readout", "Threaded Reply Tree List"],
                "forms": ["Comment Submission Input Group", "Reply Form Dialog Overlay (Layer 3)"]
            }
        ]
    },
    "documentation": {
        "archetype_id": "documentation",
        "display_name": "Technical Documentation & API Compendium",
        "primary_entity_prefixes": ["doc_", "cat_", "spec_", "version_"],
        "templates": [
            {
                "template_key": "doc_master_index",
                "filename": "index.html",
                "semantic_role": "Knowledge Base Hub & Category Cards",
                "bound_prefixes": ["cat_", "doc_"],
                "target_layers": [1, 2, 4],
                "views": ["Hero Search Bar", "Architecture Overview Cards", "Recent Updates Stream"],
                "forms": ["Live Query Filter"]
            },
            {
                "template_key": "doc_article",
                "filename": "article.html",
                "semantic_role": "Technical Specification & Code Guide",
                "bound_prefixes": ["doc_", "spec_"],
                "target_layers": [1, 2, 4],
                "views": ["Split-Pane Sidebar Navigation", "TOC Leader Lines", "Code Block Containers", "Parameter Tables"],
                "forms": ["Copy Code Action", "Feedback Thumbs"]
            },
            {
                "template_key": "doc_category_feed",
                "filename": "feed.html",
                "semantic_role": "Module Category Archive Feed",
                "bound_prefixes": ["cat_", "doc_"],
                "target_layers": [1, 2, 4],
                "views": ["Subcategory Pill Bar", "Article Index Table", "Sequential Paging Bar"],
                "forms": []
            },
            {
                "template_key": "doc_consolidated_ebook",
                "filename": "ebook.html",
                "semantic_role": "Single-File Printable & Offline Manual Compendium",
                "bound_prefixes": ["doc_", "version_"],
                "target_layers": [1, 2],
                "views": ["Cover Page Header", "Dotted Leader TOC", "Linear Sequential Chapters", "Colophon Footer"],
                "forms": ["Print / Export PDF Action"]
            }
        ]
    },
    "video_hub": {
        "archetype_id": "video_hub",
        "display_name": "Video Streaming Archive & Hub",
        "primary_entity_prefixes": ["video_", "channel_", "cat_", "playlist_"],
        "templates": [
            {
                "template_key": "video_master_index",
                "filename": "index.html",
                "semantic_role": "Video Portal Landing & Trending Carousel",
                "bound_prefixes": ["video_", "channel_", "cat_"],
                "target_layers": [1, 2, 4],
                "views": ["Featured Video Hero Stage", "Trending 16:9 Video Cards Grid", "Channel Spotlight Bar"],
                "forms": ["Search Input"]
            },
            {
                "template_key": "video_player",
                "filename": "player.html",
                "semantic_role": "Primary Video Playback & Playlist Queue",
                "bound_prefixes": ["video_", "playlist_", "channel_"],
                "target_layers": [1, 2, 4],
                "views": ["16:9 Native Video Viewport", "Playback Action Bar", "Up Next Playlist Sidebar Queue", "Metadata Specs Table"],
                "forms": ["Resolution Quality Toggle", "Theater Mode Switch"]
            },
            {
                "template_key": "video_channel",
                "filename": "channel.html",
                "semantic_role": "Creator Channel Profile & Video Archive",
                "bound_prefixes": ["channel_", "video_"],
                "target_layers": [1, 2, 4],
                "views": ["Channel Banner & Avatar", "Subscriber & Video Count Metrics", "Uploads Video Grid"],
                "forms": ["Subscribe Toggle Button"]
            }
        ]
    },
    "portfolio": {
        "archetype_id": "portfolio",
        "display_name": "Creative Portfolio & Case Studies",
        "primary_entity_prefixes": ["project_", "asset_", "client_", "service_"],
        "templates": [
            {
                "template_key": "portfolio_index",
                "filename": "index.html",
                "semantic_role": "Showcase Home & Project Grid",
                "bound_prefixes": ["project_", "asset_"],
                "target_layers": [1, 2, 4],
                "views": ["Hero Intro Header", "Discipline Filter Pills", "Project Card Matrix", "Client Logos Bar"],
                "forms": []
            },
            {
                "template_key": "project_showcase",
                "filename": "project.html",
                "semantic_role": "In-Depth Project Case Study View",
                "bound_prefixes": ["project_", "asset_", "client_"],
                "target_layers": [1, 2, 4],
                "views": ["Project Hero Banner", "Key Performance Indicator Metrics", "Asset Gallery", "Outcome Prose Body"],
                "forms": ["Live Demo Link Action"]
            },
            {
                "template_key": "asset_lightbox",
                "filename": "gallery.html",
                "semantic_role": "Interactive Media Lightbox Overlay View",
                "bound_prefixes": ["asset_", "project_"],
                "target_layers": [1, 2, 3],
                "views": ["Masonry Image Grid", "Layer 3 Fullscreen Lightbox Modal (z: 96)"],
                "forms": ["Prev / Next Asset Switchers"]
            }
        ]
    }
}


def build_bejson_template_plan(
    archetype_key: str,
    project_name: str,
    custom_templates_list: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Compiles a BEJSON 104a compliant Site Template Plan record with field mapping.
    """
    archetype_data = ARCHETYPE_BLUEPRINT_ROSTER.get(archetype_key, ARCHETYPE_BLUEPRINT_ROSTER["blog"])
    templates_roster = custom_templates_list or archetype_data["templates"]

    fields_definition = [
        {"name": "Record_Type_Parent", "type": "STRING"},
        {"name": "template_key",       "type": "STRING"},
        {"name": "filename",           "type": "STRING"},
        {"name": "semantic_role",      "type": "STRING"},
        {"name": "bound_prefixes",     "type": "ARRAY"},
        {"name": "target_layers",      "type": "ARRAY"},
        {"name": "views_list",         "type": "ARRAY"},
        {"name": "forms_list",         "type": "ARRAY"}
    ]

    values_matrix = []
    for item in templates_roster:
        values_matrix.append([
            "PlannedTemplateRecord",
            item["template_key"],
            item["filename"],
            item["semantic_role"],
            item.get("bound_prefixes", []),
            item.get("target_layers", [1, 2, 4]),
            item.get("views", []),
            item.get("forms", [])
        ])

    return {
        "Format": "BEJSON",
        "Format_Version": "104a",
        "Format_Creator": "Elton Boehnen",
        "Project_Name": project_name,
        "Archetype_Id": archetype_key,
        "Archetype_Display_Name": archetype_data["display_name"],
        "Primary_Entity_Prefixes": archetype_data["primary_entity_prefixes"],
        "Total_Templates_Metric": len(values_matrix),
        "Records_Type": ["PlannedTemplateRecord"],
        "Fields": fields_definition,
        "Values": values_matrix
    }


def generate_markdown_plan(plan_bejson: Dict[str, Any]) -> str:
    """
    Renders a clean, comprehensive Markdown architectural specification from the plan.
    """
    lines = [
        f"# Site Template Architecture Plan: {plan_bejson['Project_Name']}",
        f"\n**Archetype**: {plan_bejson['Archetype_Display_Name']} (`{plan_bejson['Archetype_Id']}`)",
        f"**Primary Entity Prefixes**: `{', '.join(plan_bejson['Primary_Entity_Prefixes'])}`",
        f"**Total Required Templates**: `{plan_bejson['Total_Templates_Metric']}`\n",
        "---",
        "\n## Required Template Suite Specifications\n",
        "| Template Key | Filename | Semantic Role | Bound Prefixes | Layers |",
        "|---|---|---|---|---|"
    ]

    for row in plan_bejson["Values"]:
        _, t_key, fname, role, prefixes, layers, _, _ = row
        prefix_str = ", ".join(prefixes)
        layer_str = ", ".join(f"L{l}" for l in layers)
        lines.append(f"| `{t_key}` | `{fname}` | {role} | `{prefix_str}` | `{layer_str}` |")

    lines.append("\n---\n")
    lines.append("## Detailed Template Breakdown & Component Projections\n")

    for row in plan_bejson["Values"]:
        _, t_key, fname, role, prefixes, layers, views, forms = row
        lines.append(f"### Template: `{fname}` (`{t_key}`)")
        lines.append(f"- **Role**: {role}")
        lines.append(f"- **Bound Entity Taxonomies**: `{', '.join(prefixes)}`")
        lines.append(f"- **Active Stacking Depth**: {', '.join(f'Layer {l} (z: {l*32})' for l in layers)}")
        lines.append("- **View Projections (Presentational)**:")
        for v in views:
            lines.append(f"  - {v}")
        if forms:
            lines.append("- **Interactive Form Controls**:")
            for f in forms:
                lines.append(f"  - {f}")
        lines.append("")

    lines.append("---")
    lines.append("\nAuthor: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton")
    return "\n".join(lines)


def scaffold_zero_filler_templates(
    plan_bejson: Dict[str, Any],
    target_directory: Path
) -> List[Path]:
    """
    Materializes bare-bones zero-filler BEHTML template files on disk for each planned template.
    """
    target_directory.mkdir(parents=True, exist_ok=True)
    created_paths = []

    for row in plan_bejson["Values"]:
        _, t_key, fname, role, prefixes, layers, views, forms = row
        dest_path = target_directory / fname

        views_markup_items = [
            f'      <!-- View Component: {v} -->\n      <div class="behtml-card" style="padding: 16px; border: 1px solid #1a1a24; margin-bottom: 12px; background: #0c0c12;">\n        <div style="font-size: 11px; color: #DE2626; text-transform: uppercase; font-weight: 600;">{v}</div>\n        <div style="font-size: 13px; color: #FFFFFF; margin-top: 4px;">Content Body Placeholder</div>\n      </div>'
            for v in views
        ]

        forms_markup_items = [
            f'      <!-- Form Component: {f} -->\n      <div class="behtml-form-group" style="padding: 12px; border: 1px solid #22222e; margin-bottom: 12px;">\n        <label style="font-size: 10px; color: #71717a; text-transform: uppercase;">{f}</label>\n        <input type="text" placeholder="Input Field" style="width: 100%; padding: 6px; background: #050508; border: 1px solid #2a2a36; color: #FFFFFF; font-size: 12px; margin-top: 4px;">\n      </div>'
            for f in forms
        ]

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>{fname} — {role}</title>
  <style>
    :root {{
      --app-height: 100vh;
      --behtml-ry: 32px;
      --behtml-bg-canvas: #000000;
      --behtml-fg-text: #FFFFFF;
      --behtml-accent-red: #DE2626;
      --behtml-border-divider: #1a1a1a;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    html, body {{
      width: 100vw;
      height: var(--app-height);
      overflow-x: hidden;
      background: var(--behtml-bg-canvas);
      color: var(--behtml-fg-text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace;
    }}
    .behtml-layer-4-header {{
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 64px;
      z-index: 128;
      background: #060608;
      border-bottom: 1px solid #1f1f28;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 16px;
    }}
    .behtml-main-canvas {{
      margin-top: 64px;
      padding: 24px 16px;
      min-height: calc(var(--app-height) - 64px);
    }}
  </style>
</head>
<body>
  <!-- Layer 4 Header Chrome (z: 128) -->
  <header class="behtml-layer-4-header">
    <div style="font-weight: 700; font-size: 13px; letter-spacing: 0.5px;">
      {plan_bejson['Project_Name']} <span style="color: #DE2626; font-size: 10px;">[{fname}]</span>
    </div>
    <div style="font-size: 11px; color: #71717a;">Taxonomies: {', '.join(prefixes)}</div>
  </header>

  <!-- Layer 2 Surface Content (z: 32) -->
  <main class="behtml-main-canvas">
{"\n".join(views_markup_items)}
{"\n".join(forms_markup_items)}
  </main>

  <script>
    if (window.visualViewport) {{
      function syncHeight() {{
        document.documentElement.style.setProperty('--app-height', window.visualViewport.height + 'px');
      }}
      window.visualViewport.addEventListener('resize', syncHeight);
      syncHeight();
    }}
  </script>
</body>
</html>
"""
        dest_path.write_text(html_content, encoding="utf-8")
        created_paths.append(dest_path)

    return created_paths


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="compose_template_plan",
        description="Template Plan Composer — Encapsulates and composes required template architectures with taxonomy awareness."
    )
    parser.add_argument("--archetype", choices=list(ARCHETYPE_BLUEPRINT_ROSTER.keys()), default="blog", help="Target domain archetype (default: blog)")
    parser.add_argument("--name", type=str, default="Sample_Site", help="Project / site title name")
    parser.add_argument("--output-json", type=str, default=None, help="Destination path for BEJSON 104a plan file")
    parser.add_argument("--output-md", type=str, default=None, help="Destination path for Markdown plan specification")
    parser.add_argument("--scaffold-dir", type=str, default=None, help="Directory to scaffold concrete zero-filler HTML template files")
    parser.add_argument("--version", action="version", version=f"compose_template_plan v{VERSION} (Release {RELEASE_VERSION})")
    return parser


def main() -> int:
    parser = build_argument_parser()
    args = parser.parse_args()

    app_logger.info("Composing template plan for archetype: '%s' (Project: %s)", args.archetype, args.name)
    plan_bejson = build_bejson_template_plan(archetype_key=args.archetype, project_name=args.name)

    # 1. Output BEJSON
    if args.output_json:
        out_json_path = Path(args.output_json).resolve()
        out_json_path.parent.mkdir(parents=True, exist_ok=True)
        out_json_path.write_text(json.dumps(plan_bejson, indent=2), encoding="utf-8")
        app_logger.info("Saved BEJSON 104a plan to: %s", out_json_path)

    # 2. Output Markdown
    if args.output_md:
        out_md_path = Path(args.output_md).resolve()
        out_md_path.parent.mkdir(parents=True, exist_ok=True)
        md_text = generate_markdown_plan(plan_bejson)
        out_md_path.write_text(md_text, encoding="utf-8")
        app_logger.info("Saved Markdown plan to: %s", out_md_path)

    # 3. Scaffold HTML Templates
    if args.scaffold_dir:
        scaffold_path = Path(args.scaffold_dir).resolve()
        scaffolded = scaffold_zero_filler_templates(plan_bejson, scaffold_path)
        app_logger.info("Scaffolded %d template files into: %s", len(scaffolded), scaffold_path)

    # If neither output option specified, print markdown to stdout
    if not args.output_json and not args.output_md and not args.scaffold_dir:
        sys.stdout.write(generate_markdown_plan(plan_bejson) + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
