/**
 * Name:           BEJSON_Template_JS_Validator
 * Description:    Basic vanilla-JS template with the BEJSON Core error registry and BEJSON Core validator embedded, not auto-invoked.
 * Version:        1 (Package_Version 100)
 * Date Created:   2026-09-09
 * Author:         Elton Boehnen
 * Contact:        boehnenelton2024@gmail.com | boehnenelton2024.pages.dev | github.com/boehnenelton
 * Format_Creator: Elton Boehnen
 * RELATIONAL_ID:  b3d7a2e6-1f94-4c58-a0e2-6c3b9f4d7a15
 * Release_Version: 300
 */

'use strict';

var BEJSON_TEMPLATE_VERSION = 1;

const BEJSON_ERRORS = {
    E_INVALID_JSON: 1,
    E_MISSING_MANDATORY_KEY: 2,
    E_INVALID_FORMAT: 3,
    E_INVALID_VERSION: 4,
    E_INVALID_RECORDS_TYPE: 5,
    E_INVALID_FIELDS: 6,
    E_INVALID_VALUES: 7,
    E_TYPE_MISMATCH: 8,
    E_RECORD_LENGTH_MISMATCH: 9,
    E_RESERVED_KEY_COLLISION: 10,
    E_INVALID_RECORD_TYPE_PARENT: 11,
    E_NULL_VIOLATION: 12,
    E_FILE_NOT_FOUND: 13,
    E_PERMISSION_DENIED: 14,
    E_ATOMIC_WRITE_FAILED: 15,
    E_INVALID_FORMAT_CREATOR: 16,

    E_CORE_PARSE_ERROR: 17,
    E_CORE_SERIALIZATION_ERROR: 18,
    E_CORE_NULL_DOCUMENT: 19,
    
    E_CORE_INVALID_VERSION: 20,
    E_CORE_INVALID_OPERATION: 21,
    E_CORE_INDEX_OUT_OF_BOUNDS: 22,
    E_CORE_FIELD_NOT_FOUND: 23,
    E_CORE_TYPE_CONVERSION_FAILED: 24,
    E_CORE_BACKUP_FAILED: 25,
    E_CORE_WRITE_FAILED: 26,
    E_CORE_QUERY_FAILED: 27,
    E_CORE_ENCRYPTION_FAILED: 28,
    E_CORE_DECRYPTION_FAILED: 29,

    E_MFDB_NOT_MANIFEST: 30,
    E_MFDB_NOT_ENTITY_FILE: 31,
    E_MFDB_MANIFEST_RECORDS_TYPE: 32,
    E_MFDB_ENTITY_NOT_FOUND: 33,
    E_MFDB_ENTITY_NAME_MISMATCH: 34,
    E_MFDB_DUPLICATE_ENTRY: 35,
    E_MFDB_NO_PARENT_HIERARCHY: 36,
    E_MFDB_MANIFEST_NOT_FOUND: 37,
    E_MFDB_BIDIRECTIONAL_FAIL: 38,
    E_MFDB_FK_UNRESOLVED: 39,
    E_MFDB_MISSING_REQUIRED_FIELD: 40,
    E_MFDB_NULL_REQUIRED: 41,
    E_MFDB_INVALID_ARCHIVE: 42,
    
    E_MFDB_CORE_MANIFEST_NOT_FOUND: 50,
    E_MFDB_CORE_ENTITY_NOT_FOUND: 51,
    E_MFDB_CORE_WRITE_FAILED: 52,
    E_MFDB_CORE_LOCK_FAILED: 53,
    E_MFDB_CORE_INVALID_OPERATION: 54,
    E_MFDB_CORE_INDEX_OUT_OF_BOUNDS: 55,
    E_MFDB_CORE_JOIN_FAILED: 56,
    E_MFDB_CORE_ARCHIVE_ERROR: 70,
    E_MFDB_CORE_MOUNT_CONFLICT: 71,
    E_MFDB_CORE_CREATE_FAILED: 72
};

if (typeof window !== 'undefined') {
    window.BEJSON_ERRORS = BEJSON_ERRORS;
}

const {
  E_INVALID_JSON,
  E_MISSING_MANDATORY_KEY,
  E_INVALID_FORMAT,
  E_INVALID_VERSION,
  E_INVALID_RECORDS_TYPE,
  E_INVALID_FIELDS,
  E_INVALID_VALUES,
  E_TYPE_MISMATCH,
  E_RECORD_LENGTH_MISMATCH,
  E_RESERVED_KEY_COLLISION,
  E_INVALID_RECORD_TYPE_PARENT,
  E_NULL_VIOLATION,
  E_FILE_NOT_FOUND,
  E_PERMISSION_DENIED,
  E_ATOMIC_WRITE_FAILED
} = BEJSON_ERRORS;

