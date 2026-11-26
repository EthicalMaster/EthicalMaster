"""Isometric contribution landscape from GitHub GraphQL. Stdlib only.
No personal token needed. No synthetic data written to production artwork.
"""
from pathlib import Path
import datetime as dt
import html, json, os, urllib.request
ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/'assets'/'contributions.svg'
QUERY='''query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount weekday contributionLevel}}}}}}'''
COLORS={'NONE':'#343434','FIRST_QUARTILE':'#737373','SECOND_QUARTILE':'#a1a1a1','THIRD_QUARTILE':'#c7c7c7','FOURTH_QUARTILE':'#eeeeee'}
HEIGHT={'NONE':0,'FIRST_QUARTILE':8,'SECOND_QUARTILE':17,'THIRD_QUARTILE':29,'FOURTH_QUARTILE':45}

def start(title):
 return [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 294" role="img" aria-labelledby="title desc"><title id="title">{html.escape(title)}</title><desc id="desc">Monochrome isometric calendar. Each tile represents one day; height encodes GitHub contribution level, not an exact count.</desc><defs><linearGradient id="bg"><stop stop-color="#0a0a0a"/><stop offset="1" stop-color="#1b1b1b"/></linearGradient><style>.sweep{{animation:sweep 3.8s ease-out both}}@keyframes sweep{{from{{opacity:0;transform:translateX(-8px)}}to{{opacity:1;transform:translateX(0)}}}}@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style></defs><rect width="900" height="294" fill="url(#bg)"/><g font-family="monospace" font-size="12" fill="#b9b9b9"><text x="44" y="33">05 / CONTINUOUS EVOLUTION</text><text x="856" y="33" text-anchor="end">GITHUB / ACTIVITY</text></g><path d="M44 49H856" stroke="#454545"/><text x="44" y="95" font-family="Arial,sans-serif" font-size="34" font-weight="400" fill="#efefef">Progress in motion.</text>']

def text(x,y,s,anchor='start',size=12):
 return f'<text x="{x}" y="{y}" text-anchor="{anchor}" fill="#b9b9b9" font-family="monospace" font-size="{size}">{html.escape(str(s))}</text>'

def placeholder():
 p=start('Contribution artwork awaiting GitHub data')
 p+=['<path d="M35 220H865" stroke="#4a4a4a" stroke-dasharray="2 7"/>',text(35,154,'AWAITING FIRST GITHUB ACTIONS RUN',size=15),text(35,181,'Actual contribution data will appear here after a successful sync.',size=13),text(35,277,'SOURCE / GITHUB CONTRIBUTION CALENDAR'),text(865,277,'NO SAMPLE STATISTICS','end'),'</svg>']
 return ''.join(p)

def render(calendar):
 weeks=calendar['weeks'];total=calendar['totalContributions']
 if not isinstance(total,int) or total<0 or not 1<=len(weeks)<=54:raise ValueError('Invalid calendar size or total')
 days=[]; seen=set()
 for i,w in enumerate(weeks):
  for d in w['contributionDays']:
   date=dt.date.fromisoformat(d['date']);day=d['weekday'];count=d['contributionCount'];level=d['contributionLevel']
   if date in seen or day not in range(7) or not isinstance(count,int) or count<0 or level not in COLORS:raise ValueError('Invalid day')
   seen.add(date);days.append((i,day,date,count,level))
 if not days:raise ValueError('Empty calendar')
 p=start(f'GitHub contribution landscape: {total} contributions')
 p.append(text(865,80,f'{total:,} CONTRIBUTIONS','end',15))
 p.append(text(865,100,f'{min(seen).isoformat()} / {max(seen).isoformat()}','end',11))
 # 3D oblique projection: week horizontal, day shifts diagonally; draw farther rows first.
 step=min(14.4,765/max(1,len(weeks)));p.append('<g class="sweep">')
 for i,day,date,count,level in sorted(days,key=lambda d:(d[1],d[0])):
  x=38+i*step+day*6;y=165+day*10;w=step-2;dx=4;dy=-4;h=HEIGHT[level];top=y-h
  a=(x,top);b=(x+w,top);c=(x+w+dx,top+dy);e=(x+dx,top+dy)
  def poly(pts,fill):return '<polygon points="'+' '.join(f'{u:.1f},{v:.1f}' for u,v in pts)+'" fill="'+fill+'"/>'
  p.append(f'<g><title>{date.isoformat()}: {count} contributions</title>')
  if h:
   p.append(poly([a,b,(x+w,y),(x,y)],'#555555' if level!='FOURTH_QUARTILE' else '#919191'))
   p.append(poly([b,c,(x+w+dx,y+dy),(x+w,y)],'#3d3d3d'))
  p.append(poly([a,b,c,e],COLORS[level]));p.append('</g>')
 p+=['</g>',text(34,277,'HEIGHT / GITHUB CONTRIBUTION LEVEL'),text(866,277,'API VIEW / '+max(seen).isoformat(),'end'),'</svg>']
 return ''.join(p)

def fetch():
 token=os.environ['GH_TOKEN'];login=os.environ['PROFILE_LOGIN']
 req=urllib.request.Request('https://api.github.com/graphql',data=json.dumps({'query':QUERY,'variables':{'login':login}}).encode(),headers={'Authorization':'Bearer '+token,'Content-Type':'application/json','User-Agent':'PARADOX-profile'},method='POST')
 with urllib.request.urlopen(req,timeout=30) as r:body=json.load(r)
 if body.get('errors'):raise RuntimeError('GitHub GraphQL returned errors; previous artwork retained.')
 return body['data']['user']['contributionsCollection']['contributionCalendar']

if __name__=='__main__':
 import sys
 svg=placeholder() if '--placeholder' in sys.argv else render(fetch())
 temp=TARGET.with_suffix('.tmp');temp.write_text(svg,encoding='utf-8');temp.replace(TARGET)
 static=TARGET.with_name("contributions-static.svg"); tmp=static.with_suffix(".tmp"); tmp.write_text(svg.replace('class="sweep"',''),encoding="utf-8"); tmp.replace(static)
