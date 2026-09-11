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
    new=r'nA=["Bestellt","Bestellt","Geliefert","Bedruckt","Abholbereit","\xDCbergeben"],tA=["#8C6D1F","#8C6D1F","#0070C0","#7A3FB0","#C77700","#1E8E3E"]'
    assert old in html, 'Stufen-Anker nicht gefunden'
    html=html.replace(old,new,1)
    assert html.count('F.stage===4')==2
    html=html.replace('F.stage===4','F.stage===5')
    anchor='!d.archived&&v.default.createElement(Ve,{kind:"primary",small:!0,onClick:()=>n(d.id)},"Status melden")'
    assert anchor in html, 'Status-melden-Anker nicht gefunden'
    btn=r'!d.archived&&w===0&&v.default.createElement(Ve,{kind:"gold",small:!0,onClick:()=>{if(confirm("Bestellung bei 11teamsports ausgel\xF6st? Alle Positionen werden auf \xABBestellt\xBB gesetzt."))x(d.id,1)}},"\u2714 Bei 11teamsports bestellt"),'
    return html

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
        r'"Jede Bestellung wurde beim Abschliessen automatisch per E-Mail an den Shop gesendet. Mengen k\xF6nnen hier ge\xE4ndert oder Positionen storniert werden – der Shop wird dabei automatisch informiert. Status pro Position weiterziehen bis ",v.default.createElement("b",null,"\xDCbergeben"),"."','hint')
    html=rep1(html, r'[o,l]=(0,v.useState)(!1),c=e.filter(d=>!d.archived),u=e.filter(d=>d.archived),f=a==="offen"?c:u,',
        r'[o,l]=(0,v.useState)(!1),[FQ,SFQ]=(0,v.useState)(""),[FS,SFS]=(0,v.useState)(""),c=e.filter(d=>!d.archived),u=e.filter(d=>d.archived),f=(a==="offen"?c:u).filter(d=>(!FQ||(d.besteller+" "+(d.empfaenger||"")+" "+Ds(d.date)+" "+(d.note||"")+" "+d.items.map(F=>F.name+" "+F.art+" "+(F.player||"")).join(" ")).toLowerCase().includes(FQ.toLowerCase()))&&(FS===""||Math.min.apply(null,d.items.map(F=>F.stage))===+FS)),','hy-state')
    html=rep1(html, r'v.default.createElement(Ve,{kind:"dark",small:!0,onClick:()=>l(!0),style:{marginLeft:"auto"}},"+ Bestellung importieren")',
        r'v.default.createElement("input",{value:FQ,onChange:d=>SFQ(d.target.value),placeholder:"Suchen: Besteller, Empf\xE4nger, Artikel, Datum",style:{...'+INPUT_STYLE+r',marginLeft:"auto"}}),v.default.createElement("select",{value:FS,onChange:d=>SFS(d.target.value),style:{padding:"7px 10px",borderRadius:999,border:"1.5px solid "+H.line,fontSize:13,fontWeight:700,color:H.navy}},v.default.createElement("option",{value:""},"Alle Status"),nA.map((d,w)=>w===0?null:v.default.createElement("option",{key:w,value:w},d)))','hy-filter')
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
      r'h=(d,w,K)=>r(AR(e.map(S=>S.id===d?{...S,items:S.items.map((F,k)=>k===w?{...F,stage:K}:F)}:S),d)),x=(d,w)=>r(AR2(e.map(K=>K.id===d?{...K,items:K.items.map(S=>({...S,stage:w}))}:K),d)),',
      'auto-archiv')
    # Stufenleiste pro Position: Bedruckt (Index 3) nur wenn Position eine Bedruckung hat
    html=rep1(html,'function uy({stage:e,onSet:r}){return v.default.createElement("div",{style:{display:"flex",gap:4,flexWrap:"wrap",justifyContent:"flex-end"}},nA.map((t,n)=>{let a=n<=e;',
      'function uy({stage:e,onSet:r,druck:dr}){return v.default.createElement("div",{style:{display:"flex",gap:4,flexWrap:"wrap",justifyContent:"flex-end"}},nA.map((t,n)=>{if(n===0)return null;if(n===3&&!dr)return null;let a=n<=e;','uy-druck')
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

