#!/usr/bin/env python3
"""
manual_builder_cli.py
Automated CLI and engine for structuring, documenting, and packaging codebases
into high-density, mobile-responsive documentation manuals and e-books.

Architecture:
  root/index.html                                     # Master Overview
  root/about.html                                     # Architecture & Governance
  root/styles.css                                     # Modular Light Theme
  root/script.js                                      # Accessible Hamburger Drawer
  root/<category>/feed.html                           # Category Feed & Download Hub
  root/<category>/<module_stem>/index.html            # Dedicated Module Documentation
  root/<category>/<module_stem>/<actual_file.ext>     # Direct Raw Source File Delivery
  root/downloads/<category>_core.zip                  # Per-Category Source Archive
  root/sitemap.xml & root/robots.txt                  # W3C Search Indexing
"""

import os
import sys
import json
import html
import re
import shutil
import zipfile
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

LANGUAGE_EXTENSIONS = {
    "python": [".py"],
    "typescript": [".ts", ".tsx"],
    "javascript": [".js", ".jsx", ".mjs", ".cjs"],
    "shell": [".sh", ".bash"],
    "go": [".go"],
    "rust": [".rs"],
    "c_cpp": [".c", ".cpp", ".h", ".hpp"],
    "java": [".java"],
    "ruby": [".rb"],
    "php": [".php"],
}

LANGUAGE_METADATA = {
    "python": {"name": "Python", "icon": "🐍", "zip_prefix": "python_core"},
    "typescript": {"name": "TypeScript", "icon": "🔷", "zip_prefix": "typescript_core"},
    "javascript": {"name": "JavaScript", "icon": "🟨", "zip_prefix": "javascript_core"},
    "shell": {"name": "POSIX Shell / Bash", "icon": "🐚", "zip_prefix": "bash_core"},
    "go": {"name": "Go", "icon": "🦫", "zip_prefix": "go_core"},
    "rust": {"name": "Rust", "icon": "🦀", "zip_prefix": "rust_core"},
    "c_cpp": {"name": "C / C++", "icon": "⚙️", "zip_prefix": "c_cpp_core"},
    "java": {"name": "Java", "icon": "☕", "zip_prefix": "java_core"},
    "ruby": {"name": "Ruby", "icon": "💎", "zip_prefix": "ruby_core"},
    "php": {"name": "PHP", "icon": "🐘", "zip_prefix": "php_core"},
    "generic": {"name": "Core Modules", "icon": "📦", "zip_prefix": "modules_core"},
}

def detect_language(file_path: Path) -> str:
    ext = file_path.suffix.lower()
    for lang, exts in LANGUAGE_EXTENSIONS.items():
        if ext in exts:
            return lang
    return "generic"

def extract_metadata(code: str, file_path: Path) -> Dict[str, Any]:
    lines = code.splitlines()
    lines_count = len(lines)
    size_kb = round(len(code.encode("utf-8")) / 1024, 1)

    version = "1.0.0"
    v_match = re.search(r"Version:\s*([0-9.]+)", code, re.IGNORECASE)
    if v_match:
        version = v_match.group(1).strip()

    description = ""
    desc_match = re.search(r"Description:\s*([^\n\r*#]+)", code, re.IGNORECASE)
    if desc_match:
        description = desc_match.group(1).strip()
    
    if not description:
        # Fallback to first non-empty comment or docstring
        docstring_match = re.search(r'"""(.*?)"""', code, re.DOTALL)
        if docstring_match:
            doc_lines = [l.strip() for l in docstring_match.group(1).splitlines() if l.strip()]
            if doc_lines:
                description = doc_lines[0]
        elif code.startswith("/**"):
            block_match = re.search(r'/\*\*(.*?)\*/', code, re.DOTALL)
            if block_match:
                for line in block_match.group(1).splitlines():
                    cleaned = re.sub(r'^[*\s]+', '', line).strip()
                    if cleaned and not cleaned.startswith('@') and not cleaned.startswith('Library:'):
                        description = cleaned
                        break

    if not description:
        description = f"{file_path.name} core implementation module."

    return {
        "version": version,
        "description": description,
        "lines_count": lines_count,
        "size_kb": size_kb
    }

