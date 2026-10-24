# The 4-Prompt Sequential Authoring Workflow

- **Document Identifier**: `four_part_article_structure.md`
- **Skill**: [`publication-blog-post-writer`](../SKILL.md)
- **Version**: 100
- **Release Version**: 300
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
- **RELATIONAL_ID**: `b38a4d10-8e1f-4c22-951b-6d7e8f9a0b12`

---

## 1. Overview & Objective

To prevent token limits, shallow summaries, or rushed conclusions, long-form technical articles must be authored across a **4-Prompt Sequential Pipeline**:
- **Prompt 1**: Architectural Blueprint & Sectional Plan
- **Prompt 2**: Draft Part 1 (Motivation) & Part 2 (Architecture)
- **Prompt 3**: Draft Part 3 (Implementation Details & Code)
- **Prompt 4**: Draft Part 4 (Production Hardening & Horizon) + Assembly

---

## 2. Prompt Execution Templates

### Prompt 1: Sectional Blueprint
```text
[TASK: Blog Post Sectional Plan]
Topic: <Selected Title>
Difficulty Tier: <Beginner | Intermediate | Advanced | God Tier>
Instructions:
1. Outline four detailed sections: Motivation/Context, Architectural Model, Concrete Implementation, Horizons.
2. Under each section, list 3-5 concrete technical talking points and verified file paths.
3. Save to: <project_dir>/01_plan.md
Negative Constraints: Zero generic marketing fluff. Strict focus on technical invariants.
```

### Prompt 2: Draft Parts 1 & 2
```text
[TASK: Draft Parts 1 & 2]
Plan: Ingest <project_dir>/01_plan.md
Instructions:
1. Write Part 1: The Operational Problem & Real-World Context (600-800 words).
2. Write Part 2: System Architecture & Design Invariants (800-1,000 words).
3. Save to: <project_dir>/02_part1_part2.md
```

### Prompt 3: Draft Part 3
```text
[TASK: Draft Part 3]
Plan: Ingest <project_dir>/01_plan.md
Instructions:
1. Write Part 3: Deep Technical Implementation & Production Code Walkthrough (1,000-1,500 words).
2. Embed verified code snippets, CLI invocations, and deterministic exit code tables.
3. Save to: <project_dir>/03_part3.md
```

### Prompt 4: Draft Part 4 & Assembly
```text
[TASK: Draft Part 4 & Final Assembly]
Plan: Ingest <project_dir>/01_plan.md
Instructions:
1. Write Part 4: Production Hardening, Edge Cases, and Future Horizons (600-800 words).
2. Run blog_post_assembler.py to combine all sections into <project_dir>/assembled_article.md.
3. Verify author crediting footer per Policy §9.2.
```

---

*Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton*
