#!/usr/bin/env python3
"""
Name:           render_tabular_menu.py
Description:    Archetype 1: Tabular Telemetry Dashboard Terminal Menu
                Implements the 57-Column BEJSON Positional Telemetry Discipline
Version:        1.2.0
Author:         Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID:  a481c920-5c31-482a-9e11-dc78912e9120
"""

from __future__ import annotations
import atexit
import os
import sys
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

VERSION: str = "1.2.0"
MAIN_DIVIDER_57: str = "=" * 57
SUB_DIVIDER_57: str = "-" * 57

# Policy §8.1 Tri-Color Palette Constants
COLOR_TRUECOLOR_RED: str = "\033[38;2;222;38;38m"  # Policy §8.1 #DE2626 Truecolor
COLOR_ANSI_RED_FALLBACK: str = "\033[1;31m"         # ANSI Bold Red fallback
COLOR_BOLD_WHITE: str = "\033[1;37m"         # White, All Caps positive feedback
CONSOLE_CLEAR_SEQUENCE: str = "\033[2J\033[H"
CURSOR_SHOW_SEQUENCE: str = "\033[?25h"

NO_COLOR_SETTING: bool = os.getenv("NO_COLOR") is not None
COLORTERM_SETTING: str = os.getenv("COLORTERM", "").lower()
SUPPORTS_24BIT_COLOR: bool = "truecolor" in COLORTERM_SETTING or "24bit" in COLORTERM_SETTING


def resolve_accent_color() -> str:
    """Return #DE2626 Truecolor or ANSI Red fallback."""
    if NO_COLOR_SETTING or not sys.stdout.isatty():
        return ""
    explicit_mode = os.getenv("TUI_COLOR_MODE", "").lower()
    if explicit_mode == "ansi":
        return COLOR_ANSI_RED_FALLBACK
    if explicit_mode in ("truecolor", "24bit", "hex") or SUPPORTS_24BIT_COLOR:
        return COLOR_TRUECOLOR_RED
    return COLOR_ANSI_RED_FALLBACK


ACCENT_RED: str = resolve_accent_color()


def restore_terminal_cursor() -> None:
    """Restore cursor visibility and reset styles upon process exit."""
    try:
        sys.stdout.write(CURSOR_SHOW_SEQUENCE + COLOR_STYLE_RESET)
        sys.stdout.flush()
    except (BrokenPipeError, OSError):
        pass


atexit.register(restore_terminal_cursor)


def clear_console_screen() -> None:
    """Clear terminal screen and home cursor before every render unless suppressed."""
    if os.getenv("TUI_NO_CLEAR", "0") != "1":
        sys.stdout.write(CONSOLE_CLEAR_SEQUENCE)
        sys.stdout.flush()


@dataclass(frozen=True)
class PositionalTelemetryStrip:
    """Encapsulates a decoupled Field-Header strip and corresponding Value row."""
    field_descriptors_list: List[Tuple[str, int]]
    value_descriptors_list: List[Tuple[str, int]]

    def render(self) -> str:
        # Header labels rendered once in #DE2626 / Red
        header_tokens: List[str] = [
            f"{field_name:<{column_width}}" for field_name, column_width in self.field_descriptors_list
        ]
        header_line_string: str = f" {ACCENT_RED}{' '.join(header_tokens)}{COLOR_STYLE_RESET}"

        # Positional values aligned underneath in default white
        value_tokens: List[str] = [
            f"{str(value_data)[:column_width]:<{column_width}}" for value_data, column_width in self.value_descriptors_list
        ]
        value_line_string: str = f" {' '.join(value_tokens)}"
        return f"{header_line_string}\n{value_line_string}"


def format_three_column_action_row(
    first_option_tuple: Tuple[str, str],
    second_option_tuple: Tuple[str, str],
    third_option_tuple: Tuple[str, str]
) -> str:
    """Render a 3-column action row formatted strictly to 57 visible columns."""
    key_one, label_one = first_option_tuple
    key_two, label_two = second_option_tuple
    key_three, label_three = third_option_tuple

    return (
        f" [{ACCENT_RED}{key_one}{COLOR_STYLE_RESET}] {label_one:<15} "
        f"[{ACCENT_RED}{key_two}{COLOR_STYLE_RESET}] {label_two:<14} "
        f"[{ACCENT_RED}{key_three}{COLOR_STYLE_RESET}] {label_three:<13}"
    )