def status_modal(html):
    """Status melden: Hinweistext + allgemeiner WhatsApp-Knopf statt Nummern-Knoepfe."""
    html=rep1(html,r'"Geht an den Besteller sowie immer an Roberto und Erol. Pro Empf\xE4nger einen Button antippen."',r'"WhatsApp \xF6ffnen, Chat oder Gruppe w\xE4hlen und senden \u2013 der Text ist vorausgef\xFCllt."','status-hint')
    html=rep1(html,r'Xg(d.besteller).map(K=>v.default.createElement("a",{key:K,href:zg(K,w),target:"_blank",rel:"noopener noreferrer",style:{textDecoration:"none",background:"#25D366",color:"#fff",borderRadius:8,fontWeight:800,padding:"10px 14px",fontSize:13}},"An ",K)),',
        r'v.default.createElement("a",{href:"https://wa.me/?text="+encodeURIComponent(w),target:"_blank",rel:"noopener noreferrer",style:{textDecoration:"none",background:"#25D366",color:"#fff",borderRadius:999,fontWeight:800,padding:"10px 14px",fontSize:13}},"WhatsApp \xF6ffnen"),','status-btn')
    return html

def order_flow(html):
    """Bestellen = Ausloesen: Start bei Bestellt, keine Melde-/Archiv-Knoepfe, Mengen aendern und loeschen in der Verfolgung."""
    html=rep1(html,'stage:0}}),archived:!1}','stage:1}}),archived:!1}','start-stage')
    a=html.index('!d.archived&&v.default.createElement("select",{defaultValue:""')
    b=html.index(r'v.default.createElement(Ve,{kind:"danger",small:!0,onClick:()=>m(d.id)},"L\xF6schen")',a)
    html=html[:a]+html[b:]
    old=r'v.default.createElement("td",{style:{padding:"10px 14px",textAlign:"right"}},d.archived?v.default.createElement("span",{style:{fontSize:12,fontWeight:700,color:tA[F.stage]}},nA[F.stage]):v.default.createElement(uy,{stage:F.stage,druck:F.druck,onSet:y=>h(d.id,k,y)}))'
    new=(r'v.default.createElement("td",{style:{padding:"10px 14px",textAlign:"right",whiteSpace:"nowrap"}},'
         r'v.default.createElement("div",{style:{display:"inline-flex",gap:6,alignItems:"center",marginRight:10}},'
         r'v.default.createElement("button",{title:"Menge verringern",onClick:()=>QTY(d.id,k,F.qty-1),style:{width:26,height:26,borderRadius:8,border:"1.5px solid "+H.line,background:"#fff",cursor:"pointer",fontWeight:900,color:H.navy}},"−"),'
         r'v.default.createElement("span",{style:{minWidth:22,display:"inline-block",fontWeight:800}},F.qty),'
         r'v.default.createElement("button",{title:"Menge erh\xF6hen",onClick:()=>QTY(d.id,k,F.qty+1),style:{width:26,height:26,borderRadius:8,border:"1.5px solid "+H.line,background:"#fff",cursor:"pointer",fontWeight:900,color:H.navy}},"+"),'
         r'v.default.createElement("button",{title:"Position stornieren",onClick:()=>QTY(d.id,k,0),style:{marginLeft:4,padding:"4px 9px",borderRadius:8,border:"1.5px solid #F1C7C1",background:"#fff",cursor:"pointer",fontWeight:800,fontSize:12,color:"#C0392B"}},"Stornieren")),'
         r'v.default.createElement(uy,{stage:F.stage,druck:F.druck,onSet:y=>h(d.id,k,y)}))')
    html=rep1(html,old,new,'qty-cell')
    html=rep1(html,'p=(d,w)=>r(e.map(K=>K.id===d?{...K,archived:w}:K)),m=d=>r(e.filter(w=>w.id!==d)),',
      'p=(d,w)=>r(e.map(K=>K.id===d?{...K,archived:w}:K)),m=d=>{if(!confirm("Ganze Bestellung stornieren? Die Shopkontakte werden per E-Mail informiert."))return;r(e.filter(w=>w.id!==d));MAILINFO("Stornierung gesendet",!0)},',
      'del-confirm')
    html=rep1(html,'let[t,n]=(0,v.useState)(null),[a,i]=(0,v.useState)("offen"),',
      'let QTY=(id,idx,q)=>{let O=e.find(z=>z.id===id);if(!O)return;let it=O.items[idx];'
      'if(q<=0&&!confirm("Position stornieren: "+it.name+"? Die Shopkontakte werden per E-Mail informiert."))return;'
      'let ni=q<=0?O.items.filter((z,j)=>j!==idx):O.items.map((z,j)=>j===idx?{...z,qty:q}:z);'
      'if(!ni.length){if(!confirm("Das war die letzte Position. Ganze Bestellung stornieren?"))return;r(e.filter(z=>z.id!==id));MAILINFO("Stornierung gesendet",!0);return}'
      'r(e.map(z=>z.id===id?{...z,items:ni}:z));MAILINFO(q>it.qty?"Mengenerh\xF6hung gesendet":"Stornierung gesendet",!0)};'
      'let[t,n]=(0,v.useState)(null),[a,i]=(0,v.useState)("offen"),','qty-fn')
    return html

