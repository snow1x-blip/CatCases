import asyncio
import httpx
import time
import json
import hmac
import hashlib
import os
from urllib.parse import urlencode

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
        "id": 888888,
        "first_name": "rest_race_user",
        "username": "rest_race_user"
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

async def test_rest_race_condition():
    # 1. Generate valid init_data
    init_data = generate_test_init_data()
    print("\n" + "="*70)
    print("TEST INIT_DATA (You can use this to test in web browser/Swagger):")
    print(init_data)
    print("="*70 + "\n")
    
    headers = {
        "x-telegram-init-data": init_data
    }
    
    base_url = "http://127.0.0.1:8000"
    case_id = 1
    
    print(f"Sending 10 concurrent /api/spin requests to {base_url}...")
    
    async with httpx.AsyncClient() as client:
        # We can't wipe inventory via API easily unless we use DB, 
        # but we can get initial count, spin 10 times, and check final count.
        
        # Get initial inventory
        try:
            resp = await client.get(f"{base_url}/api/inventory", headers=headers)
            resp.raise_for_status()
            initial_items = resp.json().get("items", [])
            initial_count = sum(item["count"] for item in initial_items)
            print(f"Initial item count: {initial_count}")
        except httpx.ConnectError:
            print(f"ERROR: Cannot connect to {base_url}. Make sure your FastAPI server is running!")
            return
            
        # Run 10 concurrent requests
        async def spin():
            return await client.get(f"{base_url}/api/spin?case_id={case_id}", headers=headers)
            
        tasks = [spin() for _ in range(10)]
        responses = await asyncio.gather(*tasks)
        
        successes = sum(1 for r in responses if r.status_code == 200)
        print(f"Completed 10 requests. Successful spins: {successes}")
        
        # Get final inventory
        resp = await client.get(f"{base_url}/api/inventory", headers=headers)
        resp.raise_for_status()
        final_items = resp.json().get("items", [])
        final_count = sum(item["count"] for item in final_items)
        
        added = final_count - initial_count
        print(f"Final item count: {final_count} (Added {added} items)")
        
        if added == 10:
            print("SUCCESS! Race condition avoided, all 10 spins were credited.")
        else:
            print(f"FAILED! Expected 10 items added, but only got {added}.")

if __name__ == "__main__":
    asyncio.run(test_rest_race_condition())
