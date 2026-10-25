#!/data/data/com.termux/files/usr/bin/env bash
# -----------------------------------------------------------------------------
# Name:           render_bejson_tui.sh
# Description:    Hardened 57-Column BEJSON Positional TUI Renderer & Event Loop
# Version:        110
# Date Created:   2026-10-23
# Date Modified:  2026-10-25
# Author:         Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
# RELATIONAL_ID:  53907437-ed56-437b-ad13-9100ac636d9b
# -----------------------------------------------------------------------------

VERSION="110"
tui_divider_main_line="========================================================="
tui_divider_sub_line="---------------------------------------------------------"

# Policy §8.1 Tri-Color Palette & Escape Sequences
tui_color_accent_red_hex=$'\033[38;2;222;38;38m'
tui_color_accent_red_ansi=$'\033[1;31m'
tui_color_style_reset=$'\033[0m'
tui_color_style_bold=$'\033[1m'
tui_color_style_dim=$'\033[2m'
tui_console_clear_seq=$'\033[2J\033[H'
tui_cursor_hide_seq=$'\033[?25l'
tui_cursor_show_seq=$'\033[?25h'

# Color Auto-Negotiation (Truecolor > ANSI Fallback)
if [[ -n "${TUI_COLOR_MODE:-}" ]]; then
    if [[ "$TUI_COLOR_MODE" == "ansi" ]]; then
        tui_color_accent_red="$tui_color_accent_red_ansi"
    else
        tui_color_accent_red="$tui_color_accent_red_hex"
    fi
elif [[ "${COLORTERM:-}" =~ ^(truecolor|24bit)$ ]]; then
    tui_color_accent_red="$tui_color_accent_red_hex"
else
    tui_color_accent_red="$tui_color_accent_red_ansi"
fi

# Cursor and Terminal Lifecycle Management
tui_cleanup_done=0
tui_cleanup() {
    if [[ "$tui_cleanup_done" -eq 0 ]]; then
        tui_cleanup_done=1
        printf "%b" "$tui_cursor_show_seq"
        if [[ -t 0 ]]; then
            stty echo 2>/dev/null || true
        fi
    fi
}
trap 'tui_cleanup' EXIT INT TERM

clear_tui_console() {
    if [[ "${TUI_NO_CLEAR:-0}" != "1" ]]; then
        printf "%b" "$tui_console_clear_seq"
    fi
}

# 57-Column Clamped Alert / Status Banner
render_bejson_tui_alert_strip() {
    local alert_level="${1:-INFO}"
    local alert_message="${2:-Ready}"
    local alert_tag="[*]"
    
    case "${alert_level^^}" in
        SUCCESS|OK) alert_tag="[✓]" ;;
        WARN|WARNING) alert_tag="[!]" ;;
        ERROR|FAIL) alert_tag="[✗]" ;;
        INFO) alert_tag="[*]" ;;
    esac

    # Truncate message to 48 characters to guarantee <= 57 total visible characters
    local truncated_message="${alert_message:0:48}"
    printf " %b%s%b %-50s\n" \
        "$tui_color_accent_red" "$alert_tag" "$tui_color_style_reset" "$truncated_message"
}

# 3-Column Action Grid Renderer (15 / 14 / 13 chars = exactly 57 columns)
render_bejson_tui_option_row() {
    local row_col1_option_key="$1"
    local row_col1_option_text="$2"
    local row_col2_option_key="$3"
    local row_col2_option_text="$4"
    local row_col3_option_key="$5"
    local row_col3_option_text="$6"

    printf " [%b%s%b] %-15s [%b%s%b] %-14s [%b%s%b] %-13s\n" \
        "$tui_color_accent_red" "$row_col1_option_key" "$tui_color_style_reset" "$row_col1_option_text" \
        "$tui_color_accent_red" "$row_col2_option_key" "$tui_color_style_reset" "$row_col2_option_text" \
        "$tui_color_accent_red" "$row_col3_option_key" "$tui_color_style_reset" "$row_col3_option_text"
}

