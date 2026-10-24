# Site Template Architecture Plan: Tech_Chronicle_Blog

**Archetype**: Editorial Blog & Magazine (`blog`)
**Primary Entity Prefixes**: `blog_, post_, cat_, author_, comment_, tag_`
**Total Required Templates**: `7`

---

## Required Template Suite Specifications

| Template Key | Filename | Semantic Role | Bound Prefixes | Layers |
|---|---|---|---|---|
| `home_master_index` | `index.html` | Portal Landing Page & Latest Post Stream | `post_, cat_, author_` | `L1, L2, L4` |
| `post_single_view` | `post.html` | Single Article & Long-Form Reading View | `post_, author_, cat_, tag_` | `L1, L2, L4` |
| `content_page` | `page.html` | Static Standalone Content Page (About, Terms, Privacy) | `page_, author_` | `L1, L2, L4` |
| `category_tag_feed` | `feed.html` | Category & Tag Filtered Post Archive Feed | `cat_, post_, tag_` | `L1, L2, L4` |
| `author_profile` | `author.html` | Author Profile & Published Works Showcase | `author_, post_` | `L1, L2, L4` |
| `contact_inquiry` | `contact.html` | Contact & Reader Inquiry Interface | `inquiry_` | `L1, L2, L4` |
| `comments_discussion_feed` | `comments.html` | Threaded Discussion & Reader Feedback Component | `comment_, post_` | `L1, L2, L3` |

---

## Detailed Template Breakdown & Component Projections

### Template: `index.html` (`home_master_index`)
- **Role**: Portal Landing Page & Latest Post Stream
- **Bound Entity Taxonomies**: `post_, cat_, author_`
- **Active Stacking Depth**: Layer 1 (z: 32), Layer 2 (z: 64), Layer 4 (z: 128)
- **View Projections (Presentational)**:
  - Hero Featured Post
  - Category Filter Bar
  - Latest Posts 8-Lane Grid
  - Author Byline Badges
- **Interactive Form Controls**:
  - Newsletter Subscription Input
  - Quick Search Input

### Template: `post.html` (`post_single_view`)
- **Role**: Single Article & Long-Form Reading View
- **Bound Entity Taxonomies**: `post_, author_, cat_, tag_`
- **Active Stacking Depth**: Layer 1 (z: 32), Layer 2 (z: 64), Layer 4 (z: 128)
- **View Projections (Presentational)**:
  - Hero Header & Metadata Bar
  - Prose Body Container
  - Tags List
  - Sequential Next/Prev Navigation
- **Interactive Form Controls**:
  - Social Share Action Buttons

### Template: `page.html` (`content_page`)
- **Role**: Static Standalone Content Page (About, Terms, Privacy)
- **Bound Entity Taxonomies**: `page_, author_`
- **Active Stacking Depth**: Layer 1 (z: 32), Layer 2 (z: 64), Layer 4 (z: 128)
- **View Projections (Presentational)**:
  - Page Title Bar
  - Document Prose Body
  - Structured Spec Table

### Template: `feed.html` (`category_tag_feed`)
- **Role**: Category & Tag Filtered Post Archive Feed
- **Bound Entity Taxonomies**: `cat_, post_, tag_`
- **Active Stacking Depth**: Layer 1 (z: 32), Layer 2 (z: 64), Layer 4 (z: 128)
- **View Projections (Presentational)**:
  - Hierarchical Breadcrumb Bar
  - Active Category Banner
  - Sorted Post Stream
  - Paging Controls
- **Interactive Form Controls**:
  - Sort Order Dropdown

### Template: `author.html` (`author_profile`)
- **Role**: Author Profile & Published Works Showcase
- **Bound Entity Taxonomies**: `author_, post_`
- **Active Stacking Depth**: Layer 1 (z: 32), Layer 2 (z: 64), Layer 4 (z: 128)
- **View Projections (Presentational)**:
  - Author Bio Card & Avatar
  - Published Articles Metric Readout
  - Author Post Archive List

### Template: `contact.html` (`contact_inquiry`)
- **Role**: Contact & Reader Inquiry Interface
- **Bound Entity Taxonomies**: `inquiry_`
- **Active Stacking Depth**: Layer 1 (z: 32), Layer 2 (z: 64), Layer 4 (z: 128)
- **View Projections (Presentational)**:
  - Contact Info Details
  - Response Time Telemetry Badge
- **Interactive Form Controls**:
  - Inquiry Form (Name, Email, Subject Select, Message Textarea, Submit Action)

### Template: `comments.html` (`comments_discussion_feed`)
- **Role**: Threaded Discussion & Reader Feedback Component
- **Bound Entity Taxonomies**: `comment_, post_`
- **Active Stacking Depth**: Layer 1 (z: 32), Layer 2 (z: 64), Layer 3 (z: 96)
- **View Projections (Presentational)**:
  - Comment Count Readout
  - Threaded Reply Tree List
- **Interactive Form Controls**:
  - Comment Submission Input Group
  - Reply Form Dialog Overlay (Layer 3)

---

Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton