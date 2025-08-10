import os, hmac, hashlib, json
from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from db import get_db
from sqlalchemy import text

router = APIRouter(prefix="/payments", tags=["payments"])
WEBHOOK_SECRET = os.getenv("DONORBOX_WEBHOOK_SECRET")

@router.post("/donorbox/webhook")
async def donorbox_webhook(request: Request, db: Session = Depends(get_db)):
    body = await request.body()
    signature = request.headers.get("X-Donorbox-Signature")
    if not signature or not WEBHOOK_SECRET:
        raise HTTPException(status_code=400, detail="Missing signature")
    digest = hmac.new(WEBHOOK_SECRET.encode(), body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(digest, signature):
        raise HTTPException(status_code=403, detail="Invalid signature")
    payload = json.loads(body.decode())

    email = payload.get("donor", {}).get("email")
    amount = int(float(payload.get("amount_in_cents", 0)))
    status = payload.get("status")
    level = None
    custom = payload.get("custom_fields", {})
    if isinstance(custom, dict):
        level = custom.get("Level")
        try:
            level = int(level) if level else None
        except:
            level = None

    if email:
        user = db.execute(text("SELECT * FROM users WHERE email=:e"), {"e": email}).mappings().first()
        if user and status and status.lower() in ("succeeded","paid","completed"):
            db.execute(text("UPDATE users SET is_active=1, donation_level=:lvl WHERE id=:uid"),
                       {"lvl": level, "uid": user["id"]})
            db.commit()
    return {"ok": True}
