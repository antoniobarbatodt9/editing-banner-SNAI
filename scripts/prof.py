import numpy as np, sys
from PIL import Image
i=int(sys.argv[1])
a=np.array(Image.open(f'f/{i:03d}.png')).astype(int)
v=a.mean(2)
def peaks(line):
    return [k for k in range(1,len(line)-1) if line[k]>=18 and line[k]>=line[k-1] and line[k]>=line[k+1]]
for x in [100,150,200]:
    print('x',x, peaks(v[:,x]))
for y in [int(t) for t in sys.argv[2:]]:
    print('y',y, peaks(v[y,:]))
