import json
import re
from pathlib import Path

skills_root = Path('/storage/emulated/0/Admin/Dev/Skills/agy-consolidated')
skills_dirs = sorted([p for p in skills_root.iterdir() if p.is_dir() and p.name != 'dev'])

# Mapping from cartographer
LAYER_NAMES = {
    1: "L0_Substrate_L1_Entities",
    2: "L1_Validation_L2_Verification",
    3: "L2_Adapters_L3_Services",
    4: "L4_Presentation_Transport",
    5: "L3_Use_Cases_Cross_Layer_Blueprinting",
    6: "L5_Composition_Root",
}

LAYER_DESC = {
    1: "Core primitives, data structures, and format invariants",
    2: "Black-box validators, schema checkers, and policy gates",
    3: "Language scaffolders, CLI standardizers, and operational tools",
    4: "BEHTML builders, spatial templates, and UI components",
    5: "Architecture planners, idea extractors, and taxonomy mappers",
    6: "Root orchestrators, cartographers, and DAG execution pipelines",
}

# Explicit layer mappings
SKILL_LAYERS = {
    "skill-architect": 6,
    "skill-ecosystem-cartographer": 6,
    "skill-chain-coordinator": 6,
    "skill-chain-recipe-composer": 6,
    "arch-layered-refactor": 6,
    "agy-skill-refactor": 6,
    "domain-cartography-coordinator": 6,
    "domain-scoped-coordinators": 6,
    "file-archive-coordinator": 6,
}

skills_info = []
for sdir in skills_dirs:
    sfile = sdir / 'SKILL.md'
    if not sfile.exists():
        continue
    raw = sfile.read_text(encoding='utf-8')
    parts = raw.split('---', 2)
    fm = parts[1] if len(parts) >= 3 else ''
    name_m = re.search(r'^name:\s*([^\n]+)$', fm, re.M)
    sname = name_m.group(1).strip().strip('\'\"') if name_m else sdir.name
    desc_m = re.search(r'description:\s*(?:>-\s*|\|\s*)?(.*?)(?=\n[a-zA-Z0-9_-]+:|\Z)', fm, re.DOTALL)
    desc = ' '.join(desc_m.group(1).split()) if desc_m else ''

    if sdir.name in SKILL_LAYERS:
        layer = SKILL_LAYERS[sdir.name]
    else:
        layer_m = re.search(r'Layer\s*([0-6])', raw)
        if layer_m:
            layer = int(layer_m.group(1))
        else:
            if sname.endswith(('-core', '-nesting-core', '-mfdb-core')):
                layer = 1
            elif sname.endswith(('-validator', '-chunker', '-auditor', '-engine')):
                layer = 2
            elif sname.endswith(('-automator', '-pipeline', '-scaffold-python', '-scaffold-javascript', '-scaffold-bash', '-manager', '-manage', '-delivery')):
                layer = 3
            elif sname.endswith(('-builder', '-diagrammer', '-decomposer', '-mapper', '-template', '-preferences')):
                layer = 4
            elif sname.endswith(('-composer', '-planner', '-architect', '-refactor', '-rewriter', '-writer', '-analysis', '-extraction', '-grounding')):
                layer = 5
            elif sname.endswith(('-coordinator', '-cartographer', '-recipe-composer')):
                layer = 6
            else:
                layer = 3

    skills_info.append({
        'dir': sdir.name,
        'name': sname,
        'layer': layer,
        'desc': desc
    })

readme = [
    '# Antigravity & Gemini Skills Consolidated Ecosystem',
    '',
    '**Author:** Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton  ',
    '**Release:** Release_Version 300 / 301 Era  ',
    '**Date:** 2026-10-24  ',
    f'**Total Production Skills:** {len(skills_info)}  ',
    '',
    '---',
    '',
    '## 1. Architectural Layer Hierarchy (L1–L6)',
    '',
    '| Layer | Tier Code | Description | Count |',
    '| :---: | :--- | :--- | :---: |',
]

for l in range(1, 7):
    count = len([s for s in skills_info if s['layer'] == l])
    readme.append(f"| **L{l}** | `{LAYER_NAMES[l]}` | {LAYER_DESC[l]} | {count} |")

readme.extend([
    '',
    '---',
    '',
    '## 2. Master Skills Catalog',
    '',
])

for l in range(1, 7):
    l_skills = [s for s in skills_info if s['layer'] == l]
    readme.append(f"### Layer {l}: {LAYER_NAMES[l]} ({len(l_skills)} skills)")
    readme.append('')
    readme.append('| Skill Directory | Canonical Name | Purpose & Triggers |')
    readme.append('| :--- | :--- | :--- |')
    for s in l_skills:
        short_desc = s['desc'][:160] + '...' if len(s['desc']) > 160 else s['desc']
        clean_desc = short_desc.replace('|', '\\|')
        readme.append(f"| [`{s['dir']}`](./{s['dir']}) | `{s['name']}` | {clean_desc} |")
    readme.append('')

readme.extend([
    '---',
    '',
    '## 3. Maintenance, Audits & Verification',
    '',
    'All consolidation tracking artifacts reside in [`dev/`](./dev/):',
    '- [`dev/checklist-20261023-235528.md`](./dev/checklist-20261023-235528.md): Granular execution checklist & verification audit.',
    '- [`dev/change-log.md`](./dev/change-log.md): Record of deduplication, superset merges, and reference repairs.',
    '- [`dev/variable_naming_issues.md`](./dev/variable_naming_issues.md): Tracked naming and namespace observations.',
    '- [`dev/security-notes.md`](./dev/security-notes.md): Security considerations and observations.',
    '',
])

(skills_root / 'README.md').write_text('\n'.join(readme) + '\n', encoding='utf-8')
print(f"Generated clean README.md with {len(skills_info)} skills across 6 layers.")
