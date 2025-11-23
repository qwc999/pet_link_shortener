import json
import aio_pika
from app.config import settings
from app.database import async_session
from app.service.user_cleanup import UserCleanupService


class UserCleanupConsumer:
    def __init__(self):
        self.connection = None
        self.channel = None

    async def start_consuming(self):
        self.connection = await aio_pika.connect_robust(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            login=settings.RABBITMQ_USER,
            password=settings.RABBITMQ_PASSWORD,
            virtualhost=settings.RABBITMQ_VHOST
        )
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=1)
        queue = await self.channel.declare_queue(
            "user_cleanup_queue",
            durable=True
        )
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                try:
                    await self._process_message(message)
                except Exception as e:
                    print(f"Error processing message: {e}")

    async def _process_message(self, message: aio_pika.IncomingMessage):
        async with message.process():
            message_body = json.loads(message.body.decode())
            user_id = message_body.get("user_id")
            user_email = message_body.get("user_email")
            print(f"Processing for {user_id=}, {user_email=}")
            await self._cleanup_user_data(user_id, user_email)

    async def _cleanup_user_data(self, user_id: int, _user_email: str):
        async with async_session() as session:
            async with session.begin():
                cleanup_service = UserCleanupService(session)
                await cleanup_service.cleanup_user_data(user_id)
                print(f"Success for {user_id=}")

    async def stop_consuming(self):
        if self.connection:
            self.connection.close()


user_cleanup_consumer = UserCleanupConsumer()
