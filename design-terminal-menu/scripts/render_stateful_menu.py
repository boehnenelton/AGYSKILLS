#!/usr/bin/env python3
"""
Name:           render_stateful_menu.py
Description:    Archetype 2: Stateful Selection & Submenu Terminal Menu
                Implements Persistent State Header, Top Action Strip, and Submenu Drill-Down
Version:        1.0.0
Author:         Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID:  f5910248-1823-4c91-a1b2-ee0294b19283
"""

from __future__ import annotations
import atexit
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

VERSION: str = "1.0.0"

# Policy §8.1 Tri-Color Palette Constants
COLOR_BOLD_RED: str = "\033[1;38;2;222;38;38m"
COLOR_ACCENT_RED: str = "\033[38;2;222;38;38m"
COLOR_ANSI_RED: str = "\033[1;31m"
COLOR_WHITE: str = "\033[1;37m"
COLOR_DIM: str = "\033[2m"
COLOR_RESET: str = "\033[0m"
CONSOLE_CLEAR: str = "\033[2J\033[H"
CURSOR_SHOW: str = "\033[?25h"

# Persistent selection state file
STATE_DIR: Path = Path(__file__).resolve().parent.parent / "data"
STATE_FILE_PATH: Path = STATE_DIR / "persistent_selection.json"


def resolve_terminal_colors() -> Tuple[str, str, str]:
    """Resolve Truecolor vs ANSI Red fallback."""
    if os.getenv("NO_COLOR") or not sys.stdout.isatty():
        return "", "", ""
    colorterm = os.getenv("COLORTERM", "").lower()
    if "truecolor" in colorterm or "24bit" in colorterm:
        return COLOR_BOLD_RED, COLOR_ACCENT_RED, COLOR_RESET
    return COLOR_ANSI_RED, COLOR_ANSI_RED, COLOR_RESET


BOLD_RED, ACCENT_RED, RESET = resolve_terminal_colors()


def restore_cursor() -> None:
    """Ensure terminal cursor is restored on exit."""
    try:
        sys.stdout.write(CURSOR_SHOW + RESET)
        sys.stdout.flush()
    except (BrokenPipeError, OSError):
        pass


atexit.register(restore_cursor)


def clear_screen() -> None:
    """Clear terminal screen and position cursor at 1,1 before every render."""
    if os.getenv("TUI_NO_CLEAR", "0") != "1":
        sys.stdout.write(CONSOLE_CLEAR)
        sys.stdout.flush()


def get_terminal_display_width() -> int:
    """Clamp separator width between 38 and 57 columns for mobile portrait readability."""
    detected_columns = shutil.get_terminal_size((46, 24)).columns
    return max(38, min(detected_columns, 57))


def load_persistent_selection() -> str:
    """Load the persistent selected item from disk."""
    if not STATE_FILE_PATH.exists():
        return "Null"
    try:
        with open(STATE_FILE_PATH, "r", encoding="utf-8") as file_handle:
            data = json.load(file_handle)
            return data.get("selected_item", "Null")
    except Exception:
        return "Null"


