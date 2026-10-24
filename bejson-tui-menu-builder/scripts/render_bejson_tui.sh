#!/data/data/com.termux/files/usr/bin/env bash
# -----------------------------------------------------------------------------
# Name:           render_bejson_tui.sh
# Description:    Reference 57-Column BEJSON Positional TUI Renderer
# Version:        100
# Date Created:   2026-10-23
# Author:         Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
# RELATIONAL_ID:  44ce9243-e48e-4e36-b288-36489e3bdf3f
# -----------------------------------------------------------------------------

DIV_MAIN="========================================================="
DIV_SUB="---------------------------------------------------------"

render_bejson_tui() {
    local pid="${1:-13319}"
    local port="${2:-8080}"
    local state="${3:-PAUSED(WEB)}"
    local mode="${4:-termux}"
    local scan="${5:-5s}"
    local gps="${6:-30s}"
    local rows="${7:-0}"
    local fix="${8:---}"
    local link="${9:-UP}"
    local ip="${10:-10.183.119.245}"
    local rssi="${11:--58dBm}"
    local ssid="${12:-Lowes-Guest-WiFi}"

    printf "%s\n" "$DIV_MAIN"
    printf " %-27s %27s\n" "WI-FI + GPS DAEMON [104a]" "~/.../wifi_allowlist.bejson"
    printf "%s\n" "$DIV_SUB"

    # Strip 1: Daemon Telemetry (Fields -> Values)
    printf " %-6s %-5s %-12s %-7s %-5s %-5s %-5s %-3s\n" \
        "PID" "PORT" "STATE" "MODE" "SCAN" "GPS" "ROWS" "FIX"
    printf " %-6s %-5s %-12.12s %-7.7s %-5s %-5s %-5s %-3s\n" \
        "$pid" "$port" "$state" "$mode" "$scan" "$gps" "$rows" "$fix"
    printf "%s\n" "$DIV_SUB"

    # Strip 2: Active Network Telemetry (Fields -> Values)
    printf " %-6s %-16s %-7s %-23s\n" "LINK" "IP_ADDR" "RSSI" "SSID"
    printf " %-6s %-16.16s %-7s %-23.23s\n" "$link" "$ip" "$rssi" "$ssid"
    printf "%s\n" "$DIV_SUB"

    # Strip 3: Allowlist Records (Fields -> Positional Values)
    printf " %-3s %-4s %-5s %-9s %-18s %-11s\n" \
        "ID" "PRI" "AUTO" "SECURITY" "BSSID" "SSID"
    if [[ "$rows" -eq 0 ]]; then
        printf " %s\n" "[0 rows - press [W] to scan & pick or [A] to add SSID]"
    fi

    printf "%s\n" "$DIV_MAIN"
    # Strip 4: 3-Column Action Grid (19 + 18 + 18 = 55 chars + leading space)
    printf " %-19s %-18s %-18s\n" "[W] Scan & Pick AP" "[A] Add Manual"   "[D] Delete Row"
    printf " %-19s %-18s %-18s\n" "[C] Connect Now"    "[X] Disconnect"   "[R] Priority Ord"
    printf " %-19s %-18s %-18s\n" "[F] Force GPS+Scan" "[S] Scan Timer"   "[G] GPS Interval"
    printf " %-19s %-18s %-18s\n" "[T] Auto-Connect"   "[P] PauseOnWeb"   "[M] Mode Cycle"
    printf " %-19s %-18s %-18s\n" "[B] Portal Probe"   "[E] Export 104a"  "[Q] Quit & Kill"
    printf "%s\n" "$DIV_MAIN"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    render_bejson_tui "$@"
fi
