#!/usr/bin/env python3
"""Deterministic KiCad 9 two-layer layout for the discrete-transistor board."""
from __future__ import annotations
import heapq, math, re, uuid
from collections import defaultdict
from pathlib import Path
from xml.etree import ElementTree
import pcbnew as k
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'boards/01-logic-gates/01-logic-gates.kicad_pcb'
LIB=Path('/usr/share/kicad/footprints')
S=0.5; W=126; H=158
P=lambda x,y:k.VECTOR2I(k.FromMM(x),k.FromMM(y))
M=k.FromMM

def canonicalize_pcb(content):
    """Sort generated top-level items before assigning repeatable KIIDs."""
    starts=[];depth=0;quoted=False;escaped=False;start=None
    for i,ch in enumerate(content):
        if quoted:
            if escaped:escaped=False
            elif ch=='\\':escaped=True
            elif ch=='"':quoted=False
            continue
        if ch=='"':quoted=True
        elif ch=='(':
            if depth==1:start=i
            depth+=1
        elif ch==')':
            depth-=1
            if depth==1 and start is not None:
                starts.append((start,i+1));start=None
    blocks=[content[a:b] for a,b in starts]
    names=[re.match(r'\(([^\s()]+)',x).group(1) for x in blocks]
    for group in ({'footprint'},{'gr_line','gr_arc','gr_text','gr_poly','gr_circle'},
                  {'segment','via'},{'zone'}):
        indices=[i for i,n in enumerate(names) if n in group]
        ordered=sorted((blocks[i] for i in indices),
                       key=lambda x:re.sub(r'\(uuid "[0-9a-f-]+"\)','(uuid)',x))
        for i,item in zip(indices,ordered):blocks[i]=item
    result=[];last=0
    for (a,b),item in zip(starts,blocks):
        result.extend((content[last:a],item));last=b
    result.append(content[last:])
    counter=iter(range(1,1_000_000))
    return re.sub(r'\(uuid "[0-9a-f-]+"\)',
                  lambda _m:f'(uuid "{uuid.uuid5(uuid.NAMESPACE_URL,f"pet-ufc:pcb-item:{next(counter)}")}")',
                  ''.join(result))

def text(b,s,x,y,size=1,thick=.18,angle=0):
    t=k.PCB_TEXT(b);t.SetText(s);t.SetLayer(k.F_SilkS);t.SetPosition(P(x,y))
    t.SetTextSize(P(size,size));t.SetTextThickness(M(thick))
    t.SetTextAngle(k.EDA_ANGLE(angle,k.DEGREES_T));b.Add(t)

def line(b,a,c,width=.3,layer=k.F_SilkS):
    t=k.PCB_SHAPE(b);t.SetShape(k.SHAPE_T_SEGMENT)
    t.SetStart(P(*a));t.SetEnd(P(*c));t.SetLayer(layer);t.SetWidth(M(width));b.Add(t)

def curve(b,pts,width=.4):
    for a,c in zip(pts,pts[1:]):line(b,a,c,width)

def outline(b):
    for a,c in [((6,3),(123,3)),((126,6),(126,155)),((123,158),(6,158)),((3,155),(3,6))]:line(b,a,c,.05,k.Edge_Cuts)
    for a,m,c in [((123,3),(125.121,3.879),(126,6)),((126,155),(125.121,157.121),(123,158)),((6,158),(3.879,157.121),(3,155)),((3,6),(3.879,3.879),(6,3))]:
        t=k.PCB_SHAPE(b);t.SetShape(k.SHAPE_T_ARC);t.SetArcGeometry(P(*a),P(*m),P(*c));t.SetLayer(k.Edge_Cuts);t.SetWidth(M(.05));b.Add(t)

