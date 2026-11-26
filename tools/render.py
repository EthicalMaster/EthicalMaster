from pathlib import Path
import os, math
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from numba import njit
A=Path(__file__).resolve().parents[1]/'assets'; A.mkdir(exist_ok=True)
F=Path(os.getenv('PARADOX_FONT_DIR','/usr/share/fonts/opentype/inter'))
def font(s,b=False):return ImageFont.truetype(str(F/('InterDisplay-Black.otf' if b else 'InterDisplay-Regular.otf')),s)
def mono(s):return ImageFont.truetype(os.getenv('PARADOX_MONO_FONT','/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'),s)
def unit(v):return v/np.maximum(1e-9,np.linalg.norm(v,axis=-1,keepdims=True))
@njit(cache=True)
def raster(v,n,f,w,h):
 z=np.full((h,w),-1e8); o=np.zeros((h,w,4),np.uint8)
 for tri in f:
  a,b,c=v[tri[0]],v[tri[1]],v[tri[2]];na,nb,nc=n[tri[0]],n[tri[1]],n[tri[2]]
  den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
  if abs(den)<1e-8:continue
  for y in range(max(0,int(min(a[1],b[1],c[1]))),min(h,int(max(a[1],b[1],c[1]))+2)):
   for x in range(max(0,int(min(a[0],b[0],c[0]))),min(w,int(max(a[0],b[0],c[0]))+2)):
    p=((b[1]-c[1])*(x+.5-c[0])+(c[0]-b[0])*(y+.5-c[1]))/den;q=((c[1]-a[1])*(x+.5-c[0])+(a[0]-c[0])*(y+.5-c[1]))/den;r=1-p-q
    if min(p,q,r)<0:continue
    dep=p*a[2]+q*b[2]+r*c[2]
    if dep<=z[y,x]:continue
    z[y,x]=dep;nn=p*na+q*nb+r*nc;nn=nn/(np.sqrt(np.sum(nn*nn))+1e-9);nx,ny,nz=nn
    rx,ry,rz=2*nz*nx,2*nz*ny,2*nz*nz-1
    l1=math.exp(-((rx+.38)/.43)**6-((ry-.63)/.36)**6) if rz>-.65 else 0.
    l2=math.exp(-((rx-.77)/.19)**4-((ry+.02)/.86)**6);l3=math.exp(-((rx+.86)/.16)**4-((ry+.02)/.78)**6);l4=math.exp(-((ry+.79)/.18)**4-((rx-.1)/.75)**6)
    l5=math.exp(-((rx-.15)/.31)**4-((ry-.14)/.72)**6) if rz<-.1 else 0.
    tone=.045+.05*(ry+1)+.85*l1+.9*l2+.65*l3+.35*l4+.25*l5+.05*max(0.,nz)+.07*(1-abs(nz))**2
    val=int(255*min(1.,max(0.,tone))**.84);o[y,x,0]=val;o[y,x,1]=val;o[y,x,2]=val;o[y,x,3]=255
 return o

def sculpture(t,kind,w,h):
 u=np.linspace(0,2*np.pi,160,endpoint=False);v=np.linspace(0,2*np.pi,40,endpoint=False)
 if kind=='knot':
  R=1.42+.55*np.cos(3*u+.16*np.sin(t));C=np.stack([R*np.cos(2*u),R*np.sin(2*u),.66*np.sin(3*u+.16*np.sin(t))],-1);width=.40+.095*np.sin(3*u+t)+.035*np.cos(5*u-t);ratio=.80
 else:
  R=1.3+.25*np.cos(3*u+t);C=np.stack([R*np.cos(u),R*np.sin(u),.48*np.sin((2 if kind=='ribbon' else 3)*u)],-1);width=.4+.10*np.cos(3*u+t);ratio=.35 if kind=='ribbon' else .85
 T=unit(np.roll(C,-1,0)-np.roll(C,1,0));B=unit(np.cross(T,[0.,0.,1.]));N=unit(np.cross(B,T));angle=v[None,:]+(.38*np.sin(u*3+t))[:,None]
 P=C[:,None,:]+width[:,None,None]*(np.cos(angle)[:,:,None]*B[:,None,:]+ratio*np.sin(angle)[:,:,None]*N[:,None,:]);norm=unit(np.cross(np.roll(P,-1,1)-np.roll(P,1,1),np.roll(P,-1,0)-np.roll(P,1,0)));norm=np.where((np.sum(norm*(P-C[:,None,:]),-1)<0)[:,:,None],-norm,norm)
 m,k=P.shape[:2];i=np.arange(m)[:,None];j=np.arange(k)[None,:];a=i*k+j;b=((i+1)%m)*k+j;c=((i+1)%m)*k+(j+1)%k;d=i*k+(j+1)%k;f=np.concatenate([np.stack([a,b,c],-1).reshape(-1,3),np.stack([a,c,d],-1).reshape(-1,3)])
 aa=.58+.12*np.sin(t);bb=-.27+.14*np.cos(t);cc=-.32+.18*np.sin(t);ca,sa=np.cos(aa),np.sin(aa);cb,sb=np.cos(bb),np.sin(bb);co,so=np.cos(cc),np.sin(cc);R=np.array([[co,-so,0],[so,co,0],[0,0,1]])@np.array([[cb,0,sb],[0,1,0],[-sb,0,cb]])@np.array([[1,0,0],[0,ca,-sa],[0,sa,ca]])
 p=P.reshape(-1,3)@R.T;n=norm.reshape(-1,3)@R.T;sc=min(w,h)/4.45;verts=np.stack([p[:,0]*sc+w*.5,-p[:,1]*sc+h*.5,p[:,2]],-1);return Image.fromarray(raster(verts,n,f,w,h),'RGBA')