def get_common_styles() -> str:
    return """
:root {
    --bg-canvas: #F8FAFC;
    --bg-surface: #FFFFFF;
    --bg-surface-alt: #F1F5F9;
    --border-subtle: rgba(0, 0, 0, 0.07);
    --border-light: rgba(0, 0, 0, 0.12);
    --text-primary: #0F172A;
    --text-secondary: #475569;
    --text-muted: #64748B;
    --accent: #DE2626;
    --accent-hover: #B91C1C;
    --accent-bg: rgba(222, 38, 38, 0.06);
    --accent-border: rgba(222, 38, 38, 0.2);
    --code-bg: #0F172A;
    --code-text: #E2E8F0;
    --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.04);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -4px rgba(0, 0, 0, 0.03);
    --radius-sm: 6px;
    --radius-md: 8px;
    --radius-lg: 12px;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background-color: var(--bg-canvas);
    color: var(--text-primary);
    line-height: 1.6;
    font-size: 15px;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

a { color: inherit; text-decoration: none; }

.site-header {
    background-color: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(8px);
    border-bottom: 1px solid var(--border-subtle);
    position: sticky;
    top: 0;
    z-index: 100;
}

.header-container {
    max-width: 1280px;
    margin: 0 auto;
    padding: 0 20px;
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
}

.header-left {
    display: flex;
    align-items: center;
    gap: 14px;
}

.menu-toggle {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: var(--radius-md);
    background: transparent;
    border: 1px solid var(--border-subtle);
    color: var(--text-primary);
    cursor: pointer;
    transition: all 0.15s ease;
}

.menu-toggle:hover {
    background: var(--bg-surface-alt);
    border-color: var(--border-light);
}

.brand-link {
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 700;
    font-size: 18px;
    letter-spacing: -0.02em;
    color: var(--text-primary);
}

.brand-badge {
    background: var(--accent);
    color: #FFFFFF;
    font-size: 11px;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 4px;
    letter-spacing: 0.05em;
}

.desktop-nav {
    display: flex;
    align-items: center;
    gap: 6px;
}

.nav-link {
    padding: 8px 14px;
    border-radius: var(--radius-sm);
    font-size: 14px;
    font-weight: 500;
    color: var(--text-secondary);
    transition: all 0.15s ease;
}

.nav-link:hover {
    color: var(--text-primary);
    background: var(--bg-surface-alt);
}

.nav-link.active {
    color: var(--accent);
    background: var(--accent-bg);
    font-weight: 600;
}

.header-right {
    display: flex;
    align-items: center;
    gap: 12px;
}

.gh-btn {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 7px 14px;
    border-radius: var(--radius-md);
    font-size: 13px;
    font-weight: 600;
    background: var(--bg-surface);
    border: 1px solid var(--border-light);
    color: var(--text-primary);
    transition: all 0.15s ease;
}

.gh-btn:hover {
    background: var(--bg-surface-alt);
    border-color: var(--text-primary);
}

/* Sidebar Drawer */
.sidebar-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(15, 23, 42, 0.4);
    backdrop-filter: blur(2px);
    z-index: 998;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.25s ease;
}

.sidebar-backdrop.open {
    opacity: 1;
    pointer-events: auto;
}

.site-sidebar {
    position: fixed;
    top: 0;
    left: 0;
    width: 320px;
    max-width: 86vw;
    height: 100vh;
    background: var(--bg-surface);
    border-right: 1px solid var(--border-subtle);
    z-index: 999;
    transform: translateX(-100%);
    transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    display: flex;
    flex-direction: column;
    box-shadow: var(--shadow-lg);
}

.site-sidebar.open {
    transform: translateX(0);
}

.sidebar-header {
    height: 64px;
    padding: 0 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid var(--border-subtle);
}

.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 700;
    font-size: 16px;
}

.close-sidebar-btn {
    width: 36px;
    height: 36px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: var(--radius-sm);
    border: none;
    background: transparent;
    font-size: 24px;
    line-height: 1;
    color: var(--text-secondary);
    cursor: pointer;
}

.close-sidebar-btn:hover {
    background: var(--bg-surface-alt);
    color: var(--text-primary);
}

.sidebar-content {
    flex: 1;
    overflow-y: auto;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.sidebar-root-links {
    display: flex;
    flex-direction: column;
    gap: 4px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border-subtle);
}

.sidebar-nav-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 9px 12px;
    border-radius: var(--radius-sm);
    font-size: 14px;
    font-weight: 500;
    color: var(--text-secondary);
    transition: all 0.15s ease;
}

.sidebar-nav-item:hover {
    background: var(--bg-surface-alt);
    color: var(--text-primary);
}

.sidebar-nav-item.active {
    background: var(--accent-bg);
    color: var(--accent);
    font-weight: 600;
}

.sidebar-lang-section {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.sidebar-feed-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 12px;
    border-radius: var(--radius-md);
    background: var(--bg-surface-alt);
    border: 1px solid var(--border-subtle);
    font-weight: 600;
    font-size: 14px;
    color: var(--text-primary);
    transition: all 0.15s ease;
}

.sidebar-feed-head:hover {
    border-color: var(--accent-border);
    background: var(--accent-bg);
    color: var(--accent);
}

.sidebar-feed-head.active {
    border-color: var(--accent);
    background: var(--accent-bg);
    color: var(--accent);
}

.feed-badge {
    font-size: 11px;
    font-weight: 600;
    padding: 2px 6px;
    border-radius: 4px;
    background: #FFFFFF;
    border: 1px solid var(--border-subtle);
    color: var(--text-secondary);
}

.sidebar-module-list {
    list-style: none;
    padding-left: 8px;
    margin-top: 4px;
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.sidebar-module-link {
    display: block;
    padding: 6px 10px;
    font-size: 12.5px;
    color: var(--text-muted);
    border-radius: var(--radius-sm);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    transition: all 0.1s ease;
}

.sidebar-module-link:hover {
    background: var(--bg-surface-alt);
    color: var(--text-primary);
}

.sidebar-module-link.active {
    background: var(--accent-bg);
    color: var(--accent);
    font-weight: 600;
}

/* Layout */
.main-wrapper {
    flex: 1;
    max-width: 1280px;
    width: 100%;
    margin: 0 auto;
    padding: 24px 20px 64px 20px;
}

.breadcrumbs {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    color: var(--text-muted);
    margin-bottom: 20px;
}

.breadcrumbs a { color: var(--text-secondary); }
.breadcrumbs a:hover { color: var(--accent); }
.breadcrumbs .sep { color: var(--border-light); }
.breadcrumbs .current { color: var(--text-primary); font-weight: 500; }

.hero-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 32px;
    margin-bottom: 24px;
    box-shadow: var(--shadow-sm);
    position: relative;
    overflow: hidden;
}

.hero-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--accent);
}

.hero-badge-row {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
}

.pill-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 3px 9px;
    border-radius: 9999px;
    font-size: 12px;
    font-weight: 600;
    background: var(--bg-surface-alt);
    color: var(--text-secondary);
    border: 1px solid var(--border-subtle);
}

.pill-badge.red {
    background: var(--accent-bg);
    color: var(--accent);
    border-color: var(--accent-border);
}

.hero-title {
    font-size: 28px;
    font-weight: 700;
    letter-spacing: -0.025em;
    color: var(--text-primary);
    margin-bottom: 8px;
}

.hero-subtitle {
    font-size: 16px;
    color: var(--text-secondary);
    max-width: 800px;
    line-height: 1.5;
}

.btn-toolbar {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 20px;
}

.btn {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 9px 16px;
    border-radius: var(--radius-md);
    font-size: 13.5px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s ease;
    border: 1px solid transparent;
}

.btn-primary {
    background: var(--accent);
    color: #FFFFFF;
    box-shadow: 0 1px 3px rgba(222, 38, 38, 0.2);
}

.btn-primary:hover {
    background: var(--accent-hover);
    color: #FFFFFF;
}

.btn-secondary {
    background: var(--bg-surface);
    border-color: var(--border-light);
    color: var(--text-primary);
}

.btn-secondary:hover {
    background: var(--bg-surface-alt);
    border-color: var(--text-primary);
}

/* Feed Grid */
.feed-filter-bar {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 12px 16px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
}

.feed-search-input {
    width: 100%;
    max-width: 460px;
    padding: 8px 12px;
    border-radius: var(--radius-sm);
    border: 1px solid var(--border-light);
    font-size: 14px;
    background: var(--bg-canvas);
    color: var(--text-primary);
}

.feed-search-input:focus {
    outline: none;
    border-color: var(--accent);
    background: #FFFFFF;
}

.feed-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
    gap: 20px;
}

.feed-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 24px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: all 0.2s ease;
    box-shadow: var(--shadow-sm);
}

.feed-card:hover {
    border-color: var(--accent-border);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

.feed-card-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 8px;
}

.feed-card-title {
    font-size: 16px;
    font-weight: 700;
    color: var(--text-primary);
    word-break: break-all;
}

.feed-card-idx {
    font-size: 12px;
    font-weight: 700;
    color: var(--accent);
    background: var(--accent-bg);
    padding: 2px 7px;
    border-radius: 4px;
    white-space: nowrap;
}

.feed-card-subtitle {
    font-size: 13.5px;
    font-weight: 600;
    color: var(--text-secondary);
    margin-bottom: 10px;
}

.feed-card-snippet {
    font-size: 13px;
    color: var(--text-muted);
    line-height: 1.5;
    margin-bottom: 16px;
    flex: 1;
}

.feed-card-meta {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px;
    padding-top: 14px;
    border-top: 1px solid var(--border-subtle);
    margin-bottom: 14px;
    font-size: 12px;
    color: var(--text-muted);
}

.feed-card-actions {
    display: flex;
    align-items: center;
    gap: 8px;
}

.feed-card-actions .btn {
    flex: 1;
    justify-content: center;
    font-size: 12.5px;
    padding: 8px 12px;
}

/* Documentation Content */
.doc-section {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 28px 32px;
    margin-bottom: 24px;
    box-shadow: var(--shadow-sm);
}

.doc-section-title {
    font-size: 18px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border-subtle);
    display: flex;
    align-items: center;
    gap: 8px;
}

.passage-content {
    color: var(--text-secondary);
    font-size: 15px;
    line-height: 1.7;
}

.passage-content p { margin-bottom: 14px; }
.passage-content p:last-child { margin-bottom: 0; }
.passage-content strong { color: var(--text-primary); }
.passage-content code {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    background: var(--bg-surface-alt);
    padding: 2px 5px;
    border-radius: 4px;
    color: var(--accent);
}

.code-stage {
    background: var(--code-bg);
    border-radius: var(--radius-lg);
    overflow: hidden;
    box-shadow: var(--shadow-md);
    margin-bottom: 24px;
}

.code-header {
    background: #090D16;
    padding: 12px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.code-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    font-weight: 500;
    color: #94A3B8;
    display: flex;
    align-items: center;
    gap: 8px;
}

.code-title .dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--accent);
}

.copy-btn {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.12);
    color: #E2E8F0;
    padding: 5px 12px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s ease;
}

.copy-btn:hover {
    background: rgba(255, 255, 255, 0.16);
    color: #FFFFFF;
}

.code-body {
    padding: 20px;
    overflow-x: auto;
    max-height: 600px;
}

.code-body pre {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    line-height: 1.55;
    color: var(--code-text);
    margin: 0;
}

.paging-feet {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 16px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    margin-top: 32px;
    box-shadow: var(--shadow-sm);
}

.paging-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 14px;
    border-radius: var(--radius-md);
    font-size: 13px;
    font-weight: 600;
    color: var(--text-secondary);
    border: 1px solid var(--border-light);
    transition: all 0.15s ease;
}

.paging-btn:hover:not(.disabled) {
    background: var(--accent-bg);
    border-color: var(--accent-border);
    color: var(--accent);
}

.paging-btn.disabled {
    opacity: 0.4;
    cursor: not-allowed;
    pointer-events: none;
}

.paging-status {
    font-size: 13px;
    font-weight: 600;
    color: var(--text-primary);
    text-align: center;
}

.site-footer {
    background: var(--bg-surface);
    border-top: 1px solid var(--border-subtle);
    margin-top: auto;
    padding: 32px 20px;
}

.footer-container {
    max-width: 1280px;
    margin: 0 auto;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    font-size: 13px;
    color: var(--text-muted);
}

.footer-links {
    display: flex;
    align-items: center;
    gap: 16px;
}

.footer-links a:hover { color: var(--accent); }

@media (max-width: 768px) {
    .desktop-nav { display: none; }
    .feed-grid { grid-template-columns: 1fr; }
    .hero-card { padding: 20px; }
    .hero-title { font-size: 22px; }
    .doc-section { padding: 20px; }
    .paging-feet { flex-direction: column; text-align: center; gap: 12px; }
    .paging-btn { width: 100%; justify-content: center; }
}
""".strip()

