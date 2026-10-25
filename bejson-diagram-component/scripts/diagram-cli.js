#!/usr/bin/env node
/**
 * File:           diagram-cli.js
 * Description:    CLI tool for BEJSON Diagrammer generation, active board extension,
 *                 spatial scaffolding, and injection into the Canvas / Component Templates.
 *                 Single Source of Truth: MFDB Diagrammer React Conversion Ecosystem.
 * Relational IDs: 64b9314e-f6bf-4807-84c7-a2852eae1771 (Ledger Blueprint)
 *                 c9f8e7d6-c5b4-4321-8765-43210fe98765 (Arrival Validation)
 * Version:        2.0.0
 * Author:         Elton Boehnen · boehnenelton2024@gmail.com
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

// ============================================================================
// 1. AI Prompt & Instruction Historical Ledger Constants
// ============================================================================

const RELATIONAL_ID = "64b9314e-f6bf-4807-84c7-a2852eae1771";
const ARRIVAL_VALIDATION_RELATIONAL_ID = "c9f8e7d6-c5b4-4321-8765-43210fe98765";

const TARGET_MODELS = [
  "gemini-3.6-flash",
  "gemini-3.8-flash",
  "gemini-3.5-flash-lite",
  "gemini-3.7-flash",
  "gemini-3.1-pro-preview"
];
const DEFAULT_MODEL = "gemini-3.6-flash";

const SYSTEM_INSTRUCTION_BLUEPRINT = `You are an expert systems diagrammer and spatial software architect.
Your task is to take natural language requirements from the user and construct a structured diagram build plan adhering to the BEJSON Diagrammer MFDB Schema.

The diagram structure consists of:
1. Shapes: Nodes on the board.
   - tempId: unique temporary identifier (e.g. 's1', 's2')
   - label: concise descriptive label
   - text: optional multi-line explanatory body text
   - kind: 'rect' or 'circle'
   - sizeClass: 'small' (100x100), 'medium' (200x100), 'large' (300x150), 'huge' (600x300)
   - color: hex color code (default '#d9d9d9' or '#b3b3b3' for child nodes)
   - fontColor: 'auto', '#ffffff', or '#000000'
   - cx: horizontal center coordinate in pixels
   - cy: vertical center coordinate in pixels
   - parentTempId: optional parent shape tempId establishing tree hierarchy

2. Connectors: Relationships between shapes.
   - fromTempId: source shape tempId
   - toTempId: destination shape tempId
   - flow: 'forward' (arrow at destination), 'backward' (arrow at source), 'bidirectional' (arrows on both ends), 'none' (solid line)

3. Territories: Bounding background regions or zones.
   - kind: 'rect' or 'circle'
   - cx: horizontal center coordinate
   - cy: vertical center coordinate
   - size: width/height or diameter in pixels (min 80, typical 240-400)
   - label: territory name
   - color: brand territory hex color (e.g. '#000000', '#DE2626', '#737373')

Layout Rules:
- Prevent overlapping shapes by providing at least 40px padding between bounding boxes.
- Group related nodes inside dedicated territories if requested.
- Place root nodes near the top (cy: 200) and cascade child tiers downward (cy + 160) or horizontally (cx + 240).
- If XML tags such as <scaffold mode="tree|flowchart|grid"/> or <zone name="..."/> are used, align spatial coordinates to the requested pattern.
- Mobile Viewport Standard: Always account for the 100 pixel lower browser toolbar on mobile devices (reserve at least 100px bottom clearance/padding on viewports, position bottom floating actions and inspectors at bottom: calc(100px + 16px), and fitView with 160px bottom clearance).

Response Format:
Return strictly a valid JSON object without surrounding markdown fences or commentary:
{
  "shapes": [ ... ],
  "connectors": [ ... ],
  "territories": [ ... ]
}`;

const SIZE_CLASSES = {
  small:  { w: 100, h: 100 },
  medium: { w: 200, h: 100 },
  large:  { w: 300, h: 150 },
  huge:   { w: 600, h: 300 },
};

const KNOWN_SIZE_CLASSES = ['small', 'medium', 'large', 'huge'];
const KNOWN_SHAPE_KINDS = ['rect', 'circle'];
const KNOWN_FLOW_VALUES = ['forward', 'backward', 'bidirectional', 'none'];
const HEX_COLOR_REGEX = /^#[0-9a-fA-F]{3,8}$/;

// ============================================================================
// 2. Ledger Prompt Formatters (Sections 2 & 3)
// ============================================================================

function buildContextAttachmentBlock(fileName, fileContent, userPrompt) {
  const block = `[ATTACHED CONTEXT FILE: "${fileName}"]
DIRECTIVE: The user has attached this file as context to be studied for use with building the diagram. Meticulously analyze the data structures, entities, schema tables, fields, code components, or workflow contained within, and construct the diagram reflecting this context.

--- BEGIN CONTEXT CONTENT: ${fileName} ---
${fileContent}
--- END CONTEXT CONTENT ---`;

  const promptSection = `[USER INSTRUCTIONS / PROMPT]
${userPrompt || "Analyze the attached context file above and construct a clear, comprehensive architecture and relationship diagram representing it."}`;

  return `${block}\n\n${promptSection}`;
}

function buildAppendModeContextBlock(existingDiagram, userPrompt) {
  const shapes = existingDiagram.shapes || [];
  const connectors = existingDiagram.connectors || [];
  const territories = existingDiagram.territories || [];

  let minX = 999999, maxX = 0, minY = 999999, maxY = 0;
  shapes.forEach(s => {
    const cx = s.cx || 200;
    const cy = s.cy || 200;
    minX = Math.min(minX, cx);
    maxX = Math.max(maxX, cx);
    minY = Math.min(minY, cy);
    maxY = Math.max(maxY, cy);
  });

  if (shapes.length === 0) {
    minX = 200; maxX = 800; minY = 200; maxY = 600;
  }

  const shapesSummary = shapes.map(s =>
    `- ID: "${s.id || s.tempId}", Label: "${s.label}", Kind: "${s.kind || 'rect'}", Size: "${s.sizeClass || 'medium'}", Position: (cx: ${s.cx}, cy: ${s.cy})`
  ).join('\n') || "(None)";

  const connectorsSummary = connectors.map(c =>
    `- From: "${c.from || c.fromTempId}" -> To: "${c.to || c.toTempId}", Flow: "${c.flow || 'forward'}"`
  ).join('\n') || "(None)";

  const territoriesSummary = territories.map(t =>
    `- Zone: "${t.label}", Kind: "${t.kind || 'rect'}", Center: (cx: ${t.cx}, cy: ${t.cy}), Size: ${t.size}px, Color: "${t.color}"`
  ).join('\n') || "(None)";

  return `[ATTACHED CONTEXT FILE: "active_board_existing_diagram.txt"]
DIRECTIVE: The user has attached this file as context to be studied for use with building the diagram. Meticulously analyze the data structures, entities, schema tables, fields, code components, or workflow contained within, and construct the diagram reflecting this context.

--- BEGIN CONTEXT CONTENT: active_board_existing_diagram.txt ---
[EXISTING ACTIVE DIAGRAM ALREADY ON CANVAS]
Total Existing Shapes: ${shapes.length}
Total Existing Connectors: ${connectors.length}
Total Existing Territories: ${territories.length}
Spatial Bounding Area of Existing Nodes: Horizontal [${minX}px to ${maxX}px], Vertical [${minY}px to ${maxY}px]

Existing Shapes:
${shapesSummary}

Existing Connectors:
${connectorsSummary}

Existing Territories:
${territoriesSummary}

CRITICAL APPEND / EXPANSION DIRECTIVES:
1. The user wants to BUILD OFF OF and EXTEND this existing diagram without stacking on top of existing shapes.
2. Calculate spatial coordinates (cx, cy) that place new nodes in open adjacent canvas space (e.g. beyond maxX + 220 horizontally, or below maxY + 180 vertically).
3. Connect new shapes to existing nodes by setting fromTempId or toTempId to an existing node ID or exact label.
4. Return ONLY the new shapes, connectors, and territories to be added to the board.
--- END CONTEXT CONTENT ---

[USER INSTRUCTIONS / PROMPT]
${userPrompt || "Extend the existing architecture diagram with the requested components."}`;
}

// ============================================================================
// 3. Official React App Validators & Remediation Pipeline (Section 4)
// ============================================================================

function validatePlanSemantics(plan) {
  const errors = [];
  const warnings = [];

  if (!plan || typeof plan !== 'object') {
    errors.push("Plan payload is not an object.");
    return { valid: false, errors, warnings };
  }

  const seenIds = new Set();
  (plan.shapes || []).forEach(s => {
    const tid = s.tempId || s.id || '?';
    if (seenIds.has(tid)) {
      errors.push(`Duplicate shape identifier '${tid}'.`);
    }
    seenIds.add(tid);

    const sc = s.sizeClass || 'medium';
    if (!KNOWN_SIZE_CLASSES.includes(sc)) {
      errors.push(`Shape '${tid}': sizeClass '${sc}' is not one of ${JSON.stringify(KNOWN_SIZE_CLASSES)}.`);
    }
    const kind = s.kind || 'rect';
    if (!KNOWN_SHAPE_KINDS.includes(kind)) {
      errors.push(`Shape '${tid}': kind '${kind}' is not one of ${JSON.stringify(KNOWN_SHAPE_KINDS)}.`);
    }
    if (typeof s.cx !== 'number' || isNaN(s.cx)) {
      errors.push(`Shape '${tid}': cx must be numeric.`);
    }
    if (typeof s.cy !== 'number' || isNaN(s.cy)) {
      errors.push(`Shape '${tid}': cy must be numeric.`);
    }
    if (s.color && !HEX_COLOR_REGEX.test(String(s.color))) {
      warnings.push(`Shape '${tid}': color '${s.color}' is not a standard hex color code.`);
    }
    if (!s.label || !String(s.label).trim()) {
      warnings.push(`Shape '${tid}': missing descriptive label.`);
    }
  });

  (plan.connectors || []).forEach((c, idx) => {
    const flow = c.flow || 'forward';
    if (!KNOWN_FLOW_VALUES.includes(flow)) {
      errors.push(`Connector #${idx} (${c.fromTempId || c.from} -> ${c.toTempId || c.to}): invalid flow '${flow}'.`);
    }
  });

  (plan.territories || []).forEach((t, idx) => {
    if (typeof t.cx !== 'number' || typeof t.cy !== 'number' || typeof t.size !== 'number') {
      errors.push(`Territory #${idx}: cx, cy, and size must be numeric.`);
    }
    if (t.size <= 0) {
      errors.push(`Territory #${idx}: size must be positive.`);
    }
    if (t.color && !HEX_COLOR_REGEX.test(String(t.color))) {
      warnings.push(`Territory #${idx}: color '${t.color}' is not a standard hex color code.`);
    }
  });

  return { valid: errors.length === 0, errors, warnings };
}

function getBoxOf(s) {
  const d = SIZE_CLASSES[s.sizeClass] || SIZE_CLASSES.medium;
  return { x: s.cx - d.w / 2, y: s.cy - d.h / 2, w: d.w, h: d.h };
}

function getTerritoryBox(t) {
  const sz = t.size || 240;
  return { x: t.cx - sz / 2, y: t.cy - sz / 2, w: sz, h: sz };
}

function boxesOverlap(a, b) {
  return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

function validateDiagram(diagram) {
  const errors = [];
  const warnings = [];

  const shapes = diagram.shapes || [];
  const connectors = diagram.connectors || [];
  const territories = diagram.territories || [];

  const shapeIds = new Set();
  const shapeMap = new Map();

  shapes.forEach(s => {
    if (shapeIds.has(s.id)) {
      errors.push(`Duplicate shape ID '${s.id}'.`);
    }
    shapeIds.add(s.id);
    shapeMap.set(s.id, s);

    if (s.sizeClass && !KNOWN_SIZE_CLASSES.includes(s.sizeClass)) {
      errors.push(`Shape '${s.id}' has unknown sizeClass '${s.sizeClass}'.`);
    }
    if (s.kind && !KNOWN_SHAPE_KINDS.includes(s.kind)) {
      errors.push(`Shape '${s.id}' has unknown kind '${s.kind}'.`);
    }
    if (s.parentId && !shapeIds.has(s.parentId) && !shapes.some(x => x.id === s.parentId)) {
      errors.push(`Shape '${s.id}' references non-existent parentId '${s.parentId}'.`);
    }
  });

  // Cycle detection in parent hierarchy
  shapes.forEach(s => {
    const visited = new Set();
    let cur = s;
    while (cur && cur.parentId) {
      if (visited.has(cur.id)) {
        errors.push(`Shape '${s.id}' is part of a parentId hierarchy cycle (infinite recursion).`);
        break;
      }
      visited.add(cur.id);
      cur = shapeMap.get(cur.parentId);
    }
  });

  // Connectors validation
  const seenConnPairs = new Set();
  connectors.forEach(c => {
    if (!shapeIds.has(c.from)) {
      errors.push(`Connector '${c.id}' references missing source shape '${c.from}'.`);
    }
    if (!shapeIds.has(c.to)) {
      errors.push(`Connector '${c.id}' references missing target shape '${c.to}'.`);
    }
    if (c.from === c.to) {
      errors.push(`Connector '${c.id}' connects shape '${c.from}' to itself.`);
    }
    const pairKey = [c.from, c.to].sort().join("<->");
    if (seenConnPairs.has(pairKey)) {
      warnings.push(`Connector '${c.id}' duplicates an existing connection between '${c.from}' and '${c.to}'.`);
    }
    seenConnPairs.add(pairKey);
  });

  // Territory overlaps
  for (let i = 0; i < territories.length; i++) {
    for (let j = i + 1; j < territories.length; j++) {
      if (boxesOverlap(getTerritoryBox(territories[i]), getTerritoryBox(territories[j]))) {
        warnings.push(`Territories '${territories[i].id}' and '${territories[j].id}' overlap.`);
      }
    }
  }

  // Shape overlaps
  for (let i = 0; i < shapes.length; i++) {
    for (let j = i + 1; j < shapes.length; j++) {
      if (boxesOverlap(getBoxOf(shapes[i]), getBoxOf(shapes[j]))) {
        errors.push(`Shapes '${shapes[i].id}' and '${shapes[j].id}' overlap (bounding box intersection).`);
      }
    }
  }

  return { valid: errors.length === 0, errors, warnings };
}

/**
 * Diagram Arrival Auto-Remediation (Section 4 protocol)
 */
