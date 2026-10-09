'use strict';
/*
 * SmartSeal — native Node port.
 * Reproduces sf_smartseal.core.seal/verify: SHA-256 content digest, a 32-hex
 * signature = sha256(digest + signer), and tamper/valid checks. The reference's
 * non-deterministic `created` timestamp is intentionally not part of the port
 * contract (only the content-addressed fields are). Uses Node's crypto only.
 */
const crypto = require('crypto');
const sha = buf => crypto.createHash('sha256').update(buf).digest('hex');

function seal(content, signer = 'SmartSeal-demo') {
  const digest = sha(Buffer.from(content, 'utf8'));
  const signature = sha(Buffer.from(digest + signer, 'utf8')).slice(0, 32);
  return { sha256: digest, signature, chain: [signer] };
}
function verify(content, receipt, signer = 'SmartSeal-demo') {
  const now = sha(Buffer.from(content, 'utf8'));
  const tampered = now !== receipt.sha256;
  const expected = sha(Buffer.from(receipt.sha256 + signer, 'utf8')).slice(0, 32);
  return { valid: !tampered && expected === receipt.signature, tampered, chain_len: receipt.chain.length };
}
module.exports = { seal, verify };
