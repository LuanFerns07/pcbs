#!/bin/sh
set -eu
cat /etc/os-release
printf '\nTools:\n'
for tool in kicad kicad-cli python3 git; do
  if command -v "$tool" >/dev/null 2>&1; then command -v "$tool"; else printf '%s: unavailable\n' "$tool"; fi
done
python3 --version
