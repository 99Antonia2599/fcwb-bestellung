<style>
#fcwb-gate{position:fixed;inset:0;z-index:1000;display:grid;place-items:center;overflow:hidden;
  background:radial-gradient(900px 500px at 20% 0%,rgba(255,195,0,.25),transparent 60%),linear-gradient(160deg,#0B2A5B 0%,#0055C8 60%,#1D6FE0 100%);
  font-family:Inter,system-ui,sans-serif;color:#fff}
#fcwb-gate .pitch{position:absolute;inset:0;background:url("__PITCH__") center/1100px 550px no-repeat;opacity:.9;pointer-events:none}
#fcwb-gate .card{position:relative;width:min(380px,92vw);background:rgba(255,255,255,.1);backdrop-filter:blur(14px);border:1px solid rgba(255,255,255,.22);
  border-radius:24px;padding:34px 28px 28px;text-align:center;box-shadow:0 30px 80px -20px rgba(0,0,0,.6);animation:gateIn .7s cubic-bezier(.2,.9,.3,1.2) both}
@keyframes gateIn{from{opacity:0;transform:translateY(30px) scale(.94)}to{opacity:1;transform:none}}
#fcwb-gate .logo{width:120px;height:auto;filter:drop-shadow(0 12px 22px rgba(0,0,0,.5));animation:logoFloat 4s ease-in-out infinite}
@keyframes logoFloat{0%,100%{transform:translateY(0) rotate(-1.5deg)}50%{transform:translateY(-8px) rotate(1.5deg)}}
#fcwb-gate h1{font-family:"Barlow Condensed",Inter,sans-serif;font-size:34px;letter-spacing:.6px;text-transform:uppercase;margin:14px 0 2px;line-height:1}
#fcwb-gate p{margin:0 0 20px;font-size:13px;color:rgba(255,255,255,.75)}
#fcwb-gate form.card{display:block}
#fcwb-gate .row{display:flex;gap:8px;flex-wrap:wrap}
#fcwb-gate .row input{min-width:0;flex:1 1 160px}
#fcwb-gate .row button{flex:1 1 auto}
@media (max-width:480px){#fcwb-gate .card{padding:26px 18px 22px}#fcwb-gate .logo{width:96px}#fcwb-gate h1{font-size:28px}#fcwb-gate .row button{flex-basis:100%}}
#fcwb-gate input{flex:1;padding:13px 16px;border-radius:999px;border:2px solid rgba(255,255,255,.35);background:rgba(255,255,255,.95);font-size:15px;color:#0B2A5B;outline:none;font-weight:600}
#fcwb-gate input:focus{border-color:#FFC300;box-shadow:0 0 0 4px rgba(255,195,0,.3)}
#fcwb-gate button{white-space:nowrap;padding:13px 18px;border:none;border-radius:999px;background:linear-gradient(135deg,#FFD84D,#FFC300);color:#0B2A5B;font-weight:800;font-size:15px;cursor:pointer;box-shadow:0 10px 20px -8px rgba(255,195,0,.8);transition:transform .12s}
#fcwb-gate button:hover{transform:translateY(-2px) scale(1.03)}
#fcwb-gate .err{min-height:18px;font-size:13px;color:#FFD84D;margin-top:12px;font-weight:700}
#fcwb-gate.shake .card{animation:shake .45s}
@keyframes shake{0%,100%{transform:translateX(0)}20%{transform:translateX(-12px)}40%{transform:translateX(10px)}60%{transform:translateX(-7px)}80%{transform:translateX(5px)}}
/* Hüpfender Ball */
#fcwb-gate .ball{position:absolute;left:8%;bottom:0;width:70px;height:70px;animation:ballX 16s ease-in-out infinite}
#fcwb-gate .ball svg{width:70px;height:70px;display:block;animation:ballY 1.7s cubic-bezier(.45,0,.55,1) infinite alternate,ballSpin 2.4s linear infinite;filter:drop-shadow(0 18px 14px rgba(0,0,0,.45))}
@keyframes ballY{from{transform:translateY(-10vh)}to{transform:translateY(-60vh)}}
@keyframes ballSpin{to{rotate:360deg}}
@keyframes ballX{0%{left:6%}50%{left:calc(94% - 70px)}100%{left:6%}}
#fcwb-gate .shadow{position:absolute;left:8%;bottom:4vh;width:70px;height:14px;border-radius:50%;background:rgba(0,0,0,.35);filter:blur(4px);animation:ballX 16s ease-in-out infinite,shadowY 1.7s cubic-bezier(.45,0,.55,1) infinite alternate}
@keyframes shadowY{from{transform:scale(1);opacity:.5}to{transform:scale(.55);opacity:.15}}
#fcwb-gate.out{animation:gateOut .6s ease forwards}
@keyframes gateOut{to{opacity:0;transform:scale(1.08);visibility:hidden}}
#fcwb-gate[hidden]{display:none}
#root.locked{visibility:hidden}
body.fcwb-locked{overflow:hidden}
@media (prefers-reduced-motion:reduce){#fcwb-gate *{animation:none !important}}
</style>
<div id="fcwb-gate" hidden>
  <div class="pitch"></div>
  <div class="shadow"></div>
  <div class="ball"><svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="48" fill="#fff" stroke="#111" stroke-width="3"/><polygon points="50,22 66,34 60,53 40,53 34,34" fill="#111"/><polygon points="50,22 34,34 22,26 32,10 46,8" fill="#fff" stroke="#111" stroke-width="2"/><polygon points="66,34 78,26 90,42 84,58 60,53" fill="#fff" stroke="#111" stroke-width="2"/><polygon points="22,26 34,34 40,53 24,66 12,50 12,40" fill="#fff" stroke="#111" stroke-width="2"/><polygon points="24,66 40,53 60,53 76,66 64,84 36,84" fill="#fff" stroke="#111" stroke-width="2"/><polygon points="12,50 24,66 36,84 22,90 8,72" fill="#111"/><polygon points="90,42 84,58 76,66 64,84 80,90 94,72 96,55" fill="#111"/><polygon points="32,10 46,8 50,22 34,34 22,26" fill="#111" opacity=".0"/><polygon points="36,84 64,84 66,96 50,99 34,96" fill="#111"/><polygon points="46,8 60,4 78,26 66,34 50,22" fill="#111" opacity=".0"/><path d="M46 8 L58 6 L78 26" fill="none" stroke="#111" stroke-width="2"/></svg></div>
  <form class="card" id="fcwb-gate-form" autocomplete="off">
    <img class="logo" src="__LOGO__" alt="FC Weinfelden-Bürglen">
    <h1>Materialbestellung</h1>
    <p>FC Weinfelden-Bürglen · Bitte Passwort eingeben</p>
    <div class="row"><input id="fcwb-pw" type="password" placeholder="Passwort" autofocus><button type="submit">Anpfiff ⚽</button></div>
    <div class="err" id="fcwb-err"></div>
  </form>
</div>
<script>
(function(){
  var HASH="__PWHASH__", KEY="fcwb_gate_ok";
  var gate=document.getElementById("fcwb-gate"), root=document.getElementById("root");
  try{ if(localStorage.getItem(KEY)===HASH.slice(0,16)) return; }catch(e){}
  root.classList.add("locked"); document.body.classList.add("fcwb-locked"); gate.hidden=false;
  setTimeout(function(){ var i=document.getElementById("fcwb-pw"); i&&i.focus(); },300);
  async function sha(s){ var b=new TextEncoder().encode(s); var h=await crypto.subtle.digest("SHA-256",b); return Array.from(new Uint8Array(h)).map(function(x){return x.toString(16).padStart(2,"0")}).join(""); }
  document.getElementById("fcwb-gate-form").addEventListener("submit",async function(ev){
    ev.preventDefault();
    var pw=document.getElementById("fcwb-pw").value.trim(); var ok=false;
    try{ ok=(await sha(pw))===HASH; }catch(e){ ok=false; }
    if(ok){ try{localStorage.setItem(KEY,HASH.slice(0,16));}catch(e){} gate.classList.add("out"); root.classList.remove("locked"); document.body.classList.remove("fcwb-locked"); setTimeout(function(){gate.remove()},650); }
    else { document.getElementById("fcwb-err").textContent="Abseits! Passwort stimmt nicht."; gate.classList.remove("shake"); void gate.offsetWidth; gate.classList.add("shake"); document.getElementById("fcwb-pw").select(); }
  });
})();
</script>
