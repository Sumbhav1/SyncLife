from flask import g
from psycopg2.pool import ThreadedConnectionPool
from .config import Config

_pool = None


def _get_pool():
    global _pool
    if _pool is None:
        _pool = ThreadedConnectionPool(
            minconn=1,
            maxconn=10,
            host=Config.DB_HOST,
            dbname=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )
    return _pool


def get_db():
    """Return this request's connection, checking one out of the pool on first use."""
    if "db" not in g:
        g.db = _get_pool().getconn()
    return g.db


def close_db(exc=None):
    """Return the request's connection to the pool. Registered as an app teardown."""
    conn = g.pop("db", None)
    if conn is not None:
        # Discard anything left uncommitted (e.g. after an error) before reuse
        conn.rollback()
        _get_pool().putconn(conn)
