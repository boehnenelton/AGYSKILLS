# Termux Playwright Technical Reference

## Execution Environment Matrix
- **Binary Architecture**: aarch64 (ARM 64-bit)
- **C Library**: Android Bionic libc
- **Chromium Path**: `/data/data/com.termux/files/usr/lib/chromium/chrome`
- **Node.js Path**: `/data/data/com.termux/files/usr/bin/node`

## Critical Runtime Directives
1. **Never pass `--single-process` on Chromium 130+**: Chromium 130+ (including 133 and 155) fails instantly with crashpad `tag not found` if single-process is requested.
2. **Always include `--js-flags=--jitless`**: Android 10+ enforces W^X memory execution; V8 JIT code generation will cause SIGSEGV if JIT is enabled on non-privileged apps.
3. **Always set `PLAYWRIGHT_NODEJS_PATH`**: Direct calls to `playwright.async_api` must point to Termux's node binary (`/data/data/com.termux/files/usr/bin/node`).
4. **Android Phantom Process Killer**: Limit concurrent background child processes to avoid reaching Android's 32-process threshold. Call `scripts/kill_browser.sh` after long tasks.
