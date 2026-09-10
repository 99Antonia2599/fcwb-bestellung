"""Lädt die Originalbilder vom 11teamsports-CDN (transparent), legt sie auf Weiss, verkleinert, speichert als JPEG-Base64 in images.json."""
import json,io,base64,urllib.request,os
from PIL import Image
BASE='https://www.11teamsports.com/cdn-cgi/image/format=png,width=400/ch-de/media/'
out={}
if os.path.exists('images.json'): out=json.load(open('images.json'))
for line in open('imgmap.txt',encoding='utf-8'):
    if not line.strip(): continue
    key,path=line.split(None,1); path=path.strip()
    if key in out: continue
    url=BASE+path if not path.startswith('de-de:') else BASE.replace('/ch-de/','/de-de/')+path[6:]
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
    try:
        data=urllib.request.urlopen(req,timeout=30).read()
        im=Image.open(io.BytesIO(data)).convert('RGBA')
        bg=Image.new('RGBA',im.size,(255,255,255,255)); bg.alpha_composite(im); im=bg.convert('RGB')
        bbox=Image.eval(Image.open(io.BytesIO(data)).convert('RGBA').split()[3],lambda a:255 if a>10 else 0).getbbox()
        if bbox: im=im.crop(bbox)
        im.thumbnail((260,260))
        canvas=Image.new('RGB',(260,260),(255,255,255)); canvas.paste(im,((260-im.width)//2,(260-im.height)//2))
        buf=io.BytesIO(); canvas.save(buf,'JPEG',quality=86,optimize=True)
        out[key]=base64.b64encode(buf.getvalue()).decode(); print('ok',key,len(buf.getvalue()))
    except Exception as e: print('FEHLER',key,e)
json.dump(out,open('images.json','w'))
print(len(out),'Bilder')
