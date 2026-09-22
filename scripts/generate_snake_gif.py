#!/usr/bin/env python3
"""Generate a dark animated contribution-snake GIF from GitHub GraphQL data.
The workflow passes GITHUB_TOKEN and GITHUB_USER.  No third-party rendering API is used.
"""
import json, os, sys, urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

USER=os.environ.get('GITHUB_USER','hardik563')
TOKEN=os.environ.get('GITHUB_TOKEN','')
OUT=Path(os.environ.get('SNAKE_OUTPUT','assets/contribution-snake.gif'))
WEEKS=52
ROWS=7
CELL=14
GAP=3
PAD=34
HEADER=34
BG=(5,8,18)
GRID=(18,25,35)
EMPTY=(20,28,39)
GREENS=[(20,55,37),(27,91,53),(35,132,69),(53,181,79),(82,218,112)]

QUERY='''query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{weeks{contributionDays{date contributionCount}}}}}}'''

def fetch():
    if not TOKEN:
        return None
    body=json.dumps({'query':QUERY,'variables':{'login':USER}}).encode()
    req=urllib.request.Request('https://api.github.com/graphql', data=body, headers={
        'Authorization':f'bearer {TOKEN}', 'Content-Type':'application/json',
        'User-Agent':'hardik563-profile-snake'
    })
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data=json.load(r)
        weeks=data['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
        return weeks[-WEEKS:]
    except Exception as e:
        print(f'contribution fetch failed: {e}', file=sys.stderr)
        return None

def fallback():
    # Deterministic placeholder until the first workflow run fetches live data.
    import random
    rng=random.Random(563)
    return [[{'date':'','contributionCount':rng.choice([0,0,0,1,2,3,5,8,13])} for _ in range(7)] for _ in range(WEEKS)]

def grid_from_weeks(weeks):
    grid=[]
    for w in weeks:
        days=w.get('contributionDays',w) if isinstance(w,dict) else w
        col=[0]*7
        for i,d in enumerate(days[:7]): col[i]=int(d.get('contributionCount',0))
        grid.append(col)
    while len(grid)<WEEKS: grid.insert(0,[0]*7)
    return grid[-WEEKS:]

def font(size,bold=False):
    paths=['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    for p in paths:
        if os.path.exists(p): return ImageFont.truetype(p,size)
    return ImageFont.load_default()

def level(v, mx):
    if v<=0:return 0
    if mx<=1:return 4
    return min(4,1+int((v/mx)*3.9))

def make_gif(grid):
    cols=WEEKS
    width=PAD*2+cols*(CELL+GAP)-GAP
    height=HEADER+PAD+ROWS*(CELL+GAP)-GAP+PAD
    mx=max(max(c) for c in grid) or 1
    # A serpentine path visits every contribution cell in a dark-grid worm motion.
    path=[]
    for x in range(cols):
        ys=range(ROWS) if x%2==0 else range(ROWS-1,-1,-1)
        for y in ys:path.append((x,y))
    # Start near the oldest week and advance; head glows, body trails behind.
    frames=[]
    trail=12
    for frame in range(0,len(path),4):
        im=Image.new('RGB',(width,height),BG)
        d=ImageDraw.Draw(im)
        d.text((PAD,8),f'CONTRIBUTION SNAKE  ·  {USER}',font=font(13,True),fill=(220,230,240))
        d.text((width-PAD,8),'LIVE · DARK MODE',font=font(11),fill=(82,218,112),anchor='ra')
        # grid — contribution blocks are the food; eaten blocks briefly dim behind the worm.
        eaten=set(path[:frame+1])
        for x in range(cols):
            for y in range(ROWS):
                px=PAD+x*(CELL+GAP); py=HEADER+y*(CELL+GAP)
                lv=level(grid[x][y],mx)
                fill=EMPTY if lv==0 else GREENS[lv]
                if (x,y) in eaten and lv>0:
                    fill=(18,52,34)
                d.rounded_rectangle((px,py,px+CELL,py+CELL),radius=4,fill=fill)
        # worm body
        for k in range(trail,0,-1):
            idx=frame-k
            if idx<0: continue
            x,y=path[idx%len(path)]
            px=PAD+x*(CELL+GAP); py=HEADER+y*(CELL+GAP)
            alpha=max(40,190-int(k*9))
            c=(45, min(255,100+alpha//2), min(255,90+alpha//2))
            d.rounded_rectangle((px-2,py-2,px+CELL+2,py+CELL+2),radius=6,outline=c,width=2)
        # head
        x,y=path[frame%len(path)]
        px=PAD+x*(CELL+GAP); py=HEADER+y*(CELL+GAP)
        d.ellipse((px-4,py-4,px+CELL+4,py+CELL+4),fill=(120,255,150),outline=(220,255,225),width=2)
        # little eyes + bite spark, so the animation visibly "eats" contribution blocks.
        d.ellipse((px+4,py+3,px+7,py+6),fill=BG); d.ellipse((px+9,py+3,px+12,py+6),fill=BG)
        for sx,sy in ((-4,5),(CELL+4,4),(CELL//2, -5),(CELL//2, CELL+4)):
            d.ellipse((px+sx-1,py+sy-1,px+sx+1,py+sy+1),fill=(120,255,150))
        frames.append(im)
    # hold final frame briefly
    frames += [frames[-1]]*4
    OUT.parent.mkdir(parents=True,exist_ok=True)
    frames[0].save(OUT,save_all=True,append_images=frames[1:],duration=75,loop=0,optimize=False)

weeks=fetch() or fallback()
make_gif(grid_from_weeks(weeks))
print(f'Wrote {OUT}')
