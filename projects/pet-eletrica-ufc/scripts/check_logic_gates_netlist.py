#!/usr/bin/env python3
"""Compare KiCad-exported schematic pin nets with every PCB pad net."""
from __future__ import annotations
import re, subprocess, tempfile
from pathlib import Path
import pcbnew
BOARD=Path(__file__).resolve().parents[1]/'boards/01-logic-gates'

def block(s,start):
    level=0;quoted=escaped=False
    for i in range(start,len(s)):
        c=s[i]
        if quoted:
            if escaped:escaped=False
            elif c=='\\':escaped=True
            elif c=='"':quoted=False
        elif c=='"':quoted=True
        elif c=='(':level+=1
        elif c==')':
            level-=1
            if not level:return s[start:i+1]
    raise ValueError('Unbalanced KiCad netlist')

def schematic_pins(s):
    result={}
    for match in re.finditer(r'\(net\s+\(code\s+',s):
        part=block(s,match.start());name=re.search(r'\(name\s+"([^"]+)"',part).group(1).lstrip('/')
        for node in re.finditer(r'\(node\s+\(ref\s+"([^"]+)"\)\s+\(pin\s+"([^"]+)"\)',part):
            ref,pin=node.groups()
            if not ref.startswith('#'):result[(ref,pin)]=name
    return result

def schematic_components(s):
    result={}
    for match in re.finditer(r'\(comp\s+\(ref\s+"([^"]+)"\)',s):
        part=block(s,match.start());ref=match.group(1)
        value=re.search(r'\(value\s+"([^"]+)"',part)
        footprint=re.search(r'\(footprint\s+"([^"]+)"',part)
        if value and footprint:result[ref]=(value.group(1),footprint.group(1))
    return result

def main():
    sch=BOARD/'01-logic-gates.kicad_sch';pcb=BOARD/'01-logic-gates.kicad_pcb'
    with tempfile.TemporaryDirectory(prefix='pet-net-') as td:
        net=Path(td)/'board.net'
        subprocess.run(['kicad-cli','sch','export','netlist',str(sch),'--output',str(net)],check=True)
        source=net.read_text()
        expected=schematic_pins(source)
        expected_components=schematic_components(source)
    actual={}
    actual_components={}
    board=pcbnew.LoadBoard(str(pcb))
    for fp in board.GetFootprints():
        actual_components[fp.GetReference()]=(fp.GetValue(),fp.GetFPIDAsString())
        for pad in fp.Pads():
            if not pad.GetNumber():continue
            key=(fp.GetReference(),pad.GetNumber());name=pad.GetNetname().lstrip('/')
            if key in actual and actual[key]!=name:raise AssertionError(f'Duplicate pin with conflicting nets: {key}')
            actual[key]=name
    errors=[]
    for key in sorted(set(expected)|set(actual)):
        if expected.get(key)!=actual.get(key):errors.append(f'{key}: schematic={expected.get(key)} PCB={actual.get(key)}')
    for ref in sorted(set(expected_components)|set(actual_components)):
        if expected_components.get(ref)!=actual_components.get(ref):
            errors.append(f'{ref}: schematic part={expected_components.get(ref)} PCB part={actual_components.get(ref)}')
    if errors:
        print('\n'.join(errors));return 1
    if not board.Zones() or not all(z.IsFilled() for z in board.Zones()):
        print('Ground zone missing or unfilled');return 1
    print(f'Parity verified: {len(expected)} pins/pads and {len(expected_components)} part values/footprints; filled zones present.')
    return 0
if __name__=='__main__':raise SystemExit(main())