# 57-Column Pagination Strip
render_bejson_tui_pagination_strip() {
    local current_page="${1:-1}"
    local total_pages="${2:-1}"
    local total_records="${3:-0}"

    printf "%b %-12s %-12s %-16s %-10s%b\n" \
        "$tui_color_accent_red" "PAGE" "TOTAL_PAGES" "TOTAL_RECORDS" "WINDOW" "$tui_color_style_reset"
    printf " %-12s %-12s %-16s %-10s\n" \
        "$current_page" "$total_pages" "$total_records" "5-per-page"
}

# Full 57-Column Positional Frame Renderer
render_bejson_tui() {
    local daemon_telemetry_pid="${1:-13319}"
    local daemon_telemetry_port="${2:-8080}"
    local daemon_telemetry_state="${3:-PAUSED(WEB)}"
    local daemon_telemetry_mode="${4:-termux}"
    local daemon_telemetry_scan="${5:-5s}"
    local daemon_telemetry_gps="${6:-30s}"
    local daemon_telemetry_rows="${7:-0}"
    local daemon_telemetry_fix="${8:---}"
    local network_telemetry_link="${9:-UP}"
    local network_telemetry_ip="${10:-10.183.119.245}"
    local network_telemetry_rssi="${11:--58dBm}"
    local network_telemetry_ssid="${12:-Lowes-Guest-WiFi}"
    local status_banner_msg="${13:-System operational. Waiting for action.}"
    local status_banner_lvl="${14:-INFO}"

    clear_tui_console
    printf "%s\n" "$tui_divider_main_line"
    # Menu Header in #DE2626 / Red
    printf " %b%-30s%b %24s\n" \
        "$tui_color_accent_red" "WI-FI + GPS DAEMON [104a]" "$tui_color_style_reset" \
        "~/.../wifi_allowlist.bejson"
    printf "%s\n" "$tui_divider_sub_line"

    # Strip 1: Daemon Telemetry (Labels in #DE2626 -> Values in default White)
    printf "%b %-6s %-5s %-12s %-7s %-5s %-5s %-5s %-3s%b\n" \
        "$tui_color_accent_red" \
        "PID" "PORT" "STATE" "MODE" "SCAN" "GPS" "ROWS" "FIX" \
        "$tui_color_style_reset"
    printf " %-6s %-5s %-12.12s %-7.7s %-5s %-5s %-5s %-3s\n" \
        "$daemon_telemetry_pid" "$daemon_telemetry_port" "$daemon_telemetry_state" \
        "$daemon_telemetry_mode" "$daemon_telemetry_scan" "$daemon_telemetry_gps" \
        "$daemon_telemetry_rows" "$daemon_telemetry_fix"
    printf "%s\n" "$tui_divider_sub_line"

    # Strip 2: Active Network Telemetry (Labels in #DE2626 -> Values in default White)
    printf "%b %-6s %-16s %-7s %-23s%b\n" \
        "$tui_color_accent_red" "LINK" "IP_ADDR" "RSSI" "SSID" "$tui_color_style_reset"
    printf " %-6s %-16.16s %-7s %-23.23s\n" \
        "$network_telemetry_link" "$network_telemetry_ip" "$network_telemetry_rssi" "$network_telemetry_ssid"
    printf "%s\n" "$tui_divider_sub_line"

    # Strip 3: Allowlist Table / Empty State Indicator
    printf "%b %-3s %-4s %-5s %-9s %-18s %-11s%b\n" \
        "$tui_color_accent_red" "ID" "PRI" "AUTO" "SECURITY" "BSSID" "SSID" "$tui_color_style_reset"
    if [[ "$daemon_telemetry_rows" -eq 0 ]]; then
        printf " [0 rows - press [%b1%b] to scan & pick or [%b2%b] to add SSID]\n" \
            "$tui_color_accent_red" "$tui_color_style_reset" \
            "$tui_color_accent_red" "$tui_color_style_reset"
    else
        printf " %-3s %-4s %-5s %-9s %-18s %-11.11s\n" "01" "1" "Y" "WPA2" "a4:2b:8c:11:09:f0" "Home-5G"
        printf " %-3s %-4s %-5s %-9s %-18s %-11.11s\n" "02" "2" "Y" "OPEN" "*" "Lowes-Guest"
    fi

    # Strip 4: Clamped Status Alert Banner
    printf "%s\n" "$tui_divider_sub_line"
    render_bejson_tui_alert_strip "$status_banner_lvl" "$status_banner_msg"

    # Strip 5: 3-Column Action Grid (Hotkeys/numbers in #DE2626)
    printf "%s\n" "$tui_divider_main_line"
    render_bejson_tui_option_row "1" "Scan & Pick AP" "2" "Add Manual"   "3" "Delete Row"
    render_bejson_tui_option_row "4" "Connect Now"    "5" "Disconnect"   "6" "Priority Ord"
    render_bejson_tui_option_row "7" "Force GPS+Scan" "8" "Scan Timer"   "9" "GPS Interval"
    render_bejson_tui_option_row "T" "Auto-Connect"   "P" "PauseOnWeb"   "M" "Mode Cycle"
    render_bejson_tui_option_row "B" "Portal Probe"   "E" "Export 104a"  "Q" "Quit & Kill"
    printf "%s\n" "$tui_divider_main_line"
    printf "%bAction (5s refresh) >%b " "$tui_color_accent_red" "$tui_color_style_reset"
}

