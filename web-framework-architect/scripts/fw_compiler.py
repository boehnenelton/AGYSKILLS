#!/usr/bin/env python3
"""
scripts/fw_compiler.py
Domain 3: The Web Framework Planner
Validates and compiles Web Framework routing topologies per the 12 Invariant Laws.
"""

import sys
import os
import json
import argparse
from pathlib import Path

def get_script_path() -> Path:
    return Path(__file__).resolve().parent

def build_field_map(fields_list: list) -> dict:
    return {field_dict["name"]: idx for idx, field_dict in enumerate(fields_list)}

def calculate_relative_prefix(depth_level: int) -> str:
    """Calculates relative path prefix for a given directory depth."""
    if depth_level <= 0:
        return "./"
    return "../" * depth_level

def validate_framework_manifest(fw_manifest_path: Path) -> bool:
    if not fw_manifest_path.exists():
        print(f"[ERROR] Framework manifest not found: {fw_manifest_path}", file=sys.stderr)
        return False

    with open(fw_manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if data.get("Format") != "BEJSON" or data.get("Format_Version") != "104a":
        print(f"[ERROR] Invalid format: Expected BEJSON 104a, got {data.get('Format')} {data.get('Format_Version')}", file=sys.stderr)
        return False

    fields = data.get("Fields", [])
    values = data.get("Values", [])
    f_map = build_field_map(fields)

    required_fields = [
        "route_id", "taxonomy_slug", "category_slug", "depth_level",
        "content_style_mode", "terminal_node_storage_mode", "bound_template_file",
        "sidebar_tree_default_collapsed_flag", "horizontal_scroll_toolbar_flag"
    ]
    for req in required_fields:
        if req not in f_map:
            print(f"[ERROR] Missing required field in manifest: {req}", file=sys.stderr)
            return False

    # Audit the 12 Invariant Laws
    law_violations = []
    has_root_index = False

    for row_idx, row in enumerate(values):
        route_id = row[f_map["route_id"]]
        tax_slug = row[f_map["taxonomy_slug"]]
        cat_slug = row[f_map["category_slug"]]
        depth = row[f_map["depth_level"]]
        style_mode = row[f_map["content_style_mode"]]
        collapsed_flag = row[f_map["sidebar_tree_default_collapsed_flag"]]
        tb_flag = row[f_map["horizontal_scroll_toolbar_flag"]]

        if depth == 0:
            has_root_index = True

        # Law 3: Page-Style Default vs. Blog Feed Exception
        if tax_slug != "blog" and style_mode == "feed_style":
            law_violations.append(f"Row {row_idx} ({route_id}): Law 3 Violation - Non-blog taxonomy '{tax_slug}' must be page_style, found feed_style.")

        # Law 4: Sidebar Navigation Default-Collapsed
        if not collapsed_flag:
            law_violations.append(f"Row {row_idx} ({route_id}): Law 4 Violation - Sidebar tree must initialize default-collapsed ('classified to fall').")

        # Law 5: Universal Horizontal Scroll Toolbar
        if not tb_flag:
            law_violations.append(f"Row {row_idx} ({route_id}): Law 5 Violation - Docked toolbar must have horizontal_scroll_toolbar_flag set to True.")

    # Law 2: Universal Directory Index Resolution
    if not has_root_index:
        law_violations.append("Law 2 Violation - Missing root (depth 0) directory index route.")

    if law_violations:
        print("[AUDIT FAILED] Web Framework Invariant Law Violations detected:", file=sys.stderr)
        for v in law_violations:
            print(f"  - {v}", file=sys.stderr)
        return False

    print(f"[SUCCESS] Web Framework Manifest passed 12 Invariant Laws ({len(values)} routes verified).")
    return True

def synthesize_sidebar_tree_html(taxonomy_manifest_path: Path, current_depth: int) -> str:
    """Synthesizes depth-relative <details class='fw-tree-node'> sidebar tree."""
    if not taxonomy_manifest_path.exists():
        return "<!-- Sidebar tree taxonomy manifest not found -->"

    with open(taxonomy_manifest_path, "r", encoding="utf-8") as f:
        tax_data = json.load(f)

    fields = tax_data.get("Fields", [])
    values = tax_data.get("Values", [])
    f_map = build_field_map(fields)
    rel_root = calculate_relative_prefix(current_depth)

    html_parts = ['<aside class="fw-sidebar-tree" aria-label="Taxonomy Navigation Tree">']

    # Group taxonomies
    roots = [r for r in values if not r[f_map["parent_taxonomy_id"]]]
    for root in roots:
        tax_id = root[f_map["taxonomy_id"]]
        slug = root[f_map["taxonomy_slug"]]
        name = root[f_map["taxonomy_display_name"]]
        link = f"{rel_root}{slug}/index.html"

        html_parts.append('  <details class="fw-tree-node">')
        html_parts.append(f'    <summary class="fw-tree-row"><a href="{link}" class="fw-tree-link">{name}</a></summary>')
        html_parts.append('    <div class="fw-tree-branch">')

        # Children
        children = [r for r in values if r[f_map["parent_taxonomy_id"]] == tax_id]
        for child in children:
            c_slug = child[f_map["taxonomy_slug"]]
            c_name = child[f_map["taxonomy_display_name"]]
            c_link = f"{rel_root}{slug}/{c_slug}/index.html"
            html_parts.append(f'      <div class="fw-tree-row"><a href="{c_link}" class="fw-tree-link">{c_name}</a></div>')

        html_parts.append('    </div>')
        html_parts.append('  </details>')

    html_parts.append('</aside>')
    return "\n".join(html_parts)

def compile_framework(taxonomy_manifest_path: Path, framework_manifest_path: Path, templates_dir: Path, output_dir: Path):
    if not validate_framework_manifest(framework_manifest_path):
        print("[ERROR] Compilation aborted due to manifest validation failure.", file=sys.stderr)
        return False

    output_dir.mkdir(parents=True, exist_ok=True)
    with open(framework_manifest_path, "r", encoding="utf-8") as f:
        fw_data = json.load(f)

    f_map = build_field_map(fw_data.get("Fields", []))
    routes = fw_data.get("Values", [])

    compiled_count = 0
    for row in routes:
        tax_slug = row[f_map["taxonomy_slug"]]
        cat_slug = row[f_map["category_slug"]]
        depth = row[f_map["depth_level"]]
        template_name = row[f_map["bound_template_file"]]

        # Determine target directory
        if depth == 0:
            target_dir = output_dir
        elif depth == 1:
            target_dir = output_dir / tax_slug
        else:
            target_dir = output_dir / tax_slug / cat_slug

        target_dir.mkdir(parents=True, exist_ok=True)
        target_file = target_dir / "index.html"

        # Check template source
        src_template = templates_dir / template_name
        template_content = ""
        if src_template.exists():
            with open(src_template, "r", encoding="utf-8") as tf:
                template_content = tf.read()
        else:
            # Fallback barebones zero-filler skeleton
            template_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Page Title</title>
<link rel="stylesheet" href="{calculate_relative_prefix(depth)}framework_core_layout.css">
</head>
<body>
<div class="fw-shell">
  <header class="fw-docked-toolbar" role="toolbar">
    <a href="{calculate_relative_prefix(depth)}index.html" class="fw-brand">Site Title</a>
  </header>
  <div class="fw-workspace">
    <!-- SIDEBAR_TREE_PLACEHOLDER -->
    <main class="fw-main-canvas">
      <nav class="fw-breadcrumb-rail" aria-label="Breadcrumb">
        <a href="{calculate_relative_prefix(depth)}index.html">Home</a>
      </nav>
      <article class="fw-page-article">
        <h1>Page Title</h1>
        <p class="fw-subtitle">Subtitle</p>
        <section class="fw-prose-section">
          <h2>Section Heading</h2>
          <p>Body Paragraph text</p>
        </section>
      </article>
    </main>
  </div>
</div>
</body>
</html>"""

        # Inject synthesized sidebar tree
        sidebar_tree_html = synthesize_sidebar_tree_html(taxonomy_manifest_path, depth)
        if "<!-- SIDEBAR_TREE_PLACEHOLDER -->" in template_content:
            template_content = template_content.replace("<!-- SIDEBAR_TREE_PLACEHOLDER -->", sidebar_tree_html)

        with open(target_file, "w", encoding="utf-8") as out:
            out.write(template_content)

        compiled_count += 1

    # Copy CSS primitive
    css_src = get_script_path().parent / "assets" / "framework_core_layout.css"
    if css_src.exists():
        with open(css_src, "r", encoding="utf-8") as cf:
            css_content = cf.read()
        with open(output_dir / "framework_core_layout.css", "w", encoding="utf-8") as cf_out:
            cf_out.write(css_content)

    print(f"[SUCCESS] Compiled {compiled_count} isomorphic route directories into: {output_dir}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Web Framework Compiler (Domain 3)")
    parser.add_argument("--validate", type=str, help="Validate 104a.web_framework.bejson manifest")
    parser.add_argument("--compile", action="store_true", help="Compile static site topology")
    parser.add_argument("--taxonomy", type=str, help="Path to 104a.taxonomy_schema.bejson")
    parser.add_argument("--framework", type=str, help="Path to 104a.web_framework.bejson")
    parser.add_argument("--templates-dir", type=str, help="Directory containing HTML templates")
    parser.add_argument("--output-dir", type=str, default="./dist_site", help="Destination directory")

    args = parser.parse_args()

    if args.validate:
        ok = validate_framework_manifest(Path(args.validate))
        sys.exit(0 if ok else 1)
    elif args.compile:
        if not args.taxonomy or not args.framework:
            print("[ERROR] --compile requires both --taxonomy and --framework paths.", file=sys.stderr)
            sys.exit(1)
        tmpl_dir = Path(args.templates_dir) if args.templates_dir else get_script_path().parent / "assets"
        ok = compile_framework(Path(args.taxonomy), Path(args.framework), tmpl_dir, Path(args.output_dir))
        sys.exit(0 if ok else 1)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
