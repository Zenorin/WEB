import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';

test('tools/reference-analysis has package.json', () => { assert.ok(fs.existsSync('package.json')); });
test('tools/reference-analysis has tsconfig.json', () => { assert.ok(fs.existsSync('tsconfig.json')); });
test('tools/reference-analysis has src/index.ts', () => { assert.ok(fs.existsSync('src/index.ts')); });