def save_persistent_selection(selected_item_value: str) -> None:
    """Persist the chosen selection to disk atomically."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    temp_file: Path = STATE_FILE_PATH.with_suffix(".tmp")
    with open(temp_file, "w", encoding="utf-8") as file_handle:
        json.dump({"selected_item": selected_item_value}, file_handle, indent=2)
        file_handle.write("\n")
    temp_file.replace(STATE_FILE_PATH)


def format_status_feedback(severity_level: str, message_text: str, max_width: int) -> str:
    """
    Format status feedback message per canonical design rules:
    - POSITIVE: WHITE, ALL CAPS with [✓]
    - BAD: lowercase, red with [X]
    - NEUTRAL: normal standard rules with [*]
    """
    severity_token: str = severity_level.upper()
    truncated_text: str = message_text[:max(10, max_width - 6)]

    if severity_token in ("POSITIVE", "SUCCESS", "OK"):
        # POSITIVE STATUS FEEDBACK: WHITE, ALL CAPS
        return f" {COLOR_WHITE}[✓] {truncated_text.upper()}{RESET}"
    elif severity_token in ("BAD", "ERROR", "FAIL"):
        # BAD FEEDBACK: lowercase red with [X]
        return f" {BOLD_RED}[X] {truncated_text.lower()}{RESET}"
    else:
        # NEUTRAL: normal standard rules
        return f" {BOLD_RED}[*]{RESET} {truncated_text}"


def render_stateful_menu_frame(
    current_view_name: str = "MAIN",
    active_selection_label: str = "Null",
    current_status_message: Optional[str] = None,
    current_status_type: str = "NEUTRAL"
) -> str:
    """
    Render the canonical Stateful Selection Menu:
    - Top rows dedicated to application state [ Selected: <item> ]
    - Global Navigation Strip:
        - Main Menu:  - S) Select - A) Action - X) Exit
        - Submenus:   - S) Select - A) Action - B) Back
    - View options and dynamic feedback line
    - Prompt box [ Choose an option: ]
    """
    width: int = get_terminal_display_width()
    divider_line: str = "-" * width

    # Format selected item box with #DE2626 red highlight
    selection_display_value: str = active_selection_label if active_selection_label else "Null"
    selection_box_string: str = f"   [   Selected:     {BOLD_RED}{selection_display_value}{RESET}    ]   "

    # Global Navigation Strip: B is global except Main Menu which has X to exit
    if current_view_name.upper() == "MAIN":
        nav_strip_string: str = f"-   {BOLD_RED}S){RESET} Select   -    {BOLD_RED}A){RESET} Action   -   {BOLD_RED}X){RESET} Exit"
        header_title: str = "STATEFUL MENU EXAMPLE"
        menu_options_list: List[str] = [
            f"  {BOLD_RED}1){RESET} Info",
            f"  {BOLD_RED}2){RESET} Configure",
            f"  {BOLD_RED}3){RESET} Exit",
            "-",
            "-"
        ]
        prompt_label: str = "Choose an option:"
    elif current_view_name.upper() == "SELECT":
        nav_strip_string: str = f"-   {BOLD_RED}S){RESET} Select   -    {BOLD_RED}A){RESET} Action   -   {BOLD_RED}B){RESET} Back"
        header_title: str = "SELECT ITEM SUBMENU"
        menu_options_list = [
            f"  {BOLD_RED}1){RESET} Executive Fade",
            f"  {BOLD_RED}2){RESET} Buzz Cut",
            f"  {BOLD_RED}3){RESET} Classic Pompadour",
            f"  {BOLD_RED}4){RESET} Textured Crop",
            f"  {BOLD_RED}5){RESET} Tapered Undercut"
        ]
        prompt_label = "Choose item to select:"
    elif current_view_name.upper() == "ACTION":
        nav_strip_string = f"-   {BOLD_RED}S){RESET} Select   -    {BOLD_RED}A){RESET} Action   -   {BOLD_RED}B){RESET} Back"
        header_title = "ACTION MENU"
        menu_options_list = [
            f"  {BOLD_RED}1){RESET} Inspect Attributes",
            f"  {BOLD_RED}2){RESET} Execute Process",
            f"  {BOLD_RED}3){RESET} Reset to Default",
            f"  {BOLD_RED}4){RESET} Export Configuration",
            "-"
        ]
        prompt_label = "Choose an action:"
    elif current_view_name.upper() == "INFO":
        nav_strip_string = f"-   {BOLD_RED}S){RESET} Select   -    {BOLD_RED}A){RESET} Action   -   {BOLD_RED}B){RESET} Back"
        header_title = "SYSTEM INFO"
        menu_options_list = [
            f"  {BOLD_RED}1){RESET} Inspect State File",
            f"  {BOLD_RED}2){RESET} Clear Loaded Selection",
            "-",
            "-",
            "-"
        ]
        prompt_label = "Choose an option:"
    else:  # CONFIG
        nav_strip_string = f"-   {BOLD_RED}S){RESET} Select   -    {BOLD_RED}A){RESET} Action   -   {BOLD_RED}B){RESET} Back"
        header_title = "CONFIGURATION"
        menu_options_list = [
            f"  {BOLD_RED}1){RESET} Toggle 57-Col Clamp",
            f"  {BOLD_RED}2){RESET} Reset Default State Path",
            "-",
            "-",
            "-"
        ]
        prompt_label = "Choose an option:"

    lines_collection: List[str] = [
        f"{BOLD_RED}{(f' {header_title} ').center(width, '=')}{RESET}",
        "",
        selection_box_string,
        "",
        nav_strip_string,
        divider_line,
    ]
    lines_collection.extend(menu_options_list)

    if current_status_message:
        lines_collection.append(format_status_feedback(current_status_type, current_status_message, width))

    lines_collection.append(f"[   {BOLD_RED}{prompt_label}{RESET} ]")
    return "\n".join(lines_collection)


def run_interactive_stateful_loop() -> None:
    """
    Interactive state router executing the Stateful Selection & Submenu Menu.
    S, A, and B are global navigation keys that jump straight between views from anywhere.
    On the main menu, B is replaced by X to exit.
    """
    catalog_items: List[str] = [
        "Executive Fade",
        "Buzz Cut",
        "Classic Pompadour",
        "Textured Crop",
        "Tapered Undercut"
    ]

    current_view: str = "MAIN"
    status_note: Optional[str] = None
    status_kind: str = "NEUTRAL"

    while True:
        current_selection: str = load_persistent_selection()
        clear_screen()
        menu_output: str = render_stateful_menu_frame(
            current_view_name=current_view,
            active_selection_label=current_selection,
            current_status_message=status_note,
            current_status_type=status_kind
        )
        print(menu_output, end=" ")
        sys.stdout.flush()

        try:
            user_input_string: str = input().strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break

        normalized_key: str = user_input_string.upper()

        # -------------------------------------------------------------
        # GLOBAL NAVIGATION INVARIANTS (S, A, B, X)
        # -------------------------------------------------------------
        if normalized_key == "S":
            # Global jump to Selection Submenu from anywhere
            current_view = "SELECT"
            status_note = "Selection Submenu active."
            status_kind = "NEUTRAL"
            continue

        elif normalized_key == "A":
            # Global jump to Action Menu from anywhere
            current_view = "ACTION"
            status_note = "Action Menu active."
            status_kind = "NEUTRAL"
            continue

        elif normalized_key in ("B", "BACK"):
            # Global Back: jumps back to MAIN from any submenu
            if current_view != "MAIN":
                current_view = "MAIN"
                status_note = "Returned to Main Menu."
                status_kind = "NEUTRAL"
            else:
                # On main menu, B is not back; inform user to use X to exit
                status_note = "Already at Main Menu. Enter 'X' to exit."
                status_kind = "NEUTRAL"
            continue

        elif normalized_key in ("X", "EXIT", "QUIT", "Q"):
            # Global Exit (specifically bound to X on main menu)
            print("\nStanding by.")
            break

        # -------------------------------------------------------------
        # VIEW-SPECIFIC DISPATCH
        # -------------------------------------------------------------
        if current_view == "MAIN":
            if normalized_key == "1":
                current_view = "INFO"
                status_note = f"Info View: Active Item='{current_selection}'"
                status_kind = "NEUTRAL"
            elif normalized_key == "2":
                current_view = "CONFIG"
                status_note = "Configuration View active."
                status_kind = "NEUTRAL"
            elif normalized_key == "3":
                # Option 3 is Exit on main menu
                print("\nStanding by.")
                break
            else:
                status_note = f"unknown command: '{user_input_string}'. enter 1, 2, 3, s, a, or x."
                status_kind = "BAD"

        elif current_view == "SELECT":
            if normalized_key.isdigit():
                picked_index = int(normalized_key) - 1
                if 0 <= picked_index < len(catalog_items):
                    new_selection = catalog_items[picked_index]
                    save_persistent_selection(new_selection)
                    status_note = f"PERSISTENTLY SELECTED '{new_selection}'"
                    status_kind = "POSITIVE"
                else:
                    status_note = f"invalid selection number: {normalized_key}. choose 1-{len(catalog_items)}."
                    status_kind = "BAD"
            else:
                status_note = f"unknown command: '{user_input_string}'. enter 1-{len(catalog_items)}, s, a, or b."
                status_kind = "BAD"

        elif current_view == "ACTION":
            action_map = {
                "1": "Inspect Attributes",
                "2": "Execute Process",
                "3": "Reset to Default",
                "4": "Export Configuration"
            }
            if normalized_key in action_map:
                action_name = action_map[normalized_key]
                if not current_selection or current_selection == "Null":
                    status_note = f"action failed: no item selected for '{action_name.lower()}'. press 's' first."
                    status_kind = "BAD"
                else:
                    status_note = f"ACTION '{action_name.upper()}' EXECUTED ON [{current_selection}] SUCCESSFULLY"
                    status_kind = "POSITIVE"
            else:
                status_note = f"unknown command: '{user_input_string}'. enter 1-4, s, a, or b."
                status_kind = "BAD"

        elif current_view == "INFO":
            if normalized_key == "1":
                status_note = f"State path: '{STATE_FILE_PATH}' (Size: {STATE_FILE_PATH.stat().st_size if STATE_FILE_PATH.exists() else 0} bytes)"
                status_kind = "NEUTRAL"
            elif normalized_key == "2":
                save_persistent_selection("Null")
                status_note = "PERSISTENT SELECTION CLEARED TO NULL"
                status_kind = "POSITIVE"
            else:
                status_note = f"unknown command: '{user_input_string}'. enter 1, 2, s, a, or b."
                status_kind = "BAD"

        elif current_view == "CONFIG":
            if normalized_key == "1":
                status_note = f"Viewport clamped at width: {get_terminal_display_width()} columns."
                status_kind = "NEUTRAL"
            elif normalized_key == "2":
                status_note = "DEFAULT PATHS VERIFIED AND LOCKED"
                status_kind = "POSITIVE"
            else:
                status_note = f"unknown command: '{user_input_string}'. enter 1, 2, s, a, or b."
                status_kind = "BAD"


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ("--render-only", "--preview"):
        sys.stdout.write(render_stateful_menu_frame("MAIN", "Null") + "\n")
    else:
        run_interactive_stateful_loop()
