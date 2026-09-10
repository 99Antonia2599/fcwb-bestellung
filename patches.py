"""Kleine Eingriffe in Erols minifizierten App-Code (nur Text-Ersetzungen)."""
import os,re
HERE=os.path.dirname(__file__)

def picker(html):
    old=open(os.path.join(HERE,'patch_picker_old.txt'),encoding='utf-8').read()
    new=('v.default.createElement("div",{style:{marginBottom:14}},z0.map(CAT=>{let L=f.filter(F=>F.cat===CAT);'
         'if(!L.length)return null;return v.default.createElement("div",{key:CAT,style:{marginBottom:10}},'
         'v.default.createElement("div",{style:{fontSize:11,fontWeight:800,letterSpacing:.5,textTransform:"uppercase",color:Fa[CAT].color,margin:"4px 0"}},Fa[CAT].label),'
         'v.default.createElement("div",{style:{display:"flex",gap:6,flexWrap:"wrap"}},L.map(F=>{let on=s.indexOf(F.id)>=0;'
         'return v.default.createElement("button",{key:F.id,onClick:()=>p(F.id),title:F.name+" \u00b7 "+F.color+" \u00b7 Art. "+F.art,'
         'style:{display:"flex",alignItems:"center",gap:8,border:"1.5px solid "+(on?H.blue:H.line),background:on?"#EAF3FB":"#fff",color:H.ink,borderRadius:10,padding:"4px 10px 4px 4px",fontSize:12,fontWeight:700,cursor:"pointer",textAlign:"left"}},'
         'F.img?v.default.createElement("img",{src:F.img,alt:"",style:{width:34,height:34,objectFit:"contain",borderRadius:6,background:"#fff"}}):null,'
         'v.default.createElement("span",null,v.default.createElement("span",{style:{display:"block"}},(on?"\u2713 ":"")+K(F.name)),'
         'v.default.createElement("span",{style:{display:"block",fontSize:10,fontWeight:600,color:H.muted}},F.color+" \u00b7 "+F.art)))})))}))')
    assert old in html, 'Picker-Anker nicht gefunden'
    return html.replace(old,new,1)

def testmode(html, phone):
    """Alle WhatsApp-Empfaenger auf eine Testnummer umleiten."""
    m=re.search(r'Gg=\{[^}]*\}',html); assert m
    names=re.findall(r'(\w+):"\d+"',m.group(0))
    new='Gg={'+','.join(f'{n}:"{phone}"' for n in names)+'}'
    return html.replace(m.group(0),new,1)

def stages(html):
    """Neue erste Stufe 'Auszuloesen' + Knopf 'Bei 11teamsports bestellt'."""
    old=r'nA=["Bestellt","Geliefert","Bedruckt","Abholbereit","\xDCbergeben"],tA=["#8C6D1F","#0070C0","#7A3FB0","#C77700","#1E8E3E"]'
    new=r'nA=["Auszul\xF6sen","Bestellt","Geliefert","Bedruckt","Abholbereit","\xDCbergeben"],tA=["#C0392B","#8C6D1F","#0070C0","#7A3FB0","#C77700","#1E8E3E"]'
    assert old in html, 'Stufen-Anker nicht gefunden'
    html=html.replace(old,new,1)
    assert html.count('F.stage===4')==2
    html=html.replace('F.stage===4','F.stage===5')
    anchor='!d.archived&&v.default.createElement(Ve,{kind:"primary",small:!0,onClick:()=>n(d.id)},"Status melden")'
    assert anchor in html, 'Status-melden-Anker nicht gefunden'
    btn=r'!d.archived&&w===0&&v.default.createElement(Ve,{kind:"gold",small:!0,onClick:()=>{if(confirm("Bestellung bei 11teamsports ausgel\xF6st? Alle Positionen werden auf \xABBestellt\xBB gesetzt."))x(d.id,1)}},"\u2714 Bei 11teamsports bestellt"),'
    return html.replace(anchor,btn+anchor,1)

