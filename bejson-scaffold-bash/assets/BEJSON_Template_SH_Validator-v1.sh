#!/usr/bin/env bash
# Name:           BEJSON_Template_SH_Validator
# Description:    Basic bash template with the BEJSON Core error registry and BEJSON Core validator embedded, not auto-invoked.
#                 Nothing below is invoked automatically -- every function
#                 is defined and exported so it can be called once this
#                 file is sourced or its main() block is extended.
# Version:        1 (Package_Version 100)
# Date Created:   2026-09-09
# Author:         Elton Boehnen
# Contact:        boehnenelton2024@gmail.com | boehnenelton2024.pages.dev | github.com/boehnenelton
# Format_Creator: Elton Boehnen
# RELATIONAL_ID:  c94e3a71-2b6d-4f80-9e15-7a3c6f1d0b52
# Release_Version: 300

set -euo pipefail
BEJSON_TEMPLATE_VERSION="1"

# Self-locating script path (Policy 4.2)
get_script_path() {
    local source="${BASH_SOURCE[0]}"
    while [ -h "$source" ]; do
        local dir="$( cd -P "$( dirname "$source" )" >/dev/null 2>&1 && pwd )"
        source="$(readlink "$source")"
        [[ $source != /* ]] && source="$dir/$source"
    done
    echo "$( cd -P "$( dirname "$source" )" >/dev/null 2>&1 && pwd )"
}
SCRIPT_PATH=$(get_script_path)

# ==== SECTION: ERROR REGISTRY (embedded) ====
# ==========================================================================
# SECTION 1 — ERROR REGISTRY
# Sources: bejson_errors v1.5.0
# ==========================================================================

# Library:        lib_bejson_Core_bejson_errors.sh
# Family:         Core
# Description:    Centralized error code registry for all Bash BEJSON libraries. Mirrors lib_bejson_Core_bejson_errors.js and lib_bejson_Core_bejson_errors.py.
# Version:        1.5.0
# Date:           2026-07-30
# Author:         Elton Boehnen
# Contact:        boehnenelton2024@gmail.com | boehnenelton2024.pages.dev | github.com/boehnenelton
# Format_Creator: Elton Boehnen
# RELATIONAL_ID:  2d9c4b71-5a3e-4f8d-b1c6-7e0a2f8d3c95
#
# Changelog:
#   1.5.0 - LEGACY ALIASES section deleted (Step 2 — 1.32 finalization).
#           E_VAL_NOT_JSON, E_VAL_MISSING_KEY, E_VAL_BAD_FORMAT,
#           E_VAL_BAD_VERSION, E_VAL_BAD_CREATOR, E_VAL_SCHEMA_MISMATCH,
#           E_VAL_INVALID_TYPE removed. lib_bejson_Core_bejson_validator.sh
#           updated to use primary unified codes at all return sites.
#   1.4.0 - Removed Core_Nesting range (130-159) — that family now owns its
#           codes in lib_bejson_CoreNesting_bejson_errors.sh. MFDB codes
#           (30-49, 50-79) remain here: MFDB is implemented as part of the
#           Core family, not a separate family directory.

# ===========================================================================
# BEJSON VALIDATOR ERRORS (1–19)  — mirrors E_* in lib_bejson_Core_bejson_errors.js / .py
# ===========================================================================
[[ -v E_INVALID_JSON                ]] || readonly E_INVALID_JSON=1
[[ -v E_MISSING_MANDATORY_KEY       ]] || readonly E_MISSING_MANDATORY_KEY=2
[[ -v E_INVALID_FORMAT              ]] || readonly E_INVALID_FORMAT=3
[[ -v E_INVALID_VERSION             ]] || readonly E_INVALID_VERSION=4
[[ -v E_INVALID_RECORDS_TYPE        ]] || readonly E_INVALID_RECORDS_TYPE=5
[[ -v E_INVALID_FIELDS              ]] || readonly E_INVALID_FIELDS=6
[[ -v E_INVALID_VALUES              ]] || readonly E_INVALID_VALUES=7
[[ -v E_TYPE_MISMATCH               ]] || readonly E_TYPE_MISMATCH=8
[[ -v E_RECORD_LENGTH_MISMATCH      ]] || readonly E_RECORD_LENGTH_MISMATCH=9
[[ -v E_RESERVED_KEY_COLLISION      ]] || readonly E_RESERVED_KEY_COLLISION=10
[[ -v E_INVALID_RECORD_TYPE_PARENT  ]] || readonly E_INVALID_RECORD_TYPE_PARENT=11
[[ -v E_NULL_VIOLATION              ]] || readonly E_NULL_VIOLATION=12
[[ -v E_FILE_NOT_FOUND              ]] || readonly E_FILE_NOT_FOUND=13
[[ -v E_PERMISSION_DENIED           ]] || readonly E_PERMISSION_DENIED=14
[[ -v E_ATOMIC_WRITE_FAILED         ]] || readonly E_ATOMIC_WRITE_FAILED=15
[[ -v E_INVALID_FORMAT_CREATOR      ]] || readonly E_INVALID_FORMAT_CREATOR=16

# ===========================================================================
# BEJSON CORE ERRORS (20–29)
# ===========================================================================
[[ -v E_CORE_INVALID_VERSION        ]] || readonly E_CORE_INVALID_VERSION=20
[[ -v E_CORE_INVALID_OPERATION      ]] || readonly E_CORE_INVALID_OPERATION=21
[[ -v E_CORE_INDEX_OUT_OF_BOUNDS    ]] || readonly E_CORE_INDEX_OUT_OF_BOUNDS=22
[[ -v E_CORE_FIELD_NOT_FOUND        ]] || readonly E_CORE_FIELD_NOT_FOUND=23
[[ -v E_CORE_TYPE_CONVERSION_FAILED ]] || readonly E_CORE_TYPE_CONVERSION_FAILED=24
[[ -v E_CORE_BACKUP_FAILED          ]] || readonly E_CORE_BACKUP_FAILED=25
[[ -v E_CORE_WRITE_FAILED           ]] || readonly E_CORE_WRITE_FAILED=26
[[ -v E_CORE_QUERY_FAILED           ]] || readonly E_CORE_QUERY_FAILED=27
[[ -v E_CORE_ENCRYPTION_FAILED      ]] || readonly E_CORE_ENCRYPTION_FAILED=28
[[ -v E_CORE_DECRYPTION_FAILED      ]] || readonly E_CORE_DECRYPTION_FAILED=29

# ===========================================================================
# MFDB VALIDATOR ERRORS (30–49)
# ===========================================================================
[[ -v E_MFDB_NOT_MANIFEST           ]] || readonly E_MFDB_NOT_MANIFEST=30
[[ -v E_MFDB_NOT_ENTITY_FILE        ]] || readonly E_MFDB_NOT_ENTITY_FILE=31
[[ -v E_MFDB_MANIFEST_RECORDS_TYPE  ]] || readonly E_MFDB_MANIFEST_RECORDS_TYPE=32
[[ -v E_MFDB_ENTITY_NOT_FOUND       ]] || readonly E_MFDB_ENTITY_NOT_FOUND=33
[[ -v E_MFDB_ENTITY_NAME_MISMATCH   ]] || readonly E_MFDB_ENTITY_NAME_MISMATCH=34
[[ -v E_MFDB_DUPLICATE_ENTRY        ]] || readonly E_MFDB_DUPLICATE_ENTRY=35
[[ -v E_MFDB_NO_PARENT_HIERARCHY    ]] || readonly E_MFDB_NO_PARENT_HIERARCHY=36
[[ -v E_MFDB_MANIFEST_NOT_FOUND     ]] || readonly E_MFDB_MANIFEST_NOT_FOUND=37
[[ -v E_MFDB_BIDIRECTIONAL_FAIL     ]] || readonly E_MFDB_BIDIRECTIONAL_FAIL=38
[[ -v E_MFDB_FK_UNRESOLVED          ]] || readonly E_MFDB_FK_UNRESOLVED=39
[[ -v E_MFDB_MISSING_REQUIRED_FIELD ]] || readonly E_MFDB_MISSING_REQUIRED_FIELD=40
[[ -v E_MFDB_NULL_REQUIRED          ]] || readonly E_MFDB_NULL_REQUIRED=41
[[ -v E_MFDB_INVALID_ARCHIVE        ]] || readonly E_MFDB_INVALID_ARCHIVE=42

# ===========================================================================
# MFDB CORE ERRORS (50–79)
# ===========================================================================
# MFDB Core error codes — aligned with canonical PY/TS registry
# NOTE (H-02, 2026-08-19): codes 57-60 below are NOT present in the real
# Lib_SH/Core/lib_bejson_Core_bejson_errors.sh (v1.5.0) source. Backfilled
# here for compiled-artifact parity only. The upstream Lib_SH errors file
# still needs this same backfill — flagging, not silently fixing it there.
[[ -v E_MFDB_CORE_MANIFEST_NOT_FOUND ]] || readonly E_MFDB_CORE_MANIFEST_NOT_FOUND=50
[[ -v E_MFDB_CORE_ENTITY_NOT_FOUND  ]] || readonly E_MFDB_CORE_ENTITY_NOT_FOUND=51
[[ -v E_MFDB_CORE_WRITE_FAILED      ]] || readonly E_MFDB_CORE_WRITE_FAILED=52
[[ -v E_MFDB_CORE_LOCK_FAILED       ]] || readonly E_MFDB_CORE_LOCK_FAILED=53
[[ -v E_MFDB_CORE_INVALID_OPERATION ]] || readonly E_MFDB_CORE_INVALID_OPERATION=54
[[ -v E_MFDB_CORE_INDEX_OUT_OF_BOUNDS ]] || readonly E_MFDB_CORE_INDEX_OUT_OF_BOUNDS=55
[[ -v E_MFDB_CORE_JOIN_FAILED       ]] || readonly E_MFDB_CORE_JOIN_FAILED=56
[[ -v E_MFDB_CORE_DUPLICATE_ENTITY_NAME ]] || readonly E_MFDB_CORE_DUPLICATE_ENTITY_NAME=57
[[ -v E_MFDB_CORE_RECORD_COUNT_SYNC_FAILED ]] || readonly E_MFDB_CORE_RECORD_COUNT_SYNC_FAILED=58
[[ -v E_MFDB_CORE_NULL_MANIFEST     ]] || readonly E_MFDB_CORE_NULL_MANIFEST=59
[[ -v E_MFDB_CORE_ENTITY_NOT_IN_MANIFEST ]] || readonly E_MFDB_CORE_ENTITY_NOT_IN_MANIFEST=60
[[ -v E_MFDB_CORE_ARCHIVE_ERROR     ]] || readonly E_MFDB_CORE_ARCHIVE_ERROR=70
[[ -v E_MFDB_CORE_MOUNT_CONFLICT    ]] || readonly E_MFDB_CORE_MOUNT_CONFLICT=71
[[ -v E_MFDB_CORE_CREATE_FAILED     ]] || readonly E_MFDB_CORE_CREATE_FAILED=72


# Core_Nesting codes moved to lib_bejson_CoreNesting_bejson_errors.sh (v1.4.0)



# ==== SECTION: BEJSON VALIDATOR (embedded) ====
# ==========================================================================
# SECTION 3 — BEJSON VALIDATOR
# Sources: bejson_validator v2.1.0
# ==========================================================================

# Library:        lib_bejson_Core_bejson_validator.sh
# Family:         Core
# Description:    Structural integrity checker for positional values and mandatory keys.
# Version:        2.1.0
# Date:           2026-07-30
# Author:         Elton Boehnen
# Contact:        boehnenelton2024@gmail.com | boehnenelton2024.pages.dev | github.com/boehnenelton
# Format_Creator: Elton Boehnen
# RELATIONAL_ID:  5f8a3c71-9d2e-4b6f-a0c4-1e7b5d9f2a83
#
# Changelog:
#   2.1.0 - Step 2 (1.32 finalization): removed local re-declarations of legacy
#           E_VAL_* aliases and migrated all 5 return sites to primary unified
#           codes (E_INVALID_JSON, E_MISSING_MANDATORY_KEY, E_INVALID_FORMAT,
#           E_INVALID_FORMAT_CREATOR, E_RECORD_LENGTH_MISMATCH). Aliases no
#           longer exist in lib_bejson_Core_bejson_errors.sh.

set -o pipefail

# Source the error registry (assumes same directory)
_VAL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

#-------------------------------------------------------------------------------
# CORE VALIDATION
#-------------------------------------------------------------------------------

bejson_validator_check_dependencies() {
    if ! command -v jq >/dev/null 2>&1; then
        echo "ERROR: jq is required for BEJSON validation" >&2
        return 1
    fi
    local jq_ver
    jq_ver=$(jq --version | sed 's/jq-//')
    local jq_major jq_minor
    jq_major="${jq_ver%%.*}"
    jq_minor="${jq_ver#*.}"; jq_minor="${jq_minor%%.*}"
    if [[ "$jq_major" -lt 1 ]] || { [[ "$jq_major" -eq 1 ]] && [[ "$jq_minor" -lt 6 ]]; }; then
        echo "ERROR: jq >= 1.6 is required. Found: $jq_ver" >&2
        return 1
    fi
    return 0
}

bejson_validator_validate_file() {
    local file_path="$1"
    if [[ ! -f "$file_path" ]]; then
        echo "ERROR: File not found: $file_path" >&2
        return 1
    fi

    # 1. Basic JSON check
    if ! jq . "$file_path" >/dev/null 2>&1; then
        return $E_INVALID_JSON
    fi

    # 2. Mandatory Keys — exact presence check via jq (FIX SH1)
    #    Using =~ on a joined key string caused substring collisions:
    #    "Format" matched inside "Format_Creator", making missing bare "Format" go undetected.
    for k in Format Format_Version Format_Creator Records_Type Fields Values; do
        if ! jq -e --arg key "$k" 'has($key)' "$file_path" >/dev/null 2>&1; then
            return $E_MISSING_MANDATORY_KEY
        fi
    done

    # 3. Format & Creator check
    local fmt creator
    fmt=$(jq -r '.Format' "$file_path")
    creator=$(jq -r '.Format_Creator' "$file_path")
    [[ "$fmt"     != "BEJSON"        ]] && return $E_INVALID_FORMAT
    [[ "$creator" != "Elton Boehnen" ]] && return $E_INVALID_FORMAT_CREATOR

    # 4. Records Length check
    local field_count bad_records
    field_count=$(jq '.Fields | length' "$file_path")
    bad_records=$(jq --argjson fc "$field_count" '.Values | map(select(length != $fc)) | length' "$file_path")
    if [[ "$bad_records" -gt 0 ]]; then
        return $E_RECORD_LENGTH_MISMATCH
    fi

    return 0
}

# Export functions for subshell use
export -f bejson_validator_check_dependencies
export -f bejson_validator_validate_file



# ---------------------------------------------------------------------------
# About / Info
# ---------------------------------------------------------------------------
bejson_template_about() {
    cat <<EOF
BEJSON_Template_SH_Validator v${BEJSON_TEMPLATE_VERSION} (Release_Version 300)
Embedded: BEJSON Core error registry + BEJSON Core validator
Author: Elton Boehnen | boehnenelton2024@gmail.com | boehnenelton2024.pages.dev | github.com/boehnenelton
EOF
}
export -f bejson_template_about

# Template only -- does not call any validator/core function against real
# data. Source this file ('source BEJSON_Template_SH_Validator.sh') then call e.g.
# bejson_validator_validate_file "path/to/doc.bejson" from your own script.
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    bejson_template_about
fi
