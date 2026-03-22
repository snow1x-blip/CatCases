import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "database": "tg_random_app",
    "user": "tg_user",
    "password": "mypassword123"
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

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