const VALID_VERSIONS    = new Set(['104', '104a', '104db']);
const MANDATORY_KEYS    = ['Format', 'Format_Version', 'Format_Creator', 'Records_Type', 'Fields', 'Values'];
const VALID_FIELD_TYPES = new Set(['string', 'integer', 'number', 'boolean', 'array', 'object']);

class BEJSONValidationError extends Error {
  constructor(message, code) {
    super(message);
    this.name = 'BEJSONValidationError';
    this.code = code;
  }
}

class ValidationState {
  constructor() {
    this.errors      = [];
    this.warnings    = [];
    this.currentFile = '';
  }
  reset() {
    this.errors      = [];
    this.warnings    = [];
    this.currentFile = '';
  }
  addError(message, location = '', context = '') {
    let entry = 'ERROR';
    if (location) entry += ` | Location: ${location}`;
    entry += ` | Message: ${message}`;
    if (context) entry += ` | Context: ${context}`;
    this.errors.push(entry);
  }
  addWarning(message, location = '') {
    let entry = 'WARNING';
    if (location) entry += ` | Location: ${location}`;
    entry += ` | Message: ${message}`;
    this.warnings.push(entry);
  }
  getErrors() { return [...this.errors]; }
  getWarnings() { return [...this.warnings]; }
  hasErrors() { return this.errors.length > 0; }
  hasWarnings() { return this.warnings.length > 0; }
  errorCount() { return this.errors.length; }
  warningCount() { return this.warnings.length; }
}

const _state = new ValidationState();

function bejson_validator_reset_state() { _state.reset(); }
function bejson_validator_get_errors() { return _state.getErrors(); }
function bejson_validator_get_warnings() { return _state.getWarnings(); }
function bejson_validator_has_errors() { return _state.hasErrors(); }
function bejson_validator_has_warnings() { return _state.hasWarnings(); }
function bejson_validator_error_count() { return _state.errorCount(); }
function bejson_validator_warning_count() { return _state.warningCount(); }
function bejson_validator_check_dependencies() { return true; }

const IO_PROVIDER = {
  readFile: (path) => {
    if (typeof require !== 'undefined') {
      try {
        const fs = require('fs');
        return fs.readFileSync(path, 'utf8');
      } catch (e) {
        throw new Error(`Node.js fs failed: ${e.message}`);
      }
    }
    throw new Error('File I/O not available in this environment');
  },
  exists: (path) => {
    if (typeof require !== 'undefined') {
      try {
        const fs = require('fs');
        return fs.existsSync(path);
      } catch (e) {
        return false;
      }
    }
    return false;
  }
};

function bejson_validator_check_json_syntax(input, isFile = false) {
  let text;
  if (isFile) {
    if (!IO_PROVIDER.exists(input)) {
      _state.addError(`File not found: ${input}`, 'File System');
      throw new BEJSONValidationError(`File not found: ${input}`, E_FILE_NOT_FOUND);
    }
    try {
      text = IO_PROVIDER.readFile(input);
      _state.currentFile = input;
    } catch (err) {
      _state.addError(`IO Error: ${err.message}`, 'File System');
      throw new BEJSONValidationError(`IO Error: ${err.message}`, E_FILE_NOT_FOUND);
    }
  } else {
    text = input;
  }

  if (typeof text === 'object' && text !== null) {
    return text;
  }

  try {
    return JSON.parse(text);
  } catch (err) {
    _state.addError(`Invalid JSON syntax: ${err.message}`, 'JSON Parse');
    throw new BEJSONValidationError(`Invalid JSON syntax: ${err.message}`, E_INVALID_JSON);
  }
}