def get_common_script() -> str:
    return """
(function() {
    const toggleBtn = document.getElementById('menuToggle');
    const closeBtn = document.getElementById('closeSidebarBtn');
    const sidebar = document.getElementById('siteSidebar');
    const backdrop = document.getElementById('sidebarBackdrop');

    function openMenu() {
        if (!sidebar || !backdrop) return;
        sidebar.classList.add('open');
        backdrop.classList.add('open');
        if (toggleBtn) toggleBtn.setAttribute('aria-expanded', 'true');
        document.body.style.overflow = 'hidden';
    }

    function closeMenu() {
        if (!sidebar || !backdrop) return;
        sidebar.classList.remove('open');
        backdrop.classList.remove('open');
        if (toggleBtn) toggleBtn.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
    }

    if (toggleBtn) toggleBtn.addEventListener('click', openMenu);
    if (closeBtn) closeBtn.addEventListener('click', closeMenu);
    if (backdrop) backdrop.addEventListener('click', closeMenu);

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && sidebar && sidebar.classList.contains('open')) {
            closeMenu();
        }
    });

    window.copyCode = function(btn) {
        const pre = btn.closest('.code-stage').querySelector('pre');
        if (!pre) return;
        navigator.clipboard.writeText(pre.innerText).then(function() {
            const orig = btn.innerText;
            btn.innerText = 'Copied!';
            setTimeout(function() { btn.innerText = orig; }, 2000);
        });
    };

    const searchInput = document.getElementById('feedSearch');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase().trim();
            const cards = document.querySelectorAll('.feed-card');
            cards.forEach(function(card) {
                const text = card.innerText.toLowerCase();
                card.style.display = text.includes(query) ? '' : 'none';
            });
        });
    }
})();
""".strip()

