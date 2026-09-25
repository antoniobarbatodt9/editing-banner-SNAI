import numpy as np, sys
from PIL import Image
i=int(sys.argv[1])
a=np.array(Image.open(f'f/{i:03d}.png')).astype(int)
v=a.max(2)
cards={'bet365':(88,80,211,198),'snai':(66,210,234,358),'wh':(87,380,212,486)}
for n,(x0,y0,x1,y1) in cards.items():
    sub=v[y0+3:y1-2,x0+3:x1-2]
    rows=np.where((sub>110).sum(1)>0)[0]
    # group rows into runs
    runs=[];s=rows[0];p=rows[0]
    for r in rows[1:]:
        if r>p+1: runs.append((s,p)); s=r
        p=r
    runs.append((s,p))
    print(n,'card',x1-x0+1,'x',y1-y0+1)
    for s,e in runs:
        cols=np.where((sub[s:e+1]>110).sum(0)>0)[0]
        print('   run y',s+y0+3,e+y0+3,'h',e-s+1,' x',cols[0]+x0+3,cols[-1]+x0+3,'w',cols[-1]-cols[0]+1)
