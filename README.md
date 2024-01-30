# Prosept

Бэкенд приложение для  "Просепт" команды №13.

На текущий момент позволяет пользователям:

- загружать в базу данных информацию о дилерах, товарах производителя и товарах дилеров через удобный загрузчик;
- получать полный список всех товаров поставщика;
- получать список дилеров, а также id дилера в базе данных по его наименованию;
- получать список товаров дилеров, отфильтрованный по дате, дилеру или статусу (имеет установленное соответствие с товаром поставщика или еще нет);
- получать статистику по дилерам - какое количество товаров поставщика заведено в матрицу клиента и какое количество из них имеет установленное соответствие с товаром поставщика;
- создавать новый объект связи между товаром дилера и товаром поставщика.


## Стек технологий

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker

## Зависимости

- Перечислены в файле prosept/requirements.txt

## Документация и архив приложения

Могут быть найдены [здесь](https://drive.google.com/drive/folders/1eP4sx6kz2HKwijyl4_u1GobqCC5bGRhZ?usp=drive_link).

## Для запуска на собственном сервере

1. Установите на сервере `docker` и `docker compose`;
2. Склонируйте себе репозиторий:
   `git clone git@github.com:zhukov1414/prosept.git`
3. Перейдите в созданную папку:
   `cd prosept`
4. Создайте в корне проекта файл `.env`;
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
DB_HOST=db
DB_PORT=<порт_базы_данных>
```

5. Из корневой директории выполните команду `docker compose up -d --build`;

После запуска контейнеров для того, чтобы наполнить базу данных, последовательно выполните команды (возможно потребуется прописать sudo)

```bash
docker compose exec backend python src/core/loader.py products src/data/marketing_product.csv
docker compose exec backend python src/core/loader.py dealers src/data/marketing_dealer.csv
docker compose exec backend python src/core/loader.py dealerprices src/data/marketing_dealerprice.csv
docker compose exec backend python src/core/loader.py productdealers src/data/marketing_productdealerkey.csv
```

6. После этого Вам должна быть доступна страница с документацией http://localhost:8000/docs/.
7. Для запуска тестов выполните в консоли команду `docker compose run -e DEBUG=true backend pytest -v`

В данной версии приложения, безопасность реализована рудиментарно: Вы можете получить JWT token обратившись по адресу /api/auth/jwt/login, но все эндпоинты доступны для всех желающих, без авторизации. Это можно изменить добавив параметр `dependencies=[Depends(current_superuser)]` в корневой роутер, один из промежуточных роутеров или в любой из path декораторов, например, `@router.get("/", response_model=list[DealerDb], dependencies=[Depends(current_superuser)], tags=["Main"])`.

Приложение полностью асинхронное (используются как асинхронные  запросы, так и асинхронный драйвер базы данных), запускается в двух процессах, по одному на каждое физическое ядро процессора и потому отличается быстродействием.

Помимо этого можно включить (раскоментировав строчку # await scheduler() в функции lifespan в файле main.py) автоматический расчет предсказаний для товаров дилеров по расписанию ежедневно в 06:00. В данный момент функция отключена, т.к. требует для работы как минимум 3 Гб свободной оперативной памяти.

## Авторы

- [Костенко Станислав](https://github.com/kubanez-create)
- [Жуков Евгений](https://github.com/zhukov1414)
