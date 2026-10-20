"""Render original, self-contained profile SVGs from the public snapshot."""
from datetime import date, timedelta
from html import escape
from pathlib import Path
from calendar import monthrange
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/v2'
OUT.mkdir(parents=True, exist_ok=True)
DATA = json.loads((ROOT / 'data/github.json').read_text())
STAMP = DATA['checkedAt'][:10]
SANS = 'Arial,Helvetica,sans-serif'
MONO = 'ui-monospace,SFMono-Regular,Menlo,Consolas,monospace'

def text(x,y,value,size=18,color='#F1F5F9',mono=False,weight=400,extra=''):
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="{MONO if mono else SANS}" font-size="{size}" font-weight="{weight}" {extra}>{escape(str(value))}</text>'

def rect(x,y,w,h,fill='#0B1120',stroke='#213A54',r=12):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>'

def svg(name,w,h,title,desc,body):
    source=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>
<defs><linearGradient id="bg"><stop stop-color="#05070D"/><stop offset="1" stop-color="#111D35"/></linearGradient><linearGradient id="accent"><stop stop-color="#2563EB"/><stop offset="1" stop-color="#38BDF8"/></linearGradient><pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".8" fill="#38BDF8" opacity=".16"/></pattern></defs>
<style>.sweep{{animation:sweep 6s ease-in-out infinite alternate}}.cursor{{animation:blink 2s steps(1) infinite}}.satellite{{animation:float 7s ease-in-out infinite}}@keyframes sweep{{from{{transform:translateX(0)}}to{{transform:translateX(140px)}}}}@keyframes blink{{0%,70%{{opacity:1}}71%,100%{{opacity:0}}}}@keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-6px)}}}}@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>
{rect(.5,.5,w-1,h-1,'url(#bg)')}
{body}
</svg>\n'''
    (OUT/name).write_text(source,encoding='utf-8')

def satellite(x,y,scale=1):
    rows=['1100000000000011','1110000000000111','0111000110001110','0011101111011100','0001111111111000','0000111111110000','0000011111100000','0000111111110000','0001111111111000','0011101111011100','0111000110001110','1110000000000111','1100000000000011']
    cells=''.join(f'<rect x="{i*4}" y="{j*4}" width="3" height="3" fill="#38BDF8" opacity="{1 if 4<i<11 else .6}"/>' for j,row in enumerate(rows) for i,v in enumerate(row) if v=='1')
    return f'<g transform="translate({x} {y}) scale({scale})"><g class="satellite" shape-rendering="crispEdges">{cells}</g></g>'

def header(mobile=False):
    w,h=(640,180) if mobile else (1000,110)
    body=f'<rect x="{w-270}" y="1" width="268" height="{h-2}" rx="12" fill="url(#dots)"/>'
    body+=f'<path d="M24 23v{h-46}" stroke="url(#accent)" stroke-width="3"/>'
    if mobile:
        body+=text(43,56,'Emmanuel Guevara',36,weight=700)+text(43,100,'Vásquez.',36,'#38BDF8',weight=700)+text(44,140,'Software Engineering student',22,'#94A3B8')+text(44,169,'ITESO · Guadalajara, México',20,'#94A3B8')
        body+=satellite(535,54,.9)
    else:
        body+=text(45,52,'Emmanuel Guevara Vásquez',35,weight=700)+text(46,82,'SOFTWARE ENGINEERING STUDENT · ITESO · GUADALAJARA, MÉXICO',13,'#94A3B8',True)
        body+=text(823,57,'EG /',30,'#38BDF8',True,700)+f'<rect class="cursor" x="926" y="35" width="13" height="26" fill="#38BDF8"/>'+text(793,82,'DEVELOPER PLAYGROUND',11,'#94A3B8',True)
    svg('header-mobile.svg' if mobile else 'header.svg',w,h,'Emmanuel Guevara Vásquez — Developer Playground','Compact animated header. Software Engineering student at ITESO, Guadalajara, México.',body)

def scan(mobile=False):
    w,h=(640,390) if mobile else (1000,265)
    body=text(28,34,'PROFILE SCAN / 01',18 if mobile else 12,'#94A3B8',True)
    line_start=w-212
    body+=f'<path d="M{line_start} 29h180" stroke="#213A54" stroke-width="2"/><path class="sweep" d="M{line_start} 29h40" stroke="#38BDF8" stroke-width="2"/>'
    body+=text(28,84,'Curiosity → code.',36,'#38BDF8',weight=700)
    body+=text(29,123,'Learning to build useful, secure',26 if mobile else 18,'#F1F5F9')+text(29,158 if mobile else 150,'and maintainable software.',26 if mobile else 18,'#F1F5F9')
    body+=text(29,192,'FOCUS',16 if mobile else 11,'#94A3B8',True)+text(29,222 if mobile else 217,'Systems · Automation · AI · APIs · Security',22 if mobile else 15,'#F1F5F9')
    if mobile:
        body+=f'<path d="M28 246h584" stroke="#213A54"/>'
        for x,value,label in [(29,DATA['profile']['public_repos'],'PUBLIC REPOS'),(242,DATA['calendar']['total'],'CONTRIBUTIONS'),(457,DATA['calendar']['activeDays'],'ACTIVE DAYS')]:
            body+=text(x,300,value,38,'#38BDF8',weight=700)+text(x,331,label,18,'#94A3B8',True)
        body+=text(29,372,f'PUBLIC SNAPSHOT · {STAMP}',19,'#94A3B8',True)
        body+=satellite(535,70,.7)
    else:
        body+='<path d="M638 58v165" stroke="#213A54"/>'
        for y,value,label in [(91,DATA['profile']['public_repos'],'public repository' if DATA['profile']['public_repos']==1 else 'public repositories'),(144,DATA['calendar']['total'],'contributions'),(197,DATA['calendar']['activeDays'],'active days')]:
            body+=text(674,y,value,32,'#38BDF8',weight=700)+text(729,y-2,label,14,'#94A3B8',True)
        body+=text(675,237,f'PUBLIC SNAPSHOT · {STAMP}',10,'#94A3B8',True)
    svg('profile-scan-mobile.svg' if mobile else 'profile-scan.svg',w,h,'Profile Scan — Emmanuel Guevara Vásquez',f'Student at ITESO. Learning software engineering. Public snapshot {STAMP}: {DATA["profile"]["public_repos"]} public repositories, {DATA["calendar"]["total"]} contributions, {DATA["calendar"]["activeDays"]} active days. These are events, not proficiency scores.',body)

def stack(mobile=False):
    w,h=(640,465) if mobile else (1000,235)
    body=text(28,35,'DEVELOPER TOOLBOX',24 if mobile else 12,'#94A3B8',True)
    groups=[('PROJECT PRACTICE',['Python · TypeScript','JavaScript · SQL · Git']),('ACADEMIC FOUNDATIONS',['Java / Object-oriented programming','C / Data structures']),('LEARNING THROUGH PROJECTS',['React · Next.js · Vue','FastAPI · SQLite · PostgreSQL'])]
    for i,(title,lines) in enumerate(groups):
        x=28 if mobile else [28,355,688][i]
        y=83+i*133 if mobile else 83
        if i:
            body+=f'<path d="M28 {y-36}h584" stroke="#213A54"/>' if mobile else f'<path d="M{x-20} 64v135" stroke="#213A54"/>'
        icons=['m6 2-5 8 5 8m10-16 5 8-5 8M13 0l-5 20','M11 4C7 1 3 1 1 2v16c3-1 6-1 10 2 4-3 7-3 10-2V2c-2-1-6-1-10 2Zm0 0v16','M2 2h6v6H2Zm12 0h6v6h-6ZM8 14h6v6H8ZM8 5h6M5 8v4l6 2m6-6v4l-6 2']
        body+=f'<g transform="translate({x} {y-18})" fill="none" stroke="#38BDF8" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"><path d="{icons[i]}"/></g>'
        body+=text(x+32,y,title,24 if mobile else 11,'#38BDF8',True,500)
        for j,line in enumerate(lines):
            body+=text(x,y+35+j*31,line,24 if mobile else 14,'#F1F5F9')
    if not mobile:
        body+=text(29,215,'Hands-on practice and coursework — learning in progress, without proficiency scores.',11,'#94A3B8',True)
    svg('toolbox-mobile.svg' if mobile else 'toolbox.svg',w,h,'Developer toolbox: practice, academic foundations and ongoing learning','Project practice: Python, TypeScript, JavaScript, SQL, Git. Academic: Java OOP and C data structures. Learning through projects: React, Next.js, Vue, FastAPI, SQLite, PostgreSQL.',body)

def projects(mobile=False):
    w,h=(640,415) if mobile else (1000,220)
    body=text(28,35,'SELECTED WORK',12,'#94A3B8',True)
    cards=[('GitHub Profile','Versioned visual identity.','Markdown · SVG · Automation','PUBLIC REPOSITORY'),('Opero Docs','Software solutions and automation.','Personal project in development.','PRIVATE / IN DEVELOPMENT')]
    for i,(title,desc,tech,status) in enumerate(cards):
        x,y,cw=(16,56+i*176,608) if mobile else (16+i*493,56,477)
        body+=rect(x,y,cw,158,'#0B1120','#213A54',9)
        body+=text(x+22,y+39,title,27 if mobile else 23,weight=700)
        body+=text(x+22,y+73,desc,24 if mobile else 15,'#F1F5F9')
        body+=text(x+22,y+103,tech,20 if mobile else 12,'#94A3B8',True)
        body+=text(x+22,y+137,status,18 if mobile else 11,'#38BDF8',True)
    svg('projects-mobile.svg' if mobile else 'projects.svg',w,h,'Selected work: GitHub Profile and Opero Docs','GitHub Profile: original versioned visual identity, Markdown, SVG and automation, with a public source link in the README. Opero Docs: private personal software and automation project in development. No implementation details disclosed.',body)

def activity(mobile=False):
    w,h=(640,300) if mobile else (1000,300)
    body=text(28,35,'PUBLIC SIGNALS / CONTRIBUTION ART',11 if mobile else 12,'#94A3B8',True)
    body+=satellite(w-96,58,.8 if mobile else 1)
    body+=text(28,83,f'{DATA["calendar"]["total"]} contributions · {DATA["calendar"]["activeDays"]} active days',25 if mobile else 30,'#F1F5F9',weight=700)
    days=DATA['calendar']['days']
    start=date.fromisoformat(days[0]['date'])
    step=10.7 if mobile else 17.1
    origin_x,origin_y=30,135
    colors=['#111D35','#164E63','#0369A1','#0284C7','#38BDF8']
    for index,day in enumerate(days):
        x=origin_x+(index//7)*step;y=origin_y+(index%7)*step
        cell=f'<rect x="{x:.1f}" y="{y:.1f}" width="{step-3:.1f}" height="{step-3:.1f}" rx="1.4" fill="{colors[day["level"]]}"><title>{day["date"]}: {day["count"]} contributions</title></rect>'
        body+=cell
        current=date.fromisoformat(day['date'])
        if (index==0 and monthrange(current.year,current.month)[1]-current.day+1>=21) or day['date'].endswith('-01'):
            value=current.strftime('%b')
            body+=text(x,121,value,9 if mobile else 11,'#94A3B8',True)
    footer_y=248 if mobile else 282
    body+=text(29,footer_y,f'{DATA["calendar"]["start"]} → {DATA["calendar"]["end"]} · SNAPSHOT {STAMP}',10 if mobile else 11,'#94A3B8',True)
    if mobile:
        body+=text(29,276,'Real public events. Decorative satellite. No altered cells.',10,'#94A3B8',True)
    svg('contributions-mobile.svg' if mobile else 'contributions.svg',w,h,'Real public GitHub contribution calendar with a decorative pixel satellite',f'Public snapshot {STAMP}. Calendar {DATA["calendar"]["start"]} to {DATA["calendar"]["end"]}. {DATA["calendar"]["total"]} publicly visible contributions across {DATA["calendar"]["activeDays"]} active days. Dates and cell values are unchanged by the animation.',body)

for mobile in (False,True):
    header(mobile);scan(mobile);stack(mobile);projects(mobile);activity(mobile)
print('Rendered 10 self-contained SVG assets; data remains unchanged by animation.')