def art(b):
    text(b,'LOGIC GATES',65,10,2.4,.4)
    text(b,'Discrete Transistor Logic | Board 01 | Rev A',65,16,.9)
    text(b,'PET Engenharia Eletrica UFC | Colecao Educacional',55,152,.85)
    for cy in (43,85):
        if cy==43:
            line(b,(49,27),(70,27),.45);line(b,(49,59),(70,59),.45);line(b,(49,27),(49,59),.45)
            curve(b,[(70+16*math.cos(-math.pi/2+i*math.pi/24),cy+16*math.sin(-math.pi/2+i*math.pi/24)) for i in range(25)],.45)
        else:
            curve(b,[(49+5*math.sin(i*math.pi/24),69+32*i/24) for i in range(25)],.45)
            for sg in (-1,1):curve(b,[(49+37*i/24,cy+sg*(16-16*(i/24)**2)) for i in range(25)],.45)
    curve(b,[(50,113),(50,145),(85,129),(50,113)],.45)
    curve(b,[(88+2*math.cos(2*math.pi*i/32),129+2*math.sin(2*math.pi*i/32)) for i in range(33)],.4)
    for title,y in [('AND',43),('OR',85),('NOT',129)]:text(b,title,9,y,2,.3,90)
    for y in (43,85,129):text(b,'Z',103,y-2,1.5,.25)
    for label,y in [('A',31),('B',50),('A',73),('B',92),('A',128)]:text(b,label,31,y,1.6,.24)
    for y,head,rows in [(39,'A  B  Z',['0  0  0','0  1  0','1  0  0','1  1  1']),
                        (81,'A  B  Z',['0  0  0','0  1  1','1  0  1','1  1  1']),
                        (125,'A   Z',['0  1','1  0'])]:
        text(b,head,110,y-8,1);line(b,(100,y-5),(122,y-5),.18)
        for i,row in enumerate(rows):text(b,row,110,y-3+3*i,.95)
    text(b,'+5V',17,17,1.1,.22);text(b,'GND',8,25,.8)
    svg=ROOT/'assets/logos/pet_logo_silkscreen.svg'
    if svg.exists():
        for el in ElementTree.parse(svg).iter('{http://www.w3.org/2000/svg}path'):
            match=re.fullmatch(r'M([0-9.]+) ([0-9.]+)H([0-9.]+)',el.get('d',''))
            if match:
                x1,y,x2=map(float,match.groups())
                line(b,(101+x1*.09,143+y*.09),(101+x2*.09,143+y*.09),.16)

def components():
    R='Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal'
    Q='Package_TO_SOT_THT:TO-92_Inline';SW='Button_Switch_THT:SW_SPST_Omron_B3F-50xx'
    d={}
    def a(ref,val,fp,x,y,ang,n):d[ref]=(val,fp,x,y,ang,n)
    a('J1','5V INPUT','Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical',13,20,0,{'1':'5V_IN','2':'GND'})
    a('D1','1N5819','Diode_THT:D_DO-41_SOD81_P10.16mm_Horizontal',35.16,20,180,{'2':'5V_IN','1':'VCC'})
    a('C1','100nF 50V','Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P2.50mm',45,20,0,{'1':'VCC','2':'GND'})
    for sw,r,net,y in [('SW1','R1','A_AND',31),('SW2','R2','B_AND',50),('SW3','R21','A_OR',73),('SW4','R22','B_OR',92),('SW5','R23','A_NOT',128)]:
        a(sw,'B3F-4050',SW,13,y,0,{'1':'VCC','2':net})
        a(r,'10k 5%',R,33,y+2,90,{'1':net,'2':'GND'})
    for ref,src,dst,x,y in [
        ('R3','A_AND','Q1_B',46,30),('R4','B_AND','Q2_B',46,50),('R5','N_AND','Q3_B',65,39),('R6','Y_AND','Q4_B',74,62),
        ('R7','A_OR','Q5_B',46,72),('R8','B_OR','Q6_B',46,92),('R9','N_OR','Q7_B',65,81),('R10','Y_OR','Q8_B',75,95),
        ('R11','A_NOT','Q9_B',46,119),('R12','Y_NOT','Q10_B',75,136)]:a(ref,'10k 5%',R,x,y,0 if ref=='R6' else 90,{'1':src,'2':dst})
    for ref,dst,x,y in [('R13','N_AND',61,25),('R14','Y_AND',105,23),('R15','N_OR',61,67),('R16','Y_OR',77,70),('R17','Y_NOT',63,111)]:
        a(ref,'2.2k 5%',R,x,y,0,{'1':'VCC','2':dst})
    for ref,base,col,emi,x,y in [
        ('Q1','Q1_B','N_AND','N_AND_MID',57,33),('Q2','Q2_B','N_AND_MID','GND',57,49),
        ('Q3','Q3_B','Y_AND','GND',72,42),('Q4','Q4_B','LED_AND_K','GND',89,54),
        ('Q5','Q5_B','N_OR','GND',57,75),('Q6','Q6_B','N_OR','GND',57,91),
        ('Q7','Q7_B','Y_OR','GND',72,84),('Q8','Q8_B','LED_OR_K','GND',83,95),
        ('Q9','Q9_B','Y_NOT','GND',62,125),('Q10','Q10_B','LED_NOT_K','GND',83,137)]:
        a(ref,'2N3904',Q,x,y,0,{'1':emi,'2':base,'3':col})
    for r,di,gate,y in [('R18','D2','AND',43),('R19','D3','OR',85),('R20','D4','NOT',129)]:
        a(r,'1.5k 5%',R,96,y-15,90,{'1':'VCC','2':f'LED_{gate}_A'})
        a(di,'TLHR5200','LED_THT:LED_D5.0mm',94,y,0,{'1':f'LED_{gate}_K','2':f'LED_{gate}_A'})
    return d

