Internet Shop API

Простой API интернет-магазина на FastAPI с PostgreSQL.

Быстрый старт:
1. Клонировать проект:
   cd internet-shop

2. Создать файл .env из .env.example:
   cp .env.example .env

3. Запустить контейнеры:
   docker-compose up --build

4. Применить миграции:
   docker-compose exec app alembic upgrade head

API доступен:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Root: http://localhost:8000/

Эндпоинты:

Products:
- GET /products
- POST /products
- GET /products/{id}
- PUT /products/{id}
- DELETE /products/{id}

Customers:
- GET /customers
- POST /customers
- GET /customers/{id}
- PUT /customers/{id}
- DELETE /customers/{id}

Orders:
- GET /orders
- POST /orders
- GET /orders/{id}
- PATCH /orders/{id}
- DELETE /orders/{id}

Полезные команды:
- Остановить контейнеры: docker-compose down
- Логи приложения: docker-compose logs -f app
