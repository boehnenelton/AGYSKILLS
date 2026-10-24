#!/usr/bin/env python3
"""
Name:           run_cms_manage
File:           run_cms_manage.py
Description:    Deterministic Layer 3 execution wrapper for BEJSON CMS management operations.
                Dispatches CLI subcommands to src/cms-manage.py with automated path detection,
                error auditing, and exit code propagation.
Version:        100
Date Created:   2026-10-21
Author:         Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID:  4a3b2c1d-0e9f-8a7b-6c5d-4e3f2a1b0c9d
Release_Version: 300
"""

import sys

if sys.version_info < (3, 10):
    sys.stderr.write("run_cms_manage requires Python 3.10 or newer.\n")
    sys.exit(20)

import os
import logging
import subprocess
from pathlib import Path
from typing import List

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
LOG = logging.getLogger("run_cms_manage")


def get_cms_cli_path() -> Path:
    env_cli = os.environ.get("CMS_CLI_PATH")
    if env_cli and Path(env_cli).exists():
        return Path(env_cli)
    default_path = Path("/storage/emulated/0/Admin/Dev/Python/Development/BEJSON_CMS/src/cms-manage.py")
    return default_path


def execute_cms_command(cli_args: List[str]) -> int:
    cli_path = get_cms_cli_path()
    if not cli_path.exists():
        LOG.error("cms-manage.py executable not found at: %s", cli_path)
        return EXIT_PATH_FAILURE

    cmd = [sys.executable, str(cli_path)] + cli_args
    LOG.info("Executing: %s", " ".join(cmd))

    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cli_path.parent),
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.stdout:
            sys.stdout.write(proc.stdout)
            sys.stdout.flush()
        if proc.stderr:
            sys.stderr.write(proc.stderr)
            sys.stderr.flush()

        if proc.returncode != 0:
            LOG.error("cms-manage.py failed with return code %d", proc.returncode)
            return EXIT_SCHEMA_FAILURE

        return EXIT_OK
    except Exception as exc:
        LOG.error("Subprocess execution failed: %s", exc)
        return EXIT_ENV_FAILURE


def main() -> None:
    args = sys.argv[1:]
    if not args:
        LOG.info("No arguments provided. Invoking default health check: 'doctor'.")
        args = ["doctor"]
    sys.exit(execute_cms_command(args))


if __name__ == "__main__":
    main()