def bg(w,h,x,y):
 yy,xx=np.mgrid[:h,:w];g=(10+20*np.exp(-((xx-x)/(w*.37))**2-((yy-y)/(h*.46))**2)).astype('uint8');return Image.fromarray(np.stack([g]*3,-1),'RGB')
def hero(t):
 im=bg(900,430,667,211);d=ImageDraw.Draw(im);d.line((35,51,865,51),fill=(61,61,61));d.line((35,379,865,379),fill=(61,61,61))
 d.text((36,23),'E T H I C A L M A S T E R',font=mono(12),fill='#bcbcbc');d.text((864,23),'INDEPENDENT DEVELOPER / 01',font=mono(12),fill='#bcbcbc',anchor='ra')
 d.text((32,85),'BEYOND',font=font(95,True),fill='#efefef');d.text((29,174),'THE CODE.',font=font(95,True),fill='#efefef')
 art=sculpture(t,'knot',900,660).resize((450,330),Image.Resampling.LANCZOS);im.paste(art,(444,55),art);d=ImageDraw.Draw(im);d.text((39,304),'T A H E R  S A I F E E',font=font(19,True),fill='#e9e9e9');d.text((39,337),'Software / AI / Data Science',font=font(17),fill='#a9a9a9');d.text((36,399),'FIG. 01 / PARADOX',font=mono(11),fill='#b4b4b4');d.text((865,399),'FORM / FUNCTION / CURIOSITY',font=mono(11),fill='#b4b4b4',anchor='ra');return im

def project(t,i):
 im=bg(420,232,210,85);d=ImageDraw.Draw(im)
 if i==0:
  for j in range(20):
   pts=[(35+k*3.05,95+(j-10)*4.1+16*math.sin(k*.065+j*.15+t)*math.cos(k*.023-j*.1)) for k in range(115)];d.line(pts,fill=(55+j*7,)*3,width=1)
 elif i==2:
  pos=[(210,45),(130,83),(290,83),(90,137),(170,137),(250,137),(330,137)]
  for a,b in [(0,1),(0,2),(1,3),(1,4),(2,5),(2,6),(1,2)]:
   x,y=pos[a];xx,yy=pos[b];d.line((x,y,xx,yy),fill='#777777');k=(t/(2*np.pi)+a*.17)%1;px=x+(xx-x)*k;py=y+(yy-y)*k;d.ellipse((px-2,py-2,px+2,py+2),fill='#eeeeee')
  for x,y in pos:d.ellipse((x-9,y-9,x+9,y+9),fill='#212121',outline='#bdbdbd',width=2);d.ellipse((x-2,y-2,x+2,y+2),fill='#eeeeee')
 else:
  art=sculpture(t,'aven' if i==1 else 'ribbon',260,150);im.paste(art,(80,9),art)
 d=ImageDraw.Draw(im);d.line((18,164,402,164),fill=(65,65,65));d.text((18,174),['AXIOM LAB','AVEN','AGENT STUDIO','PORTFOLIO'][i],font=font(22,True),fill='#efefef');d.text((18,204),['Scientific computing','Applied intelligence','Agent orchestration','Creative engineering'][i],font=font(13),fill='#b3b3b3');d.text((402,15),f'0{i+1} / STUDY',font=mono(10),fill='#bcbcbc',anchor='ra');d.text((402,184),'↗',font=font(19),fill='#c0c0c0',anchor='ra');return im

def export(name,fn,count):
 frames=[fn(2*np.pi*i/count) for i in range(count)];frames[0].save(A/(name+'.png'),optimize=True);pal=Image.new('P',(1,1));pal.putpalette([v for i in range(256) for v in (i,i,i)]);frames=[im.quantize(palette=pal,dither=Image.Dither.NONE) for im in frames];frames[0].save(A/(name+'.gif'),save_all=True,append_images=frames[1:],duration=125,loop=0,optimize=True,disposal=1);print(name,(A/(name+'.gif')).stat().st_size,flush=True)
if __name__=='__main__':
 export('paradox',hero,48)
 for i,n in enumerate(['axiom','aven','agent','portfolio']):export(n,lambda t:project(t,i),32)
