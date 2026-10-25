#!/usr/bin/env python3
"""
Name:           render_bejson_tui.py
Description:    Hardened 57-Column BEJSON Positional TUI Engine (Python 3.10+)
Version:        110
Date Created:   2026-10-25
Author:         Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID:  94a92ec9-0d88-4be3-8dbe-e4c7d1233e39
"""

from __future__ import annotations
import os
import sys
import atexit
import shutil
from dataclasses import dataclass
from typing import List, Tuple

VERSION: str = "110"
MAIN_DIVIDER: str = "=" * 57
SUB_DIVIDER: str = "-" * 57

# Policy §8.1 Tri-Color Palette Constants
COLOR_HEX_RED: str = "\033[38;2;222;38;38m"
COLOR_ANSI_RED: str = "\033[1;31m"
COLOR_RESET: str = "\033[0m"
CONSOLE_CLEAR: str = "\033[2J\033[H"
CURSOR_HIDE: str = "\033[?25l"
CURSOR_SHOW: str = "\033[?25h"


def resolve_accent_color() -> str:
    """Auto-negotiate between Truecolor RGB (222, 38, 38) and 16-color ANSI Red fallback."""
    explicit_mode = os.getenv("TUI_COLOR_MODE", "").lower()
    if explicit_mode == "ansi":
        return COLOR_ANSI_RED
    elif explicit_mode in ("truecolor", "24bit", "hex"):
        return COLOR_HEX_RED
    colorterm = os.getenv("COLORTERM", "").lower()
    if colorterm in ("truecolor", "24bit"):
        return COLOR_HEX_RED
    return COLOR_ANSI_RED


ACCENT_RED: str = resolve_accent_color()


def cleanup_terminal() -> None:
    """Ensure cursor visibility and reset styles on exit."""
    try:
        sys.stdout.write(CURSOR_SHOW + COLOR_RESET)
        sys.stdout.flush()
    except (BrokenPipeError, OSError):
        pass


atexit.register(cleanup_terminal)


def clear_console() -> None:
    """Clear terminal screen and home cursor unless suppressed."""
    if os.getenv("TUI_NO_CLEAR", "0") != "1":
        sys.stdout.write(CONSOLE_CLEAR)
        sys.stdout.flush()


@dataclass(frozen=True)
class TelemetryStrip:
    fields: List[Tuple[str, int]]  # (Name, Width)
    values: List[Tuple[str, int]]  # (Value, Width)

    def render(self) -> str:
        # Header labels rendered in #DE2626
        field_tokens = []
        for name, width in self.fields:
            field_tokens.append(f"{name:<{width}}")
        header_line = f" {ACCENT_RED}{' '.join(field_tokens)}{COLOR_RESET}"

        # Positional values rendered in default white
        val_tokens = []
        for val, width in self.values:
            val_tokens.append(f"{val[:width]:<{width}}")
        val_line = f" {' '.join(val_tokens)}"
        return f"{header_line}\n{val_line}"


def render_action_row(
    col1: Tuple[str, str], col2: Tuple[str, str], col3: Tuple[str, str]
) -> str:
    """Render a 3-column action row formatted to exactly 57 columns."""
    k1, v1 = col1
    k2, v2 = col2
    k3, v3 = col3
    return (
        f" [{ACCENT_RED}{k1}{COLOR_RESET}] {v1:<15} "
        f"[{ACCENT_RED}{k2}{COLOR_RESET}] {v2:<14} "
        f"[{ACCENT_RED}{k3}{COLOR_RESET}] {v3:<13}"
    )


def render_alert_strip(level: str, message: str) -> str:
    """Render a clamped single-line alert banner within 57 columns."""
    tags = {
        "SUCCESS": "[✓]",
        "OK": "[✓]",
        "WARN": "[!]",
        "WARNING": "[!]",
        "ERROR": "[✗]",
        "INFO": "[*]",
    }
    tag = tags.get(level.upper(), "[*]")
    truncated = message[:48]
    return f" {ACCENT_RED}{tag}{COLOR_RESET} {truncated:<50}"


