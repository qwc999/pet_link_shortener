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
        await self.channel.declare_exchange(
            "user_events",
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )

    async def close_rabbit(self):
        if self.connection:
            await self.connection.close()

    async def publish_user_deleted(self, user_id: int, user_email: str):
        ...


rabbitmq_service = RabbitMQService()