function remediateDiagram(diagram) {
  const shapes = [...(diagram.shapes || [])];
  let connectors = [...(diagram.connectors || [])];
  const territories = [...(diagram.territories || [])];

  // 1. Deduplicate & normalize shape IDs
  const seenIds = new Set();
  shapes.forEach((s, idx) => {
    if (!s.id || seenIds.has(s.id)) {
      s.id = `shape_${idx + 1}_${Math.random().toString(36).substr(2, 5)}`;
    }
    seenIds.add(s.id);
    s.cx = Math.round((s.cx || 300) / 50) * 50;
    s.cy = Math.round((s.cy || 200) / 50) * 50;
    s.sizeClass = s.sizeClass || 'medium';
    s.kind = s.kind || 'rect';
    s.color = s.color || '#d9d9d9';
    s.fontColor = s.fontColor || 'auto';
  });

  // 2. Break parent cycles & remove orphaned parents
  const shapeMap = new Map(shapes.map(s => [s.id, s]));
  shapes.forEach(s => {
    if (s.parentId && !shapeMap.has(s.parentId)) {
      s.parentId = null;
    }
    // Check cycle
    const visited = new Set();
    let cur = s;
    while (cur && cur.parentId) {
      if (visited.has(cur.id)) {
        s.parentId = null; // break cycle
        break;
      }
      visited.add(cur.id);
      cur = shapeMap.get(cur.parentId);
    }
  });

  // 3. Remove dangling connectors
  connectors = connectors.filter(c => shapeMap.has(c.from) && shapeMap.has(c.to) && c.from !== c.to);

  // 4. Normalize territories
  territories.forEach((t, idx) => {
    t.id = t.id || `terr_${idx + 1}`;
    t.cx = Math.round((t.cx || 300) / 50) * 50;
    t.cy = Math.round((t.cy || 300) / 50) * 50;
    t.size = Math.max(80, t.size || 240);
    t.kind = t.kind || 'rect';
    t.color = t.color || '#000000';
  });

  return {
    diagramId: diagram.diagramId || `diag_${Date.now()}`,
    name: diagram.name || "Architecture Diagram",
    description: diagram.description || "",
    shapes,
    connectors,
    territories
  };
}

