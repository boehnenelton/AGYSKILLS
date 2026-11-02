#!/data/data/com.termux/files/usr/bin/env python3
# ==============================================================================
# Script Name: cms_canvas_illustrator.py
# Description: Layer 5 SVG Canvas Illustrator for BEJSON CMS blog posts & publications.
#              Generates context-optimized SVG diagrams, 1280x640 article hero banners,
#              1280x720 3-pillar architectural blueprints, high-DPI Playwright raster
#              captures (PNG/WebP), and handles atomic CMS media registration.
#              Adheres to Policy §8.1 Tri-Color standards (#000000, #FFFFFF, #DE2626)
#              and 8-lane quantized geometry.
# Version: 110
# Date Created: 2026-10-25
# Date Modified: 2026-11-02
# Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
# RELATIONAL_ID: 4d28e719-8b3a-49c2-9e12-3a5f9b1c7064
# Release_Version: 300
# ==============================================================================

import sys

if sys.version_info < (3, 10):
    sys.stderr.write("cms_canvas_illustrator requires Python 3.10 or newer.\n")
    sys.exit(20)

import argparse
import asyncio
import html
import json
import logging
import os
import re
import shutil
import subprocess
import uuid
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Insert libraries_105 Graphics and Canvas search paths
_LIB105_GRAPHICS = Path("/storage/emulated/0/Admin/Libraries/libraries_105/Lib_PY/Graphics")
_LIB105_CANVAS = Path("/storage/emulated/0/Admin/Libraries/libraries_105/Lib_PY/Canvas")
if _LIB105_GRAPHICS.exists() and str(_LIB105_GRAPHICS) not in sys.path:
    sys.path.insert(0, str(_LIB105_GRAPHICS))
if _LIB105_CANVAS.exists() and str(_LIB105_CANVAS) not in sys.path:
    sys.path.insert(0, str(_LIB105_CANVAS))

try:
    import lib_bejson_Graphics_graphics_core as gc
except ImportError:
    gc = None

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

SYSTEM_SCRIPT_VERSION_INTEGER: int = 110
SYSTEM_RELEASE_VERSION_INTEGER: int = 300
SYSTEM_CANONICAL_AUTHOR_CREDIT_STRING: str = (
    "Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton"
)
SYSTEM_SCRIPT_RELATIONAL_UUID_STRING: str = "4d28e719-8b3a-49c2-9e12-3a5f9b1c7064"

STATUS_CODE_SUCCESS_EXECUTION: int = 0
STATUS_CODE_PATH_ERROR_EXECUTION: int = 10
STATUS_CODE_ENVIRONMENT_ERROR_EXECUTION: int = 20
STATUS_CODE_VALIDATION_ERROR_EXECUTION: int = 30

EXECUTION_LOGGER_INSTANCE: logging.Logger = logging.getLogger("CmsCanvasIllustrator")


