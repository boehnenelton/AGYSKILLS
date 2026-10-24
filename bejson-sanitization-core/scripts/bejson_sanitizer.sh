#!/data/data/com.termux/files/usr/bin/bash
# ==============================================================================
# Script Name: bejson_sanitizer.sh
# Description: Layer 1 Bash/jq boundary-layer sanitization primitives per Policy §10.9.
# Version: 1.0.0
# Author: Elton Boehnen · boehnenelton2024@gmail.com
# ==============================================================================

set -u

# Function: bejson_sanitize_payload_string
# Usage: sanitized_json=$(echo "$raw_json" | bejson_sanitize_payload_string)
bejson_sanitize_payload_string() {
    jq '
        # Strip string values
        def strip_str:
            if type == "string" then sub("^\\s+"; "") | sub("\\s+$"; "")
            else . end;

        # Recursively strip dictionary keys
        def strip_keys:
            if type == "object" then
                to_entries | map({
                    key: (.key | strip_str),
                    value: (.value | if type == "object" then strip_keys elif type == "array" then . else strip_str end)
                }) | from_entries
            else . end;

        strip_keys
        | if has("Fields") and (.Fields | type == "array") then
            .Fields = [
                .Fields[] | if type == "object" then
                    to_entries | map({key: (.key | strip_str), value: (.value | strip_str)}) | from_entries
                else . end
            ]
          else . end
        | if has("Values") and (.Values | type == "array") then
            .Values = [
                .Values[] | if type == "array" then
                    map(strip_str)
                else . end
            ]
          else . end
    '
}

# Function: bejson_sanitize_file_inplace
# Usage: bejson_sanitize_file_inplace "/path/to/file.bejson"
bejson_sanitize_file_inplace() {
    local target_file="$1"
    if [[ ! -f "$target_file" ]]; then
        echo "Error: file not found: $target_file" >&2
        return 1
    fi
    local tmp_file="${target_file}.tmp.$$"
    bejson_sanitize_payload_string < "$target_file" > "$tmp_file"
    mv -f "$tmp_file" "$target_file"
}

# If executed directly with file argument
if [[ "${1:-}" != "" ]] && [[ -f "$1" ]]; then
    bejson_sanitize_file_inplace "$1"
    echo "Sanitized: $1"
fi
