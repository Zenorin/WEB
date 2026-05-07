#!/usr/bin/env node
import fs from 'node:fs'; import path from 'node:path';
const blocked=[/\.map$/i,/(^|\/)background\.js$/i,/(^|\/)preload\.js$/i,/(^|\/)_next\/static\/chunks\//i]; const ignore=new Set(['node_modules','.git','dist','build','__pycache__']); let failures=[];
function walk(d){ for(const n of fs.readdirSync(d)){ if(ignore.has(n)) continue; const p=path.join(d,n); const rel=path.relative(process.cwd(),p).replaceAll('\\','/'); const st=fs.statSync(p); if(st.isDirectory()) walk(p); else if(blocked.some(rx=>rx.test(rel))) failures.push(rel); }}
walk(process.cwd()); if(failures.length){ console.error('cleanroom-audit FAIL'); for(const f of failures) console.error('- '+f); process.exit(1); } console.log('cleanroom-audit PASS');
