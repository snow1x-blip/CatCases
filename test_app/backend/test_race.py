import asyncio
import sys
import os
import time
import json
import hmac
import hashlib
from urllib.parse import urlencode
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from users_db import get_or_create_user, add_item_to_inventory, get_user_inventory_details

def generate_test_init_data():
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
        
    token = os.getenv("TELEGRAM_BOT_TOKEN", "test_token")
    if token == "test_token":
        print("WARNING: TELEGRAM_BOT_TOKEN not found in environment, using 'test_token'")
        
    user_data = {
        "id": 999999,
        "first_name": "test_race_user",
        "username": "test_race_user"
    }
    
    auth_date = int(time.time())
    
    data_dict = {
        "auth_date": str(auth_date),
        "user": json.dumps(user_data, separators=(',', ':'))
    }
    
    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(data_dict.items()))
    secret_key = hmac.new(b"WebAppData", token.encode(), hashlib.sha256).digest()
    hash_value = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    
    data_dict["hash"] = hash_value
    
    return urlencode(data_dict)

async def test_race_condition():
    telegram_id = 999999
    print(f"Testing for user {telegram_id}")
    
    # Generate and print test init_data for browser/Swagger testing
    test_init_data = generate_test_init_data()
    print("\n" + "="*50)
    print("TEST INIT_DATA FOR BROWSER / SWAGGER:")
    print(test_init_data)
    print("="*50 + "\n")
    
    # 1. Ensure user exists and wipe inventory for test
    from cats_db import get_connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE telegram_id = %s", (telegram_id,))
    conn.commit()
    cursor.close()
    conn.close() # returns to pool
    
    get_or_create_user(telegram_id, "test_race_user")
    
    # 2. Run 10 concurrent additions
    async def add_item(item_id):
        # run synchronous db call in thread pool to simulate concurrent requests
        return await asyncio.to_thread(add_item_to_inventory, telegram_id, item_id)
        
    print("Sending 10 concurrent requests...")
    tasks = [add_item(1) for _ in range(10)]
    await asyncio.gather(*tasks)
    
    # 3. Check inventory length
    inventory = get_user_inventory_details(telegram_id)
    total_count = sum(item['count'] for item in inventory)
    
    print(f"Total count of items in inventory: {total_count}")
    if total_count == 10:
        print("SUCCESS! Race condition avoided, all 10 additions registered.")
    else:
        print(f"FAILED! Expected 10, got {total_count}")

if __name__ == "__main__":
    asyncio.run(test_race_condition())
