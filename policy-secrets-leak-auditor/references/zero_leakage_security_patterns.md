# Zero-Leakage Credential Security & Sourcing Patterns (Policy Section 4.5)

## 1. The Pointer-Only Persistence Rule

Under Policy Section 4.5 and the NewAgent v3.45+ security model:
- **Forbidden**: Storing raw API secret values (e.g., `AIzaSy...`, `gsk_...`, `sk-or-v1-...`) inside disk configuration files (`config.json`, `keys.bejson`, `keys_openrouter.bejson`).
- **Mandated**: Storing abstract environment pointers formatted strictly as `ENV:<var_name>`:
  - `["key_ref", "ENV:GEMINI_KEY_1", "Gemini primary active key"]`
  - `["key_ref", "ENV:OPENROUTER_KEY_1", "OpenRouter fallback key"]`
- **Resolution**: Secret values are resolved at runtime directly from `/storage/emulated/0/.env/secure/secureenv_file.json` into volatile memory and are never persisted back to disk.

## 2. Leakage Scanning Signatures

The scanner hunts for known provider key patterns:
- **Google Gemini**: `AIzaSy[A-Za-z0-9_-]{33}`
- **Groq API**: `gsk_[A-Za-z0-9]{48,64}`
- **OpenRouter**: `sk-or-v1-[a-f0-9]{64}`
- **OpenAI**: `sk-[A-Za-z0-9]{48}`
- **GitHub Token**: `ghp_[A-Za-z0-9]{36}` or `github_pat_[A-Za-z0-9_]{82}`
- **Generic Private Keys**: `-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY-----`
- **AWS Secrets**: `AKIA[0-9A-Z]{16}`

## 3. Pre-Delivery Stage Gate (Layer 2)

Prior to running `project-delivery-packager` or committing release packages:
1. Scan all tracked files in the repository.
2. Verify all `keys*.bejson` caches contain `ENV:*` values only.
3. Assert zero raw credential matches in `logs/`, `session_*.bejson`, and `backups/`.
4. Fail with exit code `1` if any unmasked secret is discovered.
