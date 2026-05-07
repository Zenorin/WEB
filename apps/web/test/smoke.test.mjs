import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';

test('apps/web has package.json', () => { assert.ok(fs.existsSync('package.json')); });
test('apps/web has index.html', () => { assert.ok(fs.existsSync('index.html')); });
test('apps/web has src/App.tsx', () => { assert.ok(fs.existsSync('src/App.tsx')); });
test('apps/web has src/main.tsx', () => { assert.ok(fs.existsSync('src/main.tsx')); });
