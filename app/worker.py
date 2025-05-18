import asyncio
import aio_pika
import json
from app.database import database
from app.models import User, Notification
from app.email_utils import send_email
from app.config import RABBITMQ_URL

async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        data = json.loads(message.body)
        user_id = data.get("user_id")
        n_type = data.get("type")
        content = data.get("content")

        query = User.select().where(User.c.id == user_id)
        user = await database.fetch_one(query)
        if not user:
            print(f"User with id {user_id} not found. Skipping notification.")
            return

        await send_email(
            to_email=user["email"],
            subject=f"Notification: {n_type}",
            body=content,
        )

        ins_query = Notification.insert().values(
            user_id=user_id,
            type=n_type,
            content=content,
        )
        await database.execute(ins_query)
        print(f"Notification sent and saved for user {user_id}")

async def main():
    await database.connect()
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue("notifications", durable=True)
    await queue.consume(process_message)
    print("Worker started. Waiting for messages...")
    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