def build_ebook_portal(
    source_dir: Path,
    output_dir: Path,
    title: str = "BEJSON 105 Manual",
    repo_url: str = "https://github.com/boehnenelton/BEJSON_105",
    author_name: str = "Elton Boehnen",
    author_email: str = "eltonboehnen@gmail.com",
    author_website: str = "https://boehnenelton2024.pages.dev",
    license_name: str = "PolyForm Noncommercial License 1.0.0",
    descriptions_map: Optional[Dict[str, Any]] = None,
    dry_run: bool = False,
    repackage_zip: bool = True
) -> Dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    dl_dir = output_dir / "downloads"
    dl_dir.mkdir(parents=True, exist_ok=True)

    # 1. Discover libraries
    source_files = sorted([f for f in source_dir.glob("**/*") if f.is_file()])
    
    records = []
    for f in source_files:
        name = f.name
        rel_str = str(f.relative_to(source_dir))
        
        # Skip junk, demos, tests, hidden
        if name.startswith(".") or name == "__init__.py": continue
        if rel_str == "Lib_TS/index.ts": continue
        if any(tok in name.lower() for tok in ["demo", "showcase", "bugfix", "test", "jszip"]): continue
        if any(tok in rel_str.lower() for tok in ["tests/", "showcase/", "external/"]): continue
        if name.endswith((".md", ".txt", ".json", ".lock")): continue

        lang = detect_language(f)
        code = f.read_text(encoding="utf-8", errors="replace")
        meta = extract_metadata(code, f)

        # Check for unique description overrides
        custom_info = descriptions_map.get(name) if descriptions_map else None
        if isinstance(custom_info, dict):
            subtitle = custom_info.get("subtitle") or meta["description"]
            paragraphs = custom_info.get("paragraphs") or [meta["description"]]
        elif isinstance(custom_info, (list, tuple)):
            subtitle = custom_info[0] if custom_info else meta["description"]
            paragraphs = custom_info[1] if len(custom_info) > 1 else [meta["description"]]
        else:
            subtitle = meta["description"]
            paragraphs = [meta["description"]]

        records.append({
            "path": f,
            "file_name": name,
            "stem": f.stem,
            "lang": lang,
            "code": code,
            "version": meta["version"],
            "lines_count": meta["lines_count"],
            "size_kb": meta["size_kb"],
            "subtitle": subtitle,
            "paragraphs": paragraphs,
            "snippet": re.sub(r'<[^>]+>', '', paragraphs[0])[:140]
        })

    # Group by language
    categories = sorted(list({r["lang"] for r in records}))
    grouped = {c: [r for r in records if r["lang"] == c] for c in categories}
    for c in categories:
        grouped[c].sort(key=lambda x: x["file_name"].lower())

    if dry_run:
        return {
            "status": "dry_run",
            "total_modules": len(records),
            "categories": {c: len(grouped[c]) for c in categories}
        }

    # 2. Write CSS and JS
    (output_dir / "styles.css").write_text(get_common_styles(), encoding="utf-8")
    (output_dir / "script.js").write_text(get_common_script(), encoding="utf-8")
    for c in categories:
        (output_dir / c).mkdir(parents=True, exist_ok=True)
        (output_dir / c / "styles.css").write_text(get_common_styles(), encoding="utf-8")
        (output_dir / c / "script.js").write_text(get_common_script(), encoding="utf-8")

    # 3. Create Category Raw Zips
    zip_meta = {}
    for c in categories:
        c_meta = LANGUAGE_METADATA.get(c, LANGUAGE_METADATA["generic"])
        zname = f"bejson_105_{c_meta['zip_prefix']}.zip"
        zp = dl_dir / zname
        with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as zf:
            for r in grouped[c]:
                zf.writestr(r["file_name"], r["code"])
        zip_meta[c] = {
            "zip_name": zname,
            "size_kb": round(zp.stat().st_size / 1024, 1),
            "file_count": len(grouped[c]),
            "display": c_meta["name"],
            "icon": c_meta["icon"]
        }

    # Helper HTML generators
    def make_header(prefix: str, active_cat: str = ""):
        nav_links = "".join([
            f'<a href="{prefix}{c}/feed.html" class="nav-link { "active" if active_cat == c else "" }">{LANGUAGE_METADATA.get(c, LANGUAGE_METADATA["generic"])["name"]}</a>'
            for c in categories
        ])
        return f"""
        <header class="site-header">
            <div class="header-container">
                <div class="header-left">
                    <button class="menu-toggle" id="menuToggle" aria-label="Toggle navigation" aria-expanded="false">
                        <svg viewBox="0 0 24 24" width="22" height="22" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
                            <line x1="3" y1="12" x2="21" y2="12"></line>
                            <line x1="3" y1="6" x2="21" y2="6"></line>
                            <line x1="3" y1="18" x2="21" y2="18"></line>
                        </svg>
                    </button>
                    <a href="{prefix}index.html" class="brand-link">
                        <span class="brand-badge">DOCS</span>
                        <span class="brand-title">{html.escape(title)}</span>
                    </a>
                </div>
                <nav class="desktop-nav">
                    {nav_links}
                    <a href="{prefix}about.html" class="nav-link { "active" if active_cat == "about" else "" }">About</a>
                </nav>
                <div class="header-right">
                    <a href="{repo_url}" target="_blank" rel="noopener noreferrer" class="gh-btn">
                        <svg height="18" width="18" viewBox="0 0 16 16" fill="currentColor">
                            <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
                        </svg>
                        <span>GitHub</span>
                    </a>
                </div>
            </div>
        </header>
        """

    def make_sidebar(prefix: str, active_cat: str = "", active_stem: str = ""):
        cat_sections = []
        for c in categories:
            cm = zip_meta[c]
            is_cur_cat = (active_cat == c)
            mod_links = "".join([
                f'<li><a href="{prefix}{c}/{r["stem"]}/index.html" class="sidebar-module-link { "active" if is_cur_cat and active_stem == r["stem"] else "" }" title="{r["file_name"]}">{r["file_name"]}</a></li>'
                for r in grouped[c]
            ])
            cat_sections.append(f"""
            <div class="sidebar-lang-section">
                <a href="{prefix}{c}/feed.html" class="sidebar-feed-head { "active" if is_cur_cat and not active_stem else "" }">
                    <span>{cm['icon']} {cm['display']}</span>
                    <span class="feed-badge">Feed ({len(grouped[c])})</span>
                </a>
                <ul class="sidebar-module-list">
                    {mod_links}
                </ul>
            </div>
            """)

        all_cats = "\n".join(cat_sections)
        return f"""
        <div class="sidebar-backdrop" id="sidebarBackdrop"></div>
        <aside class="site-sidebar" id="siteSidebar" aria-label="Main Navigation">
            <div class="sidebar-header">
                <a href="{prefix}index.html" class="sidebar-brand">
                    <span class="brand-badge">DOCS</span>
                    <span class="brand-title">{html.escape(title)}</span>
                </a>
                <button class="close-sidebar-btn" id="closeSidebarBtn" aria-label="Close menu">&times;</button>
            </div>
            <div class="sidebar-content">
                <div class="sidebar-root-links">
                    <a href="{prefix}index.html" class="sidebar-nav-item { "active" if not active_cat and not active_stem else "" }">Manual Overview</a>
                    <a href="{prefix}about.html" class="sidebar-nav-item { "active" if active_cat == "about" else "" }">About &amp; Architecture</a>
                </div>
                {all_cats}
            </div>
        </aside>
        """

    def make_footer(prefix: str):
        return f"""
        <footer class="site-footer">
            <div class="footer-container">
                <div>
                    {html.escape(title)} &bull; Creator: <strong>{html.escape(author_name)}</strong>
                </div>
                <div class="footer-links">
                    <a href="{prefix}about.html">About &amp; License</a>
                    <a href="{repo_url}" target="_blank" rel="noopener noreferrer">Official GitHub</a>
                    <a href="{author_website}" target="_blank" rel="noopener noreferrer">Portfolio</a>
                </div>
            </div>
        </footer>
        """

    # 4. Generate 51 Module Pages
    for c in categories:
        cm = zip_meta[c]
        total_in_cat = len(grouped[c])
        for idx, r in enumerate(grouped[c], start=1):
            stem = r["stem"]
            mod_dir = output_dir / c / stem
            mod_dir.mkdir(parents=True, exist_ok=True)

            # Copy raw code file
            (mod_dir / r["file_name"]).write_text(r["code"], encoding="utf-8")

            # Paging feet
            prev_mod = grouped[c][idx - 2] if idx > 1 else None
            next_mod = grouped[c][idx] if idx < total_in_cat else None

            prev_btn = f'<a href="../{prev_mod["stem"]}/index.html" class="paging-btn">&larr; {prev_mod["file_name"]}</a>' if prev_mod else '<span class="paging-btn disabled">&larr; First Module</span>'
            next_btn = f'<a href="../{next_mod["stem"]}/index.html" class="paging-btn">{next_mod["file_name"]} &rarr;</a>' if next_mod else '<span class="paging-btn disabled">Last Module &rarr;</span>'

            paging_html = f"""
            <div class="paging-feet">
                {prev_btn}
                <div class="paging-status">{cm['display']} &bull; Module {idx} of {total_in_cat}</div>
                {next_btn}
            </div>
            """

            desc_html = "\n".join(f"<p>{p}</p>" for p in r["paragraphs"])
            root_prefix = "../../"

            doc_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{r['file_name']} &middot; {cm['display']} &middot; {title}</title>
    <meta name="description" content="{r['file_name']} in {title}. {r['subtitle']}">
    <style>
        {get_common_styles()}
    </style>
    <link rel="stylesheet" href="{root_prefix}styles.css">
