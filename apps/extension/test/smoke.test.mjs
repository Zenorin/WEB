import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';

test('apps/extension has manifest.json', () => { assert.ok(fs.existsSync('manifest.json')); });
test('apps/extension has src/background.ts', () => { assert.ok(fs.existsSync('src/background.ts')); });
test('apps/extension has src/content.ts', () => { assert.ok(fs.existsSync('src/content.ts')); });