def place(b,data):
    nets={};pads=defaultdict(list)
    for name in sorted({n for entry in data.values() for n in entry[-1].values()}):
        item=k.NETINFO_ITEM(b,'/'+name);b.Add(item);nets[name]=item
    for ref,(val,fp,x,y,ang,mapping) in data.items():
        lib,name=fp.split(':');item=k.FootprintLoad(str(LIB/f'{lib}.pretty'),name)
        if item is None:raise RuntimeError(fp)
        if ref.startswith('SW'):
            # The distro omits the footprint's B3F 3D file. A scaled stock
            # 7.3 mm pushbutton is a dimensional visualization placeholder.
            model=item.Models()[0]
            model.m_Filename='${KICAD9_3DMODEL_DIR}/Button_Switch_THT.3dshapes/SW_PUSH_6mm_H7.3mm.step'
            model.m_Scale.x=2.0;model.m_Scale.y=2.0
        item.SetReference(ref);item.SetValue(val);item.SetFPID(k.LIB_ID(lib,name))
        item.SetPosition(P(x,y));item.SetOrientationDegrees(-ang)
        item.SetPath(k.KIID_PATH('/'+str(uuid.uuid5(uuid.NAMESPACE_URL,f'pet-ufc:01-logic-gates:symbol:{ref}'))))
        item.Reference().SetVisible(True);item.Value().SetVisible(False)
        item.Reference().SetTextSize(P(.85,.85))
        item.Reference().SetTextThickness(M(.14))
        if ref in ('D2','D3','D4'):
            item.Reference().SetPosition(P(90,y-5))
        elif ref in ('R3','R4'):
            item.Reference().SetPosition(P(40,y+5))
        for pad in item.Pads():
            net=mapping.get(pad.GetNumber())
            if net:pad.SetNet(nets[net]);pads[net].append(pad)
        b.Add(item)
    return nets,pads

