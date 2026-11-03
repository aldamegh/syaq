const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const n = require('../app/static/normalizer.js');
const corpus = JSON.parse(fs.readFileSync(path.join(__dirname, '../normalization/conformance-corpus-v1.json'), 'utf8'));
for (const c of corpus.cases) assert.equal(n.normalizeForGame(c.input), c.expected, c.id);
assert.throws(() => n.normalizeForGame(null), TypeError);
console.log(`${corpus.cases.length} synthetic JavaScript conformance cases passed.`);
