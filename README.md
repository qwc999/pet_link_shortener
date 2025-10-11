1) Накатывание миграций
alembic init migrations


2) alembic:
alembic revision --autogenerate -m "comment"
alembic upgrade head


3) пре коммит хуки выключить / включить
pre-commit uninstall / install