def routing(b,nets,pads):
    occ=[defaultdict(set),defaultdict(set)];locations=defaultdict(list)
    escapes=[];pad_holes=[]
    for net,ps in pads.items():
        for p in ps:
            v=p.GetPosition();x,y=k.ToMM(v.x),k.ToMM(v.y);gx,gy=round(x/S),round(y/S)
            pad_holes.append((x,y))
            if p.GetParentFootprint().GetReference().startswith('Q') and net!='GND':
                dy=-2.5 if p.GetNumber()=='3' else 2.5
                ex,ey=round(x/S),round((y+dy)/S)
                locations[net].append((ex,ey));escapes.append((net,(x,y),(ex*S,ey*S)))
            else:locations[net].append((gx,gy))
            radius=max(k.ToMM(p.GetSize().x),k.ToMM(p.GetSize().y))/2+.53
            for ix in range(gx-math.ceil(radius/S),gx+math.ceil(radius/S)+1):
                for iy in range(gy-math.ceil(radius/S),gy+math.ceil(radius/S)+1):
                    if math.hypot(ix*S-x,iy*S-y)<=radius:
                        for layer in occ:layer[(ix,iy)].add(net)
    for net,start,end in escapes:
        tr=k.PCB_TRACK(b);tr.SetStart(P(*start));tr.SetEnd(P(*end));tr.SetWidth(M(.35))
        tr.SetLayer(k.F_Cu);tr.SetNet(nets[net]);b.Add(tr)
        for iy in range(min(round(start[1]/S),round(end[1]/S)),max(round(start[1]/S),round(end[1]/S))+1):
            ix=round(end[0]/S)
            for ox in (-1,0,1):
                for oy in (-1,0,1):
                    if math.hypot(ox,oy)*S<.65:occ[0][ix+ox,iy+oy].add(net)
    escape_coords={(round(end[0]/S),round(end[1]/S)) for _,_,end in escapes}
    def free(x,y,z,net):return 8<=x*S<=W-5 and 7<=y*S<=H-5 and not (occ[z][x,y]-{net})
    def find(src,dst,net):
        q=[(0,0,*src,0)];distance={(*src,0):0};previous={}
        while q:
            _,cost,x,y,z=heapq.heappop(q);node=(x,y,z)
            if cost!=distance.get(node):continue
            if (x,y)==dst:
                path=[node]
                while node in previous:node=previous[node];path.append(node)
                return path[::-1]
            for dx,dy,dz,w in [(1,0,0,1),(-1,0,0,1),(0,1,0,1),(0,-1,0,1),(0,0,1,22),(0,0,-1,22)]:
                xx,yy,zz=x+dx,y+dy,z+dz
                if zz not in (0,1) or not free(xx,yy,zz,net):continue
                if dz and (not free(xx,yy,z,net) or any(math.hypot(xx*S-px,yy*S-py)<1.2 for px,py in pad_holes)):continue
                nxt=(xx,yy,zz);new=cost+w
                if new<distance.get(nxt,10**9):
                    distance[nxt]=new;previous[nxt]=node
                    heapq.heappush(q,(new+abs(xx-dst[0])+abs(yy-dst[1]),new,xx,yy,zz))
        return None
    fails=[]
    for net in sorted((n for n in pads if n!='GND'),key=lambda n:(n=='VCC',len(pads[n]),n)):
        points=list(dict.fromkeys(locations[net]));connected={points[0]};remaining=set(points[1:])
        while remaining:
            dst=min(remaining,key=lambda p:min(abs(p[0]-q[0])+abs(p[1]-q[1]) for q in connected))
            src=min(connected,key=lambda p:abs(p[0]-dst[0])+abs(p[1]-dst[1]))
            path=find(src,dst,net)
            if path is None:fails.append((net,src,dst));remaining.remove(dst);continue
            if dst in escape_coords and path[-1][2]==1:
                path.append((dst[0],dst[1],0))
            for (x,y,z),(xx,yy,zz) in zip(path,path[1:]):
                if z==zz:
                    for px,py in [(x,y),(xx,yy)]:
                        for ox in (-1,0,1):
                            for oy in (-1,0,1):
                                if math.hypot(ox,oy)*S<.65:occ[z][px+ox,py+oy].add(net)
            compact=[path[0]]
            for i in range(1,len(path)-1):
                a,b1,c=path[i-1],path[i],path[i+1]
                if a[2]==b1[2]==c[2] and (b1[0]-a[0],b1[1]-a[1])==(c[0]-b1[0],c[1]-b1[1]):
                    continue
                compact.append(b1)
            compact.append(path[-1])
            for (x,y,z),(xx,yy,zz) in zip(compact,compact[1:]):
                if z!=zz:
                    via=k.PCB_VIA(b);via.SetPosition(P(x*S,y*S))
                    via.SetViaType(k.VIATYPE_THROUGH);via.SetLayerPair(k.F_Cu,k.B_Cu)
                    via.SetWidth(k.F_Cu,M(.8));via.SetDrill(M(.4));via.SetNet(nets[net]);b.Add(via)
                else:
                    tr=k.PCB_TRACK(b);tr.SetStart(P(x*S,y*S));tr.SetEnd(P(xx*S,yy*S));tr.SetWidth(M(.35))
                    tr.SetLayer(k.F_Cu if z==0 else k.B_Cu);tr.SetNet(nets[net]);b.Add(tr)
            connected.add(dst);remaining.remove(dst)
    return fails

def main():
    b=k.BOARD();b.SetCopperLayerCount(2);b.SetFileName(str(OUT))
    ds=b.GetDesignSettings();ds.m_MinClearance=M(.2);ds.m_TrackMinWidth=M(.35)
    ds.m_ViasMinSize=M(.8);ds.m_ViasMinDrill=M(.4)
    print('outlining',flush=True);outline(b);art(b)
    print('placing',flush=True);nets,pads=place(b,components())
    print('routing',flush=True);fails=routing(b,nets,pads)
    print('zoning',flush=True)
    z=k.ZONE(b);z.SetLayer(k.B_Cu);z.SetNet(nets['GND']);z.SetLocalClearance(M(.3))
    z.SetThermalReliefGap(M(.4));z.SetThermalReliefSpokeWidth(M(.4))
    poly=z.Outline();poly.NewOutline()
    for x,y in [(4,4),(125,4),(125,157),(4,157)]:poly.Append(M(x),M(y))
    b.Add(z)
    print('saving',flush=True);k.SaveBoard(str(OUT),b)
    OUT.write_text(canonicalize_pcb(OUT.read_text(encoding='utf-8')),encoding='utf-8')
    # KiCad 9's Python zone filler needs a reloaded board here to avoid a
    # pcbnew lifetime crash with newly constructed zone/track collections.
    filled=k.LoadBoard(str(OUT));filler=k.ZONE_FILLER(filled)
    filler.Fill(filled.Zones());k.SaveBoard(str(OUT),filled)
    # pcbnew allocates fresh KIIDs for generated items. Stable KIIDs keep
    # repeat runs reviewable without changing any geometry or connectivity.
    content=canonicalize_pcb(OUT.read_text(encoding='utf-8'))
    OUT.write_text(content,encoding='utf-8')
    print('Unrouted paths:',len(fails));print(*fails,sep='\n')
if __name__=='__main__':main()