def rep1(html, old, new, label):
    assert html.count(old)==1, f'{label}: Anker {html.count(old)}x gefunden'
    return html.replace(old, new, 1)

INPUT_STYLE='{padding:"7px 10px",borderRadius:999,border:"1.5px solid "+H.line,fontSize:13,minWidth:200,outline:"none"}'

def search(html):
    # A) Suche im Einzel-Bestellen (Komponente iy)
    html=rep1(html, r'[d,w]=(0,v.useState)(null),K=e.filter(b=>b.cat===o&&Hu(b,c)),',
        r'[d,w]=(0,v.useState)(null),[SQ,SSQ]=(0,v.useState)(""),K=e.filter(b=>Hu(b,c)&&(SQ?(b.name+" "+b.color+" "+b.art).toLowerCase().includes(SQ.toLowerCase()):b.cat===o)),','iy-state')
    html=rep1(html, r'"Artikel ausw\xE4hlen"),v.default.createElement("div",{style:{display:"flex",gap:6,flexWrap:"wrap",marginLeft:"auto"}},',
        r'"Artikel ausw\xE4hlen"),v.default.createElement("input",{value:SQ,onChange:b=>SSQ(b.target.value),placeholder:"Suchen: Name, Farbe, Art.-Nr.",style:'+INPUT_STYLE+r'}),v.default.createElement("div",{style:{display:"flex",gap:6,flexWrap:"wrap",marginLeft:"auto"}},','iy-input')
    return html

def tracking(html):
    # C) Verfolgung: Hinweistext, Import-Knopf raus, Suche + Statusfilter, PDF-Knopf
    html=rep1(html, r'"Die Besteller senden ihre Bestellung per WhatsApp in die Gruppe. Die ausf\xFChrende Person f\xFCgt sie hier \xFCber ",v.default.createElement("b",null,"\xABBestellung importieren\xBB")," ein und verfolgt den Status. Fertiges wandert ins ",v.default.createElement("b",null,"Archiv"),"."',
        r'"Neue Bestellungen erscheinen hier automatisch mit Status ",v.default.createElement("b",null,"Auszul\xF6sen"),". Wer bei 11teamsports bestellt hat, klickt ",v.default.createElement("b",null,"✔ Bei 11teamsports bestellt"),". Danach pro Position den Status weiterziehen bis ",v.default.createElement("b",null,"\xDCbergeben"),", fertige Bestellungen ins ",v.default.createElement("b",null,"Archiv"),". Alles wird f\xFCr alle live gespeichert."','hint')
    html=rep1(html, r'[o,l]=(0,v.useState)(!1),c=e.filter(d=>!d.archived),u=e.filter(d=>d.archived),f=a==="offen"?c:u,',
        r'[o,l]=(0,v.useState)(!1),[FQ,SFQ]=(0,v.useState)(""),[FS,SFS]=(0,v.useState)(""),c=e.filter(d=>!d.archived),u=e.filter(d=>d.archived),f=(a==="offen"?c:u).filter(d=>(!FQ||(d.besteller+" "+(d.empfaenger||"")+" "+Ds(d.date)+" "+(d.note||"")+" "+d.items.map(F=>F.name+" "+F.art+" "+(F.player||"")).join(" ")).toLowerCase().includes(FQ.toLowerCase()))&&(FS===""||Math.min.apply(null,d.items.map(F=>F.stage))===+FS)),','hy-state')
    html=rep1(html, r'v.default.createElement(Ve,{kind:"dark",small:!0,onClick:()=>l(!0),style:{marginLeft:"auto"}},"+ Bestellung importieren")',
        r'v.default.createElement("input",{value:FQ,onChange:d=>SFQ(d.target.value),placeholder:"Suchen: Besteller, Empf\xE4nger, Artikel, Datum",style:{...'+INPUT_STYLE+r',marginLeft:"auto"}}),v.default.createElement("select",{value:FS,onChange:d=>SFS(d.target.value),style:{padding:"7px 10px",borderRadius:999,border:"1.5px solid "+H.line,fontSize:13,fontWeight:700,color:H.navy}},v.default.createElement("option",{value:""},"Alle Status"),nA.map((d,w)=>v.default.createElement("option",{key:w,value:w},d)))','hy-filter')
    html=rep1(html, r'v.default.createElement(Ve,{kind:"ghost",small:!0,onClick:()=>M0(d)},"Excel"),',
        r'v.default.createElement(Ve,{kind:"ghost",small:!0,onClick:()=>M0(d)},"Excel"),v.default.createElement(Ve,{kind:"ghost",small:!0,onClick:()=>window.FCWB_PDF(d,nA)},"PDF"),','hy-pdf')
    return html

