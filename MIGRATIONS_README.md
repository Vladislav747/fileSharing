alembic init migration (Требует установить пакет глобально в linux)

alembic revision -m "create table" - Создать первую миграцию

alembic revision --autogenerate -m 'initial'(Перед этим настроить alembic.ini)

alembic upgrade head - Применить все миграции

alembic upgrade e34025b07af2 - Применить конкретную миграцию за номером e34025b07af2

alembic downgrade -1

alembic history