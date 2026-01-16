import asyncio
import time
import uuid
from fastapi import Request
from app.utils.logger import logstash_logger


async def logging_middleware(request: Request, call_next):
    start = time.time()
    request_id = str(uuid.uuid4())
    if any(path in request.url.path for path in [
        "/docs", "/redoc", "openapi.json", "/static"
    ]):
        response = await call_next(request)
        return response

    asyncio.create_task(
        logstash_logger.log(
            "INFO",
            "HTTP request started",
            log_type="http_request",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            query_params=dict(request.query_params),
            client_ip=request.client.host,
            user_agent=request.headers.get("user-agent")
        )
    )
    try:
        response = await call_next(request)
        process_time = (time.time() - start) * 1000

        asyncio.create_task(
            logstash_logger.log(
                "INFO",
                "HTTP request completed",
                log_type="http_request",
                request_id=request_id,
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                response_time_ms=round(process_time, 2)
            )
        )

        return response

    except Exception as e:
        process_time = (time.time() - start) * 1000
        asyncio.create_task(
            logstash_logger.log(
                "ERROR",
                "HTTP request failed",
                log_type="http_request",
                request_id=request_id,
                method=request.method,
                path=request.url.path,
                error_type=type(e).__name__,
                error_message=str(e),
                response_time_ms=round(process_time, 2)
            )
        )
        raise
