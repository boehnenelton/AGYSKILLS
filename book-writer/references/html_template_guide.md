# SEO & Publication HTML Template Guide

Complete integration reference for compiling multi-chapter books into publication-ready HTML documents.

## Template Placeholder Reference

The embedded template (`assets/book_template.html`) uses standard double-curly placeholders:

| Placeholder | Content Description | Example Value |
| :--- | :--- | :--- |
| `{{PAGE_TITLE}}` | Browser title & tab label | `Mastering Core BEJSON - Elton Boehnen` |
| `{{META_DESCRIPTION}}` | Concise summary for search engines (150-160 chars) | `A comprehensive guide to Core BEJSON...` |
| `{{META_KEYWORDS}}` | Comma-separated keyword tags | `bejson, typescript, database, mfdb` |
| `{{AUTHOR_NAME}}` | Primary author name | `Elton Boehnen` |
| `{{AUTHOR_URL}}` | Author homepage or profile URL | `https://boehnenelton2024.pages.dev` |
| `{{CANONICAL_URL}}` | Authoritative permanent URL for SEO indexing | `https://boehnenelton2024.pages.dev/books/guide.html` |
| `{{SITE_NAME}}` | Platform or brand publication name | `Elton Boehnen Digital Press` |
| `{{OG_TITLE}}` | Open Graph title for social sharing cards | `Mastering Core BEJSON in TypeScript` |
| `{{OG_DESCRIPTION}}` | Open Graph description text | `Technical manual for BEJSON matrix format...` |
| `{{TWITTER_TITLE}}` | Twitter card title | `Mastering Core BEJSON in TypeScript` |
| `{{TWITTER_DESCRIPTION}}`| Twitter card description | `Technical manual for BEJSON matrix format...` |
| `{{DATE_PUBLISHED}}` | ISO 8601 publication date | `2026-09-28` |
| `{{BOOK_GENRE}}` | Book classification / category | `Computer Science / Database Architecture` |
| `{{BOOK_TITLE}}` | Primary book title | `Mastering Core BEJSON in TypeScript` |
| `{{BOOK_SUBTITLE}}` | Thesis, scope, or explanatory goal | `Developer manual for low-level matrix parsing...` |
| `{{CHAPTER_COUNT}}` | Total count of chapters | `5` |
| `{{CURRENT_YEAR}}` | Four-digit copyright year | `2026` |
| `{{PUBLISHER_NAME}}` | Publishing entity or author organization | `BEJSON Core Press` |
| `{{PUBLISHER_URL}}` | Publisher website | `https://boehnenelton2024.pages.dev` |
| `{{JSON_LD_CHAPTERS}}`| Comma-separated Schema.org chapter nodes | `{"@type": "Chapter", "name": "...", "position": 1}` |
| `{{TABLE_OF_CONTENTS}}`| Rendered HTML `<li><a href="#chapter-N">...</a></li>` list | Dynamic list elements |
| `{{CHAPTERS_BODY}}` | Rendered `<article id="chapter-N">` elements | All compiled chapter bodies |

## JSON-LD Chapters Node Format

In `{{JSON_LD_CHAPTERS}}`, each chapter task maps to a Schema.org `Chapter` object:

```json
    {
      "@type": "Chapter",
      "position": 1,
      "name": "Chapter 1: Foundational Architecture",
      "url": "https://example.com/book.html#chapter-1"
    },
    {
      "@type": "Chapter",
      "position": 2,
      "name": "Chapter 2: Low-Level Operations",
      "url": "https://example.com/book.html#chapter-2"
    }
```

## HTML Chapter Article Structure

In `{{CHAPTERS_BODY}}`, each chapter renders as:

```html
<article id="chapter-1" role="article" aria-labelledby="chapter-1-title">
  <span class="chapter-badge">Chapter 1</span>
  <h2 id="chapter-1-title">Foundational Architecture</h2>
  <p>Chapter paragraph text...</p>
  <div class="bw-code-wrap" role="region" aria-label="Code example" tabindex="0">
    <pre><code class="language-python"># Code block</code></pre>
  </div>
</article>
```
