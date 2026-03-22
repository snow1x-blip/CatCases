import json
import random
from cats_db import get_connection


def ensure_cases_table():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cases (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                image_path TEXT NOT NULL,
                contents JSONB NOT NULL DEFAULT '[]'::jsonb
            )
            """
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def seed_default_case():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, rarity FROM items ORDER BY id")
        rows = cursor.fetchall()
        if not rows:
            return

        rarity_weights = {
            "common": 50,
            "rare": 30,
            "epic": 12,
            "legendary": 5,
        }
        contents = [
            {"item_id": item_id, "count": rarity_weights.get((rarity or "").lower(), 10)}
            for item_id, rarity in rows
        ]

        cursor.execute("SELECT id FROM cases WHERE name = %s", ("Starter Cat Case",))
        existing_case = cursor.fetchone()
        if existing_case:
            cursor.execute(
                "UPDATE cases SET image_path = %s, contents = %s::jsonb WHERE id = %s",
                ("/images/case1.png", json.dumps(contents), existing_case[0]),
            )
            conn.commit()
            return

        cursor.execute(
            "INSERT INTO cases (name, image_path, contents) VALUES (%s, %s, %s::jsonb)",
            ("Starter Cat Case", "/images/case1.png", json.dumps(contents)),
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def get_all_cases():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name, image_path FROM cases ORDER BY id")
        rows = cursor.fetchall()
        return [{"id": row[0], "name": row[1], "image_path": row[2]} for row in rows]
    finally:
        cursor.close()
        conn.close()


def get_case_items(case_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT
                i.id,
                i.name,
                i.image_path,
                i.rarity,
                COALESCE((entry.value->>'count')::int, 1) AS item_count
            FROM cases c
            JOIN LATERAL jsonb_array_elements(c.contents) AS entry(value) ON true
            JOIN items i ON i.id = (entry.value->>'item_id')::int
            WHERE c.id = %s
            ORDER BY i.id
            """,
            (case_id,),
        )
        rows = cursor.fetchall()

        items = []
        for row in rows:
            img_name = row[2].split("/")[-1]
            items.append(
                {
                    "id": row[0],
                    "name": row[1],
                    "image_path": f"/images/{img_name}",
                    "rarity": row[3],
                    "count": row[4],
                }
            )
        return items
    finally:
        cursor.close()
        conn.close()


def pick_case_winner(case_id: int):
    case_items = get_case_items(case_id)
    if not case_items:
        return None

    weights = [max(1, item.get("count", 1)) for item in case_items]
    return random.choices(case_items, weights=weights, k=1)[0]
