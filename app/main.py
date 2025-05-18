from fastapi import FastAPI, HTTPException
from app.database import database, engine, metadata
from app.models import User, Notification
from app.schemas import NotificationCreate, NotificationOut
from app.config import RABBITMQ_URL
import aio_pika
import os
import json
from typing import List

app = FastAPI()

metadata.create_all(bind=engine)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

async def publish_notification(message: dict):
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue("notifications", durable=True)
    await channel.default_exchange.publish(
        aio_pika.Message(body=json.dumps(message).encode()),
        routing_key=queue.name
    )
    await connection.close()

@app.post("/notifications", status_code=202)
async def create_notification(notification: NotificationCreate):
    query = User.select().where(User.c.id == notification.user_id)
    user = await database.fetch_one(query)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await publish_notification(notification.dict())
    return {"message": "Notification queued"}

@app.get("/notifications/{user_id}", response_model=List[NotificationOut])
async def get_notifications(user_id: int):
    query = Notification.select().where(Notification.c.user_id == user_id).order_by(Notification.c.created_at.desc())
    notifications = await database.fetch_all(query)
    return [NotificationOut(**notification) for notification in notifications]