def format_clamped_alert_banner(alert_severity_level: str, alert_message_text: str) -> str:
    """
    Render a clamped single-line alert banner bounded within 57 columns adhering to:
    - POSITIVE: WHITE, ALL CAPS with [✓]
    - BAD: lowercase, red with [X]
    - NEUTRAL: normal standard rules with [*]
    """
    severity_token: str = alert_severity_level.upper()
    truncated_message_text: str = alert_message_text[:48]

    if severity_token in ("POSITIVE", "SUCCESS", "OK"):
        # POSITIVE STATUS: WHITE, ALL CAPS
        return f" {COLOR_BOLD_WHITE}[✓] {truncated_message_text.upper():<48}{COLOR_STYLE_RESET}"
    elif severity_token in ("BAD", "ERROR", "FAIL"):
        # BAD STATUS: lowercase red with [X]
        return f" {ACCENT_RED}[X] {truncated_message_text.lower():<48}{COLOR_STYLE_RESET}"
    else:
        # NEUTRAL: normal standard rules
        return f" {ACCENT_RED}[*]{COLOR_STYLE_RESET} {truncated_message_text:<48}"


def render_tabular_telemetry_frame(
    menu_title_string: str = "TELEMETRY DASHBOARD [104a]",
    subtitle_path_string: str = "~/.../data_partition.bejson",
    daemon_metrics_tuple: Tuple[str, ...] = ("13319", "8080", "ONLINE", "termux", "5s", "30s", "12", "FIX"),
    network_metrics_tuple: Tuple[str, ...] = ("UP", "10.183.119.245", "-58dBm", "Core-Mesh-Network"),
    status_alert_level: str = "INFO",
    status_alert_message: str = "System operational. All metrics within tolerance."
) -> str:
    """Assemble and return a complete 57-column tabular telemetry menu frame."""
    frame_lines_collection: List[str] = [
        MAIN_DIVIDER_57,
        f" {ACCENT_RED}{menu_title_string:<30}{COLOR_STYLE_RESET} {subtitle_path_string:>24}",
        SUB_DIVIDER_57,
    ]

    # Strip 1: Process / Daemon Telemetry
    strip_one: PositionalTelemetryStrip = PositionalTelemetryStrip(
        field_descriptors_list=[
            ("PID", 6), ("PORT", 5), ("STATE", 10), ("MODE", 7),
            ("SCAN", 5), ("GPS", 5), ("ROWS", 5), ("FIX", 3)
        ],
        value_descriptors_list=[
            (daemon_metrics_tuple[0], 6), (daemon_metrics_tuple[1], 5), (daemon_metrics_tuple[2], 10),
            (daemon_metrics_tuple[3], 7), (daemon_metrics_tuple[4], 5), (daemon_metrics_tuple[5], 5),
            (daemon_metrics_tuple[6], 5), (daemon_metrics_tuple[7], 3)
        ]
    )
    frame_lines_collection.append(strip_one.render())
    frame_lines_collection.append(SUB_DIVIDER_57)

    # Strip 2: Network / Link Telemetry
    strip_two: PositionalTelemetryStrip = PositionalTelemetryStrip(
        field_descriptors_list=[("LINK", 6), ("IP_ADDR", 16), ("RSSI", 7), ("SSID", 23)],
        value_descriptors_list=[
            (network_metrics_tuple[0], 6), (network_metrics_tuple[1], 16),
            (network_metrics_tuple[2], 7), (network_metrics_tuple[3], 23)
        ]
    )
    frame_lines_collection.append(strip_two.render())
    frame_lines_collection.append(SUB_DIVIDER_57)

    # Strip 3: Clamped Status Alert Banner
    frame_lines_collection.append(format_clamped_alert_banner(status_alert_level, status_alert_message))
    frame_lines_collection.append(MAIN_DIVIDER_57)

    # Strip 4: Decoupled 3-Column Action Grid
    frame_lines_collection.append(format_three_column_action_row(("1", "Scan & Pick AP"), ("2", "Add Manual"), ("3", "Delete Row")))
    frame_lines_collection.append(format_three_column_action_row(("4", "Connect Now"), ("5", "Disconnect"), ("6", "Priority Ord")))
    frame_lines_collection.append(format_three_column_action_row(("7", "Force Probe"), ("8", "Scan Interval"), ("9", "Export 104a")))
    frame_lines_collection.append(format_three_column_action_row(("M", "Mode Switch"), ("R", "Refresh Now"), ("Q", "Quit & Exit")))
    frame_lines_collection.append(MAIN_DIVIDER_57)
    frame_lines_collection.append(f"{ACCENT_RED}Action (Enter choice) >{COLOR_STYLE_RESET} ")

    return "\n".join(frame_lines_collection)


if __name__ == "__main__":
    clear_console_screen()
    sys.stdout.write(render_tabular_telemetry_frame() + "\n")
    sys.stdout.flush()
