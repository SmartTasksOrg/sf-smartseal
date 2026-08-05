'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert'),{execFileSync}=require('child_process');
const C=path.join(__dirname,'..','..','conformance');
const got=JSON.parse(execFileSync('node',[path.join(__dirname,'..','bin','cli.js'),path.join(C,'vectors.json')],{encoding:'utf8'}));
const exp=JSON.parse(fs.readFileSync(path.join(C,'expected.json'),'utf8'));
assert.deepStrictEqual(got.results.map(r=>({...r})),exp.results.map(r=>({...r})));
console.log(`ok - ${exp.results.length} conformance cases pass`);
