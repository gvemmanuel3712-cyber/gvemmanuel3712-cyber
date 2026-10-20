"""Enable the README link only after the actual Pages site is reachable."""
from pathlib import Path
import urllib.request

URL = 'https://gvemmanuel3712-cyber.github.io/'
req = urllib.request.Request(URL, headers={'User-Agent':'Emmanuel-Portfolio-Publication-Check'})
with urllib.request.urlopen(req, timeout=30) as response:
    html = response.read().decode('utf-8')
    if response.status != 200 or 'Developer Playground' not in html or 'Emmanuel' not in html:
        raise SystemExit('The published portfolio could not be verified; README unchanged.')
path = Path(__file__).resolve().parents[1] / 'README.md'
text = path.read_text()
start = '<!-- portfolio-link:start -->'
end = '<!-- portfolio-link:end -->'
before, rest = text.split(start, 1)
_, after = rest.split(end, 1)
link = f'\n<p align="center"><a href="{URL}"><strong>Enter my Developer Playground ↗</strong></a></p>\n'
path.write_text(before + start + link + end + after)
print('Verified the real Pages site and enabled its README link. No commit or push performed.')
