from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import customers, products, orders

app = FastAPI(

    title = "API для интернет магазина",
    description = "API для управления клиентами, продуктами и заказами в интернет магазине.",
    version = "1.0.0",
    docs_url = "/docs",
    redoc_url = "/redoc"
)

# CORS (для фронта)
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

# Роутеры
app.include_router(products.router)
app.include_router(customers.router)
app.include_router(orders.router)

@app.get("/", tags = ["Root"], description = "Корневой эндпоинт")
def read_root():
    return {
        "message": "Добро пожаловать в API интернет магазина!",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
        }

@app.get("/health", tags = ["Health"], description = "Проверка состояния сервиса")
def health_check():
    return {"status": "ok"}