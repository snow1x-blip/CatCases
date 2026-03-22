from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from cats_db import get_all_items
from users_db import get_or_create_user, add_item_to_inventory, get_user_inventory_details
from cases_db import ensure_cases_table, seed_default_case, get_all_cases, get_case_items, pick_case_winner
from telegram_auth import validate_telegram_init_data, get_init_data_from_request
from pathlib import Path
import uvicorn
import os

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
IMAGES_DIR = BASE_DIR / "images"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/images", StaticFiles(directory=str(IMAGES_DIR)), name="images")


@app.on_event("startup")
def initialize_database():
    ensure_cases_table()
    seed_default_case()

@app.get("/")
def read_root():
    return {"message": "Cat Case API with Inventory"}

@app.get("/api/spin")
def spin_case(request: Request, case_id: int = 1, init_data: str | None = None):
    init_data = get_init_data_from_request(request, init_data)
    telegram_id, username = validate_telegram_init_data(init_data)
    get_or_create_user(telegram_id, username)

    winner = pick_case_winner(case_id)
    if not winner:
        raise HTTPException(status_code=404, detail="Case is empty or does not exist")

    add_item_to_inventory(telegram_id, winner["id"])
    return winner

@app.get("/api/inventory")
def get_inventory(request: Request, init_data: str | None = None):
    init_data = get_init_data_from_request(request, init_data)
    telegram_id, _ = validate_telegram_init_data(init_data)
    items = get_user_inventory_details(telegram_id)
    return {"items": items}

@app.get("/api/items")
def get_catalog(request: Request, case_id: int | None = None, init_data: str | None = None):
    init_data = get_init_data_from_request(request, init_data)
    validate_telegram_init_data(init_data)
    if case_id is not None:
        return get_case_items(case_id)
    return get_all_items()

@app.get("/api/cases")
def list_cases(request: Request, init_data: str | None = None):
    init_data = get_init_data_from_request(request, init_data)
    validate_telegram_init_data(init_data)
    return get_all_cases()

@app.get("/api/cases/{case_id}/items")
def list_case_items(case_id: int, request: Request, init_data: str | None = None):
    init_data = get_init_data_from_request(request, init_data)
    validate_telegram_init_data(init_data)
    return get_case_items(case_id)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "8000")),
        reload=os.getenv("RELOAD", "false").lower() == "true",
    )