def mail_popup(html):
    """Popup 'E-Mail wurde gesendet'."""
    html=rep1(html,'var Og={width:42,height:42','window.MAILINFO=function(t,tel){window.FCWB_MAILINFO&&window.FCWB_MAILINFO(t,tel)};var Og={width:42,height:42','mailinfo-global')
    html=rep1(html,'n([oe,...t||[]]),i(b||""),h([]),g(!1),w(oe)','n([oe,...t||[]]),i(b||""),h([]),g(!1),w(oe),window.MAILINFO&&window.MAILINFO("Bestellung ausgel\xF6st",!1)','mailinfo-order')
    return html

def cart_icon(html):
    """Warenkorb oben rechts: weisse Pille mit eigenem SVG-Symbol und Zaehler."""
    svg=('v.default.createElement("svg",{viewBox:"0 0 24 24",width:24,height:24,fill:"none",stroke:"currentColor","stroke-width":"2.2","stroke-linecap":"round","stroke-linejoin":"round",style:{display:"block"}},'
         'v.default.createElement("path",{key:"p",d:"M2.5 3h2.2l2.2 11.2a1.8 1.8 0 0 0 1.8 1.4h8.3a1.8 1.8 0 0 0 1.8-1.4L21 7H6"}),'
         'v.default.createElement("circle",{key:"c1",cx:"9.5",cy:"20",r:"1.6",fill:"currentColor",stroke:"none"}),'
         'v.default.createElement("circle",{key:"c2",cx:"17.5",cy:"20",r:"1.6",fill:"currentColor",stroke:"none"}))')
    pill=('v.default.createElement("div",{style:{marginLeft:"auto",display:"flex",alignItems:"center",paddingRight:12}},'
          'v.default.createElement("button",{id:"fcwb-cartbox",title:"Warenkorb öffnen",type:"button",'
          'onClick:()=>{r("bestellen");setTimeout(()=>window.dispatchEvent(new CustomEvent("fcwb-opencart")),60)},'
          'style:{display:"inline-flex",alignItems:"center",gap:9,background:"#fff",border:"none",cursor:"pointer",'
          'borderRadius:999,padding:"7px 14px 7px 13px",color:"#0B2A5B",fontWeight:900,lineHeight:1,'
          'boxShadow:"0 4px 14px -4px rgba(0,0,0,.5)",transition:"background .25s,color .25s,transform .2s"}},'
          +svg+','
          'v.default.createElement("span",{id:"fcwb-cartcount",style:{minWidth:26,textAlign:"center",background:"#EEF3FA",color:"#5B6B7B",'
          'borderRadius:999,padding:"3px 10px",fontSize:16,fontWeight:900,transition:"background .25s,color .25s"}},"0")))')
    html=rep1(html,'v.default.createElement(g,{id:"teams",label:"Teams"})','v.default.createElement(g,{id:"teams",label:"Teams"}),'+pill,'cart-icon')
    html=rep1(html,'Q=f.reduce((b,Y)=>b+Y.qty,0),','Q=f.reduce((b,Y)=>b+Y.qty,0),ZZ=(()=>{let el=typeof document<"u"&&document.getElementById("fcwb-cartcount");if(el)el.textContent=String(Q);return 0})(),ZZ2=(0,v.useEffect)(()=>{let hh=()=>g(!0);window.addEventListener("fcwb-opencart",hh);return()=>window.removeEventListener("fcwb-opencart",hh)},[]),','cart-count')
    return html

