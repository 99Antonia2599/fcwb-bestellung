<style>
#fcwb-saved{position:fixed;left:50%;top:50%;z-index:900;display:flex;flex-direction:column;align-items:center;gap:8px;background:linear-gradient(160deg,#0B2A5B,#0055C8);color:#fff;
  padding:26px 38px 22px;border-radius:24px;font:700 18px Inter,system-ui,sans-serif;box-shadow:0 30px 70px -20px rgba(11,42,91,.9);border:1px solid rgba(255,255,255,.2);
  pointer-events:none;opacity:0;transform:translate(-50%,-50%) scale(.6);}
#fcwb-saved.show{animation:savedIn 2.2s cubic-bezier(.2,.8,.2,1) forwards}
#fcwb-saved svg{width:72px;height:72px;display:block}
#fcwb-saved.show svg{animation:savedRoll 1s cubic-bezier(.2,.8,.2,1) 1,savedBounce .5s ease-out .95s 2}
@keyframes savedIn{0%{opacity:0;transform:translate(-50%,-50%) scale(.6)}15%{opacity:1;transform:translate(-50%,-50%) scale(1.04)}22%{transform:translate(-50%,-50%) scale(1)}78%{opacity:1;transform:translate(-50%,-50%) scale(1)}100%{opacity:0;transform:translate(-50%,-50%) scale(.9)}}
@keyframes savedRoll{from{transform:rotate(-720deg) translateY(-60px)}to{transform:none}}
@keyframes savedBounce{0%,100%{transform:translateY(0)}50%{transform:translateY(-14px)}}
#fcwb-saved b{color:#FFC300;font-family:'Barlow Condensed',Inter,sans-serif;font-size:34px;letter-spacing:1px;text-transform:uppercase;line-height:1}
#fcwb-saved small{font-size:14px;font-weight:600;opacity:.85}
@media (prefers-reduced-motion:reduce){#fcwb-saved.show{animation:savedIn 1.5s linear forwards}#fcwb-saved svg{animation:none !important}}
</style>
<div id="fcwb-saved" aria-live="polite"><svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="47" fill="#fff" stroke="#111" stroke-width="4"/><polygon points="50,24 65,35 59,53 41,53 35,35" fill="#111"/><polygon points="13,52 24,66 36,84 21,88 8,70" fill="#111"/><polygon points="88,44 84,58 76,66 64,84 80,90 93,72" fill="#111"/><polygon points="36,84 64,84 66,95 50,98 34,95" fill="#111"/><path d="M50 24 L47 9 M65 35 L80 27 M35 35 L20 27 M59 53 L76 66 M41 53 L24 66" stroke="#111" stroke-width="3" fill="none"/></svg><b>Tor!</b><small>Gespeichert</small></div>
<script>
(function(){
  var el=document.getElementById("fcwb-saved"), t=null;
  window.FCWB_SAVED=function(){
    clearTimeout(t);
    t=setTimeout(function(){ el.classList.remove("show"); void el.offsetWidth; el.classList.add("show"); },250); // sammelt schnelle Folge-Schreibungen
  };
})();
</script>
