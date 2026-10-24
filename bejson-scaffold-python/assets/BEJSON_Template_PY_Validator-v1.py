#!/usr/bin/env python3
"""
Name:           BEJSON_Template_PY_Validator
Description:    Basic executable template with the BEJSON Core error
                 registry and the BEJSON Core validator embedded inline.
                 Nothing in this file is called automatically -- every
                 function/class below is defined and ready to be
                 imported or invoked by other code that loads this file.
Version:        (see VERSION below)
Date Created:   2026-09-09
Author:         Elton Boehnen
Contact:        boehnenelton2024@gmail.com | boehnenelton2024.pages.dev | github.com/boehnenelton
Format_Creator: Elton Boehnen
RELATIONAL_ID:  d3f1a9e6-4c22-4b0a-8e77-2a6f9b1d5c40
Release_Version: 300
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Union

VERSION = 1

# ---------------------------------------------------------------------------
# Error registry (BEJSON validation codes 1-16)
# Embedded directly -- no external lib_bejson_Core_bejson_errors import.
# ---------------------------------------------------------------------------
E_INVALID_JSON               = 1
E_MISSING_MANDATORY_KEY      = 2
E_INVALID_FORMAT             = 3
E_INVALID_VERSION            = 4
E_INVALID_RECORDS_TYPE       = 5
E_INVALID_FIELDS             = 6
E_INVALID_VALUES             = 7
E_TYPE_MISMATCH              = 8
E_RECORD_LENGTH_MISMATCH     = 9
E_RESERVED_KEY_COLLISION     = 10
E_INVALID_RECORD_TYPE_PARENT = 11
E_NULL_VIOLATION             = 12
E_FILE_NOT_FOUND             = 13
E_PERMISSION_DENIED          = 14
E_ATOMIC_WRITE_FAILED        = 15
E_INVALID_FORMAT_CREATOR     = 16

VALID_VERSIONS = {"104", "104a", "104db"}
VALID_FIELD_TYPES = {"string", "integer", "number", "boolean", "array", "object"}
MANDATORY_KEYS = ("Format", "Format_Version", "Format_Creator", "Records_Type", "Fields", "Values")


# ---------------------------------------------------------------------------
# Validator (embedded from lib_bejson_Core_bejson_validator)
# ---------------------------------------------------------------------------
@dataclass
class ValidationResult:
    valid: bool = True
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    current_file: str = ""

    def add_error(self, message: str):
        self.valid = False
        self.errors.append(message)

    def add_warning(self, message: str):
        self.warnings.append(message)

    @property
    def is_valid(self) -> bool:
        return self.valid


class BEJSONValidationError(Exception):
    def __init__(self, message: str, code: int):
        super().__init__(message)
        self.code = code


def bejson_validator_check_json_syntax(input_, res: ValidationResult, is_file=False):
    if is_file:
        path = Path(input_)
        if not path.exists():
            raise BEJSONValidationError(f"File not found: {input_}", E_FILE_NOT_FOUND)
        text = path.read_text(encoding="utf-8")
        res.current_file = str(path)
    else:
        text = input_
    if isinstance(text, dict):
        return text
    try:
        return json.loads(text)
    except Exception as e:
        raise BEJSONValidationError(f"Invalid JSON: {e}", E_INVALID_JSON)


def bejson_validator_check_mandatory_keys(doc):
    for key in MANDATORY_KEYS:
        if key not in doc:
            raise BEJSONValidationError(f"Missing key: {key}", E_MISSING_MANDATORY_KEY)
    if doc["Format"] != "BEJSON":
        raise BEJSONValidationError("Invalid Format", E_INVALID_FORMAT)
    if doc["Format_Creator"] != "Elton Boehnen":
        raise BEJSONValidationError("Invalid Format_Creator: Must be 'Elton Boehnen'", E_INVALID_FORMAT_CREATOR)
    version = doc.get("Format_Version", "")
    if version not in VALID_VERSIONS:
        raise BEJSONValidationError(f"Invalid version: {version}", E_INVALID_VERSION)
    return version


def bejson_validator_check_records_type(doc, version):
    rt = doc["Records_Type"]
    if not isinstance(rt, list):
        raise BEJSONValidationError("Records_Type must be a list", E_INVALID_RECORDS_TYPE)
    count = len(rt)
    if version in ("104", "104a"):
        if count != 1:
            raise BEJSONValidationError(f"BEJSON {version} must have exactly 1 record type. Found {count}.", E_INVALID_RECORDS_TYPE)
    elif version == "104db":
        if count < 2:
            raise BEJSONValidationError("104db requires 2+ types", E_INVALID_RECORDS_TYPE)


def bejson_validator_check_record_type_parent(doc, version):
    if version != "104db":
        return True
    fields = doc["Fields"]
    if not fields or fields[0].get("name") != "Record_Type_Parent":
        raise BEJSONValidationError("104db first field must be 'Record_Type_Parent'", E_INVALID_RECORD_TYPE_PARENT)
    valid_types = set(doc["Records_Type"])
    for i, record in enumerate(doc["Values"]):
        if not record:
            continue
        rtp = record[0]
        if rtp not in valid_types:
            raise BEJSONValidationError(f"Invalid Record_Type_Parent '{rtp}' at row {i}", E_INVALID_RECORD_TYPE_PARENT)
    return True


def bejson_validator_check_fields_structure(doc, version):
    fields = doc["Fields"]
    for i, f in enumerate(fields):
        fname = f.get("name")
        ftype = f.get("type")
        if not fname or not ftype:
            raise BEJSONValidationError(f"Field {i} missing name or type", E_INVALID_FIELDS)
        if ftype not in VALID_FIELD_TYPES:
            raise BEJSONValidationError(
                f"Field '{fname}' (index {i}) has invalid type '{ftype}'. "
                f"Must be exactly one of {sorted(VALID_FIELD_TYPES)} (lowercase).",
                E_INVALID_FIELDS,
            )
        if version == "104a" and ftype in ("array", "object"):
            raise BEJSONValidationError(f"104a forbids complex type: {ftype}", E_INVALID_FIELDS)
        if version == "104db" and fname != "Record_Type_Parent" and "Record_Type_Parent" not in f:
            raise BEJSONValidationError(f"Field '{fname}' missing Record_Type_Parent in 104db", E_INVALID_RECORD_TYPE_PARENT)
    return len(fields)


def bejson_validator_check_values(doc, version, fields_count):
    fields = doc["Fields"]
    for i, record in enumerate(doc["Values"]):
        if len(record) != fields_count:
            raise BEJSONValidationError(f"Length mismatch at row {i}", E_RECORD_LENGTH_MISMATCH)
        for j, val in enumerate(record):
            ftype = fields[j].get("type")
            if val is None:
                continue
            if ftype == "string" and not isinstance(val, str):
                raise BEJSONValidationError(f"Type mismatch at row {i}, col {j} ({fields[j]['name']}): expected string", E_TYPE_MISMATCH)
            elif ftype == "integer" and (not isinstance(val, int) or isinstance(val, bool)):
                raise BEJSONValidationError(f"Type mismatch at row {i}, col {j} ({fields[j]['name']}): expected integer", E_TYPE_MISMATCH)
            elif ftype == "number" and (not isinstance(val, (int, float)) or isinstance(val, bool)):
                raise BEJSONValidationError(f"Type mismatch at row {i}, col {j} ({fields[j]['name']}): expected number, got bool", E_TYPE_MISMATCH)
            elif ftype == "boolean" and not isinstance(val, bool):
                raise BEJSONValidationError(f"Type mismatch at row {i}, col {j} ({fields[j]['name']}): expected boolean", E_TYPE_MISMATCH)
            elif ftype == "array" and not isinstance(val, list):
                raise BEJSONValidationError(f"Type mismatch at row {i}, col {j} ({fields[j]['name']}): expected array", E_TYPE_MISMATCH)
            elif ftype == "object" and not isinstance(val, dict):
                raise BEJSONValidationError(f"Type mismatch at row {i}, col {j} ({fields[j]['name']}): expected object", E_TYPE_MISMATCH)


def bejson_validator_check_custom_headers(doc, version):
    mandatory_set = set(MANDATORY_KEYS)
    for key in doc:
        if key in mandatory_set or key == "Parent_Hierarchy":
            continue
        if version in ("104", "104db"):
            raise BEJSONValidationError(f"Custom key '{key}' forbidden in {version}", E_RESERVED_KEY_COLLISION)


def validate_bejson(input_data: Union[str, dict], is_file: bool = False) -> ValidationResult:
    """Thread-safe validation. Returns a ValidationResult object."""
    res = ValidationResult()
    try:
        doc = bejson_validator_check_json_syntax(input_data, res, is_file=is_file)
        version = bejson_validator_check_mandatory_keys(doc)
        bejson_validator_check_custom_headers(doc, version)
        bejson_validator_check_records_type(doc, version)
        bejson_validator_check_record_type_parent(doc, version)
        fields_count = bejson_validator_check_fields_structure(doc, version)
        bejson_validator_check_values(doc, version, fields_count)
    except BEJSONValidationError as e:
        res.add_error(str(e))
    except Exception as e:
        res.add_error(f"Unexpected validation error: {e}")
    return res


def bejson_validator_get_report(input_data, is_file: bool = False) -> str:
    """Return a human-readable validation report string."""
    res = validate_bejson(input_data, is_file=is_file)
    lines = ["BEJSON Validation Report"]
    lines.append("  File: " + (res.current_file or "<string>"))
    lines.append("  Valid: " + str(res.valid))
    if res.errors:
        lines.append("  Errors:")
        for e in res.errors:
            lines.append("    - " + e)
    if res.warnings:
        lines.append("  Warnings:")
        for w in res.warnings:
            lines.append("    - " + w)
    return "\n".join(lines)


def bejson_validator_validate_string(json_string):
    res = validate_bejson(json_string)
    if not res.valid:
        raise BEJSONValidationError(res.errors[0], E_INVALID_FORMAT)
    return True


def bejson_validator_validate_file(file_path):
    res = validate_bejson(file_path, is_file=True)
    if not res.valid:
        raise BEJSONValidationError(res.errors[0], E_INVALID_FORMAT)
    return True


# ---------------------------------------------------------------------------
# About / Info
# ---------------------------------------------------------------------------
def about():
    return (
        "BEJSON_Template_PY_Validator v" + str(VERSION) + "\n"
        "Embedded: BEJSON Core error registry + BEJSON Core validator\n"
        "Author: Elton Boehnen | boehnenelton2024@gmail.com | "
        "boehnenelton2024.pages.dev | github.com/boehnenelton"
    )


if __name__ == "__main__":
    print(about())
