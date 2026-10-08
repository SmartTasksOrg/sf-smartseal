// SmartSeal - native Go port. Reproduces sf_smartseal.core.seal/verify.
// Standard library only (crypto/sha256, encoding/json).
package main

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
)

func sha(b []byte) string { s := sha256.Sum256(b); return hex.EncodeToString(s[:]) }

func seal(content, signer string) (string, string, []string) {
	digest := sha([]byte(content))
	sig := sha([]byte(digest + signer))[:32]
	return digest, sig, []string{signer}
}
func verify(content, recSha, recSig string, chain []string, signer string) (bool, bool, int) {
	now := sha([]byte(content))
	tampered := now != recSha
	expected := sha([]byte(recSha + signer))[:32]
	return !tampered && expected == recSig, tampered, len(chain)
}

type Case struct {
	Op, Name, Content, Signer, SealContent, VerifySigner string
}

func main() {
	vpath := filepath.Join("..", "conformance", "vectors.json")
	if len(os.Args) > 1 {
		vpath = os.Args[1]
	}
	raw, _ := os.ReadFile(vpath)
	var v struct {
		Cases []map[string]interface{} `json:"cases"`
	}
	json.Unmarshal(raw, &v)
	results := []interface{}{}
	for _, c := range v.Cases {
		name, _ := c["name"].(string)
		op, _ := c["op"].(string)
		signer := "SmartSeal-demo"
		if s, ok := c["signer"].(string); ok {
			signer = s
		}
		if op == "" || op == "seal" {
			content, _ := c["content"].(string)
			d, sig, chain := seal(content, signer)
			results = append(results, map[string]interface{}{
				"name": name, "sha256": d, "signature": sig, "chain": chain})
		} else {
			sc, _ := c["seal_content"].(string)
			content, _ := c["content"].(string)
			d, sig, chain := seal(sc, signer)
			vsigner := signer
			if s, ok := c["verify_signer"].(string); ok {
				vsigner = s
			}
			valid, tampered, clen := verify(content, d, sig, chain, vsigner)
			results = append(results, map[string]interface{}{
				"name": name, "valid": valid, "tampered": tampered, "chain_len": clen})
		}
	}
	b, _ := json.MarshalIndent(map[string]interface{}{"results": results}, "", "  ")
	fmt.Println(string(b))
}