// ============================================================================
// 4. Layout Math & Spatial Scaffolding Algorithms
// ============================================================================

function snapToGrid(val, step = 50) {
  return Math.round(val / step) * step;
}

function applyLayoutScaffolding(plan) {
  const shapes = plan.shapes || [];
  const connectors = plan.connectors || [];
  const territories = plan.territories || [];

  // Snap all coordinates to 50px increments
  shapes.forEach(s => {
    s.cx = snapToGrid(s.cx || 300);
    s.cy = snapToGrid(s.cy || 200);
  });
  territories.forEach(t => {
    t.cx = snapToGrid(t.cx || 300);
    t.cy = snapToGrid(t.cy || 300);
    t.size = snapToGrid(t.size || 280);
  });

  // Resolve overlaps between shapes
  for (let i = 0; i < shapes.length; i++) {
    for (let j = i + 1; j < shapes.length; j++) {
      while (boxesOverlap(getBoxOf(shapes[i]), getBoxOf(shapes[j]))) {
        shapes[j].cx = snapToGrid(shapes[j].cx + 260);
      }
    }
  }

  return {
    ...plan,
    shapes,
    connectors,
    territories
  };
}

// ============================================================================
// 5. Offline Synthesizer (Zero-Latency Fallback)
// ============================================================================

