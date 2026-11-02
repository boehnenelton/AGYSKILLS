# Chunked-104a Schema Specification

> **Parent Skill:** `bejson-chunker-engine` (Layer 2)  
> **Release_Version:** 300 | **Format:** BEJSON 104a Specification  
> **Author:** Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Chunked-104a Root Structure

A chunked container file (`.104a.bejson.txt`) is a standard BEJSON 104a document structured as follows:

```json
{
  "Format": "BEJSON",
  "Format_Version": "104a",
  "Format_Creator": "Elton Boehnen",
  "Records_Type": ["ChunkedArchive"],
  "Archive_Name": "My_Project_Chunk",
  "Source_Path": "/path/to/source",
  "Created_At": "2026-11-02T00:00:00Z",
  "Total_Files": 12,
  "Fields": [
    {"name": "file_path", "type": "string"},
    {"name": "file_size_bytes", "type": "integer"},
    {"name": "file_sha256", "type": "string"},
    {"name": "is_binary", "type": "boolean"},
    {"name": "file_content", "type": "string"}
  ],
  "Values": [
    [
      "src/main.py",
      1024,
      "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      false,
      "print('Hello, world!')\n"
    ]
  ]
}
```

---

## 2. Invariants & Unpacking Rules

1. **Relative Path Integrity**: All entries in `file_path` are relative to the original source root. They must never begin with `/` or contain `../` path traversal sequences.
2. **Binary Encoding**: If `is_binary` is `true`, `file_content` contains standard base64 encoding. If `false`, it contains UTF-8 text.
3. **Restoration Verification**: Unchunking verifies the SHA-256 hash of each extracted file against `file_sha256` before completing extraction.