</head>
<body>
    {make_header(root_prefix, active_cat=c)}
    {make_sidebar(root_prefix, active_cat=c, active_stem=stem)}

    <main class="main-wrapper">
        <nav class="breadcrumbs" aria-label="Breadcrumb">
            <a href="../../index.html">Manual</a>
            <span class="sep">/</span>
            <a href="../feed.html">{cm['display']} Feed</a>
            <span class="sep">/</span>
            <span class="current">{r['file_name']}</span>
        </nav>

        <section class="hero-card">
            <div class="hero-badge-row">
                <span class="pill-badge red">{cm['icon']} {cm['display']}</span>
                <span class="pill-badge">Module {idx} of {total_in_cat}</span>
                <span class="pill-badge">v{r['version']}</span>
                <span class="pill-badge">{r['lines_count']:,} Lines</span>
                <span class="pill-badge">{r['size_kb']} KB</span>
            </div>
            <h1 class="hero-title">{r['file_name']}</h1>
            <p class="hero-subtitle">{r['subtitle']}</p>

            <div class="btn-toolbar">
                <a href="{r['file_name']}" download class="btn btn-primary">
                    <svg viewBox="0 0 20 20" width="16" height="16" fill="currentColor"><path d="M10.75 2.75a.75.75 0 00-1.5 0v8.614L6.295 8.235a.75.75 0 10-1.09 1.03l4.25 4.5a.75.75 0 001.09 0l4.25-4.5a.75.75 0 00-1.09-1.03l-2.955 3.129V2.75z"/><path d="M3.5 12.75a.75.75 0 00-1.5 0v2.5A2.75 2.75 0 004.75 18h10.5A2.75 2.75 0 0018 15.25v-2.5a.75.75 0 00-1.5 0v2.5c0 .69-.56 1.25-1.25 1.25H4.75c-.69 0-1.25-.56-1.25-1.25v-2.5z"/></svg>
                    Download Raw {r['file_name']}
                </a>
                <a href="{r['file_name']}" target="_blank" class="btn btn-secondary">View Raw Source</a>
                <a href="../feed.html" class="btn btn-secondary">&larr; Back to {cm['display']} Feed</a>
                <a href="../../downloads/{cm['zip_name']}" download class="btn btn-secondary">
                    Download Full {cm['display']} Zip ({cm['file_count']} Files)
                </a>
            </div>
        </section>

        <section class="doc-section">
            <h2 class="doc-section-title">Architectural Specification &amp; Study</h2>
            <div class="passage-content">
                {desc_html}
            </div>
        </section>

        <section class="code-stage">
            <div class="code-header">
                <div class="code-title">
                    <span class="dot"></span>
                    <span>{r['file_name']}</span>
                    <span style="opacity: 0.6;">&bull; {r['lines_count']:,} lines &bull; {r['size_kb']} KB</span>
                </div>
                <button class="copy-btn" onclick="copyCode(this)">Copy Code</button>
            </div>
            <div class="code-body">
                <pre><code>{html.escape(r['code'])}</code></pre>
            </div>
        </section>

        {paging_html}
    </main>

    {make_footer(root_prefix)}
    <script src="{root_prefix}script.js"></script>
