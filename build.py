import re,sys,pathlib,os
here=pathlib.Path(__file__).parent
src=(here.parent/'index_7.html').read_text(encoding='utf-8')
url=sys.argv[1] if len(sys.argv)>1 else '__SUPABASE_URL__'
key=sys.argv[2] if len(sys.argv)>2 else '__SUPABASE_ANON_KEY__'
adapter=(here/'adapter.js').read_text(encoding='utf-8').replace('__SUPABASE_URL__',url).replace('__SUPABASE_ANON_KEY__',key)
design=(here/'design.css').read_text(encoding='utf-8')+(here/'pdf.js').read_text(encoding='utf-8')
# Firebase-Kopf (SDK + Config) entfernen
out=re.sub(r'<script src="https://www\.gstatic\.com/firebasejs[^>]*></script>\s*','',src)
out=re.sub(r'<script>\s*window\.FCWB_FIREBASE = \{.*?\};\s*</script>','',out,flags=re.S)
assert 'firebasejs' not in out and 'AIzaSy' not in out
import whiten,patches
out=whiten.process(out)
out=patches.teamorder(out)
out=patches.stages(out)
out=patches.search(out)
out=patches.tracking(out)
out=patches.colors(out)
out=patches.seedversion(out)
out=patches.teamhint(out)
out=patches.confirm_and_nav(out)
out=patches.tracking2(out)
out=patches.statuslabel(out)
out=patches.no_excel_pdf(out)
out=patches.no_phones(out)
out=out.replace('</head>',adapter+'\n'+design+'\n</head>',1)
# Login-Seite (Passwort nur als SHA-256-Pruefsumme im Code)
import base64,hashlib
login=(here/'login.js').read_text(encoding='utf-8')
logo_b64=base64.b64encode((here/'logo.png').read_bytes()).decode()
pitch=("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 600 300' fill='none' stroke='white' stroke-width='2.5' stroke-opacity='.18'>"
 "<rect x='10' y='10' width='580' height='280' rx='4'/><line x1='300' y1='10' x2='300' y2='290'/><circle cx='300' cy='150' r='55'/>"
 "<rect x='10' y='70' width='95' height='160'/><rect x='10' y='110' width='40' height='80'/><rect x='495' y='70' width='95' height='160'/><rect x='550' y='110' width='40' height='80'/>"
 "<path d='M105 115 a45 45 0 0 1 0 70'/><path d='M495 115 a45 45 0 0 0 0 70'/></svg>")
pw=os.environ.get('FCWB_PASSWORD','FCWB1914')
login=login.replace('__LOGO__','data:image/png;base64,'+logo_b64).replace('__PITCH__',pitch).replace('__PWHASH__',hashlib.sha256(pw.encode()).hexdigest())
assert '<div id="root"></div>' in out
saved=(here/'saved.js').read_text(encoding='utf-8')
out=out.replace('<div id="root"></div>','<div id="root"></div>\n'+login+'\n'+saved,1)
(here/'index.html').write_text(out,encoding='utf-8')
print('ok',len(out))