function offlineSynthesizeDiagram(prompt, contextFiles = []) {
  let domain = "Service";
  if (/auth|token|oauth|jwt/i.test(prompt)) domain = "Auth";
  else if (/event|kafka|stream|queue/i.test(prompt)) domain = "EventStream";
  else if (/ai|model|llm|agent/i.test(prompt)) domain = "AI";
  else if (/payment|checkout|ledger|stripe/i.test(prompt)) domain = "Payment";

  const shapes = [
    {
      tempId: "node_gw",
      label: "API Gateway",
      text: "Ingress proxy, TLS termination, and rate limiting.",
      kind: "rect",
      sizeClass: "medium",
      color: "#d9d9d9",
      fontColor: "auto",
      cx: 350,
      cy: 200,
      parentTempId: null
    },
    {
      tempId: "node_core",
      label: `${domain} Core Service`,
      text: `Primary business logic and execution handlers for ${domain}.`,
      kind: "rect",
      sizeClass: "large",
      color: "#b3b3b3",
      fontColor: "auto",
      cx: 650,
      cy: 200,
      parentTempId: "node_gw"
    },
    {
      tempId: "node_db",
      label: `${domain} Persistence Store`,
      text: "Persistent relational ledger with transaction isolation.",
      kind: "rect",
      sizeClass: "small",
      color: "#8c8c8c",
      fontColor: "auto",
      cx: 950,
      cy: 200,
      parentTempId: "node_core"
    },
    {
      tempId: "node_cache",
      label: "Cache Cluster (Redis)",
      text: "Distributed in-memory caching and session key storage.",
      kind: "rect",
      sizeClass: "small",
      color: "#8c8c8c",
      fontColor: "auto",
      cx: 650,
      cy: 380,
      parentTempId: "node_core"
    }
  ];

  const connectors = [
    { fromTempId: "node_gw", toTempId: "node_core", flow: "forward" },
    { fromTempId: "node_core", toTempId: "node_db", flow: "bidirectional" },
    { fromTempId: "node_core", toTempId: "node_cache", flow: "bidirectional" }
  ];

  const territories = [
    {
      kind: "rect",
      cx: 650,
      cy: 280,
      size: 700,
      label: `${domain} Architecture Zone`,
      color: "#000000"
    }
  ];

  return { shapes, connectors, territories };
}

// ============================================================================
// 6. Gemini API Invocation
// ============================================================================

