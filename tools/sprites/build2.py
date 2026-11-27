# Découpe la 2e planche (10 nouvelles troupes) -> atlas2.png (10 lignes x 7 sprites de 56x44, pied a (28,41))
import numpy as np, sys
from scipy import ndimage as nd
from PIL import Image
SRC=sys.argv[1] if len(sys.argv)>1 else 'docs/art/planche-personnages-2.png';OUT=sys.argv[2] if len(sys.argv)>2 else 'atlas2.png'
im=np.asarray(Image.open(SRC).convert('RGB')).astype(int)
CW,CH,AX,AY=56,44,28,41
def boxes():
  out=[]
  for c in range(5):  # ligne du haut : recrue + 2 voies x 3 rangs (meme gabarit que la 1re planche)
    x0=int(c*307.2);y0=0
    b=[((x0+80,y0+80,x0+240,y0+194),3)]
    for cx in (x0+92,x0+232):
      for ya,yb in ((y0+214,y0+328),(y0+334,y0+435),(y0+434,y0+512)):
        b.append(((max(x0+6,cx-80),ya,min(x0+302,cx+80),yb),3))
    out.append(b)
  for c in range(5):  # ligne du bas : recrue + 2 voies x 2 rangs
    x0=int(c*307.2);y0=512
    b=[((x0+95,y0+78,x0+225,y0+182),3)]
    for cx in (x0+88,x0+232):
      b.append(((max(x0+6,cx-80),y0+200,min(x0+302,cx+82),y0+308),3))
      b.append(((max(x0+4,cx-84),y0+318,min(x0+304,cx+84),y0+500),4))
    # ordre : recrue, voie1 r1,r2,(r2) , voie2 ...
    out.append([b[0],b[1],b[2],b[2],b[3],b[4],b[4]])
  return out
UNION=False
def cut(bx,thr=60,opening=True):
  x0,y0,x1,y1=bx;a=im[y0:y1,x0:x1];r,g,b=a[...,0],a[...,1],a[...,2]
  lum=a@[.299,.587,.114]
  bgl=(r>=b-12)&(b>.42*r)&(lum>thr)&(r>g-5)
  # fleches blanches/grises claires et texte : traites comme fond s'ils touchent le bord
  lab,n=nd.label(bgl)
  border=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
  fg=~np.isin(lab,list(border))
  if opening:fg=nd.binary_opening(fg,iterations=1)
  if UNION:  # contour sombre : garde les peaux claires (crânes rasés) et les lames
    dark=lum<70;dark=nd.binary_closing(dark,iterations=1)|dark
    l3,n3=nd.label(~dark);b3=set(np.unique(np.concatenate([l3[0],l3[-1],l3[:,0],l3[:,-1]])))-{0}
    f2=~np.isin(l3,list(b3))
    # on retire les poches de fond rose enfermees
    pink=bgl&(lum>110)&(b>g+12)&(r>b+40)
    f2&=~(pink&~fg)
    fg=fg|f2
  l2,n2=nd.label(fg)
  if n2:
    sz=nd.sum(fg,l2,range(1,n2+1));keep=[i+1 for i,s in enumerate(sz) if s>max(sz)*.06]
    fg=np.isin(l2,keep)
  return a,fg
def down(a,fg,F):
  h,w=fg.shape;h2,w2=h//F,w//F;out=np.zeros((h2,w2,4),np.uint8);lum=a@[.299,.587,.114]
  for y in range(h2):
    for x in range(w2):
      m=fg[y*F:y*F+F,x*F:x*F+F]
      if m.sum()<max(3,F*F//3):continue
      px=a[y*F:y*F+F,x*F:x*F+F][m];L=lum[y*F:y*F+F,x*F:x*F+F][m]
      if (L<55).sum()>=3:c=px[L.argmin()]
      else:mu=px.mean(0);c=px[((px-mu)**2).sum(1).argmin()]
      out[y,x,:3]=c;out[y,x,3]=255
  return out
cells=[]
UNIONS=set(range(10))  # contour sombre en plus du fond rose, pour toutes les classes
for ci,cls in enumerate(boxes()):
  for si,(bx,F) in enumerate(cls):
    globals()['UNION']=ci in UNIONS
    a,fg=cut(bx)
    out=down(a,fg,F)
    ys,xs=np.nonzero(out[...,3])
    by=ys.max();low=ys>by-(by-ys.min())*.3;fx=int(np.median(xs[low]))
    cell=np.zeros((CH,CW,4),np.uint8);dx,dy=AX-fx,AY-by;lost=0
    for y,x in zip(ys,xs):
      X,Y=x+dx,y+dy
      if 0<=X<CW and 0<=Y<CH:cell[Y,X]=out[y,x]
      else:lost+=1
    if lost:print('cellule',ci,si,'pixels hors cadre',lost,'taille',out.shape)
    cells.append(cell)
atlas=np.zeros((CH*10,CW*7,4),np.uint8)
for i,c in enumerate(cells):
  r,k=divmod(i,7);atlas[r*CH:(r+1)*CH,k*CW:(k+1)*CW]=c
Image.fromarray(atlas).save(OUT,optimize=True)
big=Image.new('RGBA',(CW*7*4,CH*10*4),(60,110,60,255));big.alpha_composite(Image.fromarray(atlas).resize((CW*7*4,CH*10*4),Image.NEAREST));big.save(OUT.replace('.png','_x4.png'))