</body>
</html>
"""
            (mod_dir / "index.html").write_text(doc_html, encoding="utf-8")

    # 5. Generate Category Feeds
    for c in categories:
        cm = zip_meta[c]
        cards = []
        for idx, r in enumerate(grouped[c], start=1):
            cards.append(f"""
            <article class="feed-card">
                <div>
                    <div class="feed-card-header">
                        <h3 class="feed-card-title">{r['file_name']}</h3>
                        <span class="feed-card-idx">#{idx}</span>
                    </div>
                    <div class="feed-card-subtitle">{r['subtitle']}</div>
                    <p class="feed-card-snippet">{r['snippet']}</p>
                </div>
                <div>
                    <div class="feed-card-meta">
                        <span>{r['lines_count']:,} lines</span>
                        <span>&bull;</span>
                        <span>{r['size_kb']} KB</span>
                        <span>&bull;</span>
                        <span>v{r['version']}</span>
                    </div>
                    <div class="feed-card-actions">
                        <a href="{r['stem']}/index.html" class="btn btn-primary">Read Documentation</a>
                        <a href="{r['stem']}/{r['file_name']}" download class="btn btn-secondary">Raw ({r['file_name'].split('.')[-1]})</a>
                    </div>
                </div>
            </article>
            """)

        cards_joined = chr(10).join(cards)
        root_prefix = "../"
        feed_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{cm['display']} Feed &middot; {title}</title>
    <meta name="description" content="Official {cm['display']} Module Feed for {title}.">
    <style>
        {get_common_styles()}
    </style>
    <link rel="stylesheet" href="{root_prefix}styles.css">
</head>
<body>
    {make_header(root_prefix, active_cat=c)}
    {make_sidebar(root_prefix, active_cat=c)}

    <main class="main-wrapper">
        <nav class="breadcrumbs" aria-label="Breadcrumb">
            <a href="../index.html">Manual</a>
            <span class="sep">/</span>
            <span class="current">{cm['display']} Feed</span>
        </nav>

        <section class="hero-card">
            <div class="hero-badge-row">
                <span class="pill-badge red">{cm['icon']} {cm['display']}</span>
                <span class="pill-badge">{len(grouped[c])} Production Modules</span>
            </div>
            <h1 class="hero-title">{cm['display']} Core Modules</h1>
            <p class="hero-subtitle">
                Official module feed for {cm['display']}. Each module includes dedicated technical documentation, unique descriptions, and raw source downloads.
            </p>

            <div class="btn-toolbar">
                <a href="../downloads/{cm['zip_name']}" download class="btn btn-primary">
                    <svg viewBox="0 0 20 20" width="16" height="16" fill="currentColor"><path d="M10.75 2.75a.75.75 0 00-1.5 0v8.614L6.295 8.235a.75.75 0 10-1.09 1.03l4.25 4.5a.75.75 0 001.09 0l4.25-4.5a.75.75 0 00-1.09-1.03l-2.955 3.129V2.75z"/><path d="M3.5 12.75a.75.75 0 00-1.5 0v2.5A2.75 2.75 0 004.75 18h10.5A2.75 2.75 0 0018 15.25v-2.5a.75.75 0 00-1.5 0v2.5c0 .69-.56 1.25-1.25 1.25H4.75c-.69 0-1.25-.56-1.25-1.25v-2.5z"/></svg>
                    Download Full {cm['display']} Zip ({len(grouped[c])} Files &bull; {cm['size_kb']} KB)
                </a>
                <a href="../index.html" class="btn btn-secondary">&larr; Return to Manual Overview</a>
            </div>
        </section>

        <div class="feed-filter-bar">
            <input type="text" id="feedSearch" class="feed-search-input" placeholder="Filter {cm['display']} modules..." aria-label="Search modules">
            <div style="font-size: 13px; color: var(--text-muted);">
                Showing <strong>{len(grouped[c])}</strong> modules
            </div>
        </div>

        <div class="feed-grid">
            {cards_joined}
        </div>
    </main>

    {make_footer(root_prefix)}
    <script src="{root_prefix}script.js"></script>
</body>
</html>
"""
        (output_dir / c / "feed.html").write_text(feed_html, encoding="utf-8")
        (output_dir / c / "index.html").write_text(feed_html, encoding="utf-8")

    # 6. Generate Root index.html
    root_sections = []
    for c in categories:
        cm = zip_meta[c]
        sample_cards = []
        for r in grouped[c][:4]:
            sample_cards.append(f"""
            <a href="{c}/{r['stem']}/index.html" class="feed-card" style="padding: 16px;">
                <div class="feed-card-header" style="margin-bottom: 4px;">
                    <span style="font-weight: 700; font-size: 14.5px; color: var(--text-primary);">{r['file_name']}</span>
                    <span class="feed-card-idx" style="font-size: 11px;">{r['size_kb']} KB</span>
                </div>
                <div style="font-size: 12.5px; color: var(--text-muted); margin-bottom: 8px;">{r['subtitle']}</div>
                <div style="font-size: 12px; color: var(--accent); font-weight: 600;">Explore Documentation &rarr;</div>
            </a>
            """)

        sample_cards_joined = chr(10).join(sample_cards)
        root_sections.append(f"""
        <section class="doc-section">
            <div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid var(--border-subtle);">
                <div>
                    <h2 style="font-size: 20px; font-weight: 700; color: var(--text-primary); display: flex; align-items: center; gap: 8px;">
                        <span>{cm['icon']}</span>
                        <span>{cm['display']}</span>
                        <span class="pill-badge" style="font-size: 12px;">{len(grouped[c])} Modules</span>
                    </h2>
                </div>
                <div style="display: flex; align-items: center; gap: 10px;">
                    <a href="{c}/feed.html" class="btn btn-primary" style="padding: 7px 14px; font-size: 13px;">View {cm['display']} Feed &rarr;</a>
                    <a href="downloads/{cm['zip_name']}" download class="btn btn-secondary" style="padding: 7px 14px; font-size: 13px;">Raw Zip ({cm['size_kb']} KB)</a>
                </div>
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 14px;">
                {sample_cards_joined}
            </div>
        </section>
        """)

    root_sections_joined = chr(10).join(root_sections)
    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
    <meta name="description" content="Authoritative documentation and raw library downloads for {html.escape(title)}.">
    <style>
        {get_common_styles()}
    </style>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    {make_header("", active_cat="")}
    {make_sidebar("", active_cat="")}

    <main class="main-wrapper">
        <section class="hero-card">
            <div class="hero-badge-row">
                <span class="pill-badge red">{len(records)} Core Modules</span>
                <span class="pill-badge"><a href="{repo_url}" target="_blank" rel="noopener noreferrer" style="display: inline-flex; align-items: center; gap: 4px;"><svg height="12" width="12" viewBox="0 0 16 16" fill="currentColor"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg> Official Repo</a></span>
            </div>
            <h1 class="hero-title">{html.escape(title)}</h1>
            <p class="hero-subtitle">
                The authoritative polyglot manual, reference guide, and raw distribution repository for {html.escape(author_name)}'s core libraries.
            </p>

            <div class="btn-toolbar">
                <a href="about.html" class="btn btn-primary">About &amp; Architecture &rarr;</a>
                <a href="{repo_url}" target="_blank" rel="noopener noreferrer" class="btn btn-secondary">
                    Official GitHub: {repo_url.replace("https://github.com/", "")}
                </a>
            </div>
        </section>

        {root_sections_joined}

        <section class="doc-section">
            <h2 class="doc-section-title">License &amp; Attribution Notice</h2>
            <div class="passage-content">
                <p>
                    All modules in this compendium are authored by <strong>{html.escape(author_name)}</strong> and published under the terms of the <strong>{html.escape(license_name)}</strong>.
                </p>
                <p>
                    Official GitHub Repository: <a href="{repo_url}" target="_blank" rel="noopener noreferrer" style="color: var(--accent);">{repo_url}</a>
                </p>
            </div>
        </section>
    </main>

    {make_footer("")}
    <script src="script.js"></script>
