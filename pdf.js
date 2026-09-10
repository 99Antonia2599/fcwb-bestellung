<script>
// Bestellschein als Druckansicht (im Browser: Drucken -> "Als PDF speichern")
window.FCWB_PDF=function(o,stages){
  var esc=function(s){return String(s==null?"":s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})};
  var d=String(o.date||"").split("-"); var datum=d.length===3?d[2]+"."+d[1]+"."+d[0]:o.date;
  var rows=o.items.map(function(it,i){return "<tr><td>"+(i+1)+"</td><td><b>"+esc(it.art)+"</b></td><td>"+esc(it.name)+"</td><td>"+esc(it.color)+"</td><td>"+esc(it.line)+"</td><td>"+esc(it.size)+"</td><td class='r'>"+esc(it.qty)+"</td><td>"+esc(it.druck)+"</td><td>"+esc(it.player)+"</td><td>"+esc(stages[it.stage]||"")+"</td></tr>"}).join("");
  var total=o.items.reduce(function(a,b){return a+(+b.qty||0)},0);
  var html='<!doctype html><html lang="de"><head><meta charset="utf-8"><title>FCWB Bestellschein '+esc(datum)+' '+esc(o.besteller)+'</title>'
   +'<style>body{font-family:Segoe UI,Arial,sans-serif;color:#0F1E33;margin:28px}h1{font-size:22px;margin:0;color:#0B2A5B}.sub{color:#5B6B7B;font-size:13px;margin:4px 0 18px}'
   +'.meta{display:grid;grid-template-columns:auto 1fr;gap:4px 16px;font-size:13px;margin-bottom:18px}.meta b{color:#0B2A5B}'
   +'table{width:100%;border-collapse:collapse;font-size:12px}th{background:#0B2A5B;color:#fff;text-align:left;padding:7px 8px}td{padding:6px 8px;border-bottom:1px solid #DCE6F1;vertical-align:top}.r{text-align:right}tfoot td{font-weight:700;border-top:2px solid #0B2A5B}'
   +'.foot{margin-top:24px;font-size:11px;color:#5B6B7B}@media print{@page{size:A4 landscape;margin:14mm}}</style></head><body>'
   +'<h1>FC Weinfelden-B&uuml;rglen &middot; Materialbestellung</h1><div class="sub">Bestellschein f&uuml;r den 11teamsports Clubshop</div>'
   +'<div class="meta"><b>Bestelldatum</b><span>'+esc(datum)+'</span><b>Besteller</b><span>'+esc(o.besteller)+'</span><b>Lieferung an</b><span>'+esc(o.empfaenger)+'</span><b>Notiz</b><span>'+esc(o.note)+'</span><b>Bestell-ID</b><span>'+esc(o.id)+'</span></div>'
   +'<table><thead><tr><th>#</th><th>Art.-Nr.</th><th>Artikel</th><th>Farbe</th><th>Linie</th><th>Gr&ouml;sse</th><th class="r">Menge</th><th>Bedruckung</th><th>Spieler</th><th>Status</th></tr></thead><tbody>'+rows+'</tbody>'
   +'<tfoot><tr><td colspan="6">Total</td><td class="r">'+total+'</td><td colspan="3"></td></tr></tfoot></table>'
   +'<div class="foot">Erstellt am '+new Date().toLocaleDateString("de-CH")+' &middot; FCWB Materialbestellung</div>'
   +'<scr'+'ipt>window.onload=function(){window.print()}</scr'+'ipt></body></html>';
  var w=window.open("","_blank"); if(!w){alert("Popup blockiert. Bitte Popups für diese Seite erlauben.");return}
  w.document.open(); w.document.write(html); w.document.close();
};
</script>