function bejson_validator_check_mandatory_keys(doc) {
  for (const key of MANDATORY_KEYS) {
    if (!(key in doc)) {
      _state.addError(`Missing mandatory top-level key: '${key}'`, 'Top-Level Keys');
      throw new BEJSONValidationError(`Missing mandatory key: ${key}`, E_MISSING_MANDATORY_KEY);
    }
  }

  if (doc['Format'] !== 'BEJSON') {
    _state.addError(`Invalid 'Format' value: Expected 'BEJSON', got '${doc['Format']}'`, 'Top-Level Keys/Format');
    throw new BEJSONValidationError('Invalid Format', E_INVALID_FORMAT);
  }

  const version = doc['Format_Version'] ?? '';
  if (!VALID_VERSIONS.has(version)) {
    _state.addError(`Invalid 'Format_Version': Expected '104', '104a', or '104db', got '${version}'`, 'Top-Level Keys/Format_Version');
    throw new BEJSONValidationError(`Invalid version: ${version}`, E_INVALID_VERSION);
  }

  if (typeof doc['Format_Creator'] !== 'string') {
    _state.addError("Invalid 'Format_Creator': Must be a string", 'Top-Level Keys/Format_Creator');
    throw new BEJSONValidationError('Invalid Format_Creator', E_INVALID_FORMAT);
  }

  const checks = [
    ['Records_Type', E_INVALID_RECORDS_TYPE, 'Top-Level Keys/Records_Type'],
    ['Fields',       E_INVALID_FIELDS,       'Top-Level Keys/Fields'],
    ['Values',       E_INVALID_VALUES,       'Top-Level Keys/Values'],
  ];
  for (const [key, code, section] of checks) {
    if (!Array.isArray(doc[key])) {
      _state.addError(`Invalid '${key}': Must be an array`, section);
      throw new BEJSONValidationError(`Invalid ${key}`, code);
    }
  }
  return version;
}

function bejson_validator_check_records_type(doc, version) {
  const rt    = doc['Records_Type'];
  const count = rt.length;
  if (version === '104' || version === '104a') {
    if (count !== 1 || typeof rt[0] !== 'string') {
      _state.addError(`For BEJSON ${version}, 'Records_Type' must contain exactly one string. Found ${count} entries.`, 'Records_Type');
      throw new BEJSONValidationError('Bad Records_Type', E_INVALID_RECORDS_TYPE);
    }
  } else if (version === '104db') {
    if (count < 2) {
      _state.addError(`For BEJSON 104db, 'Records_Type' must contain two or more unique strings. Found ${count} entries.`, 'Records_Type');
      throw new BEJSONValidationError('Bad Records_Type', E_INVALID_RECORDS_TYPE);
    }
    const seen = new Set();
    for (let i = 0; i < rt.length; i++) {
      if (typeof rt[i] !== 'string') {
        _state.addError(`Records_Type[${i}] must be a string`, `Records_Type[${i}]`);
        throw new BEJSONValidationError('Bad Records_Type entry', E_INVALID_RECORDS_TYPE);
      }
      if (seen.has(rt[i])) {
        _state.addError(`Duplicate type '${rt[i]}' found in 'Records_Type'`, 'Records_Type');
        throw new BEJSONValidationError(`Duplicate Records_Type: ${rt[i]}`, E_INVALID_RECORDS_TYPE);
      }
      seen.add(rt[i]);
    }
  }
}

function bejson_validator_check_fields_structure(doc, version) {
  const fields = doc['Fields'];
  if (!fields || fields.length === 0) {
    _state.addError("'Fields' array cannot be empty", 'Fields Array');
    throw new BEJSONValidationError('Empty Fields', E_INVALID_FIELDS);
  }

  const seenNames = new Set();
  for (let i = 0; i < fields.length; i++) {
    const fieldDef = fields[i];
    if (typeof fieldDef !== 'object' || fieldDef === null || Array.isArray(fieldDef)) {
      _state.addError(`Field at index ${i} must be an object`, `Fields[${i}]`);
      throw new BEJSONValidationError(`Field ${i} not an object`, E_INVALID_FIELDS);
    }

    const name = fieldDef['name'];
    if (typeof name !== 'string') {
      _state.addError(`Field at index ${i}: Missing or invalid 'name' (must be string)`, `Fields[${i}]`);
      throw new BEJSONValidationError(`Field ${i} bad name`, E_INVALID_FIELDS);
    }

    if (seenNames.has(name)) {
      _state.addError(`Duplicate field name '${name}' found in 'Fields' array`, `Fields[${i}]`);
      throw new BEJSONValidationError(`Duplicate field: ${name}`, E_INVALID_FIELDS);
    }
    seenNames.add(name);

    const ftype = fieldDef['type'];
    if (typeof ftype !== 'string' || !VALID_FIELD_TYPES.has(ftype)) {
      _state.addError(`Field '${name}' (index ${i}): Invalid type '${ftype}'. Valid: ${[...VALID_FIELD_TYPES].join(', ')}`, `Fields[${i}]`);
      throw new BEJSONValidationError(`Field ${name} invalid type`, E_INVALID_FIELDS);
    }

    if (version === '104a' && (ftype === 'array' || ftype === 'object')) {
      _state.addError(`Field '${name}' (index ${i}): Type '${ftype}' not allowed in 104a.`, `Fields[${i}]`);
      throw new BEJSONValidationError(`Field ${name} disallowed type for 104a`, E_INVALID_FIELDS);
    }
  }
  return fields.length;
}

