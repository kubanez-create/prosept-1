# Prosept

<!-- Бэкенд приложение для прогнозирования спроса на продукцию собственного производства "Лента" команды №13  "Горячие подсолнухи". -->

На текущий момент позволяет авторизованным пользователям:

- фильтровать данные по магазину, группе товаров, категории товаров, подкатегории товаров, и задавать диапазон дат;
- просматривать и выгружать в файл excel прогноз продаж на продукцию собственного производства;
- просматривать фактические продажи, предсказанные продажи и точность прошлых прогнозов

Помимо этого в автоматическом режиме ежедневно раз в день генерируются свежие прогнозные значения продаж в разрезе
магазин/скю и сохраняются в базу данных.

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
