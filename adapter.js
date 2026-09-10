<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.min.js"></script>
<script>
// Supabase-Anbindung. Verhält sich für die App wie Firestore (collection/doc/onSnapshot/set),
// speichert aber jede Bestellung und jedes Team als eigene Tabellenzeile.
// So überschreiben sich gleichzeitige Änderungen verschiedener Personen nicht.
window.FCWB_SUPABASE = { url: "__SUPABASE_URL__", anonKey: "__SUPABASE_ANON_KEY__" };
window.FCWB_FIREBASE = {}; // nur damit die App den Live-Modus einschaltet
(function(){
  var cfg = window.FCWB_SUPABASE;
  if (!window.supabase || !cfg.url || cfg.url.indexOf("__") === 0) return;
  var sb = window.supabase.createClient(cfg.url, cfg.anonKey);
  var TABLES = { orders: "orders", teams: "teams" };

  var docs = {};  // ein Objekt pro Tabelle, damit onSnapshot und set denselben Zustand teilen
  function doc(id){ return docs[id] || (docs[id] = makeDoc(id)); }
  function makeDoc(id){
    var table = TABLES[id]; if (!table) return { onSnapshot: function(){}, set: function(){} };
    var known = {};          // id -> JSON-String der zuletzt gesehenen Zeile
    var order = [];          // Reihenfolge (neueste zuerst)
    var listeners = [];
    var timer = null;
    var first = true;        // erstes Laden immer melden

    function emit(){
      var arr = order.map(function(k){ return JSON.parse(known[k]); });
      var row = { json: JSON.stringify(arr) };
      listeners.forEach(function(cb){ cb({ exists: true, data: function(){ return row; } }); });
    }
    function load(){
      return sb.from(table).select("id,data,pos").order("pos", { ascending: false }).then(function(r){
        if (r.error) { console.error(r.error); return; }
        var nk = {}, no = [];
        r.data.forEach(function(x){ nk[x.id] = JSON.stringify(x.data); no.push(x.id); });
        // Nur melden, wenn sich gegenüber dem lokalen Stand wirklich etwas geändert hat
        // (das Echo eigener Schreibvorgänge würde sonst den nächsten Klick in der App verschlucken).
        var same = first === false && no.length === order.length && no.every(function(k){ return known[k] === nk[k]; });
        first = false;
        known = nk; order = no;
        if (!same) emit();
      });
    }
    function scheduleLoad(){ clearTimeout(timer); timer = setTimeout(load, 150); }

    return {
      onSnapshot: function(cb){
        listeners.push(cb);
        load();
        sb.channel("live-" + table)
          .on("postgres_changes", { event: "*", schema: "public", table: table }, scheduleLoad)
          .subscribe();
      },
      set: function(v){
        var arr; try { arr = JSON.parse(v.json) || []; } catch(e){ return; }
        var seen = {}, ups = [], now = Date.now();
        arr.forEach(function(item, i){
          if (!item || !item.id) return;
          seen[item.id] = true;
          var s = JSON.stringify(item);
          if (known[item.id] !== s) {
            var rec = { id: item.id, data: item, updated_at: new Date().toISOString() };
            if (!(item.id in known)) rec.pos = now - i;   // neue Zeilen: Reihenfolge wie in der App
            ups.push(rec);
            known[item.id] = s;
            if (order.indexOf(item.id) < 0) order.unshift(item.id);
          }
        });
        var dels = Object.keys(known).filter(function(k){ return !seen[k]; });
        dels.forEach(function(k){ delete known[k]; order = order.filter(function(o){ return o !== k; }); });
        var ops = [];
        if (ups.length) ops.push(sb.from(table).upsert(ups, { onConflict: "id" }));
        if (dels.length) ops.push(sb.from(table).delete().in("id", dels));
        return Promise.all(ops).then(function(rs){ var ok=true; rs.forEach(function(r){ if (r.error) { ok=false; console.error(r.error); } }); if (ok && ops.length && window.FCWB_SAVED) window.FCWB_SAVED(); });
      }
    };
  }
  var db = { collection: function(){ return { doc: doc }; } };
  window.firebase = { apps: [db], initializeApp: function(){ return db; }, firestore: function(){ return db; } };
})();
</script>
