# Prosept

Бэкенд приложение для  "Просепт" команды №13.

На текущий момент позволяет пользователям:

- загружать в базу данных информацию о дилерах, товарах производителя и товарах дилеров через удобный загрузчик;
- получать полный список всех товаров поставщика;
- получать список дилеров, а также id дилера в базе данных по его наименованию;
- получать список товаров дилеров, отфильтрованный по дате, дилеру или статусу (имеет установленное соответствие с товаром поставщика или еще нет);
- получать статистику по дилерам - какое количество товаров поставщика заведено в матрицу клиента и какое количество из них имеет установленное соответствие с товаром поставщика;
- создавать новый объект связи между товаром дилера и товаром поставщика.

Помимо этого в автоматическом режиме ежедневно в 06:00 предсказательной моделью генерируются предсказания по соответствию товаров дилеров и товаров поставщика.

## Стек технологий

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker

## Зависимости

- Перечислены в файле prosept/requirements.txt

## Для запуска на собственном сервере

1. Установите на сервере `docker` и `docker compose`;
2. Склонируйте себе репозиторий:
   `git clone git@github.com:kubanez-create/prosept.git`
3. Перейдите в созданную папку:
   `cd prosept`
4. Создайте в корне проекта файл `.prod.env`;
   Внесите в данный файл переменные окружения:

```bash
APP_TITLE=<название_Вашего_приложения>
DATABASE_URL=<postgresql+asyncpg://postgres:postgres@db:5432/postgres>
SECRET=<Ваш_секретный_ключ>
FIRST_SUPERUSER_EMAIL=<адрес_электронной_почты>
FIRST_SUPERUSER_PASSWORD=<произвольный_пароль>
POSTGRES_DB=<произвольное_имя_базы_данных>
POSTGRES_USER=<имя_пользователя_базы_данных>
POSTGRES_PASSWORD=<пароль_к_базе_данных>
DB_HOST=<хост_базы_данных>
DB_PORT=<порт_базы_данных>
```

5. Из корневой директории выполните команду `docker compose up -d --build`;
   После запуска контейнера последовательно выполните команды (возможно потребуется прописать sudo)

```bash
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py createsuperuser
docker compose exec backend python manage.py collectstatic --no-input
docker compose exec backend python manage.py loadcsv product /app/data/pr_df.csv
docker compose exec backend python manage.py loadcsv shop /app/data/st_df.csv
docker compose exec backend python manage.py loadcsv sales /app/data/sales_2_st.csv
docker compose exec backend python manage.py loadcsv forecasts /app/data/predictions_2_st.csv
```

6. После этого Вам должна быть доступна страница с документацией http://localhost:8000/docs/.

Получить токен можно как в swagger через обращение к /api/v1/auth/token/login, так и в админке в разделе Токенs.
Чтобы авторизоваться в swagger вставьте в поле Authorize
**token some_numbers_and_letters_your_token_consists_of** (cлово "token", затем пробел и значение токена).

## Авторы

- [Костенко Станислав](https://github.com/kubanez-create)
- [Жуков Евгений](https://github.com/zhukov1414)
