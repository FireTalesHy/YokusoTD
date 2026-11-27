import numpy as np, sys
from PIL import Image
from scipy import ndimage as nd
im=np.asarray(Image.open('docs/art/planche-personnages.png').convert('RGB')).astype(int)
def boxes():
  out=[]
  for r in range(2):
    for c in range(5):
      x0=int(c*307.2);y0=r*512
      b=[(x0+95,y0+72,x0+225,y0+178)]
      for col,cx in ((0,x0+92),(1,x0+232)):
        for k,(ya,yb) in enumerate(((y0+182,y0+290),(y0+288,y0+390),(y0+382,y0+505))):
          b.append((max(x0+6,cx-80),ya,min(x0+302,cx+80),yb))
      out.append(b)
  return out
def cut(bx,thr):
  x0,y0,x1,y1=bx;a=im[y0:y1,x0:x1]
  lum=a@[.299,.587,.114]
  dark=lum<thr
  dark=nd.binary_closing(dark,iterations=1)|dark
  free=~dark
  lab,n=nd.label(free)
  border=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
  bg=np.isin(lab,list(border))
  fg=~bg
  # keep largest component(s)
  l2,n2=nd.label(fg)
  if n2:
    sz=nd.sum(fg,l2,range(1,n2+1));keep=[i+1 for i,s in enumerate(sz) if s>max(sz)*.08]
    fg=np.isin(l2,keep)
  return a,fg
if __name__=='__main__':
  thr=float(sys.argv[1]) if len(sys.argv)>1 else 70
  B=boxes();tiles=[]
  for cls in B:
    for bx in cls:
      a,fg=cut(bx,thr);rgba=np.zeros(a.shape[:2]+(4,),np.uint8);rgba[...,:3]=a;rgba[...,3]=fg*255
      t=Image.new('RGBA',(160,125),(40,140,60,255));t.alpha_composite(Image.fromarray(rgba),(0,0));tiles.append(t)
  sheet=Image.new('RGBA',(160*7,125*10))
  for i,t in enumerate(tiles):sheet.paste(t,((i%7)*160,(i//7)*125))
  sheet.save('cut.png')
