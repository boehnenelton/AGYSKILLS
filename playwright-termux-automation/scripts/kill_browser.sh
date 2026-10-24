#!/data/data/com.termux/files/usr/bin/bash
# ==============================================================================
# Script Name: kill_browser.sh
# Description: Safely reap and terminate lingering Chromium, Node.js driver, and
#              orphan browser processes in Termux to free RAM and prevent
#              triggering the Android Phantom Process Killer.
# Version: 1.0.0
# Date Created: 2026-10-21
# Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
# RELATIONAL_ID: 5c72a8bf-16f4-44cc-9e22-18275540f232
# ==============================================================================

set -euo pipefail

echo "[*] [Termux-Playwright] Checking for lingering Chromium & Playwright processes..."

# 1. First trigger the internal Python reaper ledger if termux_playwright is installed
if python3 -c "import termux_playwright.reaper" 2>/dev/null; then
    python3 -c "from termux_playwright.reaper import ProcessReaper; ProcessReaper.reap_untracked_ledger_orphans()" 2>/dev/null || true
fi

# 2. Terminate any stray Chromium browser instances
CHROME_PIDS=$(pgrep -f "chromium|headless_shell|chrome" || true)
if [ -n "$CHROME_PIDS" ]; then
    echo "[!] Found active Chromium process IDs: $CHROME_PIDS"
    pkill -15 -f "chromium" 2>/dev/null || true
    pkill -15 -f "headless_shell" 2>/dev/null || true
    sleep 1
    # Force kill any remaining stubborn processes
    pkill -9 -f "chromium" 2>/dev/null || true
    pkill -9 -f "headless_shell" 2>/dev/null || true
    echo "[✓] Chromium processes terminated."
else
    echo "[✓] No stray Chromium processes detected."
fi

# 3. Clean up ephemeral temporary directories
find /data/data/com.termux/files/usr/tmp -maxdepth 1 -name "playwright_chromiumdev_profile*" -exec rm -rf {} + 2>/dev/null || true
find /data/data/com.termux/files/usr/tmp -maxdepth 1 -name "tp_solo_*" -exec rm -rf {} + 2>/dev/null || true

echo "[✓] Ephemeral browser profiles purged."
echo "[+] All browser instances cleanly stopped."
