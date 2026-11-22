"""
Parche sobre el index.html de Elecciones (archivo único ya compilado):
  1) Las plantillas guardan también los votos de cada mesa.
  2) Autoguardado en el navegador del estado de la app (convocatoria, mesas, candidaturas y votos).
Uso: python3 votos_patch.py <index_entrada.html> <index_salida.html>
"""
import sys

src, out = sys.argv[1:3]
h = open(src, encoding="utf-8").read()

def rep(old, new, label, count=1):
    global h
    n = h.count(old)
    assert n == count, f"{label}: se esperaba {count} y hay {n}"
    h = h.replace(old, new)

# ---- 1) las plantillas incluyen los votos -------------------------------------------------
rep("""      const mesas = snap.mesas.map((m5) => ({ id: m5.id, number: m5.number, name: m5.name, location: m5.location, census: m5.census, blankVotes: 0, nullVotes: 0, votesByCandidacy: {} }));
      W4.plantillas.push({ id: "tpl-" + Date.now(), name, sub: mesas.length + " mesas · " + (cfg.seats || "—") + " puestos · " + snap.candidacies.length + " candidaturas", config: cfg,""",
    """      const mesas = snap.mesas.map((m5) => ({ id: m5.id, number: m5.number, name: m5.name, location: m5.location, census: m5.census, blankVotes: m5.blankVotes || 0, nullVotes: m5.nullVotes || 0, votesByCandidacy: { ...(m5.votesByCandidacy || {}) } }));
      const __tv = mesas.reduce((a5, m5) => a5 + (+m5.blankVotes || 0) + (+m5.nullVotes || 0) + Object.values(m5.votesByCandidacy || {}).reduce((x5, y5) => x5 + (+y5 || 0), 0), 0);
      W4.plantillas.push({ id: "tpl-" + Date.now(), name, sub: mesas.length + " mesas · " + (cfg.seats || "—") + " puestos · " + snap.candidacies.length + " candidaturas" + (__tv ? " · " + __tv.toLocaleString("es-ES") + " votos" : ""), config: cfg,""",
    "guardar plantilla con votos")
rep('children: "＋  Guardar configuración actual como plantilla" }, "save"));',
    'children: "＋  Guardar configuración y votos actuales como plantilla" }, "save"));', "texto del botón")
rep("pulsa «Guardar configuración actual como plantilla».", "pulsa «Guardar configuración y votos actuales como plantilla».", "mensaje de menú vacío")

# ---- 2) autoguardado en el navegador ------------------------------------------------------
rep("(0, a4.useState)({ title: `Elecciones a Junta de Personal · Departamento de Salud de Orihuela`,",
    "(0, a4.useState)(() => window.__VT.get('config') || { title: `Elecciones a Junta de Personal · Departamento de Salud de Orihuela`,", "estado config")
rep("(0, a4.useState)([{ id: `cand-iv`,",
    "(0, a4.useState)(() => window.__VT.get('candidacies') || [{ id: `cand-iv`,", "estado candidaturas")
rep("(0, a4.useState)([{ id: `mesa-1`, number: 1,",
    "(0, a4.useState)(() => window.__VT.get('mesas') || [{ id: `mesa-1`, number: 1,", "estado mesas")
rep("[i6, c7, n4]), d5 = (e20) => {",
    "[i6, c7, n4]), __vts = (0, a4.useEffect)(() => {\n      window.__VT.save(n4, i6, c7);\n    }, [n4, i6, c7]), d5 = (e20) => {", "efecto de guardado")

VT = ("<script>window.__VT={key:'elecciones_estado_escrutinio_v1',"
      "raw:function(){try{var d=JSON.parse(localStorage.getItem(this.key)||'null');return d&&d.v===1?d:null}catch(e){return null}},"
      "get:function(k){var d=this.raw();if(!d)return null;var x=d[k];"
      "if(k==='config')return x&&typeof x==='object'&&!Array.isArray(x)&&typeof x.seats==='number'?x:null;"
      "if(k==='candidacies')return Array.isArray(x)&&x.length>0&&x.every(function(c){return c&&typeof c.id==='string'&&typeof c.acronym==='string'})?x:null;"
      "if(k==='mesas')return Array.isArray(x)&&x.length>0&&x.every(function(m){return m&&typeof m.id==='string'&&m.votesByCandidacy&&typeof m.votesByCandidacy==='object'})?x:null;"
      "return null},"
      "save:function(c,a,m){try{localStorage.setItem(this.key,JSON.stringify({v:1,t:Date.now(),config:c,candidacies:a,mesas:m}))}catch(e){}}};</script>")
k = h.rfind('<script type="module">')
assert k > 0
h = h[:k] + VT + h[k:]

open(out, "w", encoding="utf-8").write(h)
print("OK ->", out, f"{len(h)/1024:.0f} KB")
