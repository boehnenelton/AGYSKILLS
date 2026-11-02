#!/usr/bin/env python3
"""
Name:           showcase_stateful_cli.py
Description:    Exemplar CLI implementing Loaded Chamber Stateful Target Architecture
Version:        1.0.0
Author:         Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID:  74a12903-81b4-4ef1-a832-72c058726bc1
"""

from __future__ import annotations
import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

# Self-locating path
SCRIPT_DIRECTORY: Path = Path(__file__).resolve().parent
STATE_DATA_DIRECTORY: Path = SCRIPT_DIRECTORY.parent / "data"
CHAMBER_STATE_FILE: Path = STATE_DATA_DIRECTORY / "cli_chamber_state.json"

# Policy §8.1 Palette
ANSI_RED: str = "\033[1;38;2;222;38;38m" if os.getenv("COLORTERM") else "\033[1;31m"
ANSI_WHITE: str = "\033[1;37m"
ANSI_RESET: str = "\033[0m"


def load_chamber_state() -> Dict[str, Any]:
    """Load persistent context from disk."""
    if not CHAMBER_STATE_FILE.exists():
        return {}
    try:
        with open(CHAMBER_STATE_FILE, "r", encoding="utf-8") as file_handle:
            return json.load(file_handle)
    except Exception:
        return {}


def save_chamber_state(state_payload: Dict[str, Any]) -> None:
    """Save persistent context atomically."""
    STATE_DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)
    temporary_file: Path = CHAMBER_STATE_FILE.with_suffix(".tmp")
    with open(temporary_file, "w", encoding="utf-8") as file_handle:
        json.dump(state_payload, file_handle, indent=2)
        file_handle.write("\n")
    temporary_file.replace(CHAMBER_STATE_FILE)


def clear_chamber_state() -> None:
    """Nullify loaded chamber state."""
    if CHAMBER_STATE_FILE.exists():
        CHAMBER_STATE_FILE.unlink()


def handle_context_command(parsed_arguments: argparse.Namespace) -> int:
    """Manage, inspect, or mutate the loaded chamber state."""
    if parsed_arguments.clear_flag:
        clear_chamber_state()
        # NEUTRAL STATUS: normal standard rules
        print(f"{ANSI_RED}[*]{ANSI_RESET} Chamber context cleared.")
        return 0

    current_state: Dict[str, Any] = load_chamber_state()

    has_modifications: bool = False
    if parsed_arguments.target_argument:
        current_state["active_target"] = parsed_arguments.target_argument
        has_modifications = True
    if parsed_arguments.category_argument:
        current_state["active_category"] = parsed_arguments.category_argument
        has_modifications = True
    if parsed_arguments.session_argument:
        current_state["active_session"] = parsed_arguments.session_argument
        has_modifications = True

    if has_modifications:
        save_chamber_state(current_state)
        # NEUTRAL STATUS: normal standard rules
        print(f"{ANSI_RED}[*]{ANSI_RESET} Chamber context updated.")

    if parsed_arguments.json_output:
        print(json.dumps(current_state, indent=2))
    else:
        print(f"{ANSI_RED}--- LOADED CHAMBER CONTEXT ---{ANSI_RESET}")
        for context_key, context_value in current_state.items():
            print(f"  {ANSI_RED}{context_key:<18}:{ANSI_RESET} {context_value}")
        if not current_state:
            print("  (Empty - no target loaded)")

    return 0


def handle_execute_command(parsed_arguments: argparse.Namespace) -> int:
    """Execute action against loaded target without argument repetition."""
    chamber_state: Dict[str, Any] = load_chamber_state()
    resolved_target: Optional[str] = parsed_arguments.target_override or chamber_state.get("active_target")

    if not resolved_target:
        # BAD FEEDBACK: lowercase red with [X]
        sys.stderr.write(
            f"{ANSI_RED}[X] no active target in chamber. "
            f"set via 'context --set-target <name>' or specify --target.\n{ANSI_RESET}"
        )
        return 1

    action_verb: str = parsed_arguments.action_name
    print(
        f"{ANSI_RED}[*]{ANSI_RESET} Executing action '{action_verb}' "
        f"against loaded target [{resolved_target}]..."
    )
    # POSITIVE STATUS FEEDBACK: WHITE, ALL CAPS
    print(f"{ANSI_WHITE}[✓] ACTION '{action_verb.upper()}' COMPLETED SUCCESSFULLY.{ANSI_RESET}")
    return 0


def build_cli_parser() -> argparse.ArgumentParser:
    """Assemble strict CLI command tree."""
    master_parser = argparse.ArgumentParser(
        prog="showcase_stateful_cli",
        description="Loaded Chamber Stateful CLI Exemplar"
    )
    subparsers_collection = master_parser.add_subparsers(dest="subcommand_name", required=True)

    # Context management subcommand
    context_parser = subparsers_collection.add_parser("context", help="Inspect or lock chamber state")
    context_parser.add_argument("--set-target", dest="target_argument", help="Lock active target into chamber")
    context_parser.add_argument("--set-category", dest="category_argument", help="Lock active category into chamber")
    context_parser.add_argument("--set-session", dest="session_argument", help="Lock active session ID into chamber")
    context_parser.add_argument("--clear", dest="clear_flag", action="store_true", help="Nullify chamber state")
    context_parser.add_argument("--json", dest="json_output", action="store_true", help="Emit raw JSON")

    # Execution subcommand
    execute_parser = subparsers_collection.add_parser("exec", help="Execute verb against loaded target")
    execute_parser.add_argument("action_name", help="Action verb to fire")
    execute_parser.add_argument("--target", dest="target_override", help="Override loaded target")

    return master_parser


def main() -> int:
    parser = build_cli_parser()
    arguments = parser.parse_args()

    if arguments.subcommand_name == "context":
        return handle_context_command(arguments)
    elif arguments.subcommand_name == "exec":
        return handle_execute_command(arguments)

    return 0


if __name__ == "__main__":
    sys.exit(main())
