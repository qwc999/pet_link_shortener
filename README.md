# Пет проект Link Shortener - сервис сокращения ссылок


### Стек:
FastAPI, PostgreSQL, asyncpg, redis, rabbitMQ, elk, alembic, docker-compose, pydantic, jwt


### Реализовано:
- регистрация, авторизация
- редирект по короткому коду, при переходе по короткой ссылке логируется ip, браузер и другие данные
- CRUD операции для ссылок и для пользователей
- ролевая модель, доступ к некоторым ручкам только админам
- весь проект асинхронный
- если по короткой ссылке перешли, она кешируется
- при удалении пользователя публикуется событие в rabbit, консюмер удаляет все его ссылки
- если дергают любую ручку, лог попадает в elastic (реализовано через middleware)
- если происходит бизнес-событие, лог попадает в elastic (реализовал это только для для одного бизнес события для примера)

### Команды:
1) Запустить проект
make up
2) Накатывание миграций  
alembic init migrations
2) alembic:  
alembic revision --autogenerate -m "comment"  
alembic upgrade head
3) пре коммит хуки выключить / включить  
pre-commit uninstall / install
4) проверка redis  
docker exec -it redis sh  
redis-cli  
AUTH *******  
keys *  
5) проверка elk  
http://localhost:9200/_cat/indices?v  
http://localhost:5044/  
http://localhost:5601/app/home/  
