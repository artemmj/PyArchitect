from fastapi import FastAPI
import httpx
import asyncio


# Понимание, зачем нужны health checks.
# Как проверять внутренние зависимости (БД, кеш, внешние API).
# Интеграция с Kubernetes, Docker, Prometheus, Consul.

# Критично для микросервисной архитектуры.
# Позволяет отслеживать работоспособность сервисов.
# Интегрируется с orchestrators (K8s, Docker Swarm и т.д.).


app = FastAPI()


# Проверка внутреннего состояния
@app.get("/health")
def health_check():
    checks = {
        "status": "healthy",
        "checks": {
            "database": check_database(),
            "cache": check_cache(),
            "external_api": asyncio.run(check_external_api()),
        }
    }
    overall_status = "healthy" if all(v == "ok" for v in checks["checks"].values()) else "unhealthy"
    checks["status"] = overall_status
    return checks


def check_database():
    # Здесь была бы проверка подключения к БД
    return "ok"


def check_cache():
    # Здесь была бы проверка подключения к Redis и т.д.
    return "ok"


async def check_external_api():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://google.com", timeout=5)
            return "ok" if response.status_code == 200 else "failed"
    except:
        return "failed"


# Использование
# curl http://localhost:8000/health
