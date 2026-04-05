import psycopg2

import os
import psycopg2
from psycopg2 import pool

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "tg_random_app"),
    "user": os.getenv("DB_USER", "tg_user"),
    "password": os.getenv("DB_PASSWORD", "mypassword123")
}

_db_pool = None

def get_pool():
    global _db_pool
    if _db_pool is None:
        _db_pool = psycopg2.pool.ThreadedConnectionPool(1, 20, **DB_CONFIG)
    return _db_pool

class PooledConnWrapper:
    def __init__(self, conn):
        self._conn = conn
        
    def __getattr__(self, name):
        return getattr(self._conn, name)
        
    def close(self):
        get_pool().putconn(self._conn)

def get_connection():
    return PooledConnWrapper(get_pool().getconn())

def get_all_items():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, image_path, rarity FROM items")
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"id": i[0], "name": i[1], "image_path": i[2], "rarity": i[3]} for i in items]

def get_item_by_id(item_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, image_path, rarity FROM items WHERE id = %s", (item_id,))
    item = cursor.fetchone()
    cursor.close()
    conn.close()
    if item:
        return {"id": item[0], "name": item[1], "image_path": item[2], "rarity": item[3]}
    return None
