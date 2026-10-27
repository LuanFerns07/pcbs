#!/usr/bin/env python3
"""Check the board and required manufacturing artifacts after KiCad exports."""
from pathlib import Path
import re
import pcbnew as k
ROOT=Path(__file__).resolve().parents[1]/'boards/01-logic-gates'
OUT=ROOT/'manufacturing'
BOARD=ROOT/'01-logic-gates.kicad_pcb'
REQUIRED=[
    'gerbers/01-logic-gates-F_Cu.gtl','gerbers/01-logic-gates-B_Cu.gbl',
    'gerbers/01-logic-gates-F_Mask.gts','gerbers/01-logic-gates-B_Mask.gbs',
    'gerbers/01-logic-gates-F_Silkscreen.gto','gerbers/01-logic-gates-B_Silkscreen.gbo',
    'gerbers/01-logic-gates-Edge_Cuts.gm1',
    'drill/01-logic-gates-PTH.drl','drill/01-logic-gates-NPTH.drl',
    'BOM.csv','schematic.pdf','front-assembly.pdf','back-assembly.pdf',
    'front-layout.svg','back-layout.svg','01-logic-gates.step','01-logic-gates.glb',
    'ERC.rpt','DRC.rpt','simulation.csv',
]
def main():
    missing=[p for p in REQUIRED if not (OUT/p).is_file() or (OUT/p).stat().st_size==0]
    if missing:raise SystemExit('Missing/empty manufacturing files: '+', '.join(missing))
    board=k.LoadBoard(str(BOARD))
    box=board.GetBoardEdgesBoundingBox()
    width,height=k.ToMM(box.GetWidth()),k.ToMM(box.GetHeight())
    if board.GetCopperLayerCount()!=2 or abs(width-123)>.1 or abs(height-155)>.1:
        raise SystemExit(f'Unexpected outline/layers: {width:.2f} x {height:.2f} mm, {board.GetCopperLayerCount()} layers')
    if not board.Zones() or not all(z.IsFilled() for z in board.Zones()):
        raise SystemExit('Unfilled copper zone')
    refs=[f.GetReference() for f in board.GetFootprints()]
    if len(refs)!=len(set(refs)):raise SystemExit('Duplicate footprint references')
    pads=[p for f in board.GetFootprints() for p in f.Pads() if p.HasDrilledHole()]
    vias=[t for t in board.GetTracks() if isinstance(t,k.PCB_VIA)]
    for report in ('ERC.rpt','DRC.rpt'):
        s=(OUT/report).read_text()
        if not re.search(r'Found 0 (?:DRC )?violations|0  Errors 0  Warnings',s):
            raise SystemExit(f'{report} contains violations')
    if not (OUT/'01-logic-gates.step').read_bytes().startswith(b'ISO-10303-21'):
        raise SystemExit('STEP header invalid')
    if (OUT/'01-logic-gates.glb').read_bytes()[:4]!=b'glTF':
        raise SystemExit('GLB header invalid')
    summary=(f'KiCad board: {width:.1f} x {height:.1f} mm; 2 copper layers; '
             f'{len(refs)} footprints; {len(pads)} drilled pads; {len(vias)} vias; '
             f'{len(list(board.Zones()))} filled GND zone; {len(REQUIRED)} required exports present.\n'
             'ERC and DRC reports show zero violations. Physical prototype untested.\n')
    (ROOT/'reports/manufacturing-check.txt').write_text(summary)
    print(summary,end='')
if __name__=='__main__':main()
