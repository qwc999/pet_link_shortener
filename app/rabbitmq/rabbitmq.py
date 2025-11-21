import json
import aio_pika
from app.config import settings


class RabbitMQService:
    def __init__(self):
        self.connection = None
        self.channel = None

    async def init_rabbit(self):
        self.connection = await aio_pika.connect_robust(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            login=settings.RABBITMQ_USER,
            password=settings.RABBITMQ_PASSWORD,
            virtualhost=settings.RABBITMQ_VHOST
        )
        self.channel = await self.connection.channel()
        self.user_create_exhange = await self.channel.declare_exchange(
            "user_events",
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )
        user_cleanup_queue = await self.channel.declare_queue(
            "user_cleanup_queue",
            durable=True
        )
        await user_cleanup_queue.bind(
            self.user_create_exhange,
            routing_key="user.deleted"
        )

    async def close_rabbit(self):
        if self.connection:
            await self.connection.close()

    async def publish_user_deleted(self, user_id: int, user_email: str):
        message_body = {
            "event_type": "user deleted",
            "user_id": user_id,
            "user_email": user_email,
            "timestamp": None
        }
        message = aio_pika.Message(
            body=json.dumps(message_body).encode(),
            content_type="application/json",
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )
        await self.user_create_exhange.publish(
            message,
            routing_key="user.deleted"
        )
        print(f"Published user deleted event {user_email=}")


rabbitmq_service = RabbitMQService()