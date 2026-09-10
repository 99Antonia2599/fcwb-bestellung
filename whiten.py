"""Schwarzen Bildhintergrund auf Weiss setzen (Flood-Fill vom Rand).
Schwarze Artikel (Farbe 'Schwarz') werden ausgelassen, sonst verschwinden sie."""
import re,base64,io
from collections import deque
from PIL import Image, ImageFilter

def whiten(b64, thr=40):
    im=Image.open(io.BytesIO(base64.b64decode(b64))).convert('RGB')
    w,h=im.size
    if not all(sum(im.getpixel(p))<60 for p in [(1,1),(w-2,1),(1,h-2),(w-2,h-2)]): return None
    px=im.load(); mask=Image.new('L',(w,h),0); m=mask.load()
    q=deque([(x,y) for x in range(w) for y in (0,h-1)]+[(x,y) for y in range(h) for x in (0,w-1)]); seen=set(q)
    while q:
        x,y=q.popleft()
        if max(px[x,y])>=thr: continue
        m[x,y]=255
        for n in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if 0<=n[0]<w and 0<=n[1]<h and n not in seen: seen.add(n); q.append(n)
    mask=mask.filter(ImageFilter.MaxFilter(3))  # dunkle JPEG-Saumreste mitnehmen
    out=Image.composite(Image.new('RGB',(w,h),(255,255,255)),im,mask)
    return tile(out)

def tile(im):
    """Bild auf weisse 260x260-Kachel mit Rand setzen (gleiches Format wie die Shop-Bilder)."""
    im=im.convert('RGB')
    # weissen Rand wegschneiden
    inv=Image.eval(im.convert('L'),lambda p:255 if p<245 else 0); bb=inv.getbbox()
    if bb: im=im.crop(bb)
    im.thumbnail((220,220))
    c=Image.new('RGB',(260,260),(255,255,255)); c.paste(im,((260-im.width)//2,(260-im.height)//2))
    buf=io.BytesIO(); c.save(buf,'JPEG',quality=86,optimize=True); return base64.b64encode(buf.getvalue()).decode()

def tile_b64(b64):
    im=Image.open(io.BytesIO(base64.b64decode(b64)))
    return tile(im)

def process(html):
    import json,os
    orig=json.load(open(os.path.join(os.path.dirname(__file__),'images.json'))) if os.path.exists(os.path.join(os.path.dirname(__file__),'images.json')) else {}
    n=[0,0,0]
    def rep(m):
        color=m.group(1); art=m.group(2).split(',')[0]; img=m.group(3)
        key=art+'|'+color if art+'|'+color in orig else art
        if key in orig: n[2]+=1; return m.group(0).replace(img,orig[key])
        if 'schwarz' in color.lower(): n[1]+=1; return m.group(0).replace(img,tile_b64(img))
        new=whiten(img)
        if new: n[0]+=1; return m.group(0).replace(img,new)
        return m.group(0).replace(img,tile_b64(img))  # bereits weiss (z.B. Ueberzieher): nur Kachelformat
    html=re.sub(r'color:"([^"]*)",art:"([^"]*)",pnr:"[^"]*",type:"[^"]*",price:[^,]*,sizes:\[[^\]]*\],img:"data:image/jpeg;base64,([A-Za-z0-9+/=]+)"',rep,html)
    print(f'Original-Bilder: {n[2]}, weiss gemacht: {n[0]}, schwarz belassen: {n[1]}')
    return html
