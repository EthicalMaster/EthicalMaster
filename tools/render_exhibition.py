"""Original monochrome motion panels. Run with the dependencies/font paths from render.py."""
from render import A, font, mono, bg, sculpture
from PIL import Image, ImageDraw
import math

W=900; INK='#efefef'; MUT='#b9b9b9'; DIM='#737373'; LINE='#454545'
def base(h,section,tag,phase):
 im=bg(W,h,680,h*.47);d=ImageDraw.Draw(im)
 d.text((34,19),section,font=mono(13),fill=MUT);d.text((866,19),tag,font=mono(12),fill=MUT,anchor='ra')
 d.line((34,44,866,44),fill=LINE)
 x=34+int(800*(.5-.5*math.cos(phase)))
 d.line((x,44,min(x+32,866),44),fill='#b6b6b6',width=2)
 return im,d

def footer(d,h,left,right):
 d.line((34,h-38,866,h-38),fill=LINE);d.text((34,h-26),left,font=mono(11),fill=MUT);d.text((866,h-26),right,font=mono(11),fill=MUT,anchor='ra')

def individual(t):
 h=316; im,d=base(h,'01 / THE INDIVIDUAL','PROFILE STUDY',t)
 # abstract fingerprint / interference field, intentionally not biometric
 for k in range(18):
  pts=[]
  for i in range(120):
   a=2*math.pi*i/119;r=22+k*5+3*math.sin(3*a+t+k*.22)
   pts.append((706+r*1.18*math.cos(a),169+r*.93*math.sin(a)))
  d.line(pts,fill=(53+k*7,)*3,width=1)
 d.text((33,66),'Curiosity into',font=font(53,True),fill=INK)
 d.text((33,120),'creation.',font=font(53,True),fill=INK)
 d.text((36,198),'Student developer exploring software, AI',font=font(23),fill=MUT)
 d.text((36,227),'and data science through real projects.',font=font(23),fill=MUT)
 footer(d,h,'INQUIRY / EXPERIMENT / CRAFT','FIG. 02 / INTERFERENCE');return im

def selected(t):
 h=142; im,d=base(h,'02 / SELECTED WORKS','FOUR STUDIES',t)
 d.text((33,57),'Ideas made tangible.',font=font(44,True),fill=INK)
 for k in range(4):
  x=764+k*27; v=int(110+85*(.5+.5*math.cos(t-k*.9)))
  d.rectangle((x,79,x+13,92),fill=(v,)*3)
 return im

def toolkit(t):
 h=366;im,d=base(h,'03 / INSTRUMENTS OF CREATION','WORKING TOOLKIT',t)
 d.text((33,59),'Technology as a medium.',font=font(43,True),fill=INK)
 rows=[('01','LANGUAGES','Python / JavaScript / TypeScript / SQL / C++ / Java'),('02','SOFTWARE','FastAPI / React / HTML / CSS'),('03','INTELLIGENCE & DATA','Google ADK / LLM APIs / OpenCV / Data analysis'),('04','ENGINEERING','Git / GitHub / Docker / Testing')]
 for i,(n,label,stack) in enumerate(rows):
  y=125+i*48; d.line((34,y+44,866,y+44),fill='#393939');d.text((35,y+9),n,font=mono(13),fill=MUT);d.text((79,y+7),label,font=font(17,True),fill=INK);d.text((335,y+9),stack,font=font(17),fill=MUT)
  a=int(95+130*(.5+.5*math.cos(t-i*math.pi/2)));d.ellipse((850,y+15,858,y+23),fill=(a,)*3)
 footer(d,h,'TOOLS, NOT PROFICIENCY RATINGS','FIG. 03 / INSTRUMENTS');return im

def process(t):
 h=305;im,d=base(h,'04 / THE CREATIVE PROCESS','ITERATIVE PRACTICE',t)
 d.text((33,59),'Learn by building.',font=font(48,True),fill=INK)
 nodes=[('Explore','Ask why'),('Design','Plan the system'),('Build','Make it work'),('Verify','Test and refine')]
 for i,(a,b) in enumerate(nodes):
  x=128+i*215; y=174; r=28
  if i<3:d.line((x+r,y,x+215-r,y),fill='#676767',width=1)
  v=int(100+115*(.5+.5*math.cos(t-i*math.pi/2)));d.ellipse((x-r,y-r,x+r,y+r),outline=(v,)*3,width=2)
  if i==0:
   d.ellipse((x-10,y-10,x+6,y+6),outline=INK,width=2);d.line((x+4,y+4,x+12,y+12),fill=INK,width=2)
  elif i==1:
   d.rectangle((x-11,y-10,x+11,y+10),outline=INK,width=2);d.line((x-11,y-2,x+11,y-2),fill=INK)
  elif i==2:
   d.line((x-3,y-10,x-13,y,x-3,y+10),fill=INK,width=2);d.line((x+3,y-10,x+13,y,x+3,y+10),fill=INK,width=2)
  else:d.line((x-12,y,x-3,y+9,x+13,y-10),fill=INK,width=2)
  d.text((x,213),a,font=font(20,True),fill=INK,anchor='mt');d.text((x,240),b,font=font(15),fill=MUT,anchor='mt')
 # single traveling pulse on each link
 for i in range(3):
  x=128+i*215+28+159*((t/(2*math.pi)+i*.23)%1);d.ellipse((x-2,172,x+2,176),fill=INK)
 footer(d,h,'REPEAT / IMPROVE / DOCUMENT','FIG. 04 / PRACTICE');return im

def closing(t):
 h=265;im,d=base(h,'06 / THE CLOSING SEQUENCE','ETHICALMASTER',t)
 d.text((33,75),'Always in',font=font(59,True),fill=INK);d.text((33,132),'the making.',font=font(59,True),fill=INK)
 # actual rendered 3D ribbon echoing the hero
 art=sculpture(t,'ribbon',290,190);im.paste(art,(590,52),art);d=ImageDraw.Draw(im)
 footer(d,h,'FORM / FUNCTION / CURIOSITY','END OF EXHIBITION / NOT THE WORK');return im

def export(name,fn,n=32):
 frames=[fn(2*math.pi*i/n) for i in range(n)];frames[0].save(A/(name+'.png'),optimize=True)
 pal=Image.new('P',(1,1));pal.putpalette([v for i in range(256) for v in (i,i,i)])
 fs=[f.quantize(palette=pal,dither=Image.Dither.NONE) for f in frames]
 # one pass under 5 seconds; GitHub has no native playback toggle for GIFs
 fs[0].save(A/(name+'.gif'),save_all=True,append_images=fs[1:],duration=120,optimize=True,disposal=1)
 print(name,(A/(name+'.gif')).stat().st_size,flush=True)
if __name__=='__main__':
 for name,fn in [('individual',individual),('selected',selected),('toolkit',toolkit),('process',process),('closing',closing)]: export(name,fn)
