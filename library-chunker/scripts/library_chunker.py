#!/usr/bin/env python3
"""
library_chunker.py
==================
Dedicated Library Chunking & Orchestration Engine
Elton Boehnen · boehnenelton2024@gmail.com

Orchestrates the 3-Tier Chunking Architecture for Admin Libraries (104 & 105):
1. Entire Library Snapshots (libraries_104 & libraries_105) via Project Chunker
   with --track and --chunk, registering whole projects and deploying to Chunked_Libraries.
2. Library Family Subsystems (Lib_JS, Lib_PY, Lib_SH, Lib_TS) via Simple Chunker
   into flat, lightweight .104a.bejson.txt containers.
3. Ephemeral Stage-and-Snap for cross-system collections (e.g. Core across all systems),
   automatically pruning the staging folder after chunking.
"""

import os
import sys
import shutil
import argparse
import subprocess
import glob
from pathlib import Path

# ANSI colors for 57-column TUI formatting
COLOR_RED = "\033[38;2;222;38;38m"
COLOR_RESET = "\033[0m"
COLOR_BOLD = "\033[1m"
COLOR_GRAY = "\033[90m"
COLOR_GREEN = "\033[32m"

ADMIN_LIBRARIES = os.environ.get("ADMIN_LIBRARIES", "/storage/emulated/0/Admin/Libraries")
ADMIN_LIBRARIES_104 = os.environ.get("ADMIN_LIBRARIES_104", os.path.join(ADMIN_LIBRARIES, "libraries_104"))
ADMIN_LIBRARIES_105 = os.environ.get("ADMIN_LIBRARIES_105", os.path.join(ADMIN_LIBRARIES, "libraries_105"))
CHUNKED_LIBRARIES = os.environ.get("CHUNKED_LIBRARIES", os.path.join(ADMIN_LIBRARIES, "Chunked_Libraries"))
PROJECT_CHUNKER = os.environ.get("PROJECT_CHUNKER", "/storage/emulated/0/Admin/System/Project_Chunker")
PROJECT_CHUNKER_CLI = os.path.join(PROJECT_CHUNKER, "CLI", "project_chunker.py")
SIMPLE_CHUNKER_CLI = os.path.expanduser("~/.gemini/config/skills/chunking-core/scripts/Simple_Chunker_CLI.py")
LOGGING_TOOL = os.environ.get("LOGGING_TOOL", "/storage/emulated/0/Admin/System/tools/logging_tool/logging_tool.py")

FAMILIES = ["Lib_JS", "Lib_PY", "Lib_SH", "Lib_TS"]

def log_event(message: str, key: str, status: str = "completed"):
    if os.path.isfile(LOGGING_TOOL):
        context_payload = f'{{"task": "library_chunker", "status": "{status}", "action": "{key}"}}'
        cmd = [
            sys.executable, LOGGING_TOOL, "write",
            "-m", message,
            "-l", "INFO",
            "-k", f"library_chunker.{key}",
            "-s", "library_chunker",
            "--category", "storage",
            "--flag", "chunker",
            "--context", context_payload
        ]
        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

def print_header(title: str):
    print(f"{COLOR_RED}========================================================={COLOR_RESET}")
    print(f" {COLOR_BOLD}{title.ljust(55)}{COLOR_RESET}")
    print(f"{COLOR_RED}---------------------------------------------------------{COLOR_RESET}")

def print_row(col1: str, col2: str, status: str = "OK"):
    status_str = f"{COLOR_GREEN}[✓]{COLOR_RESET}" if status == "OK" else f"{COLOR_RED}[✗]{COLOR_RESET}"
    line = f" {status_str} {col1.ljust(24)} {col2.ljust(25)}"
    print(line[:67])

def print_footer():
    print(f"{COLOR_RED}========================================================={COLOR_RESET}")

def prune_old_full_snapshots(dest_dir: str, keep_filename: str):
    """Remove outdated full library snapshots in Chunked_Libraries per AGENTS.MD."""
    pattern = os.path.join(dest_dir, "libraries_*.bejson")
    for file_path in glob.glob(pattern):
        if os.path.basename(file_path) != keep_filename:
            try:
                os.remove(file_path)
            except OSError:
                pass

