"""Render a vertical thriller short.
Outputs: output/video.mp4
Env:
  FPS=30
  DURATION=18
  W=1080
  H=1920
"""
import math, os, random, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W=int(os.getenv('W','1080'))
H=int(os.getenv('H','1920'))
FPS=int(os.getenv('FPS','30'))
DURATION=int(os.getenv('DURATION','18'))
voicefile = Path('output/voice.mp3')
if voicefile.exists():
    try:
        probe = subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(voicefile)], text=True)
        DURATION = max(18, math.ceil(float(probe.strip())))
    except Exception as exc:
        print('Audio duration probe failed:', exc)

OUT=Path('output'); OUT.mkdir(exist_ok=True)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
REG='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

def font(n,b=True):
    return ImageFont.truetype(FONT if b else REG,n)

def rect(d,b,fill,r=0,outline=None,width=1):
    bb=tuple(int(x) for x in b)
    if r:
        d.rounded_rectangle(bb,radius=r,fill=fill,outline=outline,width=width)
    else:
        d.rectangle(bb,fill=fill,outline=outline,width=width)

def txt(d,s,x,y,size=24,color='#f2f4fb',center=False,bold=True,stroke=0):
    f=font(size,bold)
    if center:
        box=d.textbbox((0,0),s,font=f)
        x-=(box[2]-box[0])/2
    d.text((int(x),int(y)),s,font=f,fill=color,stroke_width=stroke,stroke_fill='#101219')

def lerp(a,b,t): return a+(b-a)*t

def ease(t): return 3*t*t-2*t*t*t

def stamp(d,time):
    rect(d,(W*0.29,H*0.04,W*0.71,H*0.078),'#10131b',14,outline='#53525a',width=2)
    txt(d,time,W/2,H*0.047,32,'#efbd69',True)

def boxlabel(d,a,b,color):
    txt(d,a,W/2,H*0.824,58,'#ffffff',True,stroke=2)
    txt(d,b,W/2,H*0.87,54,color,True,stroke=2)

def phone_scene(t):
    im=Image.new('RGB',(W,H),'#171313'); d=ImageDraw.Draw(im)
    # background gradient
    for y in range(H):
        g=int(18+20*(y/H))
        d.line((0,y,W,y),fill=(g,g-2,g-1))
    # desk
    d.polygon([(0,H*0.72),(W,H*0.65),(W,H),(0,H)],fill='#2c2525')
    # phone motion
    pull=min(1,max(0,t/1.7))
    pull=ease(pull)
    px=lerp(W*0.54,W*0.44,pull)
    py=lerp(H*0.68,H*0.48,pull)
    ang=lerp(12,-2,pull)
    # simple hand silhouette (no cutaway)
    palm=[(W*0.70,H*0.84),(W*0.58,H*0.74),(W*0.52,H*0.75),(W*0.49,H*0.80),(W*0.58,H*0.92)]
    d.polygon(palm,fill='#c18f76')
    for off in [0,0.03,0.06,0.09]:
        d.rounded_rectangle((W*(0.56-off),H*(0.72-off*0.2),W*(0.61-off),H*(0.80-off*0.15)),radius=15,fill='#c69279')
    # phone body
    pw,ph=310,560
    phone=Image.new('RGBA',(pw,ph),(0,0,0,0))
    pd=ImageDraw.Draw(phone)
    pd.rounded_rectangle((0,0,pw,ph),radius=42,fill='#11161d',outline='#404854',width=5)
    pd.rounded_rectangle((18,44,pw-18,ph-18),radius=28,fill='#101820')
    pd.rounded_rectangle((120,18,190,32),radius=8,fill='#2c333c')
    # screen alert appears
    show=max(0,min(1,(t-0.9)/0.7))
    if show>0:
        glow=int(170+70*math.sin(t*7)**2)
        pd.rounded_rectangle((28,125,pw-28,330),radius=28,fill='#2a1417',outline=(glow,73,69),width=5)
        pd.polygon([(pw/2,155),(pw/2-34,222),(pw/2+34,222)],fill='#f35e54')
        pd.text((pw/2-8,174),'!',font=font(34),fill='#3e1818')
        pd.text((pw/2-112,246),'ЭКСТРЕННОЕ',font=font(30),fill='#ffffff')
        pd.text((pw/2-82,284),'ОПОВЕЩЕНИЕ',font=font(30),fill='#ff9b91')
    # notification bars below
    for i in range(4):
        yy=360+i*38
        pd.rounded_rectangle((35,yy,pw-35,yy+22),radius=9,fill='#26303b')
    phone=phone.rotate(ang,expand=True,resample=Image.Resampling.BICUBIC)
    im.paste(phone,(int(px-phone.size[0]/2),int(py-phone.size[1]/2)),phone)
    stamp(d,'ДЕНЬ 1 — 03:17')
    boxlabel(d,'ТЕЛЕФОН ЗАВИБРИРОВАЛ','И ВСЕ ЗАМЕРЛИ','#ff665a')
    return im

