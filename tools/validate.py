"""Local structural validation, including synthetic fixture used only for testing."""
import re, xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image
from contributions import render, placeholder
from datetime import date,timedelta
root=Path(__file__).resolve().parents[1]
for name in ('README.md','STATIC.md'):
 text=(root/name).read_text()
 for f in re.findall(r'src="([^"]+)"',text):
  p=root/f;assert p.is_file(),f
  if p.suffix=='.svg':ET.parse(p)
  else:
   with Image.open(p) as im:
    for i in range(getattr(im,'n_frames',1)): im.seek(i);im.load()
 print(name,'asset references and image frames OK')
# Test realistic 53-week geometry without publishing fictional contribution data.
start=date(2025,11,23);levels=['NONE','FIRST_QUARTILE','SECOND_QUARTILE','THIRD_QUARTILE','FOURTH_QUARTILE'];weeks=[]
for w in range(53):
 days=[]
 for d in range(7):
  k=(w+d)%5;days.append(dict(date=(start+timedelta(days=7*w+d)).isoformat(),weekday=d,contributionCount=k,contributionLevel=levels[k]))
 weeks.append({'contributionDays':days})
total=sum(d['contributionCount'] for w in weeks for d in w['contributionDays']);s=render({'weeks':weeks,'totalContributions':total});ET.fromstring(s);assert f'{total:,} CONTRIBUTIONS' in s;assert len(re.findall('<title>',s))==371;ET.fromstring(placeholder());assert 'AWAITING FIRST' in (root/'assets/contributions.svg').read_text()
print('Contribution renderer fixture, XML and placeholder OK; live GitHub API not tested.')
