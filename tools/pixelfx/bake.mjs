import { createFx, createFrame, clearFrame, PAL } from "../src/core/index.js";
import { deflateSync } from "node:zlib";
import { writeFileSync } from "node:fs";
const SPECS=JSON.parse(process.argv[2]);
const crcT=new Int32Array(256).map((_,n)=>{let c=n;for(let k=0;k<8;k++)c=c&1?0xedb88320^(c>>>1):c>>>1;return c});
const crc=b=>{let c=-1;for(const x of b)c=crcT[(c^x)&255]^(c>>>8);return(c^-1)>>>0};
function png(w,h,rgba){const raw=Buffer.alloc((w*4+1)*h);for(let y=0;y<h;y++){raw[y*(w*4+1)]=0;Buffer.from(rgba.buffer,rgba.byteOffset+y*w*4,w*4).copy(raw,y*(w*4+1)+1)}
  const ch=(t,d)=>{const l=Buffer.alloc(4);l.writeUInt32BE(d.length);const td=Buffer.concat([Buffer.from(t),d]);const c=Buffer.alloc(4);c.writeUInt32BE(crc(td));return Buffer.concat([l,td,c])};
  const ih=Buffer.alloc(13);ih.writeUInt32BE(w,0);ih.writeUInt32BE(h,4);ih[8]=8;ih[9]=6;return Buffer.concat([Buffer.from([137,80,78,71,13,10,26,10]),ch('IHDR',ih),ch('IDAT',deflateSync(raw,{level:9})),ch('IEND',Buffer.alloc(0))])}
const out={};const sheets=[];
for(const s of SPECS){
  const mod=await import(`../src/fx/${s.id}.js`),meta=mod.meta,[W,H]=meta.size,[OX,OY]=meta.origin,fps=s.fps??12;
  const opts={...(s.o||{})};if(typeof opts.palette=='string')opts.palette=PAL[opts.palette];
  const inst=createFx(mod,{x:OX,y:OY,actor:false,...opts}),f=createFrame(W,H);
  const n=Math.max(1,Math.round(Math.min(meta.duration,s.max??9)*fps));const fr=[];
  let x0=W,y0=H,x1=-1,y1=-1;
  for(let i=0;i<n;i++){if(i)inst.update(1/fps);clearFrame(f);inst.draw(f);const C=f.color.slice(),L=f.light.slice();fr.push([C,L]);
    for(let p=0;p<W*H;p++)if((C[p]>>>24)>40||Math.max(L[p]&255,(L[p]>>>8)&255,(L[p]>>>16)&255)>28){const x=p%W,y=p/W|0;if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y}}
  // drop trailing empty frames
  while(fr.length>1){const[C,L]=fr[fr.length-1];let e=true;for(let p=0;p<W*H&&e;p++)if((C[p]>>>24)>8||(L[p]&0xffffff)>0x101010)e=false;if(!e)break;fr.pop()}
  const w=x1-x0+1,h=y1-y0+1;out[s.k]={w,h,ax:OX-x0,ay:OY-y0,n:fr.length,fps};
  sheets.push({k:s.k,w,h,x0,y0,W,fr});
  console.error(s.k,s.id,'frames',fr.length,'box',w,h);
}
// pack: each effect = one row, color row then light row
const SW=Math.max(...sheets.map(s=>s.w*s.fr.length));let SH=0;for(const s of sheets){out[s.k].y=SH;SH+=s.h*2}
const img=new Uint8ClampedArray(SW*SH*4);
for(const s of sheets){const Y=out[s.k].y;s.fr.forEach(([C,L],i)=>{for(let y=0;y<s.h;y++)for(let x=0;x<s.w;x++){const p=(y+s.y0)*s.W+x+s.x0,c=C[p],l=L[p];
  let j=((Y+y)*SW+i*s.w+x)*4;img[j]=c&255;img[j+1]=(c>>>8)&255;img[j+2]=(c>>>16)&255;img[j+3]=c>>>24;
  j=((Y+s.h+y)*SW+i*s.w+x)*4;const r=l&255,g=(l>>>8)&255,b=(l>>>16)&255,m=Math.max(r,g,b);if(m>=40){img[j]=r*255/m;img[j+1]=g*255/m;img[j+2]=b*255/m;img[j+3]=m}}})}
writeFileSync('bake/fx.png',png(SW,SH,img));writeFileSync('bake/fx.json',JSON.stringify(out));console.error('sheet',SW,SH);
