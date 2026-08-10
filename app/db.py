import os
from contextlib import contextmanager
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row

DATABASE_URL = os.environ["DATABASE_URL"]

#single pool for the whole process. opened in main.py's lifespan
pool = ConnectionPool(DATABASE_URL, min_size=2, max_size=10, open=False)

@contextmanager
def get_conn():
    with pool.connection() as conn:
        conn.row_factory = dict_row
        yield conn