function bejson_validator_check_record_type_parent(doc) {
  const fields = doc['Fields'];
  const first  = fields[0] ?? {};
  if (!fields.length || first['name'] !== 'Record_Type_Parent' || first['type'] !== 'string') {
    _state.addError(`For BEJSON 104db, the first field must be {"name": "Record_Type_Parent", "type": "string"}. Found: ${JSON.stringify(first)}`, 'Fields[0]');
    throw new BEJSONValidationError('Bad Record_Type_Parent field', E_INVALID_RECORD_TYPE_PARENT);
  }

  const validTypes = new Set(doc['Records_Type']);
  for (let i = 0; i < doc['Values'].length; i++) {
    const record = doc['Values'][i];
    if (!Array.isArray(record)) {
      _state.addError(`Values[${i}] must be an array (record)`, `Values[${i}]`);
      throw new BEJSONValidationError(`Bad record at ${i}`, E_INVALID_VALUES);
    }
    const rtp = record[0] ?? null;
    if (!rtp) {
      _state.addError(`Record at 'Values' index ${i}: 'Record_Type_Parent' is missing or null`, `Values[${i}][0]`);
      throw new BEJSONValidationError(`Missing RTP at ${i}`, E_INVALID_RECORD_TYPE_PARENT);
    }
    if (!validTypes.has(rtp)) {
      _state.addError(`Record at 'Values' index ${i}: 'Record_Type_Parent' value '${rtp}' does not match any declared type in 'Records_Type'`, `Values[${i}][0]`);
      throw new BEJSONValidationError(`Invalid RTP '${rtp}' at ${i}`, E_INVALID_RECORD_TYPE_PARENT);
    }
  }
}

function _jsonType(value) {
  if (value === null)             return 'null';
  if (typeof value === 'boolean') return 'boolean';
  if (Number.isInteger(value))    return 'integer';
  if (typeof value === 'number')  return 'number';
  if (typeof value === 'string')  return 'string';
  if (Array.isArray(value))       return 'array';
  if (typeof value === 'object')  return 'object';
  return 'unknown';
}

function bejson_validator_check_values(doc, version, fieldsCount) {
  const values = doc['Values'];
  const fields = doc['Fields'];

  for (let i = 0; i < values.length; i++) {
    const record = values[i];
    if (!Array.isArray(record)) {
      _state.addError(`Values[${i}] must be an array (record)`, `Values[${i}]`);
      throw new BEJSONValidationError(`Bad record at ${i}`, E_INVALID_VALUES);
    }

    if (record.length !== fieldsCount) {
      _state.addError(`Record at 'Values' index ${i} has ${record.length} elements, but 'Fields' defines ${fieldsCount} fields.`, `Values[${i}]`);
      throw new BEJSONValidationError(`Length mismatch at ${i}`, E_RECORD_LENGTH_MISMATCH);
    }

    const recordType = (version === '104db' && record.length > 0) ? record[0] : null;

    for (let j = 0; j < record.length; j++) {
      const value     = record[j];
      const fieldDef  = fields[j];
      const fieldName = fieldDef['name'];
      const fieldType = fieldDef['type'];
      const fieldParent = fieldDef['Record_Type_Parent'] ?? '';

      if (version === '104db' && fieldParent && j > 0) {
        if (fieldParent !== recordType) {
          if (value !== null) {
            _state.addError(`Record at 'Values' index ${i} (type '${recordType}'), field '${fieldName}' (index ${j}): not applicable to this type; must be null.`, `Values[${i}][${j}]`);
            throw new BEJSONValidationError('Null violation', E_NULL_VIOLATION);
          }
          continue;
        }
      }

      if (value === null) continue;

      let typeValid = false;
      switch (fieldType) {
        case 'string':  typeValid = typeof value === 'string'; break;
        case 'integer': typeValid = Number.isInteger(value) && typeof value !== 'boolean'; break;
        case 'number':  typeValid = typeof value === 'number' && typeof value !== 'boolean'; break;
        case 'boolean': typeValid = typeof value === 'boolean'; break;
        case 'array':   typeValid = Array.isArray(value); break;
        case 'object':  typeValid = typeof value === 'object' && !Array.isArray(value); break;
      }

      if (!typeValid) {
        _state.addError(`Record at 'Values' index ${i}, field '${fieldName}' (index ${j}): Value '${value}' is of type '${_jsonType(value)}', but 'Fields' defines type '${fieldType}'.`, `Values[${i}][${j}]`);
        throw new BEJSONValidationError(`Type mismatch at [${i}][${j}]`, E_TYPE_MISMATCH);
      }
    }
  }
}

