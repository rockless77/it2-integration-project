import logging
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker
from .models import User, create_db

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("website-b")

engine = create_db()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

class IncomingUser(BaseModel):
    id: int
    name: str
    phone: str
    joined_at: str

@app.post("/api/receive")
def receive_user(user: IncomingUser):
    log.info(f"[B] Received user: {user.dict()}")

    db = SessionLocal()
    record = User(
        external_id=str(user.id),
        full_name=user.name,
        contact=user.phone,
        created_at=user.joined_at,
    )
    db.add(record)
    db.commit()

    log.info(f"[B] Stored user in DB with external_id={user.id}")

    return {"status": "stored"}
