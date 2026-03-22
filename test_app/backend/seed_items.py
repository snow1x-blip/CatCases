from cats_db import get_connection


SEED_ITEMS = [
    {"name": "Cat1", "image_path": "/images/cat1.png", "rarity": "common"},
    {"name": "Cat2", "image_path": "/images/cat2.png", "rarity": "common"},
    {"name": "Cat3", "image_path": "/images/cat3.png", "rarity": "rare"},
    {"name": "Cat4", "image_path": "/images/cat4.png", "rarity": "rare"},
    {"name": "Cat5", "image_path": "/images/cat5.png", "rarity": "rare"},
    {"name": "Cat6", "image_path": "/images/cat6.png", "rarity": "epic"},
    {"name": "Cat7", "image_path": "/images/cat7.png", "rarity": "epic"},
    {"name": "Cat8", "image_path": "/images/cat8.png", "rarity": "legendary"},
    {"name": "Cat9", "image_path": "/images/cat9.png", "rarity": "legendary"},
]


def seed_items():
    conn = get_connection()
    cursor = conn.cursor()
    inserted = 0

    try:
        for item in SEED_ITEMS:
            cursor.execute("SELECT id FROM items WHERE name = %s", (item["name"],))
            existing = cursor.fetchone()

            if existing:
                continue

            cursor.execute(
                "INSERT INTO items (name, image_path, rarity) VALUES (%s, %s, %s)",
                (item["name"], item["image_path"], item["rarity"]),
            )
            inserted += 1

        conn.commit()
        print(f"Seed completed: inserted {inserted} new items, skipped {len(SEED_ITEMS) - inserted} existing.")
    
    except Exception:
        conn.rollback()
        raise
    
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    seed_items()
