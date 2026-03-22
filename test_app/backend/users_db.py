import psycopg2
import json
from cats_db import get_connection

def get_or_create_user(telegram_id, username=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, telegram_id, username, inventory FROM users WHERE telegram_id = %s", (telegram_id,))
    user = cursor.fetchone()
    
    if not user:
        cursor.execute(
            "INSERT INTO users (telegram_id, username, inventory) VALUES (%s, %s, '[]'::jsonb) RETURNING id, telegram_id, username, inventory",
            (telegram_id, username)
        )
        user = cursor.fetchone()
        conn.commit()
    
    cursor.close()
    conn.close()
    
    return {
        "id": user[0],
        "telegram_id": user[1],
        "username": user[2],
        "inventory": user[3]
    }

def add_item_to_inventory(telegram_id, item_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT inventory FROM users WHERE telegram_id = %s", (telegram_id,))
    result = cursor.fetchone()
    
    if not result:
        cursor.close()
        conn.close()
        return False
        
    inventory = result[0] or []
    
    found = False
    for item in inventory:
        if item.get('item_id') == item_id:
            item['count'] = item.get('count', 0) + 1
            found = True
            break
    
    if not found:
        inventory.append({"item_id": item_id, "count": 1})
    
    cursor.execute(
        "UPDATE users SET inventory = %s::jsonb WHERE telegram_id = %s",
        (json.dumps(inventory), telegram_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return True

def get_user_inventory_details(telegram_id):
    user = get_or_create_user(telegram_id)
    inventory_ids = user['inventory']
    
    if not inventory_ids:
        return []
    
    ids_to_fetch = [item['item_id'] for item in inventory_ids]
    
    conn = get_connection()
    cursor = conn.cursor()
    
    placeholders = ','.join(['%s'] * len(ids_to_fetch))
    cursor.execute(f"SELECT id, name, image_path, rarity FROM items WHERE id IN ({placeholders})", ids_to_fetch)
    items_data = cursor.fetchall()
    cursor.close()
    conn.close()
    
    items_map = {i[0]: {"name": i[1], "image_path": i[2], "rarity": i[3]} for i in items_data}
    
    result = []
    for inv_item in inventory_ids:
        item_id = inv_item['item_id']
        if item_id in items_map:
            img_name = items_map[item_id]['image_path'].split('/')[-1]
            result.append({
                "id": item_id,
                "name": items_map[item_id]['name'],
                "image_path": f"/images/{img_name}",
                "rarity": items_map[item_id]['rarity'],
                "count": inv_item['count']
            })
            
    return result
