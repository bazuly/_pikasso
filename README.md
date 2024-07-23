Bike Rental API *Test project
Этот проект предоставляет API для аренды велосипедов, включая функции регистрации пользователей, аренды велосипедов,
возврата велосипедов и просмотра истории аренды. Документация API доступна через Swagger.


Требования
Docker,
Docker Compose,
Для РФ можно использовать Podman или настроить зеркало в docker
Postman/CURL


Развертывание
Шаг 1: Клонирование репозитория
Клонируйте репозиторий на вашу локальную машину:
git clone https://github.com/ваш-username/bike-rental-api.git
cd pikasso

Шаг 2: Настройка окружения
Убедитесь, что у вас есть файл .env, для удобства не добавлял его в gitingore
Если есть желание, можно использовать свои переменные для postgresql 
Пример: 
POSTGRES_DB=имя_вашей_базы_данных
POSTGRES_USER=имя_пользователя
POSTGRES_PASSWORD=пароль
POSTGRES_HOST=db
POSTGRES_PORT=5432

Шаг 3: Запуск контейнеров Docker
Запустите контейнеры Docker с помощью Docker Compose:

Для docker:
docker-compose up --build

Для Podman:
podman-compose up --build

Шаг 5: Создание суперпользователя
Создайте суперпользователя для доступа к админ-панели Django:
docker-compose run web python manage.py createsuperuser

Шаг 6: Доступ к приложению
После успешного запуска контейнеров приложение будет доступно по адресу http://localhost:8000/api/

Шаг 7: Доступ к документации API
Документация API будет доступна по следующим URL:

Swagger UI: http://localhost:8000/swagger/
Redoc: http://localhost:8000/redoc/

Основные эндпоинты API
Регистрация пользователя: POST /register/
Получение токена: POST /token/
Обновление токена: POST /token/refresh/
Просмотр доступных велосипедов: GET /bikes/
Аренда велосипеда: POST /rent-bike/<bike_id>/
Возврат велосипеда: POST /return-bike/<rental_id>/
История аренды: GET /rental-history/

Тестирование
Чтобы запустить тесты, используйте следующую команду:

Примеры запросов и тестирования с помощью Postman.
Аналогично можно использовать документацию swagger.

<img width="1440" alt="Screenshot 2024-07-23 at 15 55 38" src="https://github.com/user-attachments/assets/3755b8b3-6540-4ab4-805c-f6df8c8e88b5">

<img width="1440" alt="Screenshot 2024-07-23 at 15 55 44" src="https://github.com/user-attachments/assets/d81090f1-cf27-4b61-9a9b-7e51369f4ecc">

<img width="1440" alt="Screenshot 2024-07-23 at 15 55 47" src="https://github.com/user-attachments/assets/830130c5-e1c2-4273-b024-8553afb26b7e">

<img width="1440" alt="Screenshot 2024-07-23 at 15 55 51" src="https://github.com/user-attachments/assets/18f6aa19-1600-4901-86dc-ad0a8b733be5">

<img width="1440" alt="Screenshot 2024-07-23 at 15 55 54" src="https://github.com/user-attachments/assets/82a7b6ec-4b48-4017-8d92-cda3b8580043">

<img width="1440" alt="Screenshot 2024-07-23 at 15 55 56" src="https://github.com/user-attachments/assets/19a4492c-d263-4130-8aa0-3b6e741e84f1">