async function callGeminiApi(prompt, systemInstruction, model, apiKey) {
  return new Promise((resolve, reject) => {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`;
    const payload = {
      systemInstruction: { parts: [{ text: systemInstruction }] },
      contents: [{ parts: [{ text: prompt }] }],
      generationConfig: { responseMimeType: "application/json" }
    };
    const data = JSON.stringify(payload);
    const req = https.request(url, {
      method: "POST",
      headers: { "Content-Type": "application/json", "Content-Length": Buffer.byteLength(data) }
    }, (res) => {
      let body = "";
      res.on("data", chunk => body += chunk);
      res.on("end", () => {
        try {
          const parsed = JSON.parse(body);
          if (parsed.error) return reject(new Error(parsed.error.message || "API Error"));
          const text = parsed.candidates?.[0]?.content?.parts?.[0]?.text;
          if (!text) return reject(new Error("Empty model response"));
          resolve(JSON.parse(text));
        } catch (e) {
          reject(e);
        }
      });
    });
    req.on("error", reject);
    req.write(data);
    req.end();
  });
}

// ============================================================================
// 7. Template Injection
// ============================================================================

function injectDiagramIntoTemplate(templatePath, diagramData, outputPath, customTitle) {
  if (!fs.existsSync(templatePath)) {
    throw new Error(`Template not found: ${templatePath}`);
  }

  let html = fs.readFileSync(templatePath, 'utf8');
  const title = customTitle || diagramData.name || "Architecture Diagram";
  const desc = diagramData.description || "Technical Architecture Specification";
  const jsonString = JSON.stringify(diagramData, null, 2);

  // Injected data replacement
  const placeholderPattern = /\/\*\s*__DIAGRAM_DATA__\s*\*\//;
  if (placeholderPattern.test(html)) {
    html = html.replace(placeholderPattern, jsonString);
  } else {
    html = html.replace(
      /<script class="w-diag-data" type="application\/json">[\s\S]*?<\/script>/,
      `<script class="w-diag-data" type="application/json">\n${jsonString}\n    </script>`
    );
    html = html.replace(
      /<script id="injected-diagram-data" type="application\/json">[\s\S]*?<\/script>/,
      `<script id="injected-diagram-data" type="application/json">\n${jsonString}\n  </script>`
    );
  }

  const instanceId = "inst_" + Math.random().toString(36).substring(2, 9);
  html = html.replace(/__INSTANCE_ID__/g, instanceId);
  html = html.replace(/__DIAGRAM_TITLE__/g, title);
  html = html.replace(/__DIAGRAM_DESCRIPTION__/g, desc);

  const outDir = path.dirname(outputPath);
  if (!fs.existsSync(outDir)) {
    fs.mkdirSync(outDir, { recursive: true });
  }

  fs.writeFileSync(outputPath, html, 'utf8');
  return outputPath;
}

// ============================================================================
// 8. CLI Subcommands
// ============================================================================


function buildActiveDiagramContextSummary(existing) {
  const shapes = existing.shapes || [];
  const connectors = existing.connectors || [];
  const territories = existing.territories || [];

  let minX = 999999, maxX = 0, minY = 999999, maxY = 0;
  shapes.forEach(s => {
    if (s.cx < minX) minX = s.cx;
    if (s.cx > maxX) maxX = s.cx;
    if (s.cy < minY) minY = s.cy;
    if (s.cy > maxY) maxY = s.cy;
  });

  const shapesSummary = shapes.map(s =>
    `- ID: "${s.id}", Label: "${s.label}", Kind: "${s.kind}", Size: "${s.sizeClass}", Position: (cx: ${s.cx}, cy: ${s.cy})${s.parentId ? `, Parent: "${s.parentId}"` : ""}${s.text ? `, Description: "${s.text}"` : ""}`
  ).join("\n");

  const connectorsSummary = connectors.map(c =>
    `- From: "${c.from}" -> To: "${c.to}", Flow: "${c.flow || "forward"}"`
  ).join("\n");

  const territoriesSummary = territories.map(t =>
    `- Zone: "${t.label}", Kind: "${t.kind}", Center: (cx: ${t.cx}, cy: ${t.cy}), Size: ${t.size}px, Color: "${t.color}"`
  ).join("\n");

  return `[ATTACHED CONTEXT FILE: "active_board_existing_diagram.txt"]\nDIRECTIVE: The user has attached this file as context to be studied for use with building the diagram. Meticulously analyze the data structures, entities, schema tables, fields, code components, or workflow contained within, and construct the diagram reflecting this context.\n\n--- BEGIN CONTEXT CONTENT: active_board_existing_diagram.txt ---\n[EXISTING ACTIVE DIAGRAM ALREADY ON CANVAS]\nTotal Existing Shapes: ${shapes.length}\nTotal Existing Connectors: ${connectors.length}\nTotal Existing Territories: ${territories.length}\nSpatial Bounding Area of Existing Nodes: Horizontal [${minX === 999999 ? 200 : minX}px to ${maxX === 0 ? 800 : maxX}px], Vertical [${minY === 999999 ? 200 : minY}px to ${maxY === 0 ? 600 : maxY}px]\n\nExisting Shapes:\n${shapesSummary || "(None)"}\n\nExisting Connectors:\n${connectorsSummary || "(None)"}\n\nExisting Territories:\n${territoriesSummary || "(None)"}\n\nCRITICAL APPEND / EXPANSION DIRECTIVES:\n1. The user wants to BUILD OFF OF and EXTEND this existing diagram without stacking on top of existing shapes.\n2. Calculate spatial coordinates (cx, cy) that place new nodes in open adjacent canvas space (e.g. beyond maxX + 220 horizontally, or below maxY + 180 vertically).\n3. Connect new shapes to existing nodes by setting fromTempId or toTempId to an existing node ID or exact label.\n4. Return ONLY the new shapes, connectors, and territories to be added to the board.\n--- END CONTEXT CONTENT ---`;
}

function offlineSynthesizeAppend(prompt, existing) {
  const shapes = existing.shapes || [];
  let maxX = 0;
  shapes.forEach(s => { if (s.cx > maxX) maxX = s.cx; });
  const startX = Math.max(800, maxX + 260);

  const newShapes = [
    {
      tempId: "node_append_1",
      label: "Monitoring & Telemetry",
      text: "Prometheus metrics scrapers and operational health telemetry",
      kind: "rect",
      sizeClass: "medium",
      color: "#8c8c8c",
      fontColor: "auto",
      cx: startX,
      cy: 220,
      parentTempId: null
    },
    {
      tempId: "node_append_2",
      label: "Alerting Webhook Hub",
      text: "Automated incident dispatch to PagerDuty and Slack",
      kind: "rect",
      sizeClass: "medium",
      color: "#666666",
      fontColor: "#ffffff",
      cx: startX,
      cy: 420,
      parentTempId: "node_append_1"
    }
  ];

  const targetNode = shapes.length > 0 ? shapes[shapes.length - 1].id : "node_append_1";
  const newConnectors = [
    {
      fromTempId: targetNode,
      toTempId: "node_append_1",
      flow: "forward"
    },
    {
      fromTempId: "node_append_1",
      toTempId: "node_append_2",
      flow: "forward"
    }
  ];

  const newTerritories = [
    {
      kind: "rect",
      cx: startX,
      cy: 320,
      size: 440,
      label: "Observability Zone",
      color: "#2a6496"
    }
  ];

  return { shapes: newShapes, connectors: newConnectors, territories: newTerritories };
}

async function cmdAppend(args) {
  const existingPath = args.existing || args.e;
  if (!existingPath || !fs.existsSync(existingPath)) {
    console.error(`[ERROR] Existing diagram path required (--existing <file.json>)`);
    process.exit(1);
  }

  const prompt = args.prompt || args.p || "Extend active diagram";
  const model = args.model || args.m || DEFAULT_MODEL;
  const apiKey = args.apiKey || args.k || process.env.GEMINI_API_KEY || "";
  const outFile = args.out || args.o || "diagram_extended.json";
  const templatePath = args.inject || args.i;
  const isOffline = args.offline || !apiKey;

  console.log(`[BEJSON CLI] Appending to active diagram: ${existingPath}`);
  console.log(`- Prompt: "${prompt}"`);

  const existingData = JSON.parse(fs.readFileSync(existingPath, "utf8"));
  let appendPlan;

  if (isOffline) {
    console.log(`[INFO] Using local offline synthesizer for append.`);
    appendPlan = offlineSynthesizeAppend(prompt, existingData);
  } else {
    const contextBlock = buildActiveDiagramContextSummary(existingData);
    const fullPrompt = `${contextBlock}\n\n[USER INSTRUCTIONS / PROMPT]\n${prompt}`;
    try {
      appendPlan = await callGeminiApi(fullPrompt, SYSTEM_INSTRUCTION_BLUEPRINT, model, apiKey);
    } catch (err) {
      console.warn(`[WARN] Gemini API call failed: ${err.message}. Falling back to offline synthesizer.`);
      appendPlan = offlineSynthesizeAppend(prompt, existingData);
    }
  }

  const sem = validatePlanSemantics(appendPlan);
  if (!sem.valid) {
    console.warn(`[WARN] Semantic warnings in append plan:`, sem.errors);
  }

  const mergedShapes = [...(existingData.shapes || [])];
  const mergedConnectors = [...(existingData.connectors || [])];
  const mergedTerritories = [...(existingData.territories || [])];

  const existingIds = new Set(mergedShapes.map(s => s.id));
  (appendPlan.shapes || []).forEach((s, idx) => {
    let id = s.tempId || s.id || `shape_ext_${idx + 1}`;
    if (existingIds.has(id)) id = `${id}_ext_${idx + 1}`;
    mergedShapes.push({
      id,
      label: s.label || `Node ${mergedShapes.length + 1}`,
      text: s.text || "",
      kind: s.kind || "rect",
      sizeClass: s.sizeClass || "medium",
      color: s.color || "#d9d9d9",
      fontColor: s.fontColor || "auto",
      cx: s.cx,
      cy: s.cy,
      parentId: s.parentTempId || s.parentId || null
    });
  });

  (appendPlan.connectors || []).forEach((c, idx) => {
    mergedConnectors.push({
      id: c.id || `conn_ext_${idx + 1}`,
      from: c.fromTempId || c.from,
      to: c.toTempId || c.to,
      flow: c.flow || "forward"
    });
  });

  (appendPlan.territories || []).forEach((t, idx) => {
    mergedTerritories.push({
      id: t.id || `terr_ext_${idx + 1}`,
      kind: t.kind || "rect",
      cx: t.cx,
      cy: t.cy,
      size: t.size || 280,
      label: t.label || `Zone ${mergedTerritories.length + 1}`,
      color: t.color || "#000000"
    });
  });

  const mergedPayload = remediateDiagram({
    diagramId: existingData.diagramId || "diag_" + Date.now(),
    name: args.title || existingData.name || "Extended Architecture Diagram",
    description: (existingData.description ? existingData.description + "; " : "") + prompt,
    shapes: mergedShapes,
    connectors: mergedConnectors,
    territories: mergedTerritories
  });

  const diagVal = validateDiagram(mergedPayload);
  console.log(`\n[DIAGRAM VALIDATOR] Append Arrival Verification:`);
  console.log(`- Status: ${diagVal.valid ? "PASSED (Valid)" : "WARNINGS DETECTED"}`);
  console.log(`- Total Nodes: ${mergedPayload.shapes.length}`);
  console.log(`- Total Connectors: ${mergedPayload.connectors.length}`);
  console.log(`- Total Territories: ${mergedPayload.territories.length}`);

  fs.writeFileSync(outFile, JSON.stringify(mergedPayload, null, 2), "utf8");
  console.log(`[SUCCESS] Wrote extended diagram to: ${outFile}`);

  if (templatePath) {
    const htmlOut = outFile.endsWith(".json") ? outFile.replace(/\.json$/, ".html") : outFile + ".html";
    injectDiagramIntoTemplate(templatePath, mergedPayload, htmlOut, args.title || mergedPayload.name);
    console.log(`[SUCCESS] Injected extended diagram into: ${htmlOut}`);
  }
}

async function cmdGenerate(args) {
  const prompt = args.prompt || args.p || "";
  const model = args.model || args.m || DEFAULT_MODEL;
  const apiKey = args.apiKey || args.k || process.env.GEMINI_API_KEY || "";
  const outFile = args.out || args.o || "diagram_plan.json";
  const templatePath = args.inject || args.i;
  const isOffline = args.offline || !apiKey;

  const contextFiles = [];
  const contextArg = args.context || args.c;
  if (contextArg) {
    const list = Array.isArray(contextArg) ? contextArg : [contextArg];
    for (const f of list) {
      if (fs.existsSync(f)) {
        contextFiles.push({ name: path.basename(f), content: fs.readFileSync(f, 'utf8') });
      }
    }
  }

  console.log(`[BEJSON CLI] Generating architecture diagram...`);
  console.log(`- Model: ${model}`);
  console.log(`- Prompt: "${prompt}"`);
  console.log(`- Context Files: ${contextFiles.length}`);

  let plan;
  if (isOffline) {
    console.log(`[INFO] Using local offline synthesizer (Section 11.1 zero-latency mode).`);
    plan = offlineSynthesizeDiagram(prompt, contextFiles);
  } else {
    console.log(`[INFO] Calling Gemini API (${model})...`);
    let fullPrompt = prompt;
    if (contextFiles.length > 0) {
      fullPrompt = buildContextAttachmentBlock(contextFiles[0].name, contextFiles[0].content, prompt);
    }
    try {
      plan = await callGeminiApi(fullPrompt, SYSTEM_INSTRUCTION_BLUEPRINT, model, apiKey);
    } catch (err) {
      console.warn(`[WARN] Gemini API call failed: ${err.message}. Falling back to offline synthesizer.`);
      plan = offlineSynthesizeDiagram(prompt, contextFiles);
    }
  }

  // Pre-validation: Plan Semantics
  const semanticVal = validatePlanSemantics(plan);
  if (!semanticVal.valid) {
    console.error(`[ERROR] Plan semantic validation failed:`, semanticVal.errors);
  }
  if (semanticVal.warnings.length > 0) {
    console.warn(`[WARN] Plan warnings:`, semanticVal.warnings);
  }

  // Apply layout scaffolding & arrival auto-remediation
  plan = applyLayoutScaffolding(plan);
  const diagramPayload = remediateDiagram({
    diagramId: "diag_" + Date.now(),
    name: args.title || "Architecture Diagram",
    description: prompt,
    shapes: (plan.shapes || []).map((s, idx) => ({
      id: s.tempId || s.id || `shape_${idx + 1}`,
      label: s.label || `Node ${idx + 1}`,
      text: s.text || "",
      kind: s.kind || "rect",
      sizeClass: s.sizeClass || "medium",
      color: s.color || "#d9d9d9",
      fontColor: s.fontColor || "auto",
      cx: s.cx,
      cy: s.cy,
      parentId: s.parentTempId || s.parentId || null
    })),
    connectors: (plan.connectors || []).map((c, idx) => ({
      id: c.id || `conn_${idx + 1}`,
      from: c.fromTempId || c.from,
      to: c.toTempId || c.to,
      flow: c.flow || "forward"
    })),
    territories: (plan.territories || []).map((t, idx) => ({
      id: t.id || `terr_${idx + 1}`,
      kind: t.kind || "rect",
      cx: t.cx,
      cy: t.cy,
      size: t.size || 240,
      label: t.label || `Zone ${idx + 1}`,
      color: t.color || "#000000"
    }))
  });

  // Post-assembly diagram validation
  const diagVal = validateDiagram(diagramPayload);
  console.log(`\n[DIAGRAM VALIDATOR] Arrival Verification:`);
  console.log(`- Status: ${diagVal.valid ? "PASSED (Valid)" : "WARNINGS DETECTED"}`);
  console.log(`- Nodes: ${diagramPayload.shapes.length}`);
  console.log(`- Connectors: ${diagramPayload.connectors.length}`);
  console.log(`- Territories: ${diagramPayload.territories.length}`);

  fs.writeFileSync(outFile, JSON.stringify(diagramPayload, null, 2), 'utf8');
  console.log(`[SUCCESS] Wrote diagram JSON to: ${outFile}`);

  if (templatePath) {
    const htmlOut = outFile.endsWith('.json') ? outFile.replace(/\.json$/, '.html') : outFile + '.html';
    injectDiagramIntoTemplate(templatePath, diagramPayload, htmlOut, args.title);
    console.log(`[SUCCESS] Injected diagram into template: ${htmlOut}`);
  }
}

function cmdValidate(args) {
  const filePath = args.file || args.f;
  if (!filePath || !fs.existsSync(filePath)) {
    console.error(`[ERROR] File required (--file <path>)`);
    process.exit(1);
  }

  const rawText = fs.readFileSync(filePath, 'utf8');
  let data;
  try {
    data = JSON.parse(rawText);
  } catch (e) {
    console.error(`[ERROR] Invalid JSON: ${e.message}`);
    process.exit(1);
  }

  console.log(`\n======================================================`);
  console.log(`DIAGRAM VALIDATION REPORT (Relational ID: ${ARRIVAL_VALIDATION_RELATIONAL_ID})`);
  console.log(`Target: ${filePath}`);
  console.log(`======================================================`);

  // 1. Plan Semantics
  const sem = validatePlanSemantics(data);
  console.log(`1. Plan Semantics: ${sem.valid ? "PASSED" : "FAILED"}`);
  sem.errors.forEach(e => console.error(`   ✖ ${e}`));
  sem.warnings.forEach(w => console.warn(`   ⚠ ${w}`));

  // 2. Structural & Relational Verification
  const diagVal = validateDiagram(data);
  console.log(`\n2. Relational & Spatial Verification: ${diagVal.valid ? "PASSED" : "FAILED"}`);
  console.log(`   - Total Shapes: ${data.shapes?.length || 0}`);
  console.log(`   - Total Connectors: ${data.connectors?.length || 0}`);
  console.log(`   - Total Territories: ${data.territories?.length || 0}`);
  diagVal.errors.forEach(e => console.error(`   ✖ ${e}`));
  diagVal.warnings.forEach(w => console.warn(`   ⚠ ${w}`));

  const overallValid = sem.valid && diagVal.valid;
  console.log(`\nOVERALL STATUS: ${overallValid ? "100% VALID" : "VALIDATION ISSUES REPORTED"}`);
}

function parseArgs(args) {
  const parsed = { _: [] };
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith("--")) {
      const key = arg.slice(2);
      if (i + 1 < args.length && !args[i + 1].startsWith("-")) {
        parsed[key] = args[++i];
      } else {
        parsed[key] = true;
      }
    } else if (arg.startsWith("-")) {
      const key = arg.slice(1);
      if (i + 1 < args.length && !args[i + 1].startsWith("-")) {
        parsed[key] = args[++i];
      } else {
        parsed[key] = true;
      }
    } else {
      parsed._.push(arg);
    }
  }
  return parsed;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const command = args._[0];

  switch (command) {
    case "generate":
    case "gen":
      await cmdGenerate(args);
      break;
    case "component":
    case "widget":
      const compTemplate = args.template || args.t || path.join(__dirname, "..", "assets", "diagram_component_template.html");
      const compOut = args.out || args.o || "diagram_component.html";
      const diagIn = args.diagram || args.d;
      if (!diagIn) {
        console.error("[ERROR] Diagram JSON path required (--diagram <file.json>)");
        process.exit(1);
      }
      const diagData = JSON.parse(fs.readFileSync(diagIn, "utf8"));
      injectDiagramIntoTemplate(compTemplate, diagData, compOut, args.title);
      console.log(`[SUCCESS] Injected embeddable component into: ${compOut}`);
      break;
    case "inject":
      const injTemplate = args.template || args.t || path.join(__dirname, "..", "assets", "diagram_canvas_template.html");
      const injOut = args.out || args.o || "diagram_canvas.html";
      const inData = JSON.parse(fs.readFileSync(args.diagram || args.d, "utf8"));
      injectDiagramIntoTemplate(injTemplate, inData, injOut, args.title);
      console.log(`[SUCCESS] Injected canvas into: ${injOut}`);
      break;
    case "append":
    case "extend":
      await cmdAppend(args);
      break;
    case "validate":
      cmdValidate(args);
      break;
    default:
      console.log(`BEJSON Diagrammer CLI Tool (Relational ID: ${RELATIONAL_ID})`);
      console.log(`Commands: generate, append, component, inject, validate`);
      break;
  }
}

if (require.main === module) {
  main().catch(err => {
    console.error(`[FATAL]`, err.message);
    process.exit(1);
  });
}

module.exports = {
  SYSTEM_INSTRUCTION_BLUEPRINT,
  RELATIONAL_ID,
  ARRIVAL_VALIDATION_RELATIONAL_ID,
  validatePlanSemantics,
  validateDiagram,
  remediateDiagram,
  applyLayoutScaffolding,
  injectDiagramIntoTemplate
};
