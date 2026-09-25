import numpy as np, cv2
from PIL import Image
def cards(i):
    a=np.array(Image.open(f'f/{i:03d}.png')).astype(int)
    r,g,b=a[...,0],a[...,1],a[...,2]
    m=((b-r)>=3)&((b-r)<=8)&(r<=12)&(abs(g-r)<=2)
    m=m.astype(np.uint8)
    m[:40]=0; m[520:]=0
    m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,np.ones((9,9),np.uint8))
    n,l,st,c=cv2.connectedComponentsWithStats(m)
    out=[tuple(st[k][:4]) for k in range(1,n) if st[k][4]>1500]
    return sorted(out,key=lambda s:s[1])
for i in range(40,136):
    print(i, cards(i))