function bejson_validator_check_custom_headers(doc, version) {
  const mandatorySet = new Set(MANDATORY_KEYS);
  for (const key of Object.keys(doc)) {
    if (mandatorySet.has(key) || key === 'Parent_Hierarchy') continue;
    if (version === '104' || version === '104db') {
      _state.addError(`For BEJSON ${version}, custom top-level key '${key}' is not permitted.`, `Top-Level Keys/${key}`);
      throw new BEJSONValidationError(`Unexpected key: ${key}`, E_RESERVED_KEY_COLLISION);
    }
  }
}

function bejson_validator_validate_string(jsonString) {
  bejson_validator_reset_state();
  const doc          = bejson_validator_check_json_syntax(jsonString, false);
  const version      = bejson_validator_check_mandatory_keys(doc);
  bejson_validator_check_custom_headers(doc, version);
  bejson_validator_check_records_type(doc, version);
  const fieldsCount  = bejson_validator_check_fields_structure(doc, version);
  if (version === '104db') bejson_validator_check_record_type_parent(doc);
  bejson_validator_check_values(doc, version, fieldsCount);
  return true;
}

function bejson_validator_validate_file(filePath) {
  bejson_validator_reset_state();
  try {
    const text = IO_PROVIDER.readFile(filePath);
    _state.currentFile = filePath;
    return bejson_validator_validate_string(text);
  } catch (err) {
    _state.addError(`IO Error: ${err.message}`, 'File System');
    throw new BEJSONValidationError(`IO Error: ${err.message}`, E_FILE_NOT_FOUND);
  }
}

function bejson_validator_get_report(input, isFile = false) {
  let valid = false;
  try {
    if (isFile) {
      valid = bejson_validator_validate_file(input);
    } else {
      valid = bejson_validator_validate_string(input);
    }
  } catch (_) {}

  const lines = [
    '=== BEJSON Validation Report ===',
    `Status: ${valid ? 'VALID' : 'INVALID'}`,
    '',
    `Errors: ${bejson_validator_error_count()}`,
  ];
  if (bejson_validator_has_errors()) {
    lines.push('---');
    lines.push(...bejson_validator_get_errors());
  }
  lines.push('', `Warnings: ${bejson_validator_warning_count()}`);
  if (bejson_validator_has_warnings()) {
    lines.push('---');
    lines.push(...bejson_validator_get_warnings());
  }
  return lines.join('\n');
}

function bejson_template_about() {
  return [
    'BEJSON_Template_JS_Validator v' + BEJSON_TEMPLATE_VERSION + ' (Release_Version 300)',
    'Embedded: BEJSON Core error registry + BEJSON Core validator',
    'Author: Elton Boehnen | boehnenelton2024@gmail.com | boehnenelton2024.pages.dev | github.com/boehnenelton'
  ].join('\n');
}

if (typeof window !== 'undefined') {
  window.bejson_template_about = bejson_template_about;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    BEJSON_ERRORS: BEJSON_ERRORS,
    BEJSONValidationError: BEJSONValidationError,
    bejson_validator_validate_string: bejson_validator_validate_string,
    bejson_validator_validate_file: bejson_validator_validate_file,
    bejson_validator_get_report: bejson_validator_get_report,
    bejson_validator_reset_state: bejson_validator_reset_state,
    bejson_validator_get_errors: bejson_validator_get_errors,
    bejson_validator_get_warnings: bejson_validator_get_warnings,
    bejson_validator_has_errors: bejson_validator_has_errors,
    bejson_validator_has_warnings: bejson_validator_has_warnings,
    bejson_template_about: bejson_template_about
  };
}

if (typeof require !== 'undefined' && require.main === module) {
  console.log(bejson_template_about());
}
