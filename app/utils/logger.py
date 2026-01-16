import asyncio
import json
from datetime import datetime
from typing import Any
import aiohttp


class LogstashLogger:
    def __init__(self):
        self.logstash_url = "http://localhost:5044"
        self.session = None
        self._queue = asyncio.Queue(maxsize=10000)
        self._worker_task = None

    def _make_serializable(self, obj: Any):
        if obj is None:
            return None
        elif isinstance(obj, (str, int, float, bool)):
            return obj
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, dict):
            return {k: self._make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple, set)):
            return [self._make_serializable(i) for i in obj]
        elif hasattr(obj, "__dict__"):
            return self._make_serializable(obj.__dict__)
        else:
            return str(obj)

    async def setup(self):
        try:
            self.session = aiohttp.ClientSession()
            self._worker_task = asyncio.create_task(self._worker())
        except Exception as e:
            print(f"Error setting up: {e}")
            raise

    async def log(self, level: str, message: str, **kwargs):
        extra = self._make_serializable(kwargs)
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level.upper(),
            "message": message,
            "service": "link_shortener",
            **extra
        }
        try:
            await self._queue.put(log_entry)
        except Exception as e:
            print(f"Log error: {e}")

    async def _worker(self):
        while True:
            try:
                log_entry = await self._queue.get()
                await self._send_to_logstash(log_entry)
                self._queue.task_done()
            except Exception as e:
                print(f"Log worker error: {e}")
                await asyncio.sleep(1)
            # finally:
            #     self._queue.task_done()

    async def _send_to_logstash(self, log_entry):
        try:
            json_data = json.dumps(log_entry)
            async with self.session.post(
                self.logstash_url,
                data=json_data,
                # headers={"Content-Type": "application/json"},
                timeout=aiohttp.ClientTimeout(total=5)
            ) as response:
                if response.status != 200:
                    print(f"Logstash error: {response.status}")
        except Exception as e:
            print(f"Log sender to logstash error: {e}")

    async def close(self):
        if self._worker_task:
            self._worker_task.cancel()
        if self.session:
            await self.session.close()
            self.session = None


logstash_logger = LogstashLogger()
