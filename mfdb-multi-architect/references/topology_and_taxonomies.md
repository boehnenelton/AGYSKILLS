# Multi-MFDB Topology & Taxonomy Reference Guide

> **Parent Skill:** `mfdb-multi-architect` (Layer 5)  
> **Release_Version:** 300 | **Format:** Markdown Specifications  
> **Author:** Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Topological Archetypes in Detail

### 1.1 Topology A: Centralized Single-Site Master
- **Structure**:
  ```text
  storage/mfdb/
  ├── 104a.mfdb.bejson          # Root Manifest (Master)
  └── data/
      ├── pages.104.bejson      # Content entity (Slave)
      ├── authors.104.bejson    # Author profiles (Slave)
      ├── assets.104.bejson     # Media asset records (Slave)
      └── categories.104.bejson # Taxonomy terms (Slave)
  ```
- **Operational Model**: A single unified database handle (`CMSCore` or `MFDBCore`).
- **Locking Scope**: Acquires an advisory PID lock (`.mfdb.lock`) on the root directory during mutations.
- **When to Choose**: Applications where 90% of queries cross-reference multiple entities (e.g. blog post + author + category + featured image) or where total database size is `< 100 MB`.

---

### 1.2 Topology B: Federated Multi-Domain Cluster
- **Structure**:
  ```text
  storage/
  ├── master/
  │   └── 104a.mfdb.bejson      # Cluster Master Manifest
  └── domains/
      ├── auth/
      │   ├── 104a.mfdb.bejson  # Auth Domain Manifest (Proxy / Sub-Master)
      │   └── data/
      │       ├── users.104.bejson
      │       └── roles.104.bejson
      ├── content/
      │   ├── 104a.mfdb.bejson  # Content Domain Manifest
      │   └── data/
      │       ├── posts.104.bejson
      │       └── comments.104.bejson
      └── telemetry/
          ├── 104a.mfdb.bejson  # Telemetry Domain Manifest
          └── data/
              └── events.104.bejson
  ```
- **Operational Model**: Microservices or modular blueprints interact exclusively with their domain manifest.
- **Locking Scope**: Mutating `posts.104.bejson` locks only `domains/content/.mfdb.lock`. The auth and telemetry domains continue reading and writing without blocking.
- **When to Choose**: High-throughput multi-agent systems, multi-user web backends, or applications with distinct lifecycle frequencies (e.g. telemetry events write every second, while content updates daily).

---

### 1.3 Topology C: Hierarchical Proxy Mesh
- **Structure**:
  ```text
  edge_cluster/
  ├── root.104a.mfdb.bejson     # Master Cluster Manifest
  └── nodes/
      ├── node_01/
      │   ├── proxy.104a.mfdb.bejson
      │   └── data/sensors.104.bejson
      └── node_02/
          ├── proxy.104a.mfdb.bejson
          └── data/sensors.104.bejson
  ```
- **Operational Model**: Edge nodes write to local proxy manifests offline. Synchronization daemons aggregate sensor summaries up to the root manifest when network connectivity is established.

---

## 2. Canonical Domain Prefix Registries

Every entity MUST declare a 3-6 character snake_case prefix. All columns in that entity must begin with this prefix.

### 2.1 Standard Domain Registries
```text
Domain              Entity Name          Prefix      Canonical Columns
---------------------------------------------------------------------------------------------------
Content Management  ContentPage          page_       page_uuid, page_title, page_slug, page_content
Content Management  AuthorProfile        author_     author_uuid, author_name, author_email_hash
Content Management  CategoryTerm         cat_        cat_uuid, cat_name, cat_slug, cat_parent_uuid_fk
Asset Pipeline      MediaAsset           asset_      asset_uuid, asset_filename, asset_sha256, asset_size
Asset Pipeline      ExternalEmbed        embed_      embed_uuid, embed_service, embed_external_id
User Management     UserAccount          usr_        usr_uuid, usr_username, usr_role, usr_created_at
User Management     SessionAuth          sess_       sess_uuid, sess_usr_uuid_fk, sess_expires_at
System Automation   TaskItem             task_       task_uuid, task_title, task_status, task_priority
System Automation   CronSchedule         cron_       cron_uuid, cron_expression, cron_last_run
AI Agent Swarm      AgentProfile         agent_      agent_uuid, agent_role, agent_model, agent_status
AI Agent Swarm      EpisodicMemory       mem_        mem_uuid, mem_agent_uuid_fk, mem_summary, mem_timestamp
AI Agent Swarm      ToolTelemetry        telem_      telem_uuid, telem_tool_name, telem_duration_ms
Audit & Security    SecurityEvent        sec_        sec_uuid, sec_event_type, sec_ip_hash, sec_timestamp
Audit & Security    RowSignature         sig_        sig_uuid, sig_target_table, sig_row_sha256
```

---

## 3. Two-Tier Content Architecture

To maintain high query performance and prevent database bloat, Multi-MFDB enforces **Two-Tier Storage**:
- **Tier 1 (MFDB Metadata Record)**: Tabular row storing structured metadata (title, author, timestamp, tags, word count, file size, content file relative pointer).
- **Tier 2 (Decoupled Blob / Content File)**: Large text payloads (Markdown articles, HTML bodies, source code files, binary assets) are stored as standalone files on disk:
  ```text
  storage/
  ├── mfdb/data/pages.104.bejson   # Tier 1: Metadata row with 'page_content_file' pointer
  └── content/pages/               # Tier 2: Standalone Markdown / HTML files
      ├── post_alpha.md
      └── post_beta.md
  ```
- **Integrity Rule**: Tier 1 records must store the SHA-256 hash of their associated Tier 2 file (`page_content_sha256`) to guarantee tamper evidence.

---

## 4. Foreign Key Cascade Behaviors

In Multi-MFDB schemas, relationships specify explicit `fk_on_delete` behaviors:
- **`cascade`**: Deleting the parent record automatically unlinks or deletes all dependent child rows.
- **`null`**: Deleting the parent sets the child foreign key column to `null`.
- **`restrict`**: Deleting the parent is blocked if any dependent child rows exist.
- **`default`**: Deleting the parent sets the child foreign key column to a designated fallback UUID.
