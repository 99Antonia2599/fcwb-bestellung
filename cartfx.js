<style>
#fcwb-cartfx{position:fixed;left:50%;top:86px;transform:translateX(-50%) translateY(-20px);z-index:940;opacity:0;pointer-events:none;
  background:#1E8E3E;color:#fff;border-radius:999px;padding:12px 22px;font:800 15px Inter,system-ui,sans-serif;box-shadow:0 16px 34px -12px rgba(0,0,0,.6);display:flex;align-items:center;gap:10px}
#fcwb-cartfx.show{animation:cfx 1.8s cubic-bezier(.2,.9,.3,1.2) forwards}
@keyframes cfx{0%{opacity:0;transform:translateX(-50%) translateY(-24px) scale(.8)}15%{opacity:1;transform:translateX(-50%) translateY(0) scale(1.05)}25%{transform:translateX(-50%) translateY(0) scale(1)}80%{opacity:1}100%{opacity:0;transform:translateX(-50%) translateY(-12px)}}
.fcwb-cart-pulse{animation:cartPulse .8s cubic-bezier(.2,.9,.3,1.2) 2}
@keyframes cartPulse{0%,100%{transform:scale(1)}35%{transform:scale(1.22) rotate(-6deg)}70%{transform:scale(1.05) rotate(3deg)}}
</style>
<div id="fcwb-cartfx"><span style="font-size:20px">🛒</span><span id="fcwb-cartfx-text">In den Warenkorb gelegt</span></div>
<script>
(function(){
  var box=document.getElementById("fcwb-cartfx"), txt=document.getElementById("fcwb-cartfx-text"), last=0;
  window.FCWB_CARTFX=function(n){
    txt.textContent=(n&&n>1?n+" Positionen":"1 Artikel")+" in den Warenkorb gelegt";
    box.classList.remove("show"); void box.offsetWidth; box.classList.add("show");
    var cart=document.querySelector('#root span[title="Warenkorb"]');
    if(cart){cart.classList.remove("fcwb-cart-pulse"); void cart.offsetWidth; cart.classList.add("fcwb-cart-pulse");}
  };
  // Zaehler beobachten: steigt er, Effekt ausloesen
  setInterval(function(){
    var el=document.getElementById("fcwb-cartcount"); if(!el) return;
    var n=parseInt(el.textContent||"0",10)||0;
    if(n>last) window.FCWB_CARTFX(n-last);
    last=n;
  },250);
})();
</script>