def render_bejson_tui_frame(
    title: str = "WI-FI + GPS DAEMON [104a]",
    subtitle: str = "~/.../wifi_allowlist.bejson",
    daemon_stats: Tuple[str, ...] = ("13319", "8080", "PAUSED(WEB)", "termux", "5s", "30s", "0", "--"),
    network_stats: Tuple[str, ...] = ("UP", "10.183.119.245", "-58dBm", "Lowes-Guest-WiFi"),
    alert_level: str = "INFO",
    alert_msg: str = "System operational. Waiting for action.",
) -> str:
    """Assemble and return a complete 57-column BEJSON TUI frame string."""
    lines: List[str] = [
        MAIN_DIVIDER,
        f" {ACCENT_RED}{title:<30}{COLOR_RESET} {subtitle:>24}",
        SUB_DIVIDER,
    ]

    # Strip 1: Daemon Telemetry
    strip1 = TelemetryStrip(
        fields=[
            ("PID", 6),
            ("PORT", 5),
            ("STATE", 12),
            ("MODE", 7),
            ("SCAN", 5),
            ("GPS", 5),
            ("ROWS", 5),
            ("FIX", 3),
        ],
        values=[
            (daemon_stats[0], 6),
            (daemon_stats[1], 5),
            (daemon_stats[2], 12),
            (daemon_stats[3], 7),
            (daemon_stats[4], 5),
            (daemon_stats[5], 5),
            (daemon_stats[6], 5),
            (daemon_stats[7], 3),
        ],
    )
    lines.append(strip1.render())
    lines.append(SUB_DIVIDER)

    # Strip 2: Network Telemetry
    strip2 = TelemetryStrip(
        fields=[("LINK", 6), ("IP_ADDR", 16), ("RSSI", 7), ("SSID", 23)],
        values=[
            (network_stats[0], 6),
            (network_stats[1], 16),
            (network_stats[2], 7),
            (network_stats[3], 23),
        ],
    )
    lines.append(strip2.render())
    lines.append(SUB_DIVIDER)

    # Strip 3: Allowlist Table
    table_header = f" {ACCENT_RED}{'ID':<3} {'PRI':<4} {'AUTO':<5} {'SECURITY':<9} {'BSSID':<18} {'SSID':<11}{COLOR_RESET}"
    lines.append(table_header)
    lines.append(
        f" [0 rows - press [{ACCENT_RED}1{COLOR_RESET}] to scan & pick or [{ACCENT_RED}2{COLOR_RESET}] to add SSID]"
    )
    lines.append(SUB_DIVIDER)

    # Strip 4: Clamped Alert Banner
    lines.append(render_alert_strip(alert_level, alert_msg))
    lines.append(MAIN_DIVIDER)

    # Strip 5: 3-Column Action Grid
    lines.append(render_action_row(("1", "Scan & Pick AP"), ("2", "Add Manual"), ("3", "Delete Row")))
    lines.append(render_action_row(("4", "Connect Now"), ("5", "Disconnect"), ("6", "Priority Ord")))
    lines.append(render_action_row(("7", "Force GPS+Scan"), ("8", "Scan Timer"), ("9", "GPS Interval")))
    lines.append(render_action_row(("T", "Auto-Connect"), ("P", "PauseOnWeb"), ("M", "Mode Cycle")))
    lines.append(render_action_row(("B", "Portal Probe"), ("E", "Export 104a"), ("Q", "Quit & Kill")))
    lines.append(MAIN_DIVIDER)
    lines.append(f"{ACCENT_RED}Action (5s refresh) >{COLOR_RESET} ")

    return "\n".join(lines)


if __name__ == "__main__":
    clear_console()
    sys.stdout.write(render_bejson_tui_frame() + "\n")
    sys.stdout.flush()