def street_scene(t):
    im=Image.new('RGB',(W,H),'#a9a99c'); d=ImageDraw.Draw(im)
    # sky/fog
    for y in range(int(H*0.65)):
        k=y/(H*0.65)
        g=int(164-32*k)
        d.line((0,y,W,y),fill=(g,g,int(g*0.92)))
    road_top=int(H*0.52)
    d.polygon([(0,road_top+60),(W*0.46,road_top),(W*0.54,road_top),(W,road_top+58),(W,H),(0,H)],fill='#737979')
    # sidewalks
    d.polygon([(0,road_top+120),(W*0.46,road_top+10),(W*0.47,road_top+12),(W*0.24,H),(0,H)],fill='#a4a399')
    d.polygon([(W,road_top+118),(W*0.54,road_top+10),(W*0.53,road_top+12),(W*0.76,H),(W,H)],fill='#a8a89b')
    # buildings
    for side in (-1,1):
        for j in range(6,0,-1):
            depth=j/6
            width=int(50+220*depth)
            hh=int(220+530*depth)
            vx=W/2 + side*(75+(j-1)*58)
            left=vx-width if side<0 else vx
            top=road_top-hh
            color='#afb3ab' if side<0 else '#9aa29b'
            d.polygon([(left,top),(left+width,top+18),(left+width,road_top+20),(left,road_top+40)],fill=color,outline='#8d948e')
            cols=max(2,int(width/28))
            for row in range(2,11):
                wy=top+row*(hh-40)/12
                for col in range(1,cols):
                    wx=left+col*width/(cols+1)
                    ww=max(6,int(5+depth*6))
                    hh2=max(8,int(9+depth*7))
                    rect(d,(wx,wy,wx+ww,wy+hh2),'#e4bb73' if (row+col+j)%6==0 else '#606e72',2)
    # trees
    for j in range(5,0,-1):
        sc=(j/5)**1.25
        x=W/2+(-1 if j%2 else 1)*(85+sc*310)
        y=road_top+35+sc*320
        d.line((x,y,x,y-130*sc),fill='#5b584a',width=max(3,int(10*sc)))
        for a,b,rr,c in [(-34,-112,42,'#b98e49'),(21,-138,44,'#d1a454'),(42,-94,32,'#89915a'),(-48,-84,34,'#c3a052')]:
            d.ellipse((x+(a-rr)*sc,y+(b-rr)*sc,x+(a+rr)*sc,y+(b+rr)*sc),fill=c)
    # correct-direction car left->right
    carx=int(-180 + t*260)
    cary=int(road_top+190)
    d.polygon([(carx,cary),(carx+150,cary-12),(carx+185,cary+42),(carx-18,cary+50)],fill='#a63d31')
    rect(d,(carx+34,cary-26,carx+112,cary+6),'#3b5258',8)
    for cx in (carx+22,carx+138):
        d.ellipse((cx-18,cary+28,cx+18,cary+64),fill='#242424')
        d.ellipse((cx-8,cary+38,cx+8,cary+54),fill='#707070')
    # alert card
    if t>1.0:
        glow=int(145+70*math.sin(t*6)**2)
        rect(d,(W*0.08,H*0.33,W*0.92,H*0.50),'#29141b',35,outline=(glow,73,69),width=6)
        d.polygon([(W/2,H*0.355),(W/2-50,H*0.415),(W/2+50,H*0.415)],fill='#f35e54')
        txt(d,'!',W/2,H*0.371,48,'#3e1818',True)
        txt(d,'НЕ ВЫХОДИТЕ',W/2,H*0.437,42,'#ffffff',True)
    stamp(d,'ДЕНЬ 1 — 03:19')
    boxlabel(d,'ЧЕРЕЗ ДВЕ МИНУТЫ','УЛИЦА ОПУСТЕЛА','#ffbf63')
    return im

