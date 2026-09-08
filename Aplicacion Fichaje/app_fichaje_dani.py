import sqlite3
import os
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash

app = Flask(__name__)
app.secret_key = "fichaje-oficina-2024"

DB_PATH = os.path.join(os.path.dirname(__file__), "fichaje.db")


# ── Base de datos ──────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS empleados (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre    TEXT NOT NULL,
            apellidos TEXT NOT NULL,
            email     TEXT UNIQUE NOT NULL,
            pin       TEXT NOT NULL,
            activo    INTEGER DEFAULT 1,
            creado_en TEXT DEFAULT (datetime('now','localtime'))
        );

        CREATE TABLE IF NOT EXISTS fichajes (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            empleado_id INTEGER NOT NULL,
            tipo        TEXT NOT NULL CHECK(tipo IN ('entrada','salida')),
            timestamp   TEXT DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (empleado_id) REFERENCES empleados(id)
        );
    """)
    # Empleados de ejemplo
    try:
        conn.execute("""
            INSERT OR IGNORE INTO empleados (nombre, apellidos, email, pin)
            VALUES
                ('Ana',    'García López',   'ana.garcia@empresa.com',   '1234'),
                ('Carlos', 'Martínez Ruiz',  'carlos.martinez@empresa.com','5678'),
                ('Laura',  'Sánchez Pérez',  'laura.sanchez@empresa.com', '9012')
        """)
    except Exception:
        pass
    conn.commit()
    conn.close()


# ── Helpers ────────────────────────────────────────────────────
def ultimo_fichaje(empleado_id):
    conn = get_db()
    row = conn.execute(
        "SELECT tipo FROM fichajes WHERE empleado_id=? ORDER BY id DESC LIMIT 1",
        (empleado_id,)
    ).fetchone()
    conn.close()
    return row["tipo"] if row else None


def horas_hoy(empleado_id):
    hoy = date.today().isoformat()
    conn = get_db()
    rows = conn.execute(
        """SELECT tipo, timestamp FROM fichajes
           WHERE empleado_id=? AND date(timestamp)=?
           ORDER BY id""",
        (empleado_id, hoy)
    ).fetchall()
    conn.close()

    total = 0
    entrada = None
    for r in rows:
        ts = datetime.fromisoformat(r["timestamp"])
        if r["tipo"] == "entrada":
            entrada = ts
        elif r["tipo"] == "salida" and entrada:
            total += (ts - entrada).total_seconds()
            entrada = None
    if entrada:
        total += (datetime.now() - entrada).total_seconds()

    h, rem = divmod(int(total), 3600)
    m = rem // 60
    return f"{h}h {m:02d}m"


# ── Rutas ──────────────────────────────────────────────────────
@app.route("/")
def index():
    conn = get_db()
    empleados = conn.execute(
        "SELECT * FROM empleados WHERE activo=1 ORDER BY nombre"
    ).fetchall()
    conn.close()

    empleados_info = []
    for e in empleados:
        ultimo = ultimo_fichaje(e["id"])
        empleados_info.append({
            "id":        e["id"],
            "nombre":    e["nombre"],
            "apellidos": e["apellidos"],
            "email":     e["email"],
            "estado":    "dentro" if ultimo == "entrada" else "fuera",
            "horas_hoy": horas_hoy(e["id"]),
        })
    return render_template("index.html", empleados=empleados_info)


@app.route("/fichar", methods=["POST"])
def fichar():
    empleado_id = request.form.get("empleado_id")
    pin         = request.form.get("pin", "").strip()

    conn = get_db()
    emp = conn.execute(
        "SELECT * FROM empleados WHERE id=? AND activo=1", (empleado_id,)
    ).fetchone()

    if not emp:
        flash("Empleado no encontrado.", "error")
        conn.close()
        return redirect(url_for("index"))

    if emp["pin"] != pin:
        flash(f"PIN incorrecto para {emp['nombre']}.", "error")
        conn.close()
        return redirect(url_for("index"))

    ultimo = ultimo_fichaje(empleado_id)
    tipo   = "salida" if ultimo == "entrada" else "entrada"

    conn.execute(
        "INSERT INTO fichajes (empleado_id, tipo) VALUES (?, ?)",
        (empleado_id, tipo)
    )
    conn.commit()
    conn.close()

    emoji = "✅" if tipo == "entrada" else "👋"
    flash(f"{emoji} {emp['nombre']} — {tipo.capitalize()} registrada correctamente.", "success")
    return redirect(url_for("index"))


@app.route("/historial")
def historial():
    conn = get_db()
    rows = conn.execute("""
        SELECT f.id, e.nombre, e.apellidos, f.tipo, f.timestamp
        FROM fichajes f
        JOIN empleados e ON e.id = f.empleado_id
        ORDER BY f.id DESC
        LIMIT 200
    """).fetchall()
    conn.close()
    return render_template("historial.html", fichajes=rows)


@app.route("/empleados")
def empleados():
    conn = get_db()
    emps = conn.execute("SELECT * FROM empleados ORDER BY nombre").fetchall()
    conn.close()
    return render_template("empleados.html", empleados=emps)


@app.route("/empleados/nuevo", methods=["POST"])
def nuevo_empleado():
    nombre    = request.form.get("nombre", "").strip()
    apellidos = request.form.get("apellidos", "").strip()
    email     = request.form.get("email", "").strip()
    pin       = request.form.get("pin", "").strip()

    if not all([nombre, apellidos, email, pin]):
        flash("Completa todos los campos.", "error")
        return redirect(url_for("empleados"))

    try:
        conn = get_db()
        conn.execute(
            "INSERT INTO empleados (nombre, apellidos, email, pin) VALUES (?,?,?,?)",
            (nombre, apellidos, email, pin)
        )
        conn.commit()
        conn.close()
        flash(f"Empleado {nombre} {apellidos} añadido.", "success")
    except sqlite3.IntegrityError:
        flash("Ya existe un empleado con ese email.", "error")

    return redirect(url_for("empleados"))


@app.route("/empleados/<int:emp_id>/toggle", methods=["POST"])
def toggle_empleado(emp_id):
    conn = get_db()
    emp = conn.execute("SELECT * FROM empleados WHERE id=?", (emp_id,)).fetchone()
    if emp:
        nuevo = 0 if emp["activo"] else 1
        conn.execute("UPDATE empleados SET activo=? WHERE id=?", (nuevo, emp_id))
        conn.commit()
        accion = "activado" if nuevo else "desactivado"
        flash(f"Empleado {emp['nombre']} {accion}.", "success")
    conn.close()
    return redirect(url_for("empleados"))


@app.route("/api/estado")
def api_estado():
    conn = get_db()
    empleados = conn.execute("SELECT * FROM empleados WHERE activo=1").fetchall()
    conn.close()
    resultado = []
    for e in empleados:
        ultimo = ultimo_fichaje(e["id"])
        resultado.append({
            "id":     e["id"],
            "nombre": f"{e['nombre']} {e['apellidos']}",
            "estado": "dentro" if ultimo == "entrada" else "fuera",
        })
    return jsonify(resultado)


if __name__ == "__main__":
    init_db()
    print("\n🏢  Sistema de Fichaje de Oficina")
    print("   Abre http://127.0.0.1:5000  en tu navegador\n")
    app.run(debug=True, port=5000)