def chunk_full_project(era: str) -> bool:
    """Chunk entire 104 or 105 library suite using Project Chunker."""
    target_dir = ADMIN_LIBRARIES_104 if era == "104" else ADMIN_LIBRARIES_105
    dest_dir = os.path.join(CHUNKED_LIBRARIES, era)
    os.makedirs(dest_dir, exist_ok=True)

    if not os.path.isdir(target_dir):
        print_row(f"Full {era}", "Directory not found", "ERR")
        return False

    # Track project
    track_cmd = [sys.executable, PROJECT_CHUNKER_CLI, "--track", target_dir]
    if era == "105":
        track_cmd.extend(["-V", "5.8.1", "-P", "112", "--type", "library"])
    
    subprocess.run(track_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Chunk project
    chunk_cmd = [sys.executable, PROJECT_CHUNKER_CLI, "--chunk", target_dir]
    if era == "105":
        chunk_cmd.extend(["-V", "5.8.1", "-P", "112", "--type", "library"])

    res = subprocess.run(chunk_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print_row(f"Full {era}", "Project Chunker failed", "ERR")
        return False

    # Find generated snapshot
    snap_dir = os.path.join(PROJECT_CHUNKER, "storage", "project_snapshots", f"libraries_{era}", "data")
    snaps = sorted(glob.glob(os.path.join(snap_dir, f"libraries_{era}-V*.bejson")), key=os.path.getmtime)
    if not snaps:
        print_row(f"Full {era}", "Snapshot file missing", "ERR")
        return False

    latest_snap = snaps[-1]
    dest_snap = os.path.join(dest_dir, os.path.basename(latest_snap))
    shutil.copy2(latest_snap, dest_snap)

    # Clean up outdated full snapshots per AGENTS.MD
    prune_old_full_snapshots(dest_dir, os.path.basename(latest_snap))
    print_row(f"Full libraries_{era}", os.path.basename(latest_snap), "OK")
    return True

def chunk_families(era: str) -> bool:
    """Chunk individual language families using Simple Chunker."""
    base_dir = ADMIN_LIBRARIES_104 if era == "104" else ADMIN_LIBRARIES_105
    dest_dir = os.path.join(CHUNKED_LIBRARIES, era)
    os.makedirs(dest_dir, exist_ok=True)

    success_all = True
    for family in FAMILIES:
        family_dir = os.path.join(base_dir, family)
        if not os.path.isdir(family_dir):
            continue

        cmd = [
            sys.executable, SIMPLE_CHUNKER_CLI,
            "--chunk", family_dir,
            "--dest", dest_dir
        ]
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if res.returncode == 0:
            print_row(f"{era} {family}", f"Chunked_{family}.104a...", "OK")
        else:
            print_row(f"{era} {family}", "Simple Chunker failed", "ERR")
            success_all = False

    return success_all

def stage_and_snap(staging_dir: str, target_name: str, dest_dir: str, items: list) -> bool:
    """
    Stage specified modules/families into a temporary staging folder,
    chunk the staged directory into a single container, and remove the staged directory.
    """
    staging_path = Path(staging_dir)
    staging_path.mkdir(parents=True, exist_ok=True)
    os.makedirs(dest_dir, exist_ok=True)

    try:
        # Copy items to staging
        for src_path in items:
            p = Path(src_path)
            if p.is_dir():
                shutil.copytree(p, staging_path / p.name, dirs_exist_ok=True)
            elif p.is_file():
                shutil.copy2(p, staging_path / p.name)

        # Chunk the staged directory
        cmd = [
            sys.executable, SIMPLE_CHUNKER_CLI,
            "--chunk", str(staging_path),
            "--dest", dest_dir
        ]
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if res.returncode == 0:
            print_row(f"Stage-and-Snap", f"{target_name} -> {dest_dir}", "OK")
            return True
        else:
            print_row(f"Stage-and-Snap", f"Chunking failed", "ERR")
            return False
    finally:
        # Guarantee removal of staging directory after snapshotting
        if staging_path.exists():
            shutil.rmtree(staging_path, ignore_errors=True)

def main():
    parser = argparse.ArgumentParser(description="Dedicated Library Chunking & Orchestration Engine")
    parser.add_argument("--target", choices=["104", "105", "all"], default="all",
                        help="Target library era to chunk (default: all)")
    parser.add_argument("--tier", choices=["all", "full", "families"], default="all",
                        help="Chunking tier: full project, families only, or all (default: all)")
    parser.add_argument("--stage-snap", action="store_true",
                        help="Run stage-and-snap on all Core modules across systems into Compiled_Core")
    args = parser.parse_args()

    print_header("LIBRARY CHUNKER ENGINE")

    eras = ["104", "105"] if args.target == "all" else [args.target]

    for era in eras:
        if args.tier in ["all", "full"]:
            chunk_full_project(era)
        if args.tier in ["all", "families"]:
            chunk_families(era)

    if args.stage_snap:
        # Example stage-and-snap: Compile Core modules across systems for 104
        staging_dir = os.path.join(ADMIN_LIBRARIES, "stage")
        dest_dir = os.path.join(ADMIN_LIBRARIES, "Compiled_Core")
        core_items = []
        for sys_name in FAMILIES:
            core_dir = os.path.join(ADMIN_LIBRARIES_104, sys_name, "Core")
            if os.path.isdir(core_dir):
                core_items.append(core_dir)
        if core_items:
            stage_and_snap(staging_dir, "Compiled_Core_104", dest_dir, core_items)

    print_footer()
    log_event(f"Completed library chunking for era(s): {','.join(eras)} tier={args.tier}", "execution")

if __name__ == "__main__":
    main()
