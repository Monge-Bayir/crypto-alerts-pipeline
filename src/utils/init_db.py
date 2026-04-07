from pathlib import Path

from src.utils.db import get_connection
from src.utils.logger import get_logger

logger = get_logger('init_db')


def init_tables():
    project_root = Path(__file__).resolve().parents[2]
    sql_file = project_root / "sql" / "init_tables.sql"

    with open(sql_file, "r", encoding="utf-8") as f:
        sql = f.read()

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    init_tables()
    logger.info("Tables created successfully.")