1) Накатывание миграций  
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
