import cut, numpy as np
from scipy import ndimage as nd
from PIL import Image
def cut3(bx,thr=60):
  x0,y0,x1,y1=bx;a=cut.im[y0:y1,x0:x1];r,g,b=a[...,0],a[...,1],a[...,2]
  lum=a@[.299,.587,.114]
  bgl=(r>=b-12)&(b>.42*r)&(lum>thr)&(r>g-5)&(b>=g-6)
  lab,n=nd.label(bgl)
  border=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
  fg=~np.isin(lab,list(border))
  fg=nd.binary_opening(fg,iterations=1)
  l2,n2=nd.label(fg)
  if n2:
    sz=nd.sum(fg,l2,range(1,n2+1));keep=[i+1 for i,s in enumerate(sz) if s>max(sz)*.06]
    fg=np.isin(l2,keep)
  return a,fg
if __name__=='__main__':
  B=cut.boxes();tiles=[]
  for cls in B:
    for bx in cls:
      a,fg=cut3(bx);rgba=np.zeros(a.shape[:2]+(4,),np.uint8);rgba[...,:3]=a;rgba[...,3]=fg*255
      t=Image.new('RGBA',(160,125),(40,140,60,255));t.alpha_composite(Image.fromarray(rgba),(0,0));tiles.append(t)
  sheet=Image.new('RGBA',(160*7,125*10))
  for i,t in enumerate(tiles):sheet.paste(t,((i%7)*160,(i//7)*125))
  sheet.save('cut3.png')
