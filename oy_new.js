function oy({order:e,onNew:r}){
const E=v.default.createElement;
let t=XP(e),n="https://wa.me/?text="+encodeURIComponent(t);
let copy=async()=>{try{await navigator.clipboard.writeText(t),alert("Bestelltext kopiert.")}catch{alert("Kopieren nicht m\xF6glich.")}};
let goTab=id=>window.dispatchEvent(new CustomEvent("fcwb-tab",{detail:id}));
let total=e.items.reduce((a,b)=>a+(+b.qty||0),0);
let card={background:"#fff",border:"1px solid "+H.line,borderRadius:16,padding:18,marginBottom:14};
let sec=(title,sub)=>E("div",{style:{marginBottom:10}},E("div",{style:{fontWeight:800,color:H.navy,fontSize:14}},title),sub?E("div",{style:{fontSize:12,color:H.muted}},sub):null);
return E("div",{style:{maxWidth:640,margin:"0 auto",paddingBottom:30}},
 E("div",{style:{textAlign:"center",padding:"26px 10px 18px"}},
  E("div",{style:{width:64,height:64,borderRadius:"50%",background:"#1E8E3E",color:"#fff",display:"grid",placeItems:"center",fontSize:34,margin:"0 auto 10px",boxShadow:"0 14px 30px -12px rgba(30,142,62,.8)"}},"✓"),
  E("h2",{style:{margin:"0 0 4px",color:H.navy}},"Bestellung erfasst"),
  E("div",{style:{color:H.muted,fontSize:13}},"Sie ist f\xFCr alle sichtbar unter \xABVerfolgung\xBB mit Status ",E("b",null,"Auszul\xF6sen"),".")),
 E("div",{style:card},
  E("div",{style:{display:"grid",gridTemplateColumns:"repeat(auto-fit, minmax(140px, 1fr))",gap:10,marginBottom:14}},
   [["Besteller",e.besteller],["Bestelldatum",Ds(e.date)],["Lieferung an",e.empfaenger||"—"],["Positionen",total+" St\xFCck"]].map(([k,val])=>E("div",{key:k,style:{background:H.fill,borderRadius:10,padding:"8px 12px"}},E("div",{style:{fontSize:11,color:H.muted,fontWeight:700,textTransform:"uppercase",letterSpacing:.4}},k),E("div",{style:{fontWeight:800,color:H.navy}},val)))),
  e.items.map((it,i)=>E("div",{key:i,style:{display:"flex",gap:10,alignItems:"center",padding:"8px 0",borderTop:"1px solid "+H.line}},
   E("span",{style:{minWidth:34,height:34,borderRadius:10,background:H.navy,color:"#fff",display:"grid",placeItems:"center",fontWeight:900}},it.qty+"\xD7"),
   E("div",{style:{flex:1,minWidth:0}},E("div",{style:{fontWeight:800,fontSize:13}},it.name),E("div",{style:{fontSize:12,color:H.muted}},"Art.-Nr. "+it.art+" \xB7 "+it.line+(it.color?" \xB7 "+it.color:"")+" \xB7 Gr. "+it.size+(it.player?" \xB7 "+it.player:"")+(it.druck?" \xB7 Druck: "+it.druck:""))))),
  e.note?E("div",{style:{marginTop:10,fontSize:12,color:H.muted}},"Notiz: "+e.note):null),
 E("div",{style:card},sec("Weitermelden per WhatsApp","WhatsApp \xF6ffnen, Chat oder Gruppe w\xE4hlen und senden – der Bestelltext ist vorausgef\xFCllt."),
  E("div",{style:{display:"flex",gap:8,flexWrap:"wrap"}},
   E("a",{href:n,target:"_blank",rel:"noopener noreferrer",style:{textDecoration:"none",background:"#25D366",color:"#fff",borderRadius:999,fontWeight:800,padding:"11px 16px",fontSize:14}},"WhatsApp \xF6ffnen"),
   E(Ve,{kind:"ghost",small:!0,onClick:copy},"Text kopieren"))),
 E("div",{style:{display:"flex",gap:10,justifyContent:"center",flexWrap:"wrap",marginTop:6}},
  E(Ve,{kind:"primary",onClick:r},"← Zur\xFCck zum Katalog"),
  E(Ve,{kind:"gold",onClick:()=>{r();goTab("verfolgung")}},"Zur Verfolgung →"))
)}
