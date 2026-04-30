#cat > /mnt/user-data/outputs/database.py << 'EOF'
import sqlite3
from datetime import datetime
from typing import Optional


DB_PATH = "savorafrik.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS avis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_plat TEXT NOT NULL,
            pays TEXT,
            note INTEGER NOT NULL CHECK(note BETWEEN 1 AND 5),
            commentaire TEXT,
            auteur TEXT DEFAULT 'Anonyme',
            date_creation TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS suggestions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            email TEXT,
            sujet TEXT NOT NULL,
            message TEXT NOT NULL,
            date_creation TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def inserer_avis(nom_plat: str, pays: Optional[str], note: int,
                 commentaire: Optional[str], auteur: Optional[str]) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    maintenant = datetime.now().isoformat()
    auteur = auteur or "Anonyme"
    pays = pays or "Non précisé"

    cursor.execute("""
        INSERT INTO avis (nom_plat, pays, note, commentaire, auteur, date_creation)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nom_plat.strip().title(), pays, note, commentaire, auteur, maintenant))

    conn.commit()
    avis_id = cursor.lastrowid
    conn.close()
    return avis_id


def inserer_suggestion(nom: Optional[str], email: Optional[str],
                       sujet: str, message: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    maintenant = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO suggestions (nom, email, sujet, message, date_creation)
        VALUES (?, ?, ?, ?, ?)
    """, (nom, email, sujet, message, maintenant))

    conn.commit()
    suggestion_id = cursor.lastrowid
    conn.close()
    return suggestion_id


def get_stats_plats(limite: int = 10) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            nom_plat,
            pays,
            ROUND(AVG(note), 1) as note_moyenne,
            COUNT(*) as nombre_avis
        FROM avis
        GROUP BY nom_plat
        ORDER BY note_moyenne DESC, nombre_avis DESC
        LIMIT ?
    """, (limite,))

    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_stats_pays() -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            pays,
            COUNT(DISTINCT nom_plat) as nombre_plats,
            ROUND(AVG(note), 1) as note_moyenne
        FROM avis
        WHERE pays IS NOT NULL AND pays != 'Non précisé'
        GROUP BY pays
        ORDER BY nombre_plats DESC
    """)

    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_avis_par_plat(nom_plat: str) -> dict:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            ROUND(AVG(note), 1) as note_moyenne,
            COUNT(*) as nombre_avis
        FROM avis
        WHERE LOWER(nom_plat) = LOWER(?)
    """, (nom_plat,))

    row = cursor.fetchone()
    conn.close()
    if row and row["note_moyenne"]:
        return {"note_moyenne": row["note_moyenne"], "nombre_avis": row["nombre_avis"]}
    return {"note_moyenne": None, "nombre_avis": 0}
#EOF
#echo "database.py créé"

#Sortie
#database.py créé
