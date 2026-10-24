#!/usr/bin/env node
/**
 * ==============================================================================
 * Script Name: bejson_sanitizer.js
 * Description: Layer 1 JavaScript/Node boundary-layer sanitization primitives
 *              for BEJSON payloads and record rows per Policy §10.9.
 * Version: 1.0.0
 * Author: Elton Boehnen · boehnenelton2024@gmail.com
 * ==============================================================================
 */

'use strict';

/**
 * Strips leading and trailing whitespace from string values while preserving other types.
 * @param {*} value
 * @returns {*}
 */
function sanitizeStringValue(value) {
    if (typeof value === 'string') {
        return value.trim();
    }
    return value;
}

/**
 * Sanitizes an individual record row array by stripping boundary whitespace from string entries.
 * @param {Array} rowArray
 * @returns {Array}
 */
function bejsonSanitizeRow(rowArray) {
    if (!Array.isArray(rowArray)) {
        return rowArray;
    }
    return rowArray.map(item => sanitizeStringValue(item));
}

/**
 * Sanitizes field definition objects in the Fields array.
 * @param {Array} fieldsArray
 * @returns {Array}
 */
function bejsonSanitizeFieldDefinitions(fieldsArray) {
    if (!Array.isArray(fieldsArray)) {
        return fieldsArray;
    }
    return fieldsArray.map(fieldDef => {
        if (typeof fieldDef === 'object' && fieldDef !== null) {
            const cleanDef = {};
            for (const [key, val] of Object.entries(fieldDef)) {
                cleanDef[typeof key === 'string' ? key.trim() : key] = sanitizeStringValue(val);
            }
            return cleanDef;
        }
        return fieldDef;
    });
}

/**
 * Completely sanitizes a BEJSON document payload per Policy §10.9.
 * @param {Object} rawDoc
 * @returns {Object}
 */
function bejsonSanitizePayload(rawDoc) {
    if (typeof rawDoc !== 'object' || rawDoc === null) {
        return rawDoc;
    }

    const sanitizedDoc = {};

    for (const [key, val] of Object.entries(rawDoc)) {
        const cleanKey = typeof key === 'string' ? key.trim() : key;

        if (cleanKey === 'Fields' && Array.isArray(val)) {
            sanitizedDoc[cleanKey] = bejsonSanitizeFieldDefinitions(val);
        } else if (cleanKey === 'Values' && Array.isArray(val)) {
            sanitizedDoc[cleanKey] = val.map(row => bejsonSanitizeRow(row));
        } else if (typeof val === 'string') {
            sanitizedDoc[cleanKey] = val.trim();
        } else if (typeof val === 'object' && val !== null && !Array.isArray(val)) {
            sanitizedDoc[cleanKey] = bejsonSanitizePayload(val);
        } else {
            sanitizedDoc[cleanKey] = val;
        }
    }

    return sanitizedDoc;
}

/**
 * Express / Connect / HTTP Middleware for automatic boundary sanitization.
 */
function bejsonSanitizationMiddleware(req, res, next) {
    if (req.body && typeof req.body === 'object') {
        req.body = bejsonSanitizePayload(req.body);
    }
    if (typeof next === 'function') {
        next();
    }
}

module.exports = {
    bejsonSanitizePayload,
    bejsonSanitizeRow,
    bejsonSanitizeFieldDefinitions,
    bejsonSanitizationMiddleware
};
