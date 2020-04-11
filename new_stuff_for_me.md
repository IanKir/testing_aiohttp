### Something new for me

New commands:
* docker run --name dbserver -p 5432:5432 -e POSTGRES_PASSWORD=testuser -d postgres
* docker exec -it dbserver psql -U postgres
    * \\d - Показать все таблицы в БД (__только Postgres!__)

By default устанавливается db - postgres, username - postgres
Пароли конечно стоит хранить в отдельном не отслеживаемом файле, но
в качестве теста можно и так.
    