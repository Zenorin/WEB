#!/usr/bin/env node
import fs from 'node:fs';
for (const p of ['package.json','tsconfig.base.json','.codex/scaffold-manifest.json']) { if (!fs.existsSync(p)) { console.error('workspace-check FAIL: missing '+p); process.exit(1); } }
const pkg=JSON.parse(fs.readFileSync('package.json','utf8'));
for (const s of ['test:api','validate:scaffold','validate:planning','validate:dev-flow','validate:all']) { if (!pkg.scripts || !pkg.scripts[s]) { console.error('workspace-check FAIL: missing script '+s); process.exit(1); } }
if (/echo|No tests configured|exit 0|true$/.test(pkg.scripts.test || '')) { console.error('workspace-check FAIL: root test script appears to be no-op'); process.exit(1); }
console.log('workspace-check PASS');