def teamorder(html):
    """Ganze Team-Bestell-Komponente (fy) durch neue Version ersetzen."""
    a=html.find('function fy('); assert a>0
    b=html.find('function ',a+10); assert b>a
    new=open(os.path.join(HERE,'fy_new.js'),encoding='utf-8').read().strip()
    return html[:a]+new+html[b:]

def colors(html):
    """Roly-Farbcodes der Ueberzieher mit Namen versehen."""
    for code,name in [("221","Neongelb"),("222","Neongr\xFCn"),("223","Neonorange"),("228","Neonpink")]:
        old='color:"%s",art:"RY0417'%code
        assert html.count(old)==2, old
        html=html.replace(old,'color:"%s %s",art:"RY0417'%(name,code))
    return html

def seedversion(html):
    """Katalog-Version hochzaehlen, damit Browser den zwischengespeicherten Katalog ersetzen."""
    import time
    v=int(time.strftime('%Y%m%d%H%M'))
    assert html.count('}],Qg=3,')==1
    return html.replace('}],Qg=3,','}],Qg=%d,'%v,1)

def teamhint(html):
    old='"Excel-Spalten (Titel in Zeile 1): "'
    assert html.count(old)==1, html.count(old)
    return html.replace(old,'"Zum Bearbeiten direkt in eine Zelle klicken (Nr., Name, Initialen, Gr\xF6ssen, Bedruckung) \u2013 wird sofort f\xFCr alle gespeichert. Excel-Spalten (Titel in Zeile 1): "',1)

def confirm_and_nav(html):
    """Neue Bestaetigungsseite, Import-Code aus WhatsApp-Text, Home-Klick, Reiterwechsel per Ereignis, Warenkorb fest unten rechts."""
    # oy ersetzen
    a=html.find('function oy('); b=html.find('function ',a+10); assert a>0 and b>a
    html=html[:a]+open(os.path.join(HERE,'oy_new.js'),encoding='utf-8').read().strip()+html[b:]
    # Import-Code aus dem Nachrichtentext entfernen
    html=rep1(html,'+`\n\n`+a}function bP(','}function bP(','xp-code')
    # Ou: auf Ereignis fcwb-tab hoeren (Reiter wechseln von ueberall)
    html=rep1(html,'let g=({id:d,label:w})=>v.default.createElement("button",{onClick:()=>r(d)',
        '(0,v.useEffect)(()=>{let hh=ev=>r(ev.detail);window.addEventListener("fcwb-tab",hh);return()=>window.removeEventListener("fcwb-tab",hh)},[]);let g=({id:d,label:w})=>v.default.createElement("button",{onClick:()=>r(d)','ou-event')
    # Titel klickbar -> Startseite (Bestellen)
    html=rep1(html,'v.default.createElement("div",{style:{fontWeight:900,fontSize:18}},"Materialbestellung")',
        'v.default.createElement("div",{onClick:()=>r("bestellen"),title:"Zur Startseite",style:{fontWeight:900,fontSize:18,cursor:"pointer"}},"Materialbestellung")','title-home')
    # Warenkorb-Knopf: fest unten rechts, immer sichtbar
    html=rep1(html,'Q>0&&!m&&v.default.createElement("div",{style:{position:"sticky",bottom:12,display:"flex",justifyContent:"center"}}',
        'Q>0&&!m&&v.default.createElement("div",{style:{position:"fixed",right:18,bottom:18,zIndex:60,display:"flex",justifyContent:"flex-end"}}','cart-fixed')
    return html

