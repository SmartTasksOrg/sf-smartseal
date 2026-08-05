#!/usr/bin/env bash
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; PORTS="$(dirname "$HERE")"
EXP="$HERE/expected.json"; VEC="$HERE/vectors.json"; TMP="$(mktemp -d)"
command -v python3 >/dev/null 2>&1 && python3 "$HERE/gen_expected.py" >/dev/null 2>&1
pass=0; fail=0; skip=0
grade(){ if python3 "$HERE/compare.py" "$EXP" < "$2" >"$TMP/c" 2>&1; then echo "  $1: $(cat "$TMP/c")"; pass=$((pass+1));
         else echo "  $1: FAIL"; sed 's/^/     /' "$TMP/c"; fail=$((fail+1)); fi; }
echo "SmartSeal port conformance ($(python3 -c "import json;print(len(json.load(open('$VEC'))['cases']))") cases):"
if command -v node  >/dev/null 2>&1; then node "$PORTS/node/bin/cli.js" "$VEC" >"$TMP/node" 2>/dev/null; grade node "$TMP/node"; else echo "  node: SKIP"; skip=$((skip+1)); fi
if command -v php   >/dev/null 2>&1; then php "$PORTS/php/smartseal.php" "$VEC" >"$TMP/php" 2>/dev/null; grade php "$TMP/php"; else echo "  php:  SKIP"; skip=$((skip+1)); fi
if command -v go    >/dev/null 2>&1; then ( cd "$PORTS/go" && go run main.go "$VEC" ) >"$TMP/go" 2>/dev/null; grade go "$TMP/go"; else echo "  go:   SKIP"; skip=$((skip+1)); fi
if command -v javac >/dev/null 2>&1; then ( cd "$PORTS/java/src" && javac SmartSeal.java && java SmartSeal "$VEC" ) >"$TMP/java" 2>/dev/null; grade java "$TMP/java"; else echo "  java: SKIP"; skip=$((skip+1)); fi
rm -rf "$TMP"; echo "summary: pass=$pass fail=$fail skip=$skip"; [ "$fail" -eq 0 ]
