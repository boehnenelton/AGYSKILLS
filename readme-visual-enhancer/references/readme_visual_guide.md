# README Authoring, Visual Enhancement & 420p Scaling Specification

**Author**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton  
**Relational ID**: `ff0c7a93-b206-4a67-a7a8-67cd8a5732b7`  
**Version**: 1.2.0  
**Effective Date**: October 21, 2026  

---

## 1. Absolute Negative Constraints for READMEs

Every README authored or enhanced must strictly adhere to three absolute prohibitions:

1. **Never Include Hardcoded Paths**:
   - Do **NOT** embed absolute machine paths (e.g., `/storage/emulated/0/...`, `/data/data/com.termux/...`, `/home/user/...`, `C:\...`).
   - **Single Exemption**: Providing explicit setup guidance to the user showing which environment variables or paths they need to configure (e.g., `export PROJECT_DATA="/path/to/your/storage"`).
   - In all runtime examples, repository links, image references, and documentation text, use clean relative paths (`./images/screenshot.png`, `lib/module.py`) or portable environment variable references (`$PROJECT_ROOT`, `$APP_DIR`).

2. **Never Mention Internal Policies, Rules, or Agent Instructions**:
   - Do **NOT** cite, quote, or reference governance documents, system policies, user instructions, or agent prompts (e.g., do not write "per Policy §8.1", "per user rules", "GEMINI.md", "mandatory compliance", or "system prompt constraints").
   - Documentation must present pure, objective technical facts and project specifications without referencing the governing framework.

3. **Never Vocalize or Indicate AI Authorship**:
   - Do **NOT** vocalize, state, imply, or hint that the document was authored by AI, an LLM, an assistant, ChatGPT, Claude, or Gemini.
   - Maintain a grounded, senior developer perspective. Write authoritatively and professionally as the maintainer of the project.

---

## 2. Mandatory README Authoring Lifecycle

### Phase 1: Deep Target Codebase Study (Pre-Writing)
Before writing a single line of documentation:
1. Examine the root directory, configuration files, and manifest trackers.
2. Read main entry points (`main.py`, `app.py`, `run.sh`), CLI argument parsers, and public APIs.
3. Trace data flows, persistence engines, database schemas, and external dependencies.
4. Understand real workflows from the perspective of an end user and a contributing developer.

### Phase 2: Two-Phase Document Architecture
Structure the README with clear semantic sections and an explicit Table of Contents:

| Document Half | Focus Areas | Mandatory Contents |
|---|---|---|
| **First Half** | **Setup, Usage & Features** | • Project Title & High-Level Summary<br>• Table of Contents (TOC) with anchor links<br>• Prerequisites & Environment Setup (highlighting paths to customize)<br>• Quick Start & Installation<br>• Core Features & Workflows<br>• Visual Interface Tour (Playwright 420p captures) |
| **Second Half** | **Technical Details & Architecture** | • System & Architectural Diagram<br>• Directory Structure & Component Inventory<br>• Data Models, Schemas & Storage Formats<br>• CLI Reference & Flag Matrix<br>• Error Handling & Exit Codes<br>• Development, Testing & Verification |

### Phase 3: Post-Writing Hostile Audit
After completing the draft, rigorously challenge the work with a hostile mindset:
- **Completeness**: "Is there anything more to add? Are all CLI flags documented? Are error cases handled? Is installation completely reproducible?"
- **Cleanliness**: Run `scripts/readme_auditor.py` to ensure zero hardcoded paths, zero policy leaks, zero AI vocalizations, and 100% TOC coverage.

---

## 3. The 420p Aspect-Ratio Scaling Law

Raw browser screenshots (captured at 1280x800 or 1920x1080) consume 100 KB to 500 KB each. Embedding multiple unscaled figures balloons repository clone weight and introduces sluggish rendering on mobile environments.

Downscaling images so that the **maximum of the highest dimension is 420px** delivers the ideal equilibrium:
- **Aspect Ratio Preservation**: Maintains exact UI proportions without stretching, warping, or cropping.
- **Extreme Lightweight Footprint**: Typical file sizes drop to 12 KB – 28 KB (an 85%–92% reduction).
- **Legibility**: Text, buttons, navigation menus, and data tables remain crisp.

### Aspect Ratio Scaling Formula
Given source dimensions $(W_{source}, H_{source})$ and maximum highest dimension limit $D_{max} = 420$:

$$D_{highest} = \max(W_{source}, H_{source})$$

$$\text{Scaling Factor} = \frac{D_{max}}{D_{highest}} = \frac{420}{\max(W_{source}, H_{source})}$$

$$W_{target} = \text{round}(W_{source} \times \text{Scaling Factor})$$

$$H_{target} = \text{round}(H_{source} \times \text{Scaling Factor})$$

#### Mathematical Example (1280x800 Viewport):
$$\text{Scaling Factor} = \frac{420}{1280} = 0.328125$$
$$W_{target} = 1280 \times 0.328125 = 420\text{px}, \quad H_{target} = 800 \times 0.328125 = 262.5 \approx 263\text{px}$$
$$\text{Resulting Size} = 420\text{px} \times 263\text{px}$$

---

## 4. Mathematical Line Interval Distribution

When embedding $N$ visual figures into a Markdown document containing $L$ total lines:

$$\text{Line Interval} = \left\lfloor \frac{L}{N} \right\rfloor$$

### Safe Insertion Invariants:
1. **Zero Text Collisions**: Never insert an image inside fenced code blocks (` ``` `), block quotes (`>`), or mid-paragraph.
2. **Boundary Snapping**: Target insertion lines snap to the nearest empty line or markdown section divider (`---`).
3. **Relative Pathing**: All image links use relative project paths (`images/filename.png`).
4. **Descriptive Italicized Captions**: Every embedded figure must feature an italicized descriptive caption below the image:
   ```markdown
   ![Dashboard Interface Overview](images/01_dashboard.png)
   *_Figure 1: Dashboard Interface Overview_*
   ```

---

## 5. Automated Tooling Reference

- `scripts/resize_420p.py`: Scales single images or entire directories to 420px max dimension while preserving aspect ratio.
- `scripts/readme_embed_pipeline.py`: Automates capture via native Termux Playwright, 420p scaling, and even distribution embedding.
- `scripts/readme_auditor.py`: Executes hostile auditing to verify zero hardcoded paths, zero policy leaks, zero AI vocalization, mandatory TOC, and 420p visual compliance.