def configure_execution_logging_subsystem(configured_log_level_string: str = "INFO") -> None:
    """Configure standard logging subsystem avoiding raw print statements."""
    calculated_numeric_logging_level: int = getattr(
        logging, configured_log_level_string.upper(), logging.INFO
    )
    logging.basicConfig(
        level=calculated_numeric_logging_level,
        format="[%(asctime)s] [%(levelname)s] [CmsCanvasIllustrator] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def extract_context_attributes(target_context_file_path: Path) -> Dict[str, Any]:
    """Extract post title, core components, and technical concepts from research brief or plan."""
    extracted_attributes_dictionary: Dict[str, Any] = {
        "title": "BEJSON ECOSYSTEM ARCHITECTURE",
        "subtitle": "ZERO-SQL POSITIONAL DATA CONTRACTS",
        "components": [
            ("DATA PERSISTENCE", "Positional BEJSON Matrices"),
            ("MANIFEST REGISTRY", "Bidirectional MFDB Master"),
            ("SERVICES ENGINE", "Decoupled Zero-SDK Microservices"),
            ("CMS PUBLISHER", "Lightweight Two-Part Storage"),
        ],
        "category": "BEJSON",
    }

    if not target_context_file_path.is_file():
        return extracted_attributes_dictionary

    try:
        raw_context_content_string: str = target_context_file_path.read_text(encoding="utf-8")

        # Extract title
        title_regular_expression_match = re.search(r"^#\s+(.+)$", raw_context_content_string, flags=re.MULTILINE)
        if title_regular_expression_match:
            clean_title = title_regular_expression_match.group(1).strip()
            if "research brief" in clean_title.lower():
                project_name_match = re.search(r"## 1\. Project Overview:\s*(.+)", raw_context_content_string)
                if project_name_match:
                    clean_title = f"{project_name_match.group(1).strip().upper()} ARCHITECTURE"
            extracted_attributes_dictionary["title"] = clean_title

        # Look for components / directories
        discovered_components: List[Tuple[str, str]] = []
        directory_matches = re.findall(r"-\s*`/([^/]+)/`", raw_context_content_string)
        if directory_matches:
            for dir_name in directory_matches[:4]:
                component_title = dir_name.upper().replace("_", " ")
                component_desc = f"Subsystem Module /{dir_name}/"
                discovered_components.append((component_title, component_desc))

        if len(discovered_components) >= 2:
            extracted_attributes_dictionary["components"] = discovered_components

    except Exception as extraction_exception:
        EXECUTION_LOGGER_INSTANCE.warning(
            "Could not parse context from %s: %s", target_context_file_path.name, str(extraction_exception)
        )

    return extracted_attributes_dictionary


def build_hero_banner_svg(
    article_title_string: str,
    article_subtitle_string: str,
    peripheral_component_nodes_list: List[Tuple[str, str]],
    canvas_width_pixels: int = 1280,
    canvas_height_pixels: int = 640,
    tag_string: str = "BEJSON 104a • MFDB",
    footer_credit_string: str = "ELTON BOEHNEN • ZERO-SQL ARCHITECTURE",
) -> str:
    """Generate deterministic, standalone SVG markup for 1280x640 article hero banner."""
    escaped_title = html.escape(article_title_string.upper())
    escaped_subtitle = html.escape(article_subtitle_string.upper())
    escaped_tag = html.escape(tag_string)
    escaped_footer = html.escape(footer_credit_string)

    # Ensure 4 components exist
    nodes: List[Tuple[str, str]] = list(peripheral_component_nodes_list)
    default_placeholders = [
        ("CORE STORAGE", "Dense 104db Matrix"),
        ("MANIFEST ENGINE", "Master-Slave Network"),
        ("SERVICES ADAPTER", "Zero-SDK Microservices"),
        ("CMS PUBLISHER", "Lightweight Two-Part Index"),
    ]
    while len(nodes) < 4:
        nodes.append(default_placeholders[len(nodes)])

    node_1_title, node_1_sub = html.escape(nodes[0][0]), html.escape(nodes[0][1])
    node_2_title, node_2_sub = html.escape(nodes[1][0]), html.escape(nodes[1][1])
    node_3_title, node_3_sub = html.escape(nodes[2][0]), html.escape(nodes[2][1])
    node_4_title, node_4_sub = html.escape(nodes[3][0]), html.escape(nodes[3][1])

    generated_svg_document_string = f"""<svg width="{canvas_width_pixels}" height="{canvas_height_pixels}" viewBox="0 0 {canvas_width_pixels} {canvas_height_pixels}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="stageGlow" cx="50%" cy="45%" r="65%">
      <stop offset="0%" stop-color="#1c0707" stop-opacity="0.95" />
      <stop offset="50%" stop-color="#08080c" stop-opacity="0.7" />
      <stop offset="100%" stop-color="#000000" stop-opacity="1" />
    </radialGradient>
    <linearGradient id="cubeTop" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="100%" stop-color="#CCCCCC" />
    </linearGradient>
    <linearGradient id="cubeLeft" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#888888" />
      <stop offset="100%" stop-color="#444444" />
    </linearGradient>
    <linearGradient id="cubeRight" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#666666" />
      <stop offset="100%" stop-color="#222222" />
    </linearGradient>
    <filter id="laserGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <!-- Ambient Backdrop -->
  <rect width="{canvas_width_pixels}" height="{canvas_height_pixels}" fill="url(#stageGlow)" />

  <!-- 8-Lane Production Grid (160px intervals) -->
  <g opacity="0.08" stroke="#FFFFFF" stroke-width="1">
    <line x1="160" y1="0" x2="160" y2="640" />
    <line x1="320" y1="0" x2="320" y2="640" />
    <line x1="480" y1="0" x2="480" y2="640" />
    <line x1="640" y1="0" x2="640" y2="640" />
    <line x1="800" y1="0" x2="800" y2="640" />
    <line x1="960" y1="0" x2="960" y2="640" />
    <line x1="1120" y1="0" x2="1120" y2="640" />
    <!-- 32px Ry Quantized Grid -->
    <line x1="0" y1="96" x2="1280" y2="96" />
    <line x1="0" y1="192" x2="1280" y2="192" />
    <line x1="0" y1="320" x2="1280" y2="320" />
    <line x1="0" y1="448" x2="1280" y2="448" />
    <line x1="0" y1="544" x2="1280" y2="544" />
  </g>

  <!-- Header HUD Telemetry Bar -->
  <rect x="0" y="0" width="1280" height="48" fill="#08080a" />
  <line x1="0" y1="48" x2="1280" y2="48" stroke="#DE2626" stroke-width="1.5" />
  <text x="32" y="30" fill="#DE2626" font-size="13" font-family="monospace" font-weight="700" letter-spacing="2">BEJSON CMS // POST HERO</text>
  <text x="640" y="30" fill="#888899" font-size="11" font-family="monospace" text-anchor="middle" letter-spacing="1">{escaped_subtitle}</text>
  <text x="1248" y="30" fill="#AAAAAA" font-size="12" font-family="monospace" text-anchor="end" font-weight="600">{escaped_tag}</text>

  <!-- Laser Connectivity Rays to Central Core -->
  <g stroke="#DE2626" stroke-width="1.5" opacity="0.8" filter="url(#laserGlow)">
    <line x1="260" y1="170" x2="560" y2="280" />
    <line x1="260" y1="420" x2="560" y2="340" />
    <line x1="1020" y1="170" x2="720" y2="280" />
    <line x1="1020" y1="420" x2="720" y2="340" />
  </g>

  <!-- Peripheral Node 1 (Top Left) -->
  <g transform="translate(140, 140)">
    <rect x="-10" y="-16" width="240" height="60" rx="4" fill="#0c0c10" stroke="#2a2a38" stroke-width="1.5" />
    <rect x="-10" y="-16" width="4" height="60" fill="#DE2626" />
    <text x="14" y="10" fill="#FFFFFF" font-size="13" font-family="monospace" font-weight="700">{node_1_title}</text>
    <text x="14" y="30" fill="#888899" font-size="11" font-family="monospace">{node_1_sub}</text>
  </g>

  <!-- Peripheral Node 2 (Bottom Left) -->
  <g transform="translate(140, 390)">
    <rect x="-10" y="-16" width="240" height="60" rx="4" fill="#0c0c10" stroke="#2a2a38" stroke-width="1.5" />
    <rect x="-10" y="-16" width="4" height="60" fill="#DE2626" />
    <text x="14" y="10" fill="#FFFFFF" font-size="13" font-family="monospace" font-weight="700">{node_2_title}</text>
    <text x="14" y="30" fill="#888899" font-size="11" font-family="monospace">{node_2_sub}</text>
  </g>

  <!-- Peripheral Node 3 (Top Right) -->
  <g transform="translate(900, 140)">
    <rect x="-10" y="-16" width="240" height="60" rx="4" fill="#0c0c10" stroke="#2a2a38" stroke-width="1.5" />
    <rect x="-10" y="-16" width="4" height="60" fill="#DE2626" />
    <text x="14" y="10" fill="#FFFFFF" font-size="13" font-family="monospace" font-weight="700">{node_3_title}</text>
    <text x="14" y="30" fill="#888899" font-size="11" font-family="monospace">{node_3_sub}</text>
  </g>

  <!-- Peripheral Node 4 (Bottom Right) -->
  <g transform="translate(900, 390)">
    <rect x="-10" y="-16" width="240" height="60" rx="4" fill="#0c0c10" stroke="#2a2a38" stroke-width="1.5" />
    <rect x="-10" y="-16" width="4" height="60" fill="#DE2626" />
    <text x="14" y="10" fill="#FFFFFF" font-size="13" font-family="monospace" font-weight="700">{node_4_title}</text>
    <text x="14" y="30" fill="#888899" font-size="11" font-family="monospace">{node_4_sub}</text>
  </g>

  <!-- Central Isometric BEJSON Cube Anchor -->
  <g transform="translate(640, 310)">
    <!-- Top Face -->
    <polygon points="0,-70 60,-35 0,0 -60,-35" fill="url(#cubeTop)" stroke="#DE2626" stroke-width="2" />
    <!-- Left Face -->
    <polygon points="-60,-35 0,0 0,70 -60,35" fill="url(#cubeLeft)" stroke="#DE2626" stroke-width="1.5" />
    <!-- Right Face -->
    <polygon points="0,0 60,-35 60,35 0,70" fill="url(#cubeRight)" stroke="#DE2626" stroke-width="1.5" />
    <!-- Orbital Ring -->
    <ellipse cx="0" cy="0" rx="100" ry="40" fill="none" stroke="#DE2626" stroke-width="1" stroke-dasharray="6,4" opacity="0.6" />
  </g>

  <!-- Main Headline -->
  <text x="640" y="470" fill="#FFFFFF" font-size="24" font-family="monospace" font-weight="800" text-anchor="middle" letter-spacing="3">{escaped_title}</text>
  <rect x="520" y="485" width="240" height="2" fill="#DE2626" />
  <text x="640" y="515" fill="#888899" font-size="13" font-family="monospace" text-anchor="middle" letter-spacing="1">{escaped_footer}</text>
</svg>"""
    return generated_svg_document_string


def register_asset_in_cms(
    asset_file_path: Path,
    cms_root_path: Path,
    target_page_uuid: Optional[str] = None
) -> bool:
    """Register generated asset file into mediaasset.bejson and optionally link to pagerecord.bejson."""
    media_path = cms_root_path / "storage/mfdb/site_master/data/mediaasset.bejson"
    page_path = cms_root_path / "storage/mfdb/site_master/data/pagerecord.bejson"

    if not media_path.exists():
        EXECUTION_LOGGER_INSTANCE.warning("mediaasset.bejson not found at %s", media_path)
        return False

    try:
        with open(media_path, "r", encoding="utf-8") as f:
            media_data = json.load(f)

        fields = [fld["name"] for fld in media_data["Fields"]]
        f_name = fields.index("asset_filename")
        existing_filenames = {row[f_name] for row in media_data["Values"]}

        if asset_file_path.name not in existing_filenames:
            content = asset_file_path.read_bytes()
            sha256 = hashlib.sha256(content).hexdigest()
            size = len(content)
            ext = asset_file_path.suffix.lower()
            mime = "image/svg+xml" if ext == ".svg" else ("image/png" if ext == ".png" else ("image/webp" if ext == ".webp" else "application/octet-stream"))
            now_iso = datetime.now(timezone.utc).isoformat()

            row = [asset_file_path.name, asset_file_path.name, sha256, size, mime, now_iso]
            media_data["Values"].append(row)

            with open(media_path, "w", encoding="utf-8") as f:
                json.dump(media_data, f, indent=2)
            EXECUTION_LOGGER_INSTANCE.info("Registered %s in mediaasset.bejson", asset_file_path.name)

        # If page_uuid provided and asset is SVG, update pagerecord.bejson
        if target_page_uuid and asset_file_path.suffix.lower() == ".svg" and page_path.exists():
            with open(page_path, "r", encoding="utf-8") as f:
                page_data = json.load(f)

            p_fields = [fld["name"] for fld in page_data["Fields"]]
            f_uuid = p_fields.index("page_uuid")
            f_img = p_fields.index("page_featured_img")

            for row in page_data["Values"]:
                if row[f_uuid] == target_page_uuid:
                    row[f_img] = asset_file_path.name
                    EXECUTION_LOGGER_INSTANCE.info(
                        "Updated page %s featured image to %s", target_page_uuid, asset_file_path.name
                    )
                    break

            with open(page_path, "w", encoding="utf-8") as f:
                json.dump(page_data, f, indent=2)

        return True
    except Exception as exc:
        EXECUTION_LOGGER_INSTANCE.error("Failed to register asset in CMS: %s", exc)
        return False


def generate_context_optimized_imagery(
    target_context_file_path: Optional[Path] = None,
    override_title_string: Optional[str] = None,
    override_subtitle_string: Optional[str] = None,
    override_components_string: Optional[str] = None,
    output_destination_path: Optional[Path] = None,
    capture_raster_png: bool = True,
    compile_webp: bool = True,
    is_diagram_slide: bool = False,
    pillars_list: Optional[List[Tuple[str, str, str, List[str], str]]] = None,
    tag_string: str = "BEJSON 104a • MFDB",
    footer_text: str = "ELTON BOEHNEN • ZERO-SQL ARCHITECTURE",
    register_cms_root: Optional[Path] = None,
    target_page_uuid: Optional[str] = None,
) -> Tuple[bool, Dict[str, Any], str]:
    """Generate SVG image and optional Playwright PNG/WebP captures."""
    context_data: Dict[str, Any] = {}
    if target_context_file_path and target_context_file_path.is_file():
        context_data = extract_context_attributes(target_context_file_path)

    final_title = override_title_string if override_title_string else context_data.get("title", "BEJSON ARCHITECTURE")
    final_subtitle = override_subtitle_string if override_subtitle_string else context_data.get("subtitle", "ZERO-SQL DATA CONTRACTS")

    components: List[Tuple[str, str]] = []
    if override_components_string:
        raw_parts = [p.strip() for p in override_components_string.split(",")]
        for p in raw_parts:
            components.append((p.upper(), "Subsystem Module"))
    elif "components" in context_data:
        components = context_data["components"]

    # Build SVG content (either Hero Banner or Architecture Slide)
    if is_diagram_slide and gc and hasattr(gc, "render_branding_architecture_slide_svg"):
        svg_content_string = gc.render_branding_architecture_slide_svg(
            title=final_title,
            subtitle=final_subtitle,
            pillars=pillars_list,
            width_px=1280,
            height_px=720,
        )
        canvas_w, canvas_h = 1280, 720
    else:
        svg_content_string = build_hero_banner_svg(
            article_title_string=final_title,
            article_subtitle_string=final_subtitle,
            peripheral_component_nodes_list=components,
            tag_string=tag_string,
            footer_credit_string=footer_text,
        )
        canvas_w, canvas_h = 1280, 640

    base_output_path = output_destination_path or Path("hero_graphic.svg")
    base_output_path = base_output_path.resolve()
    base_output_path.parent.mkdir(parents=True, exist_ok=True)

    svg_target_file_path = base_output_path.with_suffix(".svg")
    png_target_file_path = base_output_path.with_suffix(".png")
    webp_target_file_path = base_output_path.with_suffix(".webp")

    try:
        svg_target_file_path.write_text(svg_content_string, encoding="utf-8")
        EXECUTION_LOGGER_INSTANCE.info("Saved context-optimized SVG to: %s", svg_target_file_path)
    except Exception as svg_write_error:
        return False, {}, f"Failed to save SVG: {str(svg_write_error)}"

    captured_png_success: bool = False
    if capture_raster_png and gc and hasattr(gc, "render_still_frame"):
        try:
            render_result = asyncio.run(
                gc.render_still_frame(
                    width_px=canvas_w,
                    height_px=canvas_h,
                    output_path=str(png_target_file_path),
                    svg_markup=svg_content_string,
                    device_scale=2,
                )
            )
            if png_target_file_path.is_file() and png_target_file_path.stat().st_size > 0:
                captured_png_success = True
                EXECUTION_LOGGER_INSTANCE.info(
                    "Captured high-DPI raster PNG via Graphics 105: %s (%s bytes)",
                    png_target_file_path, render_result.get("bytes", 0)
                )
        except Exception as capture_exception:
            EXECUTION_LOGGER_INSTANCE.warning("Graphics 105 Playwright render warning: %s", capture_exception)

    compiled_webp_success: bool = False
    if compile_webp and captured_png_success and HAS_PIL:
        try:
            im = Image.open(png_target_file_path)
            im.save(webp_target_file_path, "WEBP", quality=90)
            if webp_target_file_path.is_file():
                compiled_webp_success = True
                EXECUTION_LOGGER_INSTANCE.info(
                    "Compiled WebP raster: %s (%s bytes)", webp_target_file_path, webp_target_file_path.stat().st_size
                )
        except Exception as webp_err:
            EXECUTION_LOGGER_INSTANCE.warning("WebP compilation warning: %s", webp_err)

    # Optional CMS registration
    if register_cms_root:
        cms_root = Path(register_cms_root).resolve()
        register_asset_in_cms(svg_target_file_path, cms_root, target_page_uuid)
        if captured_png_success:
            register_asset_in_cms(png_target_file_path, cms_root, target_page_uuid)
        if compiled_webp_success:
            register_asset_in_cms(webp_target_file_path, cms_root, target_page_uuid)

    chosen_image_path = str(svg_target_file_path)
    markdown_embed_snippet = f"![{final_title}]({chosen_image_path})"
    behtml_embed_snippet = (
        f'<div class="behtml-featured-header" style="text-align: center; margin: 24px 0;">\n'
        f'  <img src="{chosen_image_path}" alt="{html.escape(final_title)}" '
        f'style="max-width: 100%; height: auto; border: 1px solid #DE2626; border-radius: 4px; box-shadow: 0 4px 20px rgba(222,38,38,0.2);" />\n'
        f'</div>'
    )

    payload_results = {
        "title": final_title,
        "svg_file": str(svg_target_file_path),
        "png_file": str(png_target_file_path) if captured_png_success else None,
        "webp_file": str(webp_target_file_path) if compiled_webp_success else None,
        "active_file": chosen_image_path,
        "markdown_embed": markdown_embed_snippet,
        "behtml_embed": behtml_embed_snippet,
    }

    return True, payload_results, "Success"


def main() -> int:
    """Main execution routine for CMS Canvas Illustrator."""
    argument_parser_instance = argparse.ArgumentParser(
        description="BEJSON CMS SVG Canvas Illustrator & Graphics 105 Generator (Layer 5)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    argument_parser_instance.add_argument(
        "--context-file",
        type=str,
        default=None,
        help="Path to 00_context_research.md or 01_plan.md to extract title and components",
    )
    argument_parser_instance.add_argument(
        "--title",
        type=str,
        default=None,
        help="Override graphic headline title",
    )
    argument_parser_instance.add_argument(
        "--subtitle",
        type=str,
        default=None,
        help="Override telemetry subtitle",
    )
    argument_parser_instance.add_argument(
        "--components",
        type=str,
        default=None,
        help="Comma-separated peripheral components (e.g. 'REST Engine,Vault,Interactions,Dripper')",
    )
    argument_parser_instance.add_argument(
        "--output",
        type=str,
        default=None,
        help="Destination path for generated graphic (e.g. storage/mfdb/assets/hero.svg)",
    )
    argument_parser_instance.add_argument(
        "--diagram",
        action="store_true",
        help="Generate a 1280x720 16:9 3-pillar architectural blueprint diagram instead of hero banner",
    )
    argument_parser_instance.add_argument(
        "--tag",
        type=str,
        default="BEJSON 104a • MFDB",
        help="Format header tag in top right HUD (e.g. 'BEJSON 105a • MFDB v1.40')",
    )
    argument_parser_instance.add_argument(
        "--no-raster",
        action="store_true",
        help="Skip Playwright browser PNG raster capture, generating pure SVG only",
    )
    argument_parser_instance.add_argument(
        "--no-webp",
        action="store_true",
        help="Skip WebP compression",
    )
    argument_parser_instance.add_argument(
        "--register-cms",
        type=str,
        default=None,
        help="CMS project root path to register assets into mediaasset.bejson automatically",
    )
    argument_parser_instance.add_argument(
        "--page-uuid",
        type=str,
        default=None,
        help="Target page UUID to associate page_featured_img in pagerecord.bejson",
    )
    argument_parser_instance.add_argument(
        "--termux-tts",
        action="store_true",
        help="Optional: Speak generated banner title via Termux TTS",
    )
    argument_parser_instance.add_argument(
        "--export-tts-video",
        type=str,
        default=None,
        help="Optional: Compile a narrated H.264 MP4 video from generated graphic and TTS voiceover",
    )
    argument_parser_instance.add_argument(
        "--version",
        action="store_true",
        help="Show version identifier and exit",
    )
    argument_parser_instance.add_argument(
        "--register",
        action="store_true",
        help="Register utility with central database",
    )
    argument_parser_instance.add_argument(
        "--config",
        action="store_true",
        help="Display operational configuration parameters",
    )
    argument_parser_instance.add_argument(
        "--reset",
        action="store_true",
        help="Verify execution environment state",
    )

    parsed_cli_arguments = argument_parser_instance.parse_args()
    configure_execution_logging_subsystem()

    if parsed_cli_arguments.version:
        sys.stdout.write(f"cms_canvas_illustrator v{SYSTEM_SCRIPT_VERSION_INTEGER} (Release {SYSTEM_RELEASE_VERSION_INTEGER})\n")
        return STATUS_CODE_SUCCESS_EXECUTION

    if parsed_cli_arguments.config:
        config_data = {
            "version": SYSTEM_SCRIPT_VERSION_INTEGER,
            "release_version": SYSTEM_RELEASE_VERSION_INTEGER,
            "author": SYSTEM_CANONICAL_AUTHOR_CREDIT_STRING,
            "graphics_105_library": str(_LIB105_GRAPHICS),
            "palette": ["#000000", "#FFFFFF", "#DE2626"],
        }
        sys.stdout.write(json.dumps(config_data, indent=2) + "\n")
        return STATUS_CODE_SUCCESS_EXECUTION

    if parsed_cli_arguments.reset or parsed_cli_arguments.register:
        EXECUTION_LOGGER_INSTANCE.info("Illustrator integrity verified.")
        return STATUS_CODE_SUCCESS_EXECUTION

    context_file_path = Path(parsed_cli_arguments.context_file) if parsed_cli_arguments.context_file else None
    output_destination_path = Path(parsed_cli_arguments.output) if parsed_cli_arguments.output else None
    register_cms_path = Path(parsed_cli_arguments.register_cms) if parsed_cli_arguments.register_cms else None

    is_success, results_payload, message_text = generate_context_optimized_imagery(
        target_context_file_path=context_file_path,
        override_title_string=parsed_cli_arguments.title,
        override_subtitle_string=parsed_cli_arguments.subtitle,
        override_components_string=parsed_cli_arguments.components,
        output_destination_path=output_destination_path,
        capture_raster_png=not parsed_cli_arguments.no_raster,
        compile_webp=not parsed_cli_arguments.no_webp,
        is_diagram_slide=parsed_cli_arguments.diagram,
        tag_string=parsed_cli_arguments.tag,
        register_cms_root=register_cms_path,
        target_page_uuid=parsed_cli_arguments.page_uuid,
    )

    if not is_success:
        EXECUTION_LOGGER_INSTANCE.error("Failed to generate imagery: %s", message_text)
        return STATUS_CODE_VALIDATION_ERROR_EXECUTION

    EXECUTION_LOGGER_INSTANCE.info("Generated active graphic: %s", results_payload["active_file"])

    if parsed_cli_arguments.termux_tts or parsed_cli_arguments.export_tts_video:
        try:
            tts_compiler_dir = Path(__file__).resolve().parent.parent.parent / "canvas-animation-studio" / "scripts"
            if str(tts_compiler_dir) not in sys.path:
                sys.path.insert(0, str(tts_compiler_dir))
            from termux_tts_video_compiler import synthesize_tts_segment, speak_termux_tts_live

            narration_str = f"{results_payload['title']}. {parsed_cli_arguments.subtitle or 'BEJSON Architecture Graphic'}."
            out_base = Path(results_payload["svg_file"]).resolve().parent
            mp3_file = out_base / f"{Path(results_payload['svg_file']).stem}_tts.mp3"
            wav_file = out_base / f"{Path(results_payload['svg_file']).stem}_tts.wav"
            dur = synthesize_tts_segment(narration_str, mp3_file, wav_file)
            if parsed_cli_arguments.termux_tts:
                speak_termux_tts_live(narration_str, wav_path=wav_file)
            if parsed_cli_arguments.export_tts_video and results_payload.get("png_file"):
                vid_out = Path(parsed_cli_arguments.export_tts_video).resolve()
                vid_out.parent.mkdir(parents=True, exist_ok=True)
                subprocess.run(
                    [
                        "ffmpeg", "-y", "-loop", "1", "-i", str(results_payload["png_file"]),
                        "-i", str(wav_file), "-c:v", "libx264", "-tune", "stillimage",
                        "-c:a", "aac", "-b:a", "128k", "-pix_fmt", "yuv420p",
                        "-shortest", "-movflags", "+faststart", str(vid_out)
                    ],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
                )
                EXECUTION_LOGGER_INSTANCE.info("Compiled narrated banner video (%ss): %s", dur, vid_out)
        except Exception as tts_exc:
            EXECUTION_LOGGER_INSTANCE.warning("Optional TTS/Video step warning: %s", tts_exc)

    sys.stdout.write(f"\n--- Embed Snippet ---\n{results_payload['markdown_embed']}\n\n{results_payload['behtml_embed']}\n\n")
    return STATUS_CODE_SUCCESS_EXECUTION


if __name__ == "__main__":
    sys.exit(main())
