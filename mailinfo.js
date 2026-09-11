<style>
#fcwb-mailinfo{position:fixed;inset:0;z-index:950;display:none;place-items:center;background:rgba(3,20,40,.45);padding:16px}
#fcwb-mailinfo.show{display:grid;animation:miFade .25s ease}
@keyframes miFade{from{opacity:0}to{opacity:1}}
#fcwb-mailinfo .box{background:#fff;border-radius:20px;max-width:420px;width:100%;padding:26px 24px;text-align:center;box-shadow:0 30px 70px -20px rgba(11,42,91,.6);animation:miIn .35s cubic-bezier(.2,.9,.3,1.2)}
@keyframes miIn{from{transform:scale(.85);opacity:0}to{transform:none;opacity:1}}
#fcwb-mailinfo .ico{width:56px;height:56px;border-radius:50%;background:#1E8E3E;color:#fff;display:grid;place-items:center;font-size:28px;margin:0 auto 10px}
#fcwb-mailinfo h3{font-family:"Barlow Condensed",Inter,sans-serif;text-transform:uppercase;font-size:24px;margin:0 0 4px;color:#0B2A5B}
#fcwb-mailinfo p{margin:0 0 14px;font:400 14px Inter,system-ui,sans-serif;color:#5B6B7B}
#fcwb-mailinfo .tel{background:#FFF6D6;border:1px solid #FFC300;border-radius:12px;padding:12px;font:700 14px Inter,system-ui,sans-serif;color:#0F1E33;margin-bottom:14px}
#fcwb-mailinfo .tel a{color:#0055C8;font-size:18px;display:block;margin-top:4px}
#fcwb-mailinfo button{border:none;border-radius:999px;background:#0B2A5B;color:#fff;font:800 15px Inter,system-ui,sans-serif;padding:12px 26px;cursor:pointer}
</style>
<div id="fcwb-mailinfo"><div class="box">
  <div class="ico">✉</div>
  <h3 id="fcwb-mailinfo-title">E-Mail wurde gesendet</h3>
  <p id="fcwb-mailinfo-text">Die Shopkontakte wurden automatisch informiert.</p>
  <div class="tel">Bitte zusätzlich telefonisch bei 11teamsports melden<a href="tel:+41443620555">044 362 05 55</a></div>
  <button type="button" id="fcwb-mailinfo-ok">Verstanden</button>
</div></div>
<script>
(function(){
  var el=document.getElementById("fcwb-mailinfo");
  document.getElementById("fcwb-mailinfo-ok").onclick=function(){el.classList.remove("show")};
  el.onclick=function(e){if(e.target===el)el.classList.remove("show")};
  window.FCWB_ARCHIVED=function(bes,emp){
    document.getElementById("fcwb-mailinfo-title").textContent="Bestellung abgeschlossen";
    document.getElementById("fcwb-mailinfo-text").textContent="Alle Positionen sind übergeben. Die Bestellung von "+(bes||"")+(emp?" an "+emp:"")+" wurde ins Archiv verschoben.";
    el.querySelector(".tel").style.display="none";
    el.querySelector(".ico").textContent="🏆";
    el.classList.add("show");
  };
  window.FCWB_MAILINFO=function(t,withTel){
    el.querySelector(".tel").style.display=withTel?"":"none";
    el.querySelector(".ico").textContent="✉";
    document.getElementById("fcwb-mailinfo-title").textContent=t||"E-Mail wurde gesendet";
    document.getElementById("fcwb-mailinfo-text").textContent="Die Shopkontakte wurden automatisch per E-Mail informiert.";
    el.classList.add("show");
  };
})();
</script>
