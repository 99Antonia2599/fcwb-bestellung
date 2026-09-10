function fy({teams:e,catalog:r,onAdd:t}){
const E=v.default.createElement;
let[n,a]=(0,v.useState)(e[0]?e[0].id:""),[i,A]=(0,v.useState)("Herren"),[s,o]=(0,v.useState)([]),[l,c]=(0,v.useState)({}),[cat,setCat]=(0,v.useState)("match"),[q,setQ]=(0,v.useState)(""),[open,setOpen]=(0,v.useState)(!1);
let u=e.find(F=>F.id===n),players=(u&&u.players)||[];
let f=r.filter(F=>Hu(F,i)&&F.line!=="Beispiel"&&(q?(F.name+" "+F.color+" "+F.art).toLowerCase().includes(q.toLowerCase()):F.cat===cat));
let h=s.map(F=>r.find(k=>k.id===F)).filter(Boolean);
let x=(F,k)=>F+"|"+k,K=F=>F.replace("Nike ","");
let addArt=F=>{o(k=>k.indexOf(F)>=0?k:[...k,F]);setOpen(!1)};
let remArt=F=>{o(k=>k.filter(y=>y!==F));c(y=>{let D={...y};Object.keys(D).forEach(z=>{z.endsWith("|"+F)&&delete D[z]});return D})};
let tog=(P,F)=>c(y=>{let D={...y};D[x(P,F)]=!D[x(P,F)];return D});
let setAll=(F,on)=>c(y=>{let D={...y};players.forEach(P=>{D[x(P.id,F)]=on});return D});
let cnt=Object.keys(l).filter(F=>l[F]).length;
let go=()=>{if(!u)return;let F=[];players.forEach(P=>{h.forEach(y=>{l[x(P.id,y.id)]&&F.push({id:y.id,size:ly(y,P),qty:1,player:P.name||(P.number?"Nr. "+P.number:"Spieler"),druck:cy(P)})})});if(!F.length){alert("Bitte mindestens einen Spieler ankreuzen.");return}t(F);c({});o([]);alert(F.length+" Positionen in den Warenkorb gelegt. Unten \xFCber den Warenkorb abschliessen.")};
let pill=(on,extra)=>({border:"1.5px solid "+(on?H.navy:H.line),background:on?H.navy:"#fff",color:on?"#fff":H.ink,borderRadius:999,padding:"6px 12px",fontSize:12,fontWeight:700,cursor:"pointer",...extra});
let card={background:"#fff",border:"1px solid "+H.line,borderRadius:14,padding:14,marginBottom:12};
let step=(nr,txt)=>E("div",{style:{display:"flex",alignItems:"center",gap:10,margin:"18px 0 8px"}},E("span",{style:{width:26,height:26,borderRadius:"50%",background:H.navy,color:"#fff",display:"grid",placeItems:"center",fontWeight:900,fontSize:13}},nr),E("span",{style:{fontWeight:800,color:H.navy,fontSize:15}},txt));
return E("div",{style:{paddingBottom:90}},
 step(1,"Team und Linie"),
 E("div",{style:{...card,display:"flex",gap:12,flexWrap:"wrap",alignItems:"center"}},
  E("select",{value:n,onChange:F=>a(F.target.value),style:{padding:"8px 12px",borderRadius:999,border:"1.5px solid "+H.line,fontWeight:700,fontSize:13}},e.map(F=>E("option",{key:F.id,value:F.id},F.name+" ("+(F.players||[]).length+" Spieler)"))),
  E("div",{style:{display:"flex",gap:6}},["Herren","Damen","Kids"].map(F=>E("button",{key:F,onClick:()=>A(F),style:pill(i===F)},F))),
  players.length?null:E("span",{style:{color:"#C0392B",fontSize:12,fontWeight:700}},"Dieses Team hat keine Spieler. Im Reiter \xABTeams\xBB anlegen oder Excel importieren.")),
 step(2,"Artikel hinzuf\xFCgen"),
 E("div",{style:card},
  E("div",{style:{display:"flex",gap:8,flexWrap:"wrap",alignItems:"center",marginBottom:10}},
   z0.map(b=>E("button",{key:b,onClick:()=>{setCat(b);setQ("")},style:pill(cat===b&&!q,{borderColor:cat===b&&!q?Fa[b].color:H.line,background:cat===b&&!q?Fa[b].color:"#fff"})},Fa[b].label)),
   E("input",{value:q,onChange:b=>setQ(b.target.value),placeholder:"Suchen: Name, Farbe, Art.-Nr.",style:{marginLeft:"auto",padding:"7px 12px",borderRadius:999,border:"1.5px solid "+H.line,fontSize:13,minWidth:220}})),
  E("div",{style:{display:"grid",gridTemplateColumns:"repeat(auto-fill, minmax(150px, 1fr))",gap:8}},f.map(F=>{let on=s.indexOf(F.id)>=0;return E("button",{key:F.id,onClick:()=>on?remArt(F.id):addArt(F.id),title:F.name,style:{textAlign:"left",display:"flex",gap:8,alignItems:"center",border:"1.5px solid "+(on?H.blue:H.line),background:on?"#EAF3FB":"#fff",borderRadius:12,padding:6,cursor:"pointer",color:H.ink}},
   F.img?E("img",{src:F.img,alt:"",style:{width:44,height:44,objectFit:"contain",borderRadius:8,flex:"none"}}):null,
   E("span",{style:{minWidth:0}},E("span",{style:{display:"block",fontSize:12,fontWeight:800,lineHeight:1.2}},(on?"✓ ":"")+K(F.name)),E("span",{style:{display:"block",fontSize:10,color:H.muted,fontWeight:600}},F.color+" \xB7 "+F.art)))}))),
 h.length?step(3,"Wer bekommt was? Spieler antippen"):null,
 h.map(F=>{let sel=players.filter(P=>l[x(P.id,F.id)]).length;return E("div",{key:F.id,style:{...card,borderLeft:"5px solid "+(Fa[F.cat]?Fa[F.cat].color:H.blue)}},
  E("div",{style:{display:"flex",gap:12,alignItems:"center",flexWrap:"wrap",marginBottom:10}},
   F.img?E("img",{src:F.img,alt:"",style:{width:56,height:56,objectFit:"contain",borderRadius:10}}):null,
   E("div",{style:{flex:1,minWidth:160}},E("div",{style:{fontWeight:800,fontSize:14}},F.name),E("div",{style:{fontSize:12,color:H.muted}},F.color+" \xB7 Art.-Nr. "+F.art+" \xB7 Gr\xF6sse aus "+((F.type==="shorts"||F.type==="pants")?"Unterteil":"Oberteil"))),
   E("span",{style:{fontWeight:800,color:H.navy,fontSize:13}},sel+" / "+players.length),
   E("button",{onClick:()=>setAll(F.id,!0),style:pill(!1)},"Alle"),
   E("button",{onClick:()=>setAll(F.id,!1),style:pill(!1)},"Keine"),
   E("button",{onClick:()=>remArt(F.id),title:"Artikel entfernen",style:pill(!1,{color:"#C0392B",borderColor:"#F1C7C1"})},"✕")),
  E("div",{style:{display:"flex",gap:8,flexWrap:"wrap"}},players.map(P=>{let on=!!l[x(P.id,F.id)],sz=ly(F,P),dr=cy(P);return E("button",{key:P.id,onClick:()=>tog(P.id,F.id),style:{...pill(on,{padding:"7px 12px",display:"flex",gap:8,alignItems:"center"})}},
   E("span",{style:{display:"inline-grid",placeItems:"center",width:22,height:22,borderRadius:"50%",background:on?"#FFC300":H.fill,color:H.navy,fontSize:11,fontWeight:900}},P.number||"–"),
   E("span",null,P.name||"Spieler"),
   E("span",{style:{opacity:.75,fontWeight:600}},"Gr. "+(sz||"?")+(dr?" \xB7 "+dr:"")))})))}),
 h.length?E("div",{style:{position:"sticky",bottom:12,zIndex:5,marginRight:230,display:"flex",gap:12,alignItems:"center",justifyContent:"space-between",background:H.navy,color:"#fff",borderRadius:16,padding:"12px 16px",boxShadow:"0 14px 30px -12px rgba(11,42,91,.7)"}},
  E("div",null,E("b",{style:{fontSize:16}},cnt)," Positionen \xB7 ",h.length," Artikel"),
  E(Ve,{kind:"gold",onClick:go,disabled:!cnt},"In den Warenkorb")):null
)}
