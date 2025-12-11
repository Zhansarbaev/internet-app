from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.routers import customers, products, orders

app = FastAPI(

    title = "API для интернет магазина",
    description = "API для управления клиентами, продуктами и заказами в интернет магазине.",
    version = "1.0.0",
    redoc_url = None,  # отключаем стандартный ReDoc
    docs_url = "/docs",
    swagger_ui_parameters = {"syntaxHighlight.theme": "obsidian"},
)

# CORS (для фронта)
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

app.include_router(products.router)
app.include_router(customers.router)
app.include_router(orders.router)

# Кастомный ReDoc через CDN
@app.get("/redoc", include_in_schema = False)
def redoc():
    return HTMLResponse(
        """
        <!DOCTYPE html>
        <html>
          <head>
            <title>ReDoc - API Документация</title>
            <meta charset="utf-8"/>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
            <style>
              body {
                margin: 0;
                padding: 0;
              }
            </style>
          </head>
          <body>
            <redoc spec-url="/openapi.json"></redoc>
            <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
          </body>
        </html>
        """
    )

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