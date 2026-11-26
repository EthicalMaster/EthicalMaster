"""Original monochrome motion panels. Run with the dependencies/font paths from render.py."""
from render import A, font, mono, bg, sculpture
from PIL import Image, ImageDraw
import math

W=900; INK='#efefef'; MUT='#b9b9b9'; DIM='#737373'; LINE='#454545'
def base(h,section,tag,phase):
 im=bg(W,h,680,h*.47);d=ImageDraw.Draw(im)
 d.text((44,24),section,font=mono(13),fill=MUT);pass
 d.line((44,49,856,49),fill=LINE)
 x=44+int(776*(.5-.5*math.cos(phase)))
 d.line((x,49,min(x+24,856),49),fill='#b6b6b6',width=1)
 return im,d

def footer(d,h,left,right):
 pass

def individual(t):
 h=290; im,d=base(h,'01 / THE INDIVIDUAL','PROFILE STUDY',t)
 # abstract fingerprint / interference field, intentionally not biometric
 for k in range(18):
  pts=[]
  for i in range(120):
   a=2*math.pi*i/119;r=22+k*5+3*math.sin(3*a+t+k*.22)
   pts.append((706+r*1.18*math.cos(a),169+r*.93*math.sin(a)))
  d.line(pts,fill=(53+k*7,)*3,width=1)
 d.text((44,86),'Curiosity into creation.',font=font(37,True),fill=INK)
 d.text((46,153),'Student developer exploring software, AI',font=font(21),fill=MUT)
 d.text((46,186),'and data science through real projects.',font=font(21),fill=MUT)
 footer(d,h,'INQUIRY / EXPERIMENT / CRAFT','FIG. 02 / INTERFERENCE');return im

def selected(t):
 h=120; im,d=base(h,'02 / SELECTED WORKS','FOUR STUDIES',t)
 d.text((44,65),'Ideas made tangible.',font=font(33,True),fill=INK)
 for k in range(4):
  x=764+k*27; v=int(110+85*(.5+.5*math.cos(t-k*.9)))
  d.rectangle((x,79,x+13,92),fill=(v,)*3)
 return im

def toolkit(t):
 h=350;im,d=base(h,'03 / INSTRUMENTS OF CREATION','WORKING TOOLKIT',t)
 d.text((44,72),'Technology as a medium.',font=font(35,True),fill=INK)
 rows=[('01','Languages','Python / JavaScript / TypeScript / SQL / C++ / Java'),('02','Software','FastAPI / React / HTML / CSS'),('03','AI & data','Google ADK / LLM APIs / OpenCV / Data analysis'),('04','Engineering','Git / GitHub / Docker / Testing')]
 for i,(n,label,stack) in enumerate(rows):
  y=135+i*48; d.line((34,y+44,866,y+44),fill='#393939');d.text((46,y+7),label,font=font(19,True),fill=INK);d.text((282,y+9),stack,font=font(19),fill=MUT)
  a=int(95+130*(.5+.5*math.cos(t-i*math.pi/2)));d.ellipse((850,y+15,858,y+23),fill=(a,)*3)
 footer(d,h,'TOOLS, NOT PROFICIENCY RATINGS','FIG. 03 / INSTRUMENTS');return im

def process(t):
 h=280;im,d=base(h,'04 / THE CREATIVE PROCESS','ITERATIVE PRACTICE',t)
 d.text((44,72),'Learn by building.',font=font(35,True),fill=INK)
 nodes=[('Explore','Ask why'),('Design','Plan the system'),('Build','Make it work'),('Verify','Test and refine')]
 for i,(a,b) in enumerate(nodes):
  x=128+i*215; y=174; r=24
  if i<3:d.line((x+r,y,x+215-r,y),fill='#676767',width=1)
  v=int(100+115*(.5+.5*math.cos(t-i*math.pi/2)));d.ellipse((x-r,y-r,x+r,y+r),outline=(v,)*3,width=2)
  if i==0:
   d.ellipse((x-10,y-10,x+6,y+6),outline=INK,width=2);d.line((x+4,y+4,x+12,y+12),fill=INK,width=2)
  elif i==1:
   d.rectangle((x-11,y-10,x+11,y+10),outline=INK,width=2);d.line((x-11,y-2,x+11,y-2),fill=INK)
  elif i==2:
   d.line((x-3,y-10,x-13,y,x-3,y+10),fill=INK,width=2);d.line((x+3,y-10,x+13,y,x+3,y+10),fill=INK,width=2)
  else:d.line((x-12,y,x-3,y+9,x+13,y-10),fill=INK,width=2)
  d.text((x,213),a,font=font(20,True),fill=INK,anchor='mt');d.text((x,240),b,font=font(17),fill=MUT,anchor='mt')
 # single traveling pulse on each link
 for i in range(3):
  x=128+i*215+28+159*((t/(2*math.pi)+i*.23)%1);d.ellipse((x-2,172,x+2,176),fill=INK)
 footer(d,h,'REPEAT / IMPROVE / DOCUMENT','FIG. 04 / PRACTICE');return im

def closing(t):
 h=245;im,d=base(h,'06 / THE CLOSING SEQUENCE','ETHICALMASTER',t)
 d.text((44,91),'Always in the making.',font=font(39,True),fill=INK);d.text((46,150),'Form, function and curiosity.',font=font(20),fill=MUT)
 # actual rendered 3D ribbon echoing the hero
 art=sculpture(t,'ribbon',260,172);im.paste(art,(595,55),art);d=ImageDraw.Draw(im)
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
