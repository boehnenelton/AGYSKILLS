---
name: playwright-stealth-agent
description: >-
  Navigate protected web applications and anti-bot challenge surfaces on Android Termux
  using cloaked browser fingerprints and human behavioral physics. Injects Canvas 2D
  sub-pixel LSB noise, AudioContext frequency deviations, WebGL vendor masking, and
  removes navigator.webdriver. Synthesizes non-linear Cubic Bézier mouse trajectories
  with micro-jitter and humanized keyboard typing cadence with variable dwell times.
  Use when automating interactions on bot-protected pages, testing WAF challenge
  flows (Cloudflare/DataDome), or simulating realistic human navigation. Do NOT use for basic unblocked page scraping (use playwright-termux-automation) or
  canvas pixel error auditing (use playwright-debugger-auditor).
---

# Playwright Stealth Agent (Layer 3 Behavioral Stealth Engine)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 3`
- **Date Created**: `2026-10-23`
- **RELATIONAL_ID**: `1f5905e6-ae00-4b25-9b2e-018699ff25b4`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

## Summary

`playwright-stealth-agent` equips headless Chromium automation on Android Termux with anti-bot evasion techniques. It overrides `navigator.webdriver`, spoofs WebGL hardware vendor strings (`ARM Mali-G78`, `Qualcomm Adreno 740`), injects sub-pixel LSB noise into HTML5 canvas snapshots, and generates non-linear Cubic Bézier curves with randomized dwell times and micro-jitter for mouse cursor trajectories.

## When to Use

- Navigating web targets protected by bot detection or CAPTCHA challenges.
- Simulating organic human mouse trajectories using Cubic Bézier physics.
- Masking headless browser signatures (`navigator.webdriver`, fake permissions proxy).

## When NOT to Use

- Do NOT use for general headless browser lifecycle management without anti-bot constraints (use `playwright-termux-automation`).
- Do NOT use for canvas pixel buffer debugging or crash auditing (use `playwright-debugger-auditor`).

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