def tracking2(html):
    """Auto-Archiv nach Uebergeben (mit Rueckfrage) + Stufe Bedruckt nur bei bedruckten Positionen."""
    # Stufen setzen: danach pruefen, ob alles uebergeben -> Rueckfrage -> Archiv
    html=rep1(html,
      r'h=(d,w,K)=>r(e.map(S=>S.id===d?{...S,items:S.items.map((F,k)=>k===w?{...F,stage:K}:F)}:S)),x=(d,w)=>r(e.map(K=>K.id===d?{...K,items:K.items.map(S=>({...S,stage:w}))}:K)),',
      r'AR=(L,id)=>L.map(S=>S.id!==id||S.archived||!S.items.every(F=>F.stage===5)?S:(confirm("Alle Positionen sind übergeben. Bestellung jetzt ins Archiv verschieben?")?{...S,archived:!0}:S)),'
      r'h=(d,w,K)=>r(AR(e.map(S=>S.id===d?{...S,items:S.items.map((F,k)=>k===w?{...F,stage:K}:F)}:S),d)),x=(d,w)=>r(AR(e.map(K=>K.id===d?{...K,items:K.items.map(S=>({...S,stage:w}))}:K),d)),',
      'auto-archiv')
    # Stufenleiste pro Position: Bedruckt (Index 3) nur wenn Position eine Bedruckung hat
    html=rep1(html,'function uy({stage:e,onSet:r}){return v.default.createElement("div",{style:{display:"flex",gap:4,flexWrap:"wrap",justifyContent:"flex-end"}},nA.map((t,n)=>{let a=n<=e;',
      'function uy({stage:e,onSet:r,druck:dr}){return v.default.createElement("div",{style:{display:"flex",gap:4,flexWrap:"wrap",justifyContent:"flex-end"}},nA.map((t,n)=>{if(n===3&&!dr)return null;let a=n<=e;','uy-druck')
    html=rep1(html,'v.default.createElement(uy,{stage:F.stage,onSet:y=>h(d.id,k,y)})','v.default.createElement(uy,{stage:F.stage,druck:F.druck,onSet:y=>h(d.id,k,y)})','uy-call')
    # "alle setzen": Bedruckt nur wenn irgendeine Position bedruckt ist
    html=rep1(html,'nA.map((F,k)=>v.default.createElement("option",{key:k,value:k},F))','nA.map((F,k)=>k===3&&!d.items.some(I=>I.druck)?null:v.default.createElement("option",{key:k,value:k},F))','alle-setzen')
    return html

def statuslabel(html):
    return rep1(html,'Gemeinsam (live)"','Verbunden"','status-label')

def no_excel_pdf(html):
    """Excel-/PDF-Knoepfe in Verfolgung entfernen (Bestaetigungsseite: oy_new.js)."""
    html=rep1(html,'v.default.createElement(Ve,{kind:"ghost",small:!0,onClick:()=>M0(d)},"Excel"),v.default.createElement(Ve,{kind:"ghost",small:!0,onClick:()=>window.FCWB_PDF(d,nA)},"PDF"),','','no-excel-pdf')
    return html

def no_phones(html):
    """Alle Handynummern entfernen: WhatsApp nur noch ueber 'Chat waehlen' / 'Text kopieren'."""
    m=re.search(r'Gg=\{[^}]*\}',html); assert m
    html=html.replace(m.group(0),'Gg={}',1)
    assert not re.search(r'417\d{8}',html), 'Nummer noch im Code'
    html=html.replace('"Geht an den Besteller sowie immer an Roberto und Erol. Pro Empf\xE4nger einen Button antippen."','"WhatsApp \xF6ffnen, Chat oder Gruppe w\xE4hlen und senden \u2013 der Text ist vorausgef\xFCllt."')
    return html
