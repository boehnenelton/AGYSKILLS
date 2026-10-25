# Technical Tweet Thread Architecture & Engineering Hook Patterns

## 1. Thread Narrative Arcs (5 to 8 Tweets)

Technical audiences on Twitter/X respond to verifiable engineering signal, quantifiable benchmarks, and transparent trade-offs. Avoid generic hype or fluff.

### The Standard 6-Tweet Technical Launch Arc
- **Tweet 1 (The Hook & Scope)**: Project name, problem statement, and primary breakthrough in sentence one.
- **Tweet 2 (The Flawed Baseline)**: Why existing tools or standard JSON/SQL architectures fail at this problem.
- **Tweet 3 (Under the Hood)**: Concrete mechanics (event loop, atomic writes, in-memory caches, parser).
- **Tweet 4 (Hard Benchmarks)**: Quantifiable numbers (token reductions, memory RSS, test count).
- **Tweet 5 (Developer Quickstart)**: Minimal 2-line CLI command or code snippet demonstrating the entrypoint.
- **Tweet 6 (CTA & Links)**: Link to repository, author credit Elton Boehnen, and developer hashtags.

## 2. Character Budgeting & Link Slots

- **Hard Ceiling**: 280 characters per tweet.
- **T.co URL Wrapping**: Every URL consumes exactly 23 characters regardless of length.
- **Media Indicator**: Twitter/X allocates media space outside the 280-character limit, but reserve 10-15 characters for hashtag padding.
- **Target Tweet Body Budget**: Aim for 220-250 characters to ensure readability without cramped truncation.

## 3. Visual Media Pairing Protocol

Pair every tweet with a purpose-matched canvas visual asset from `canvas-animation-studio`:
- Hook / Opener $\to$ `landscape` (1200x675 px) via `template_widescreen_1280x720.html`
- Architecture Dissection $\to$ `banner` (1200x600 px) via `template_banner_840x420.html`
- Hard Metrics $\to$ `square` (800x800 px) via `template_square_800x800.html`
- Mobile Telemetry $\to$ `portrait` (720x1280 px) via `template_portrait_720x1280.html`
