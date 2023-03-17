### Тестовый проект с курса Егора

uvicorn main:app

pip install -r requirements.txt

alembic init migration (Требует установить пакет глобально в linux)

alembic revision -m "create table" - Создать первую миграцию

alembic revision --autogenerate -m 'initial'(Перед этим настроить alembic.ini)

alembic upgrade head - Применить все миграции

alembic upgrade e34025b07af2 - Применить конкретную миграцию за номером  e34025b07af2

Создание миграции

``bash
.\venv\Scripts\python.exe -m alembic revision --autogenerate -m "Поменяли password на hashed_password"
``

Запуск воркера celery
``bash
python -m celery -A worker worker -l info -Q queue -P solo
``

Боевая сборка
``
sudo docker-compose -f docker-compose.prod.yml up -d
``
 