</body>
</html>
"""
    (output_dir / "index.html").write_text(index_html, encoding="utf-8")

    # 7. Generate about.html
    about_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About &middot; {html.escape(title)}</title>
    <meta name="description" content="Architecture, governance, and licensing for {html.escape(title)}.">
    <style>
        {get_common_styles()}
    </style>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    {make_header("", active_cat="about")}
    {make_sidebar("", active_cat="about")}

    <main class="main-wrapper">
        <nav class="breadcrumbs" aria-label="Breadcrumb">
            <a href="index.html">Manual</a>
            <span class="sep">/</span>
            <span class="current">About</span>
        </nav>

        <section class="hero-card">
            <h1 class="hero-title">About {html.escape(title)}</h1>
            <p class="hero-subtitle">
                System architecture, design invariants, and governance guidelines.
            </p>
        </section>

        <section class="doc-section">
            <h2 class="doc-section-title">Author &amp; Repository Credits</h2>
            <div class="passage-content">
                <p><strong>Author &amp; Creator:</strong> {html.escape(author_name)}</p>
                <p><strong>Official Repository:</strong> <a href="{repo_url}" target="_blank" rel="noopener noreferrer" style="color: var(--accent);">{repo_url}</a></p>
                <p><strong>Website:</strong> <a href="{author_website}" target="_blank" rel="noopener noreferrer" style="color: var(--accent);">{author_website}</a></p>
                <p><strong>Contact:</strong> <a href="mailto:{author_email}" style="color: var(--accent);">{author_email}</a></p>
                <p><strong>Licensing:</strong> {html.escape(license_name)}</p>
            </div>
        </section>
    </main>

    {make_footer("")}
    <script src="script.js"></script>
</body>
</html>
"""
    (output_dir / "about.html").write_text(about_html, encoding="utf-8")

    # 8. Generate sitemap.xml & robots.txt
    sitemap_urls = [
        f"  <url><loc>{author_website}/index.html</loc><priority>1.0</priority></url>",
        f"  <url><loc>{author_website}/about.html</loc><priority>0.8</priority></url>"
    ]
    for c in categories:
        sitemap_urls.append(f"  <url><loc>{author_website}/{c}/feed.html</loc><priority>0.9</priority></url>")
        for r in grouped[c]:
            sitemap_urls.append(f"  <url><loc>{author_website}/{c}/{r['stem']}/index.html</loc><priority>0.85</priority></url>")

    sitemap_urls_joined = chr(10).join(sitemap_urls)
    sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sitemap_urls_joined}\n</urlset>"""
    (output_dir / "sitemap.xml").write_text(sitemap_xml, encoding="utf-8")

    robots_txt = f"User-agent: *\nAllow: /\nSitemap: {author_website}/sitemap.xml\n"
    (output_dir / "robots.txt").write_text(robots_txt, encoding="utf-8")

    # 9. Master ZIP
    zip_path = None
    if repackage_zip:
        zip_path = output_dir.parent / f"{output_dir.name}.zip"
        all_files = [Path("index.html"), Path("about.html"), Path("styles.css"), Path("script.js"), Path("sitemap.xml"), Path("robots.txt")]
        for c in categories:
            all_files.append(Path("downloads") / zip_meta[c]["zip_name"])
            all_files.append(Path(c) / "feed.html")
            all_files.append(Path(c) / "index.html")
            for r in grouped[c]:
                all_files.append(Path(c) / r["stem"] / "index.html")
                all_files.append(Path(c) / r["stem"] / r["file_name"])

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for rel in all_files:
                p = output_dir / rel
                if p.exists():
                    zf.write(p, arcname=str(rel))

    return {
        "status": "success",
        "output_dir": str(output_dir),
        "total_modules": len(records),
        "categories": {c: len(grouped[c]) for c in categories},
        "zip_path": str(zip_path) if zip_path else None
    }

def main():
    parser = argparse.ArgumentParser(
        description="Build mobile-responsive, SEO-structured documentation manuals and e-books from source codebases."
    )
    parser.add_argument("--source", "-s", required=True, help="Path to directory containing source library files")
    parser.add_argument("--output", "-o", required=True, help="Destination directory for generated documentation site")
    parser.add_argument("--title", "-t", default="BEJSON 105 Manual", help="Title of the manual/e-book")
    parser.add_argument("--repo-url", "-r", default="https://github.com/boehnenelton/BEJSON_105", help="Official repository URL")
    parser.add_argument("--author", "-a", default="Elton Boehnen", help="Author & Creator name")
    parser.add_argument("--author-email", default="eltonboehnen@gmail.com", help="Author contact email")
    parser.add_argument("--author-website", default="https://boehnenelton2024.pages.dev", help="Author portfolio/website URL")
    parser.add_argument("--license", default="PolyForm Noncommercial License 1.0.0", help="License name")
    parser.add_argument("--dry-run", action="store_true", help="Scan files and print metadata without writing")
    parser.add_argument("--no-zip", action="store_true", help="Skip packaging the master zip archive")

    args = parser.parse_args()

    source_path = Path(args.source).resolve()
    if not source_path.exists():
        print(f"Error: Source directory {source_path} does not exist.")
        sys.exit(1)

    output_path = Path(args.output).resolve()

    res = build_ebook_portal(
        source_dir=source_path,
        output_dir=output_path,
        title=args.title,
        repo_url=args.repo_url,
        author_name=args.author,
        author_email=args.author_email,
        author_website=args.author_website,
        license_name=args.license,
        dry_run=args.dry_run,
        repackage_zip=not args.no_zip
    )

    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main()
