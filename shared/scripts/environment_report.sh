#!/bin/sh
set -eu
cat /etc/os-release
printf '\nTools:\n'
for tool in kicad kicad-cli python3 git; do
  if command -v "$tool" >/dev/null 2>&1; then command -v "$tool"; else printf '%s: unavailable\n' "$tool"; fi
done
python3 --version
if command -v kicad-cli >/dev/null 2>&1; then
  printf '\nkicad-cli version: '
  kicad-cli version
fi
python3 -c 'import pcbnew; print("pcbnew:", pcbnew.GetBuildVersion())' 2>&1 || printf 'pcbnew: unavailable for system Python\n'