def building_scene(t):
    im=Image.new('RGB',(W,H),'#080c13'); d=ImageDraw.Draw(im)
    random.seed(11)
    for _ in range(90):
        x=random.randrange(W); y=random.randrange(H); d.point((x,y),fill='#222f3f')
    stamp(d,'ДЕНЬ 1 — 04:02')
    txt(d,'ДОМ № 17',W/2,160,42,'#dce5ef',True)
    rect(d,(100,260,980,1388),'#141b27',8,outline='#435165',width=4)
    for floor in range(7):
        y=290+floor*152
        d.line((108,y+120,972,y+120),fill='#465266',width=5)
        for room in range(4):
            x=138+room*208
            rect(d,(x,y+18,x+154,y+98),'#26374a' if (floor+room)%3==0 else '#1b2634',6)
            rect(d,(x+24,y+34,x+122,y+92),'#e5b366' if (floor*5+room)%7==0 else '#425168',4)
            d.line((x+77,y+34,x+77,y+92),fill='#1f2d40',width=5)
    path=[]
    for idx in range(7):
        y=336+idx*152
        path.append((220 if idx%2 else 854,y))
    d.line(path,fill='#728bbb',width=7,joint='curve')
    frac=min(1,max(0,t/5.0)); pos=frac*(len(path)-1); j=min(len(path)-2,int(pos)); v=pos-j
    x=path[j][0]*(1-v)+path[j+1][0]*v; y=path[j][1]*(1-v)+path[j+1][1]*v
    d.ellipse((x-24,y-24,x+24,y+24),fill='#ff654f')
    d.ellipse((x-40,y-40,x+40,y+40),outline='#f57469',width=4)
    d.ellipse((725-20,670-20,725+20,670+20),fill='#49dcb1')
    rect(d,(170,1450,910,1530),'#262023',18,outline='#f05b57',width=4)
    txt(d,'СОСЕДИ СПУСКАЮТСЯ ВНИЗ',W/2,1468,30,'#ffaba4',True)
    boxlabel(d,'НО НИКТО НЕ ОБЪЯСНЯЛ','ПОЧЕМУ ОНИ УХОДЯТ','#ffbf63')
    return im

def map_scene(t):
    im=Image.new('RGB',(W,H),'#0b0f17'); d=ImageDraw.Draw(im)
    stamp(d,'ДЕНЬ 1 — 04:11')
    txt(d,'КАРТА РАЙОНА',W/2,160,40,'#cbd3df',True)
    for i in range(8):
        for j in range(6):
            x=44+i*128; y=270+j*180
            rect(d,(x,y,x+95,y+138),'#232c38' if (i+j)%3 else '#313744',6)
    for x in [155,410,665,920]: d.line((x,230,x,1470),fill='#51596a',width=24)
    for y in [450,810,1170,1500]: d.line((0,y,W,y),fill='#50586a',width=20)
    txt(d,'ЛЕСНАЯ',470,760,28,'#939aa6',True)
    d.line((0,1350,W,940),fill='#5f7487',width=8)
    d.ellipse((240,1070,300,1130),fill='#4fe3b8')
    d.ellipse((220,1050,320,1150),outline='#4fe3b8',width=5)
    rect(d,(170,1160,370,1215),'#17352f',10)
    txt(d,'ВАШ ДОМ',270,1174,22,'#b5ffdc',True)
    # approaching signals
    base=min(1,t/6)
    sx=840-300*base; sy=560+260*base
    rad=36+20*math.sin(t*5)**2
    for m in [0,40,84]:
        d.ellipse((sx-rad-m,sy-rad-m,sx+rad+m,sy+rad+m),outline='#ff675a',width=4)
    d.ellipse((sx-16,sy-16,sx+16,sy+16),fill='#ff6254')
    rect(d,(210,1470,870,1550),'#321d26',16,outline='#b14d54',width=4)
    txt(d,'НЕИЗВЕСТНЫЙ СИГНАЛ ДВИГАЛСЯ К ДОМУ',W/2,1490,26,'#ffaaa5',True)
    boxlabel(d,'И ТОГДА СТАЛО ПОНЯТНО','ПРЕДУПРЕЖДЕНИЕ БЫЛО НЕ СЛУЧАЙНЫМ','#ff665a')
    return im

def render(t):
    # Split the narration duration between four animated sequences.
    scene_len = DURATION / 4
    if t < scene_len: return phone_scene(t * 4 / scene_len)
    if t < 2*scene_len: return street_scene((t-scene_len) * 5 / scene_len)
    if t < 3*scene_len: return building_scene((t-2*scene_len) * 5 / scene_len)
    return map_scene((t-3*scene_len) * 4 / scene_len)

def main():
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT/'video.mp4')]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for n in range(DURATION*FPS):
        frame=render(n/FPS)
        try:
            p.stdin.write(frame.tobytes())
        except BrokenPipeError:
            break
    p.stdin.close()
    if p.wait()!=0:
        raise RuntimeError('FFmpeg render failed')
    print('Created',OUT/'video.mp4')

if __name__=='__main__':
    main()
