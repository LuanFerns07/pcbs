#!/usr/bin/env python3
"""Make 2D plot and an explicitly illustrative isometric assembly preview."""
from pathlib import Path
from subprocess import run
from PIL import Image, ImageDraw, ImageFont
from generate_logic_gates_pcb import components, OUT
ROOT=Path(__file__).resolve().parents[1]
RENDERS=ROOT/'boards/01-logic-gates/renders';RENDERS.mkdir(exist_ok=True)
SVG=RENDERS/'01-logic-gates-front.svg';PNG=RENDERS/'01-logic-gates-2d.png'
run(['kicad-cli','pcb','export','svg','--mode-single','-l','F.SilkS,F.Mask,Edge.Cuts',
     '--page-size-mode','2','--exclude-drawing-sheet','--black-and-white',
     '--output',str(SVG),str(OUT)],check=True)
run(['convert','-background','white',str(SVG),'-resize','1000x',str(PNG)],check=True)
SVG.unlink()
back_svg=RENDERS/'01-logic-gates-back.svg'
run(['kicad-cli','pcb','export','svg','--mode-single','-l','B.SilkS,B.Mask,Edge.Cuts',
     '--page-size-mode','2','--exclude-drawing-sheet','--black-and-white','--mirror',
     '--output',str(back_svg),str(OUT)],check=True)
run(['convert','-background','white',str(back_svg),'-resize','1000x',
     str(RENDERS/'01-logic-gates-back.png')],check=True)
back_svg.unlink()
source=Image.open(PNG).convert('RGBA')
w,h=source.size
canvas=Image.new('RGBA',(1320,930),(238,242,246,255))
quad=[(285,80),(1185,205),(1015,855),(105,710)]

def solve(A,b):
    A=[row+[value] for row,value in zip(A,b)]
    for i in range(8):
        j=max(range(i,8),key=lambda r:abs(A[r][i]));A[i],A[j]=A[j],A[i]
        s=A[i][i];A[i]=[v/s for v in A[i]]
        for j in range(8):
            if i!=j:
                t=A[j][i];A[j]=[a-t*c for a,c in zip(A[j],A[i])]
    return [A[i][-1] for i in range(8)]
A=[];B=[]
for (x,y),(u,v) in zip(quad,[(0,0),(w,0),(w,h),(0,h)]):
    A.extend([[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]])
    B.extend([u,v])
coeff=solve(A,B)
warped=source.transform(canvas.size,Image.Transform.PERSPECTIVE,coeff,
                        resample=Image.Resampling.BICUBIC,fillcolor=(0,0,0,0))
# Board thickness, then white solder mask and silk from KiCad's own plot.
draw=ImageDraw.Draw(canvas)
for a,b in [(0,1),(1,2),(2,3)]:
    p,q=quad[a],quad[b]
    draw.polygon([p,q,(q[0],q[1]+15),(p[0],p[1]+15)],fill=(140,150,165,255))
canvas.alpha_composite(warped)
draw=ImageDraw.Draw(canvas)

def project(x,y):
    u=(x-3)/123;v=(y-3)/155
    x0=(1-u)*quad[0][0]+u*quad[1][0];y0=(1-u)*quad[0][1]+u*quad[1][1]
    x1=(1-u)*quad[3][0]+u*quad[2][0];y1=(1-u)*quad[3][1]+u*quad[2][1]
    return ((1-v)*x0+v*x1,(1-v)*y0+v*y1)

def box(x,y,rx,ry,height,color):
    pts=[project(x-rx,y-ry),project(x+rx,y-ry),project(x+rx,y+ry),project(x-rx,y+ry)]
    top=[(p[0],p[1]-height) for p in pts]
    draw.polygon([pts[2],pts[3],top[3],top[2]],fill=tuple(max(0,int(c*.72)) for c in color)+(255,))
    draw.polygon([pts[1],pts[2],top[2],top[1]],fill=tuple(max(0,int(c*.8)) for c in color)+(255,))
    draw.polygon(top,fill=color+(255,),outline=(65,65,65,255))

items=components()
for ref,(value,fp,x,y,angle,nets) in items.items():
    if ref.startswith('SW'):
        box(x+6.25,y,.0+6.1,4,19,(32,35,39))
        px,py=project(x+6.25,y)
        draw.ellipse((px-15,py-34,px+15,py-4),fill=(13,16,21,255),outline=(85,85,85,255),width=2)
    elif ref.startswith('Q'):
        box(x+1.3,y,2.2,1.8,10,(22,24,28))
    elif ref.startswith('R'):
        if angle==90:box(x,y+5.08,1.1,3.1,5,(214,184,128))
        else:box(x+5.08,y,3.1,1.1,5,(214,184,128))
    elif ref in ('D2','D3','D4'):
        px,py=project(x+1.27,y)
        draw.ellipse((px-17,py-25,px+17,py+9),fill=(183,13,22,255),outline=(83,5,8,255),width=2)
        draw.ellipse((px-8,py-19,px+3,py-11),fill=(255,184,184,255))
    elif ref=='D1':box(x-5.08,y,4,1.6,4,(30,30,34))
    elif ref=='C1':box(x+1.25,y,2.2,1.3,8,(186,111,49))
    elif ref=='J1':box(x,y+1.27,2.8,2.8,13,(25,27,30))
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',19)
draw.text((47,874),'Illustrative 3D preview from current KiCad PCB; component shapes are approximate.',font=font,fill=(48,57,67,255))
canvas.convert('RGB').save(RENDERS/'01-logic-gates-3d-preview.png',quality=95)
canvas.convert('RGB').save(RENDERS/'01-logic-gates-3d.png',quality=95)
print('Saved 2D and illustrative 3D previews.')