def auto_archive(html):
    """Bestellung automatisch ins Archiv, sobald alle Positionen uebergeben sind (mit Popup)."""
    html=rep1(html,'h=(d,w,K)=>r(AR(e.map(S=>S.id===d?{...S,items:S.items.map((F,k)=>k===w?{...F,stage:K}:F)}:S),d)),',
      'h=(d,w,K)=>r(AR2(e.map(S=>S.id===d?{...S,items:S.items.map((F,k)=>k===w?{...F,stage:K}:F)}:S),d)),','auto-arch-h')
    html=rep1(html,'AR=(L,id)=>L.map(S=>S.id!==id||S.archived||!S.items.every(F=>F.stage===5)?S:(confirm("Alle Positionen sind \xFCbergeben. Bestellung jetzt ins Archiv verschieben?")?{...S,archived:!0}:S)),',
      'AR2=(L,id)=>L.map(S=>{if(S.id!==id||S.archived||!S.items.every(F=>F.stage===5))return S;setTimeout(()=>window.FCWB_ARCHIVED&&window.FCWB_ARCHIVED(S.besteller,S.empfaenger),200);return{...S,archived:!0}}),','auto-arch-fn')
    return html

def bulk_status(html):
    """Dropdown in der Kopfzeile: Status fuer die ganze Bestellung setzen."""
    anchor=r'v.default.createElement(Ve,{kind:"danger",small:!0,onClick:()=>m(d.id)},"L\xF6schen")'
    sel=(r'v.default.createElement("select",{value:"",title:"Status f\xFCr die ganze Bestellung",onChange:F=>{if(F.target.value!==""){x(d.id,Number(F.target.value));F.target.value=""}},'
         r'style:{padding:"6px 10px",borderRadius:999,border:"1.5px solid "+H.line,fontSize:12,fontWeight:700,color:H.navy,background:"#fff",cursor:"pointer"}},'
         r'v.default.createElement("option",{value:""},"Status f\xFCr alle …"),'
         r'nA.map((F,k)=>k===0||k===3&&!d.items.some(I=>I.druck)?null:v.default.createElement("option",{key:k,value:k},F))),')
    return rep1(html,anchor,sel+anchor,'bulk-status')

def cart_persist(html):
    """Warenkorb ueberlebt den Reiterwechsel (sessionStorage)."""
    html=rep1(html,'[f,h]=(0,v.useState)([]),[x,p]=(0,v.useState)(null),',
      '[f,h]=(0,v.useState)(()=>{try{return JSON.parse(sessionStorage.getItem("fcwb_cart")||"[]")}catch(z){return[]}}),[x,p]=(0,v.useState)(null),','cart-init')
    html=rep1(html,'ZZ2=(0,v.useEffect)(()=>{let hh=()=>g(!0);window.addEventListener("fcwb-opencart",hh);return()=>window.removeEventListener("fcwb-opencart",hh)},[]),',
      'ZZ2=(0,v.useEffect)(()=>{let hh=()=>g(!0);window.addEventListener("fcwb-opencart",hh);return()=>window.removeEventListener("fcwb-opencart",hh)},[]),ZZ3=(0,v.useEffect)(()=>{try{sessionStorage.setItem("fcwb_cart",JSON.stringify(f))}catch(z){}},[f]),','cart-persist')
    return html
