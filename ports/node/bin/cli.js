#!/usr/bin/env node
'use strict';
const fs = require('fs'), path = require('path');
const { seal, verify } = require('../lib/seal.js');
function run(c) {
  const signer = c.signer || 'SmartSeal-demo';
  if ((c.op || 'seal') === 'seal') return Object.assign({ name: c.name }, seal(c.content || '', signer));
  const r = seal(c.seal_content || '', signer);
  return Object.assign({ name: c.name }, verify(c.content || '', r, c.verify_signer || signer));
}
const vpath = process.argv[2] || path.join(__dirname, '..', '..', 'conformance', 'vectors.json');
const v = JSON.parse(fs.readFileSync(vpath, 'utf8'));
process.stdout.write(JSON.stringify({ results: v.cases.map(run) }, null, 2) + '\n');
