import cut, numpy as np, json
from scipy import ndimage as nd
from PIL import Image
from cut3 import cut3
exec(open('cut3.py').read().split("if __name__")[0])
import importlib
def cut2(bx,thr=60):
  x0,y0,x1,y1=bx;a=cut.im[y0:y1,x0:x1];r,g,b=a[...,0],a[...,1],a[...,2]
  lum=a@[.299,.587,.114]
  bgl=(r>=b-12)&(b>.42*r)&(lum>thr)&(r>g-5)
  lab,n=nd.label(bgl)
  border=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
  fg=~np.isin(lab,list(border))
  if not NOOPEN:fg=nd.binary_opening(fg,iterations=1)
  return a,fg
def clean(fg):
  l2,n2=nd.label(fg)
  if n2:
    sz=nd.sum(fg,l2,range(1,n2+1));keep=[i+1 for i,s in enumerate(sz) if s>max(sz)*.06]
    fg=np.isin(l2,keep)
  return fg
NOOPEN=False
F=3;CW,CH=56,44;AX,AY=28,41
B=cut.boxes();cells=[];meta=[]
for ci,cls in enumerate(B):
  for si,bx in enumerate(cls):
    NOOPEN=(ci,si) in ((0,0),(9,0),(6,1),(9,1));globals()['NOOPEN']=NOOPEN
    a,fg=cut2(bx)
    if ci==3:
      _,f1=cut.cut(bx,70);fg=fg|f1
    fg=clean(fg)
    h,w=fg.shape;h2,w2=h//F,w//F
    out=np.zeros((h2,w2,4),np.uint8)
    lum=a@[.299,.587,.114]
    for y in range(h2):
      for x in range(w2):
        m=fg[y*F:y*F+F,x*F:x*F+F]
        if m.sum()<3:continue
        px=a[y*F:y*F+F,x*F:x*F+F][m];L=lum[y*F:y*F+F,x*F:x*F+F][m]
        if (L<55).sum()>=3:c=px[L.argmin()]
        else:
          mu=px.mean(0);c=px[((px-mu)**2).sum(1).argmin()]
        out[y,x,:3]=c;out[y,x,3]=255
    al=out[...,3]>0
    ys,xs=np.nonzero(al)
    by=ys.max();low=ys>by-(by-ys.min())*.3
    fx=int(np.median(xs[low]))
    cell=np.zeros((CH,CW,4),np.uint8)
    dx,dy=AX-fx,AY-by
    for y,x in zip(ys,xs):
      X,Y=x+dx,y+dy
      if 0<=X<CW and 0<=Y<CH:cell[Y,X]=out[y,x]
    cells.append(cell)
atlas=np.zeros((CH*10,CW*7,4),np.uint8)
for i,c in enumerate(cells):
  r,k=divmod(i,7);atlas[r*CH:(r+1)*CH,k*CW:(k+1)*CW]=c
Image.fromarray(atlas).save('atlas.png',optimize=True)
big=Image.new('RGBA',(CW*7*4,CH*10*4),(60,110,60,255));big.alpha_composite(Image.fromarray(atlas).resize((CW*7*4,CH*10*4),Image.NEAREST));big.save('atlas_x4.png')
