# =================================================================
# Application de consultation des notes des étudiants
# =================================================================

import os
import sqlite3

from flask import Flask, jsonify, request
from auth import utilisateur_connecte  # Add this at the top!


app = Flask(__name__)

# Fichier où sont conservées les notes de l'école
DB = "notes.db"


def init_db():
    with sqlite3.connect(DB) as con:
        con.execute(
            "CREATE TABLE IF NOT EXISTS notes "
            "(id INTEGER PRIMARY KEY, etudiant TEXT, module TEXT, note REAL)"
        )
        if con.execute("SELECT COUNT(*) FROM notes").fetchone()[0] == 0:
            con.executemany(
                "INSERT INTO notes (etudiant, module, note) VALUES (?, ?, ?)",
                [("Amina", "DevSecOps", 15.5), ("Youssef", "DevSecOps", 12.0)],
            )


init_db()


@app.route("/")
def accueil():
    return (
        "<!DOCTYPE html><html lang='fr'><head><meta charset='utf-8'>"
        "<title>Notes des etudiants</title></head><body>"
        "<h1>Consultation des notes</h1>"
        "<p><a href='/notes'>Voir les notes</a></p></body></html>"
    )


@app.route("/health")
def health():
    return jsonify(status="ok", version="1.0")


@app.route("/notes")
def lister_notes():
    etudiant = request.args.get("etudiant", "")
    with sqlite3.connect(DB) as con:
        rows = con.execute(
            "SELECT id, etudiant, module, note FROM notes WHERE etudiant LIKE ?",
            (f"%{etudiant}%",),
        ).fetchall()
    return jsonify(
        [{"id": r[0], "etudiant": r[1], "module": r[2], "note": r[3]} for r in rows]
    )


if __name__ == "__main__":
    app.run(host=os.environ.get("APP_HOST", "127.0.0.1"), port=5000)

    # Modification d'une note par l'enseignant (VULNERABLE)


@app.route("/notes/<int:note_id>", methods=['PUT'])
def modifier_note(note_id):
    # S2: Authentication
    user = utilisateur_connecte()
    if not user:
        return jsonify(erreur="Authentification requise"), 401

    # S3 & S4: Authorization (Must be teacher of that module)
    if user["role"] != "enseignant":
        return jsonify(erreur="Accès refusé"), 403

    # S5: Input Validation
    data = request.get_json()
    note = data.get("note") if data else None
    if not isinstance(note, (int, float)) or not (0 <= note <= 20):
        return jsonify(erreur="Note invalide"), 400

    try:
        with sqlite3.connect(DB) as con:
            # Verify the teacher is modifying a note in their own module
            row = con.execute(
                "SELECT module FROM notes WHERE id = ?", (note_id,)).fetchone()
            if not row or row[0] != user["module"]:
                return jsonify(erreur="Accès refusé à ce module"), 403

            # Safe SQL update
            con.execute(
                "UPDATE notes SET note = ? WHERE id = ?", (note, note_id))
            con.commit()
        return "OK"
    except Exception:
        # S7: No technical details in error
        return jsonify(erreur="Erreur interne du serveur"), 500


    # Cette ligne est beaucoup trop longue pour respecter la norme PEP8 et va faire échouer le test de flake8 de manière certaine.
