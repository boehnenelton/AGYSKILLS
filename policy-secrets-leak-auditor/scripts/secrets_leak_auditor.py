#!/usr/bin/env python3
"""
File:          secrets_leak_auditor.py
Description:   Layer 2 Policy Section 4.5 Zero-Leakage Credential & Secrets Auditor.
               Scans codebases, configuration files, BEJSON caches, and session logs
               for unmasked API keys, raw tokens, and private keys. Enforces pointer-only
               persistence (ENV:<var_name>) before release packaging or git commits.
Version:       1.0.0
Date Created:  2026-10-25
Author:        Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID: 8b7c6d5e-4f3a-2b1c-0d9e-8f7a6b5c4d3e
"""

import argparse
import json
import logging
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

if sys.version_info < (3, 10):
    sys.stderr.write("secrets_leak_auditor requires Python 3.10 or newer.\n")
    sys.exit(1)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [secrets_auditor]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger("secrets_leak_auditor")

SECRET_PATTERNS = [
    ("Google Gemini Key", re.compile(r"\bAIzaSy[A-Za-z0-9_-]{33}\b")),
    ("Groq API Key", re.compile(r"\bgsk_[A-Za-z0-9]{48,64}\b")),
    ("OpenRouter API Key", re.compile(r"\bsk-or-v1-[a-f0-9]{64}\b")),
    ("OpenAI API Key", re.compile(r"\bsk-[A-Za-z0-9]{48}\b")),
    ("GitHub Classic Token", re.compile(r"\bghp_[A-Za-z0-9]{36}\b")),
    ("GitHub Fine-Grained Token", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{82}\b")),
    ("Private Key Header", re.compile(r"-----BEGIN (?:RSA|EC|OPENSSH) PRIVATE KEY-----")),
    ("AWS Access Key", re.compile(r"\bAKIA[0-9A-Z]{16}\b"))
]

IGNORED_DIRS = {
    ".git", "__pycache__", ".pytest_cache", "venv", ".venv", "node_modules", ".env"
}


def mask_secret(secret_str: str) -> str:
    """Masks secret to prevent sensitive disclosure in audit logs."""
    if len(secret_str) <= 8:
        return "****"
    return f"{secret_str[:4]}...{secret_str[-4:]}"


def scan_file(filepath: Path) -> List[Dict[str, Any]]:
    """Scans a single file for exposed secrets and non-compliant pointer entries."""
    findings = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:
        logger.warning(f"Could not read {filepath}: {exc}")
        return findings

    lines = content.splitlines()

    # 1. Regex scanning
    for line_idx, line in enumerate(lines, start=1):
        for provider_name, pattern in SECRET_PATTERNS:
            matches = pattern.findall(line)
            for m in matches:
                # Exclude obvious template placeholders
                if "PLACEHOLDER" in m or "YOUR_KEY" in m:
                    continue
                findings.append({
                    "file": str(filepath),
                    "line": line_idx,
                    "provider": provider_name,
                    "masked_value": mask_secret(m),
                    "severity": "CRITICAL",
                    "reason": "Exposed plaintext API secret in source or config"
                })

    # 2. Check BEJSON key cache pointer compliance
    if filepath.name.startswith("keys") and filepath.suffix == ".bejson":
        try:
            doc = json.loads(content)
            fields = doc.get("Fields", [])
            fnames = [f.get("name") for f in fields if isinstance(f, dict)]
            val_idx = fnames.index("key_value") if "key_value" in fnames else (fnames.index("var_value") if "var_value" in fnames else -1)

            if val_idx != -1:
                for row_idx, row in enumerate(doc.get("Values", []), start=1):
                    if isinstance(row, list) and len(row) > val_idx:
                        val = row[val_idx]
                        if isinstance(val, str) and val and not val.startswith("ENV:"):
                            findings.append({
                                "file": str(filepath),
                                "line": row_idx,
                                "provider": "BEJSON Key Cache",
                                "masked_value": mask_secret(val),
                                "severity": "HIGH",
                                "reason": f"Cache row {row_idx} must store 'ENV:<var_name>' pointer, not raw value"
                            })
        except Exception:
            pass

    return findings


def scan_directory(target_dir: Path) -> Tuple[List[Dict[str, Any]], int]:
    """Recursively scans repository files for credentials."""
    all_findings = []
    scanned_count = 0

    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for f in sorted(files):
            # Skip binary extensions
            if f.endswith((".png", ".jpg", ".jpeg", ".zip", ".tar", ".gz", ".pyc", ".pdf", ".mp4", ".m4a")):
                continue
            fpath = Path(root) / f
            scanned_count += 1
            findings = scan_file(fpath)
            all_findings.extend(findings)

    return all_findings, scanned_count


def update_audit_manifest(
    manifest_path: Path,
    record: Dict[str, Any]
) -> None:
    """Updates the audit tracking manifest."""
    manifest_data: Dict[str, Any] = {"Values": []}
    if manifest_path.exists():
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest_data = json.load(f)
        except Exception:
            manifest_data = {"Values": []}

    fields = manifest_data.get("Fields", [
        {"name": "audit_id", "type": "string"},
        {"name": "target_directory", "type": "string"},
        {"name": "scanned_files_count", "type": "integer"},
        {"name": "leaks_detected_count", "type": "integer"},
        {"name": "pointer_compliance_pct", "type": "number"},
        {"name": "audit_verdict", "type": "string"},
        {"name": "report_path", "type": "string"},
        {"name": "audit_timestamp", "type": "string"}
    ])
    manifest_data["Fields"] = fields

    field_map = {f["name"]: idx for idx, f in enumerate(fields)}
    row = [None] * len(fields)
    for k, v in record.items():
        if k in field_map:
            row[field_map[k]] = v

    manifest_data.setdefault("Values", []).append(row)
    manifest_data["Format"] = "BEJSON"
    manifest_data["Format_Version"] = "104a"
    manifest_data["Format_Creator"] = "Elton Boehnen"
    manifest_data["Records_Type"] = ["SecretsAuditRecord"]

    tmp_path = manifest_path.parent / f"{manifest_path.name}.tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2)
    os.replace(tmp_path, manifest_path)
    logger.info(f"Updated secrets audit manifest: {manifest_path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Policy Section 4.5 Zero-Leakage Secrets & Credential Auditor"
    )
    parser.add_argument("target", type=Path, help="Directory or file to scan for credential leaks")
    parser.add_argument("--output-report", type=Path, default=None, help="Save structured audit findings to file")
    parser.add_argument("--manifest", type=Path, default=None, help="Optional BEJSON 104a audit registry path")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not args.target.exists():
        logger.error(f"Target path does not exist: {args.target}")
        sys.exit(1)

    logger.info(f"Initiating credential leakage scan on: {args.target}")
    if args.target.is_file():
        findings = scan_file(args.target)
        scanned_count = 1
    else:
        findings, scanned_count = scan_directory(args.target)

    logger.info(f"Scan finished: {scanned_count} files inspected. {len(findings)} findings.")

    if findings:
        logger.error(f"FAIL: Discovered {len(findings)} potential secret leakage(s):")
        for idx, fd in enumerate(findings, start=1):
            logger.error(f"  [{idx}] {fd['file']}:{fd['line']} | {fd['provider']} | {fd['masked_value']} ({fd['reason']})")
    else:
        logger.info("PASS: Zero secret leakages discovered. All caches comply with Policy Section 4.5.")

    verdict = "FAIL" if findings else "CLEAN"
    compliance_pct = 100.0 if not findings else round(max(0.0, 100.0 - (len(findings) * 5.0)), 1)

    if args.output_report:
        args.output_report.parent.mkdir(parents=True, exist_ok=True)
        report_data = {
            "verdict": verdict,
            "target": str(args.target),
            "files_scanned": scanned_count,
            "findings_count": len(findings),
            "findings": findings,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        with open(args.output_report, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2)
        logger.info(f"Saved audit report: {args.output_report}")

    if args.manifest:
        update_audit_manifest(
            manifest_path=args.manifest,
            record={
                "audit_id": f"aud_{int(datetime.now(timezone.utc).timestamp())}",
                "target_directory": str(args.target),
                "scanned_files_count": scanned_count,
                "leaks_detected_count": len(findings),
                "pointer_compliance_pct": compliance_pct,
                "audit_verdict": verdict,
                "report_path": str(args.output_report) if args.output_report else "console_only",
                "audit_timestamp": datetime.now(timezone.utc).isoformat()
            }
        )

    sys.exit(1 if findings else 0)


if __name__ == "__main__":
    main()
