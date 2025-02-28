from fastapi import FastAPI
from pydantic import BaseModel
import redis

app = FastAPI()

# 1️⃣ redis-service (같은 네임스페이스에서 단순 이름으로 접근 가능)
# 2️⃣ redis-service.default (네임스페이스 포함)
# 3️⃣ redis-service.default.svc (서비스 도메인 포함)
# 4️⃣ redis-service.default.svc.cluster.local (전체 FQDN)

redis_host: str = "redis-service.hello"

redis_client = redis.Redis(host=redis_host, port=6379, db=0)


class KeyValue(BaseModel):
    key: str
    value: str


@app.post("/api/set")
async def set_value(data: KeyValue):
    """
    Redis에 key-value 쌍을 저장하는 API
    """
    redis_client.set(data.key, data.value)
    return {"message": f"Value for key '{data.key}' set successfully."}


@app.get("/api/get/{key}")
async def get_value(key: str):
    """
    Redis에서 key에 해당하는 값을 가져오는 API
    """
    value = redis_client.get(key)
    if value is None:
        return {"message": f"Key '{key}' not found."}
    return {"key": key, "value": value.decode("utf-8")}


@app.get("/")
async def root():
    return {"message": "Hello from FastAPI"}


@app.get("/api")
async def api():
    return {"message": "This is FastAPI behind Nginx"}
