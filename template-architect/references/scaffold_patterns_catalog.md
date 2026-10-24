# Scaffold Patterns Catalog & Functional Placeholder Reference

Authoritative catalog of bare-bones structural scaffolds and functional placeholder conventions across BEHTML and modern HTML5.

## 1. Permitted Functional Placeholder Vocabulary

Use ONLY these literal tags when defining empty regions in templates:

| Structural Area | Allowed Placeholder Tags | Strictly Banned Variations |
| :--- | :--- | :--- |
| **Top Navigation** | `"topnav"`, `"nav_link_1"`, `"nav_link_2"`, `"App Brand"` | `"Home"`, `"About Us"`, `"Click here to navigate"` |
| **Sidebar Navigation** | `"Sidebar"`, `"Sidebar link1"`, `"Sidebar link2"`, `"Menu Item 1"` | `"Dashboard"`, `"Settings"`, `"Helpful Links"` |
| **Headers & Titles** | `"Page Title"`, `"Section Heading"`, `"Card Title"`, `"Subtitle"` | `"Welcome to Acme Corp"`, `"Our Latest News"` |
| **Body Content** | `"Body Paragraph text"`, `"Primary Canvas"`, `"Main Content"` | `"Lorem ipsum dolor..."`, `"Insert your article here..."` |
| **Form Inputs** | `"Input Field"`, `"Search text"`, `"Select Option"`, `"Text Area"` | `"Enter your email..."`, `"Search our 10,000 products"` |
| **Buttons & Controls** | `"Action Button"`, `"Submit"`, `"Cancel"`, `"Execute"` | `"Get Started Now for Free"`, `"Click Me"` |
| **Footer** | `"Footer"`, `"footer_text"`, `"footer_link_1"` | `"Copyright 2026 Acme Corp. All Rights Reserved."` |

## 2. Standard App Layout Scaffolds

### Pattern A: Holy Grail Layout (BEHTML 8-Lane Grid)
```
x_start: 0, x_span: 8, y_span: 1 -> "Header" / "topnav"
x_start: 0, x_span: 2, y_span: 10 -> "Sidebar" ("Sidebar link1", "Sidebar link2")
x_start: 2, x_span: 6, y_span: 10 -> "Main Content" ("Page Title", "Body Paragraph text")
x_start: 0, x_span: 8, y_span: 1 -> "Footer"
```

### Pattern B: Admin Dashboard Layout (HTML5 Flexbox)
```html
<div class="scaffold-dashboard">
  <header class="scaffold-toolbar">
    <span class="scaffold-brand">App Brand</span>
    <nav class="scaffold-topnav">
      <span>topnav link1</span>
      <span>topnav link2</span>
    </nav>
  </header>
  <div class="scaffold-body">
    <aside class="scaffold-sidebar">
      <div>Sidebar link1</div>
      <div>Sidebar link2</div>
    </aside>
    <main class="scaffold-main">
      <h1>Page Title</h1>
      <div class="scaffold-metrics-row">
        <div class="scaffold-card">Metric 1 Title</div>
        <div class="scaffold-card">Metric 2 Title</div>
        <div class="scaffold-card">Metric 3 Title</div>
      </div>
      <div class="scaffold-data-table">Data Table / Primary Canvas</div>
    </main>
  </div>
</div>
```

### Pattern C: Split-Pane Editor (BEHTML 8-Lane Grid)
```
x_start: 0, x_span: 8, y_span: 1 -> "App Header"
x_start: 0, x_span: 4, y_span: 12 -> "Input Workspace" ("Editor Title", "Body Paragraph text")
x_start: 4, x_span: 4, y_span: 12 -> "Output Display" ("Preview Title", "Rendered Canvas")
x_start: 0, x_span: 8, y_span: 1 -> "Toolbar" ("Action Button", "Cancel")
```

### Pattern D: Centered Modal / Dialog
```html
<div class="scaffold-modal-backdrop">
  <div class="scaffold-modal-box">
    <h2>Dialog Title</h2>
    <div class="scaffold-modal-body">Body Paragraph text</div>
    <div class="scaffold-modal-actions">
      <button>Cancel</button>
      <button>Action Button</button>
    </div>
  </div>
</div>
```

## 3. Banned Content Patterns (Immediate Quality Gate Failures)

The following will trigger automatic linter rejection:
1. Multi-word descriptive guidance: *"This area is designed for user comments and reviews."*
2. Simulated corporate jargon: *"Leading provider of scalable AI-driven synergies."*
3. Placeholder images: `https://via.placeholder.com/150`, unrequested SVG icons, or fake avatar circles with initials.
4. Visible framework debugging: *"BEHTML grid initialized: 8 lanes active."*
