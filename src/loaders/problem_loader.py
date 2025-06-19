# 백준 문제 데이터 로더

import sqlite3
import os
from langchain.schema import Document

SQL_DUMP_PATH = os.getenv("BOJ_SQL_DUMP")

def load_boj_problems() -> list[Document]:
    dump_path = SQL_DUMP_PATH
    if not os.path.exists(dump_path):
        raise FileNotFoundError(f"SQL dump not found at '{dump_path}'")

    conn = sqlite3.connect(":memory:")
    cur  = conn.cursor()
    with open(dump_path, "r", encoding="utf-8") as f:
        sql_script = f.read()
    cur.executescript(sql_script)

    query = """
        SELECT id, title, description, tier, correct_rate
        FROM problem
        WHERE description IS NOT NULL
    """
    rows = cur.execute(query).fetchall()

    docs: list[Document] = []
    for id_, title, description, tier, correct_rate in rows:
        text = f"# {title}\n\n{description}"
        metadata = {
            "id": id_,
            "tier": tier,
            "correct_rate": correct_rate
        }
        docs.append(Document(page_content=text, metadata=metadata))

    conn.close()
    return docs