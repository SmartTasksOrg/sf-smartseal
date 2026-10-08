<?php
/* SmartSeal - native PHP port. Reproduces sf_smartseal.core.seal/verify. No deps. */
function seal_it(string $content, string $signer): array {
    $digest = hash('sha256', $content);
    $sig = substr(hash('sha256', $digest . $signer), 0, 32);
    return ['sha256' => $digest, 'signature' => $sig, 'chain' => [$signer]];
}
function verify_it(string $content, array $receipt, string $signer): array {
    $now = hash('sha256', $content);
    $tampered = $now !== $receipt['sha256'];
    $expected = substr(hash('sha256', $receipt['sha256'] . $signer), 0, 32);
    return ['valid' => (!$tampered && $expected === $receipt['signature']),
            'tampered' => $tampered, 'chain_len' => count($receipt['chain'])];
}
$vpath = $argv[1] ?? __DIR__ . '/../conformance/vectors.json';
$v = json_decode(file_get_contents($vpath), true);
$results = [];
foreach ($v['cases'] as $c) {
    $signer = $c['signer'] ?? 'SmartSeal-demo';
    if (($c['op'] ?? 'seal') === 'seal') {
        $results[] = array_merge(['name' => $c['name']], seal_it($c['content'] ?? '', $signer));
    } else {
        $r = seal_it($c['seal_content'] ?? '', $signer);
        $results[] = array_merge(['name' => $c['name']],
            verify_it($c['content'] ?? '', $r, $c['verify_signer'] ?? $signer));
    }
}
echo json_encode(['results' => $results], JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES), "\n";
