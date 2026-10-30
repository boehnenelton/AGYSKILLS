---
name: playwright-termux-automation
description: >-
  Start, stop, navigate, scrape, screenshot, and manage native Chromium and Playwright browser automation workflows directly on Android Termux (ARM64) without PRoot or root privileges. Use when executing headless or headful browser sessions in Termux, capturing page screenshots, rendering dynamic SPAs, evaluating in-browser JavaScript, handling HTTP authentication, and managing browser process lifecycles. Do NOT use for standard non-browser HTTP requests (use curl, requests, or httpx) or standard Termux URL opening in the external Android Chrome app (use termux-open).
---

# Skill: `playwright-termux-automation`

- **Target Architecture**: Android Termux (aarch64 / ARM 64-bit, Android Bionic libc)
- **Primary Runtime**: Python 3.10+ & Node.js 26+
- **Binding Package**: `termux-playwright` & native `chromium`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
- **RELATIONAL_ID**: `fcde8873-38bd-4c0f-81f7-199e42f62687`

---

## 1. When to Use & When NOT to Use

### Use This Skill When:
- Running headless browser automation natively on Android/Termux without PRoot Ubuntu or root.
- Taking automated screenshots or PDF renders of local servers (e.g. Flask, Express, Django) or live websites.
- Scraping JavaScript-heavy Single Page Applications (SPAs) where raw HTML parsers (`BeautifulSoup`, `requests`) fail.
- Interacting with web forms, clicking buttons, submitting credentials, or testing web application interfaces.
- Starting, stopping, and cleanly reaping Chromium browser processes on Termux.

### Do NOT Use This Skill When:
- Performing simple static HTTP GET/POST calls that return JSON or plain HTML (use `requests`, `httpx`, or `curl`).
- Launching external Android browser apps via Android intents (use `termux-open-url`).
- Creating PRoot Ubuntu containers or running x86 emulators (native Chromium is already installed).

---

## 2. Starting Browser Sessions

### A. Asynchronous Pattern (Standard / Preferred)
```python
import asyncio
from termux_playwright import async_playwright_termux, launch

async def run_automation():
    # 1. async_playwright_termux sets up Bionic node paths and process ledgers
    async with async_playwright_termux() as playwright_instance:
        # 2. launch() applies --no-sandbox, --disable-gpu, and --js-flags=--jitless
        browser = await launch(playwright_instance, headless=True)
        page = await browser.new_page()
        
        # 3. Navigate with mobile-safe timeouts
        await page.goto("https://example.com", timeout=30000, wait_until="domcontentloaded")
        page_title = await page.title()
        print(f"Page Title: {page_title}")
        
        # 4. Clean close
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_automation())
```

### B. Synchronous Pattern
```python
from termux_playwright import sync_playwright_termux, launch_sync

def run_sync_automation():
    with sync_playwright_termux() as playwright_instance:
        browser = launch_sync(playwright_instance, headless=True)
        page = browser.new_page()
        page.goto("https://example.com", timeout=30000)
        print(page.title())
        browser.close()

if __name__ == "__main__":
    run_sync_automation()
```

---

## 3. Stopping & Cleaning Up Browser Processes

### Safe Teardown Protocol
1. **Always close page and browser objects**:
   ```python
   await page.close()
   await browser.close()
   ```
2. **Context recycling for loops**:
   In continuous crawlers, destroy and recreate contexts every 50-100 pages to purge the Node.js RPC buffer and stay well below the 32-process Android Phantom Process Killer limit:
   ```python
   context = await browser.new_context()
   # ... do work ...
   await context.close()
   ```

### Emergency Process Killer (Shell)
If a script crashes or leaves zombie Chromium processes in the background:
```bash
bash ~/.gemini/config/skills/playwright-termux-automation/scripts/kill_browser.sh
```
Or run the Python reaper directly:
```bash
python3 -c "from termux_playwright.reaper import ProcessReaper; ProcessReaper.reap_untracked_ledger_orphans()"
```

---

## 4. General Automation Patterns

### A. Taking Page Screenshots
```python
await page.set_viewport_size({"width": 1280, "height": 800})
# Viewport only
await page.screenshot(path="screenshot.png")
# Full scrolling page
await page.screenshot(path="full_page.png", full_page=True)
```

### B. Authenticated Routes (HTTP Basic Auth)
```python
context = await browser.new_context(
    http_credentials={"username": "admin", "password": "changeme"},
    viewport={"width": 1280, "height": 800}
)
page = await context.new_page()
await page.goto("http://127.0.0.1:5001/")
```

### C. Waiting for Dynamic DOM Elements
```python
# Wait for element to attach
await page.wait_for_selector("#dynamic-content", timeout=15000)
content_text = await page.inner_text("#dynamic-content")

# Evaluate arbitrary client-side JS
user_agent = await page.evaluate("() => navigator.userAgent")
```

### D. Anti-Sleep WakeLock for Long Scraping Runs
```python
from termux_playwright import TermuxWakeLock

with TermuxWakeLock(fail_silently=True):
    # Device CPU remains awake while screen is off
    ...
```

---

## 5. Built-in Skill Scripts

The skill provides ready-to-execute CLI utilities in `scripts/`:

1. **`scripts/capture_page.py`**: Quick one-liner to screenshot or dump HTML from any URL:
   ```bash
   python3 ~/.gemini/config/skills/playwright-termux-automation/scripts/capture_page.py \
       --url "http://127.0.0.1:5001/" \
       --output "dashboard.png" \
       --dump-html "dashboard.html" \
       --user "admin" --password "changeme"
   ```

2. **`scripts/kill_browser.sh`**: Safely purges stray Chromium and Node.js child processes and wipes ephemeral browser profile directories.
   ```bash
   bash ~/.gemini/config/skills/playwright-termux-automation/scripts/kill_browser.sh
   ```

---

## 6. Critical Android Invariants

- ❌ **NEVER add `--single-process`**: Modern Chromium (v130+) throws crashpad `tag not found` and aborts immediately if single-process is requested on Android.
- ❌ **NEVER run `playwright install`**: This installs incompatible glibc x86_64 binaries.
- ⚡ **Always keep `--js-flags=--jitless`**: Required on Android 10+ (SDK >= 29) to adhere to non-privileged W^X memory restrictions.