# Hardened Interactive Event Loop Mode
run_bejson_tui_event_loop() {
    local refresh_interval="${1:-5}"
    local active_status="TUI daemon initialized in portrait mode."
    local active_level="INFO"
    local simulated_mode="termux"
    local simulated_state="PAUSED(WEB)"
    local simulated_rows=2

    while true; do
        render_bejson_tui \
            "$$" "8080" "$simulated_state" "$simulated_mode" "5s" "30s" "$simulated_rows" "--" \
            "UP" "10.183.119.245" "-58dBm" "Lowes-Guest-WiFi" "$active_status" "$active_level"

        # Read 1 character with timeout
        local user_key=""
        if read -r -s -t "$refresh_interval" -n 1 user_key; then
            case "${user_key^^}" in
                1)
                    active_status="Scanning for nearby Wi-Fi APs..."
                    active_level="INFO"
                    ;;
                4)
                    active_status="Forcing immediate connect sequence..."
                    active_level="SUCCESS"
                    simulated_state="CONNECTED"
                    ;;
                5)
                    active_status="Disconnecting active link..."
                    active_level="WARN"
                    simulated_state="DISCONNECTED"
                    ;;
                7)
                    active_status="Capturing raw GPS NMEA + Wi-Fi snapshot..."
                    active_level="SUCCESS"
                    ;;
                B)
                    active_status="Probing captive portal HTTP 204: REACHABLE."
                    active_level="SUCCESS"
                    ;;
                M)
                    if [[ "$simulated_mode" == "termux" ]]; then
                        simulated_mode="wpa_cli"
                    else
                        simulated_mode="termux"
                    fi
                    active_status="Connect mode switched to $simulated_mode."
                    active_level="INFO"
                    ;;
                Q)
                    printf "\n%bQuitting TUI daemon session.%b\n" "$tui_color_accent_red" "$tui_color_style_reset"
                    break
                    ;;
                *)
                    active_status="Key [$user_key] registered."
                    active_level="INFO"
                    ;;
            esac
        else
            # Timed out: regular telemetry tick
            active_status="Telemetry refresh tick ($(date +%H:%M:%S))."
            active_level="INFO"
        fi
    done
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    if [[ "${1:-}" == "--loop" || "${1:-}" == "-l" ]]; then
        run_bejson_tui_event_loop "${2:-5}"
    else
        render_bejson_tui "$@"
        echo ""
    fi
fi
