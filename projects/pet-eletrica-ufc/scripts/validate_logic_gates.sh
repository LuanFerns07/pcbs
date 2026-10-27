#!/usr/bin/env bash
set -euo pipefail

project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
board_dir="$project_dir/boards/01-logic-gates"
config_home="${KICAD_CONFIG_HOME:-}"
temp_config=0

if [[ -z "$config_home" ]]; then
  config_home="$(mktemp -d "${TMPDIR:-/tmp}/pet-kicad-config.XXXXXX")"
  mkdir -p "$config_home/9.0"
  cp /usr/share/kicad/template/sym-lib-table "$config_home/9.0/"
  cp /usr/share/kicad/template/fp-lib-table "$config_home/9.0/"
  printf '(design_block_lib_table\n  (version 7)\n)\n' > "$config_home/9.0/design-block-lib-table"
  temp_config=1
fi

cleanup() {
  if [[ "$temp_config" == 1 ]]; then
    rm -rf "$config_home"
  fi
}
trap cleanup EXIT

python3 "$project_dir/scripts/generate_schematic.py"
python3 "$project_dir/scripts/generate_logic_gates_pcb.py"
KICAD_CONFIG_HOME="$config_home" python3 "$project_dir/scripts/check_logic_gates_netlist.py"
KICAD_CONFIG_HOME="$config_home" kicad-cli sch erc \
  "$board_dir/01-logic-gates.kicad_sch" \
  --output "$board_dir/reports/ERC.rpt" --severity-all --exit-code-violations
KICAD_CONFIG_HOME="$config_home" kicad-cli pcb drc "$board_dir/01-logic-gates.kicad_pcb" \
  --output "$board_dir/reports/DRC.rpt" --severity-all --schematic-parity --exit-code-violations
KICAD_CONFIG_HOME="$config_home" kicad-cli sch export bom "$board_dir/01-logic-gates.kicad_sch" \
  --output "$board_dir/BOM.csv"
