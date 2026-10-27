#!/usr/bin/env bash
set -euo pipefail
project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
board_dir="$project_dir/boards/01-logic-gates"
board="$board_dir/01-logic-gates.kicad_pcb"
sch="$board_dir/01-logic-gates.kicad_sch"
out="$board_dir/manufacturing"
if [[ -z "${KICAD_CONFIG_HOME:-}" ]]; then
  export KICAD_CONFIG_HOME
  KICAD_CONFIG_HOME="$(mktemp -d "${TMPDIR:-/tmp}/pet-kicad-export.XXXXXX")"
  trap 'rm -rf "$KICAD_CONFIG_HOME"' EXIT
  mkdir -p "$KICAD_CONFIG_HOME/9.0"
  cp /usr/share/kicad/template/sym-lib-table /usr/share/kicad/template/fp-lib-table "$KICAD_CONFIG_HOME/9.0/"
  printf '(design_block_lib_table\n  (version 7)\n)\n' > "$KICAD_CONFIG_HOME/9.0/design-block-lib-table"
fi
mkdir -p "$out/gerbers" "$out/drill"
"$project_dir/scripts/validate_logic_gates.sh"
kicad-cli pcb export gerbers "$board" --layers F.Cu,B.Cu,F.Mask,B.Mask,F.SilkS,B.SilkS,Edge.Cuts,F.Fab,B.Fab --output "$out/gerbers"
kicad-cli pcb export drill "$board" --format excellon --excellon-units mm --excellon-separate-th --generate-map --map-format pdf --output "$out/drill"
kicad-cli sch export pdf "$sch" --output "$out/schematic.pdf"
kicad-cli pcb export pdf "$board" --mode-single --layers F.SilkS,F.Mask,Edge.Cuts --black-and-white --output "$out/front-assembly.pdf"
kicad-cli pcb export pdf "$board" --mode-single --layers B.SilkS,B.Mask,Edge.Cuts --black-and-white --mirror --output "$out/back-assembly.pdf"
kicad-cli pcb export svg "$board" --mode-single --layers F.SilkS,F.Mask,Edge.Cuts --black-and-white --exclude-drawing-sheet --page-size-mode 2 --output "$out/front-layout.svg"
kicad-cli pcb export svg "$board" --mode-single --layers B.SilkS,B.Mask,Edge.Cuts --black-and-white --exclude-drawing-sheet --mirror --page-size-mode 2 --output "$out/back-layout.svg"
sed -i 's/[[:blank:]]*$//' "$out/front-layout.svg" "$out/back-layout.svg"
kicad-cli pcb export step "$board" --output "$out/01-logic-gates.step" --force
kicad-cli pcb export glb "$board" --include-silkscreen --include-soldermask --output "$out/01-logic-gates.glb" --force
cp "$board_dir/BOM.csv" "$out/BOM.csv"
cp "$board_dir/reports/ERC.rpt" "$out/ERC.rpt"
cp "$board_dir/reports/DRC.rpt" "$out/DRC.rpt"
if [[ -f "$board_dir/reports/simulation.csv" ]]; then cp "$board_dir/reports/simulation.csv" "$out/simulation.csv"; fi
python3 "$project_dir/scripts/check_manufacturing.py"
cp "$board_dir/reports/manufacturing-check.txt" "$out/manufacturing-check.txt"
find "$out" -type f -printf '%P %s bytes\n' | sort
