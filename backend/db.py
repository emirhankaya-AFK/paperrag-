import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from .config import settings

def get_db_connection():
    conn = sqlite3.connect(settings.SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS papers (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        authors TEXT NOT NULL,
        pub_date TEXT,
        venue TEXT,
        abstract TEXT,
        file_path TEXT NOT NULL,
        uploaded_at TEXT NOT NULL,
        keywords TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS extractions (
        paper_id TEXT PRIMARY KEY,
        key_contributions TEXT,
        methodology TEXT,
        main_results TEXT,
        limitations TEXT,
        FOREIGN KEY (paper_id) REFERENCES papers (id) ON DELETE CASCADE
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS summaries (
        paper_id TEXT PRIMARY KEY,
        executive_summary TEXT,
        problem TEXT,
        solution TEXT,
        results TEXT,
        impact TEXT,
        key_takeaways TEXT,
        FOREIGN KEY (paper_id) REFERENCES papers (id) ON DELETE CASCADE
    )
    """)
    conn.commit()
    conn.close()

# Paper operations
def save_paper(paper_data: Dict[str, Any]) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO papers (id, title, authors, pub_date, venue, abstract, file_path, uploaded_at, keywords)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        paper_data["id"],
        paper_data["title"],
        ",".join(paper_data["authors"]) if isinstance(paper_data["authors"], list) else paper_data["authors"],
        paper_data.get("pub_date"),
        paper_data.get("venue"),
        paper_data.get("abstract"),
        paper_data["file_path"],
        paper_data.get("uploaded_at", datetime.now().isoformat()),
        json.dumps(paper_data.get("keywords", []))
    ))
    conn.commit()
    conn.close()

def get_paper(paper_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    row = cursor.execute("SELECT * FROM papers WHERE id = ?", (paper_id,)).fetchone()
    conn.close()
    if row:
        paper = dict(row)
        paper["authors"] = [a.strip() for a in paper["authors"].split(",") if a.strip()]
        paper["keywords"] = json.loads(paper["keywords"]) if paper["keywords"] else []
        return paper
    return None

def list_papers() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    rows = cursor.execute("SELECT * FROM papers ORDER BY uploaded_at DESC").fetchall()
    conn.close()
    papers = []
    for r in rows:
        p = dict(r)
        p["authors"] = [a.strip() for a in p["authors"].split(",") if a.strip()]
        p["keywords"] = json.loads(p["keywords"]) if p["keywords"] else []
        papers.append(p)
    return papers

def delete_paper(paper_id: str) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM papers WHERE id = ?", (paper_id,))
    cursor.execute("DELETE FROM extractions WHERE paper_id = ?", (paper_id,))
    cursor.execute("DELETE FROM summaries WHERE paper_id = ?", (paper_id,))
    conn.commit()
    conn.close()

# Extraction operations
def save_extraction(paper_id: str, ext_data: Dict[str, Any]) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO extractions (paper_id, key_contributions, methodology, main_results, limitations)
    VALUES (?, ?, ?, ?, ?)
    """, (
        paper_id,
        json.dumps(ext_data["key_contributions"]),
        ext_data["methodology"],
        json.dumps(ext_data["main_results"]),
        json.dumps(ext_data["limitations"])
    ))
    conn.commit()
    conn.close()

def get_extraction(paper_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    row = cursor.execute("SELECT * FROM extractions WHERE paper_id = ?", (paper_id,)).fetchone()
    conn.close()
    if row:
        ext = dict(row)
        ext["key_contributions"] = json.loads(ext["key_contributions"])
        ext["main_results"] = json.loads(ext["main_results"])
        ext["limitations"] = json.loads(ext["limitations"])
        return ext
    return None

# Summary operations
def save_summary(paper_id: str, sum_data: Dict[str, Any]) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO summaries (paper_id, executive_summary, problem, solution, results, impact, key_takeaways)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        paper_id,
        sum_data["executive_summary"],
        sum_data["problem"],
        sum_data["solution"],
        sum_data["results"],
        sum_data["impact"],
        json.dumps(sum_data["key_takeaways"])
    ))
    conn.commit()
    conn.close()

def get_summary(paper_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    row = cursor.execute("SELECT * FROM summaries WHERE paper_id = ?", (paper_id,)).fetchone()
    conn.close()
    if row:
        s = dict(row)
        s["key_takeaways"] = json.loads(s["key_takeaways"])
        return s
    return None
