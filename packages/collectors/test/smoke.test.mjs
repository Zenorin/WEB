import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';

test('packages/collectors has package.json', () => { assert.ok(fs.existsSync('package.json')); });
test('packages/collectors has tsconfig.json', () => { assert.ok(fs.existsSync('tsconfig.json')); });
test('packages/collectors has src/index.ts', () => { assert.ok(fs.existsSync('src/index.ts')); });
