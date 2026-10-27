#!/usr/bin/env python3
"""Run reproducible ngspice DC checks for all logic input combinations.

The compact transistor/diode models are illustrative, not vendor-qualified.
The circuit topology and resistor values mirror the KiCad schematic.
"""
from __future__ import annotations
import csv, os, re, shutil, subprocess, tempfile
from pathlib import Path
BOARD=Path(__file__).resolve().parents[1]/'boards/01-logic-gates'
REPORT=BOARD/'reports/simulation.csv'
BODY='''PET UFC discrete transistor logic gates - DC model
VMAIN VIN 0 {supply}
DPROT VIN VCC DSH
C1 VCC 0 100n
* Five independent active-high switches and their pull-downs.
R1 A_AND 0 10k
R2 B_AND 0 10k
R21 A_OR 0 10k
R22 B_OR 0 10k
R23 A_NOT 0 10k
EAA A_AND 0 VCC 0 {a}
EBA B_AND 0 VCC 0 {b}
EAO A_OR 0 VCC 0 {a}
EBO B_OR 0 VCC 0 {b}
EAN A_NOT 0 VCC 0 {a}
* AND: Q1/Q2 series NAND, Q3 output inverter, Q4 LED buffer.
R3 A_AND Q1_B 10k
R4 B_AND Q2_B 10k
Q1 N_AND Q1_B N_AND_MID NPN3904
Q2 N_AND_MID Q2_B 0 NPN3904
R13 VCC N_AND 2.2k
R5 N_AND Q3_B 10k
Q3 Y_AND Q3_B 0 NPN3904
R14 VCC Y_AND 2.2k
R6 Y_AND Q4_B 10k
Q4 LED_AND_K Q4_B 0 NPN3904
R18 VCC LED_AND_A 1.5k
D2 LED_AND_A LED_AND_K REDLED
* OR: Q5/Q6 parallel NOR, Q7 output inverter, Q8 LED buffer.
R7 A_OR Q5_B 10k
R8 B_OR Q6_B 10k
Q5 N_OR Q5_B 0 NPN3904
Q6 N_OR Q6_B 0 NPN3904
R15 VCC N_OR 2.2k
R9 N_OR Q7_B 10k
Q7 Y_OR Q7_B 0 NPN3904
R16 VCC Y_OR 2.2k
R10 Y_OR Q8_B 10k
Q8 LED_OR_K Q8_B 0 NPN3904
R19 VCC LED_OR_A 1.5k
D3 LED_OR_A LED_OR_K REDLED
* NOT: Q9 common-emitter inverter, Q10 LED buffer.
R11 A_NOT Q9_B 10k
Q9 Y_NOT Q9_B 0 NPN3904
R17 VCC Y_NOT 2.2k
R12 Y_NOT Q10_B 10k
Q10 LED_NOT_K Q10_B 0 NPN3904
R20 VCC LED_NOT_A 1.5k
D4 LED_NOT_A LED_NOT_K REDLED
.model NPN3904 NPN(IS=1e-14 BF=80 VAF=50)
.model REDLED D(IS=1e-17 N=2 RS=10)
.model DSH D(IS=1e-5 N=1.2 RS=0.2)
.control
op
print v(vcc) v(a_and) v(b_and) v(y_and) v(y_or) v(y_not)
print v(n_and) v(n_and_mid) v(n_or) v(led_and_k) v(led_or_k) v(led_not_k)
print @d2[id] @d3[id] @d4[id]
quit
.endc
.end
'''
FIELDS=['VIN_V','A','B','VCC_V','A_V','B_V','AND_V','OR_V','NOT_V','NAND_V','NOR_V','LED_AND_mA','LED_OR_mA','LED_NOT_mA','Q1_VCE','Q2_VCE','Q3_VCE','Q4_VCE','Q5_VCE','Q6_VCE','Q7_VCE','Q8_VCE','Q9_VCE','Q10_VCE']

def main():
    binary=os.environ.get('NGSPICE') or shutil.which('ngspice')
    if not binary:raise SystemExit('ngspice unavailable; set NGSPICE=/path/to/ngspice')
    rows=[]
    with tempfile.TemporaryDirectory(prefix='pet-spice-') as temp:
        for supply in (4.75,5.0,5.25):
          for a in (0,1):
            for b in (0,1):
                deck=Path(temp)/f'logic-{supply}-{a}{b}.cir';deck.write_text(BODY.format(a=a,b=b,supply=supply))
                run=subprocess.run([binary,'-b',str(deck)],capture_output=True,text=True,check=True)
                values={name:float(number) for name,number in re.findall(r'([@a-zA-Z0-9_()\[\]]+)\s*=\s*([-+0-9.eE]+)',run.stdout)}
                required=['v(vcc)','v(a_and)','v(b_and)','v(y_and)','v(y_or)','v(y_not)',
                          'v(n_and)','v(n_and_mid)','v(n_or)','v(led_and_k)','v(led_or_k)','v(led_not_k)',
                          '@d2[id]','@d3[id]','@d4[id]']
                missing=set(required)-set(values)
                if missing:raise RuntimeError(f'Incomplete ngspice output: {missing}\n{run.stdout}\n{run.stderr}')
                v=lambda n:values[f'v({n})']
                row=[supply,a,b,v('vcc'),v('a_and'),v('b_and'),v('y_and'),v('y_or'),v('y_not'),
                     v('n_and'),v('n_or'),values['@d2[id]']*1000,values['@d3[id]']*1000,values['@d4[id]']*1000,
                     v('n_and')-v('n_and_mid'),v('n_and_mid'),v('y_and'),v('led_and_k'),
                     v('n_or'),v('n_or'),v('y_or'),v('led_or_k'),v('y_not'),v('led_not_k')]
                result=dict(zip(FIELDS,row))
                expected={'AND_V':a & b,'OR_V':a | b,'NOT_V':1-a}
                for key,logic in expected.items():
                    volts=result[key]
                    if not (volts>=3.5 if logic else volts<=0.4):
                        raise AssertionError(f'{a}{b} {key}: {volts:.3f} V, expected {logic}')
                rows.append(result)
    REPORT.parent.mkdir(exist_ok=True)
    with REPORT.open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=FIELDS,lineterminator='\n');writer.writeheader();writer.writerows(rows)
    print(f'{len(rows)} input combinations passed; report: {REPORT}')
    for r in rows:
        print(f"VIN={r['VIN_V']:.2f}V A={r['A']} B={r['B']} AND={r['AND_V']:.3f}V OR={r['OR_V']:.3f}V NOT={r['NOT_V']:.3f}V LED={r['LED_AND_mA']:.2f}/{r['LED_OR_mA']:.2f}/{r['LED_NOT_mA']:.2f}mA")
if __name__=='__main__':main()
