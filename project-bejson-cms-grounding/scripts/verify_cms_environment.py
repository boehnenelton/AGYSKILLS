#!/usr/bin/env python3
"""
Name:           verify_cms_environment
File:           verify_cms_environment.py
Description:    Deterministic Layer 2 / Layer 5 verification script for BEJSON CMS.
                Audits project root, storage structures, central 104a.mfdb.bejson
                manifest, and runs live diagnostic validation.
Version:        100
Date Created:   2026-10-21
Author:         Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID:  7b9a1c3e-5f8d-4206-b31a-9e4f2a7c8052
Release_Version: 300
"""

import sys

if sys.version_info < (3, 10):
    sys.stderr.write("verify_cms_environment requires Python 3.10 or newer.\n")
    sys.exit(20)

import os
import json
import logging
import subprocess
from pathlib import Path
from typing import Dict, Any, List

VERSION: int = 100
RELEASE_VERSION: int = 300

EXIT_OK: int = 0
EXIT_PATH_FAILURE: int = 10
EXIT_ENV_FAILURE: int = 20
EXIT_SCHEMA_FAILURE: int = 30

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
LOG = logging.getLogger("verify_cms_environment")


def get_script_path() -> Path:
    return Path(__file__).resolve().parent


def verify_bejson_cms_grounding(repo_path_str: str) -> int:
    repo_path = Path(repo_path_str)
    if not repo_path.exists():
        LOG.error("Target BEJSON CMS repository does not exist at %s", repo_path)
        return EXIT_PATH_FAILURE

    # Verify key paths
    manifest_path = repo_path / "storage" / "mfdb" / "site_master" / "104a.mfdb.bejson"
    cli_path = repo_path / "src" / "cms-manage.py"
    tracker_path = repo_path / ".bejson_project.json"

    for required_file in (manifest_path, cli_path, tracker_path):
        if not required_file.exists():
            LOG.error("Missing critical file: %s", required_file)
            return EXIT_PATH_FAILURE

    LOG.info("Verified critical files present at %s", repo_path)

    # Validate manifest format
    try:
        manifest_data = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest_data.get("Format") != "BEJSON":
            LOG.error("Manifest at %s is not valid BEJSON.", manifest_path)
            return EXIT_SCHEMA_FAILURE
    except Exception as exc:
        LOG.error("Failed to parse manifest: %s", exc)
        return EXIT_SCHEMA_FAILURE

    # Run cms-manage.py doctor as a subprocess
    try:
        cmd_result = subprocess.run(
            [sys.executable, str(cli_path), "doctor"],
            cwd=str(cli_path.parent),
            capture_output=True,
            text=True,
            check=False,
        )
        if cmd_result.returncode != 0:
            LOG.error("cms-manage.py doctor reported issues:\n%s", cmd_result.stdout)
            return EXIT_SCHEMA_FAILURE
        LOG.info("cms-manage.py doctor completed cleanly:\n%s", cmd_result.stdout.strip())
    except Exception as exc:
        LOG.error("Failed to execute cms-manage.py doctor: %s", exc)
        return EXIT_ENV_FAILURE

    LOG.info("BEJSON CMS environment verification SUCCEEDED.")
    return EXIT_OK


def main() -> None:
    target_repo = os.environ.get(
        "CMS_REPO_PATH",
        "/storage/emulated/0/Admin/Dev/Python/Development/BEJSON_CMS",
    )
    exit_code = verify_bejson_cms_grounding(target_repo)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
