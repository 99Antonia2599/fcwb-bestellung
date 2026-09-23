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
#fcwb-gate button[disabled]{opacity:.6;cursor:default;transform:none}
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
/* Abmelden: unauffaellige Pille unten rechts, erscheint erst nach der Anmeldung */
#fcwb-logout{position:fixed;right:14px;bottom:14px;z-index:900;padding:9px 16px;border:none;border-radius:999px;
  background:rgba(255,255,255,.95);color:#0B2A5B;font-family:Inter,system-ui,sans-serif;font-weight:800;font-size:13px;
  cursor:pointer;box-shadow:0 6px 18px -6px rgba(0,0,0,.45);opacity:.6;transition:opacity .2s,transform .2s}
#fcwb-logout:hover{opacity:1;transform:translateY(-1px)}
@media print{#fcwb-logout{display:none}}
@media (prefers-reduced-motion:reduce){#fcwb-gate *{animation:none !important}}
</style>
<div id="fcwb-gate" hidden>
  <div class="pitch"></div>
  <div class="shadow"></div>
  <div class="ball"><svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="48" fill="#fff" stroke="#111" stroke-width="3"/><polygon points="50,22 66,34 60,53 40,53 34,34" fill="#111"/><polygon points="50,22 34,34 22,26 32,10 46,8" fill="#fff" stroke="#111" stroke-width="2"/><polygon points="66,34 78,26 90,42 84,58 60,53" fill="#fff" stroke="#111" stroke-width="2"/><polygon points="22,26 34,34 40,53 24,66 12,50 12,40" fill="#fff" stroke="#111" stroke-width="2"/><polygon points="24,66 40,53 60,53 76,66 64,84 36,84" fill="#fff" stroke="#111" stroke-width="2"/><polygon points="12,50 24,66 36,84 22,90 8,72" fill="#111"/><polygon points="90,42 84,58 76,66 64,84 80,90 94,72 96,55" fill="#111"/><polygon points="32,10 46,8 50,22 34,34 22,26" fill="#111" opacity=".0"/><polygon points="36,84 64,84 66,96 50,99 34,96" fill="#111"/><polygon points="46,8 60,4 78,26 66,34 50,22" fill="#111" opacity=".0"/><path d="M46 8 L58 6 L78 26" fill="none" stroke="#111" stroke-width="2"/></svg></div>
  <form class="card" id="fcwb-gate-form">
    <img class="logo" src="__LOGO__" alt="FC Weinfelden-Bürglen">
    <h1>Materialbestellung</h1>
    <p>FC Weinfelden-Bürglen · Bitte Passwort eingeben</p>
    <div class="row"><input id="fcwb-pw" type="password" placeholder="Passwort" autocomplete="current-password" autofocus><button type="submit" id="fcwb-go">Anpfiff ⚽</button></div>
    <div class="err" id="fcwb-err"></div>
  </form>
</div>
<script>
// Anmeldung gegen Supabase Auth. Das Passwort steht NICHT im Code: geprüft wird es von
// der Datenbank. Erst mit gültiger Sitzung geben die Tabellen etwas heraus (RLS, siehe
// supabase_setup.sql) – die Maske hier ist also echter Zugangsschutz, keine Attrappe.
// Alle sechs Personen teilen sich ein Vereinskonto; die Adresse dazu wird beim Bauen
// eingesetzt, das Passwort setzt man im Supabase-Dashboard.
(function(){
  var EMAIL="__LOGIN_EMAIL__";
  var gate=document.getElementById("fcwb-gate"), root=document.getElementById("root");
  var form=document.getElementById("fcwb-gate-form"), errBox=document.getElementById("fcwb-err");
  var input=document.getElementById("fcwb-pw"), btn=document.getElementById("fcwb-go");
  var sb=window.FCWB_SB;

  // Bis feststeht, ob eine Sitzung besteht, bleibt die App verdeckt – sonst blitzt sie kurz auf.
  root.classList.add("locked"); document.body.classList.add("fcwb-locked");

  function showGate(msg){
    gate.hidden=false;
    if(msg) errBox.textContent=msg;
    setTimeout(function(){ input && input.focus(); },300);
  }
  function unlock(){
    root.classList.remove("locked"); document.body.classList.remove("fcwb-locked");
    if(gate.hidden){ gate.remove(); }
    else { gate.classList.add("out"); setTimeout(function(){ gate.remove(); },650); }
    addLogout();
  }
  function fail(msg){
    errBox.textContent=msg;
    gate.classList.remove("shake"); void gate.offsetWidth; gate.classList.add("shake");
    input.select();
  }
  function busy(on){
    btn.disabled=on; btn.textContent=on?"Moment …":"Anpfiff ⚽";
  }
  function addLogout(){
    if(document.getElementById("fcwb-logout")) return;
    var b=document.createElement("button");
    b.id="fcwb-logout"; b.type="button"; b.textContent="Abmelden";
    b.title="Von diesem Gerät abmelden";
    b.addEventListener("click",function(){
      if(confirm("Von diesem Gerät abmelden?")) sb.auth.signOut();
    });
    document.body.appendChild(b);
  }

  // Ohne Supabase-Client (CDN nicht erreichbar oder Build ohne Zugangsdaten) kann weder
  // angemeldet noch synchronisiert werden. Dann lieber ehrlich sperren als scheinbar öffnen.
  if(!sb){ showGate("Keine Verbindung zur Datenbank. Bitte Seite neu laden."); btn.disabled=true; return; }

  // Abmeldung – auch wenn die Sitzung von aussen abläuft – setzt die Seite sauber zurück.
  sb.auth.onAuthStateChange(function(evt){ if(evt==="SIGNED_OUT") location.reload(); });

  sb.auth.getSession().then(function(r){
    if(r && r.data && r.data.session) unlock(); else showGate();
  }).catch(function(){ showGate("Keine Verbindung. Bitte Seite neu laden."); });

  form.addEventListener("submit",function(ev){
    ev.preventDefault();
    var pw=input.value;
    if(!pw){ fail("Bitte Passwort eingeben."); return; }
    busy(true); errBox.textContent="";
    sb.auth.signInWithPassword({email:EMAIL,password:pw}).then(function(r){
      busy(false);
      if(r.error){
        fail(/invalid login/i.test(r.error.message||"") ? "Abseits! Passwort stimmt nicht." : "Anmeldung fehlgeschlagen: "+(r.error.message||"unbekannter Fehler"));
        return;
      }
      unlock();
    }).catch(function(){
      busy(false); fail("Keine Verbindung. Internet prüfen und nochmals versuchen.");
    });
  });
})();
</script>
