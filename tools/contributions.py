"""Render only the calendar actually returned by GitHub. No external dependencies."""
import os,json,urllib.request,html
from pathlib import Path
query='''query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount weekday contributionLevel}}}}}}'''
req=urllib.request.Request('https://api.github.com/graphql',data=json.dumps({'query':query,'variables':{'login':os.environ['PROFILE_LOGIN']}}).encode(),headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Content-Type':'application/json','User-Agent':'PARADOX-contributions'},method='POST')
with urllib.request.urlopen(req,timeout=30) as r: body=json.load(r)
if body.get('errors'):raise RuntimeError('GitHub GraphQL returned errors; artwork not updated.')
cal=body['data']['user']['contributionsCollection']['contributionCalendar'];weeks=cal['weeks'];total=cal['totalContributions']
if not weeks:raise RuntimeError('No calendar returned')
colors={'NONE':'#242424','FIRST_QUARTILE':'#555555','SECOND_QUARTILE':'#858585','THIRD_QUARTILE':'#b5b5b5','FOURTH_QUARTILE':'#eeeeee'}
w=900; step= min(15, 840/len(weeks));parts=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} 186" role="img"><title>GitHub contribution calendar — {total} contributions</title><rect width="900" height="186" rx="8" fill="#111111"/><text x="30" y="27" font-family="monospace" font-size="12" fill="#bbbbbb">CONTINUOUS EVOLUTION / GITHUB CONTRIBUTIONS</text><text x="870" y="27" text-anchor="end" font-family="monospace" font-size="12" fill="#eeeeee">{total} TOTAL</text>']
for i,week in enumerate(weeks):
 for day in week['contributionDays']:
  x=30+i*step;y=42+day['weekday']*step; color=colors[day['contributionLevel']];label=html.escape(f"{day['date']}: {day['contributionCount']} contributions")
  parts.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{step-2:.2f}" height="{step-2:.2f}" rx="2" fill="{color}"><title>{label}</title></rect>')
parts.append('<text x="30" y="173" font-family="monospace" font-size="11" fill="#aaaaaa">GITHUB API / CALENDAR AS RETURNED TO THE WORKFLOW TOKEN</text></svg>')
path=Path(__file__).resolve().parents[1]/'assets'/'contributions.svg';path.write_text(''.join(parts),encoding='utf-8')
