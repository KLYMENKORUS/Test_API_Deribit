<h1>Тестовое задание на позицию junior back-end разработчика</h1>
  <h2>Задание</h2>
<ol>
  <li>Написать для криптобиржи Deribit асинхронный клиент на aiohhtp.</li>
    <ul>
      <li>Клиент должен каждую минуту забирать с биржи текущую цену BTC и ETH, после
        чего сохранять в базу данных тикер валюты, текущую цену и время в UNIX.</li>
    </ul>
  <li>Написать внешнее API для обработки сохраненных данных на FastAPI.</li>
    Должны быть следующие методы:
    <ul>
      <li>Получение всех сохраненных данных по указанной валюте</li>
      <li>Получение последней цены валюты</li>
      <li>Получение цены валюты с фильтром по дате</li>
      Все методы должны быть GET и у каждого метода дожен быть обязятельный query-
        параметр "ticker".
      Вместо pydantic-моделей желательно использовать dataclass-модели.
    </ul>
  <li>Написать тесты для клиента</li>
    <ul>
      <li>Написать простой тест на метод получения данных с биржи.</li>
    </ul>
</ol>
  <h2>Технологии</h2>
  <div>
    <img src="https://img.shields.io/badge/Python-blue?style=for-the-badge&logo=python&logoColor=white&color=9cf" alt="Postgresql Badge"/>
    <img src="https://img.shields.io/badge/FastAPI-blue?style=for-the-badge&logo=fastapi&logoColor=white&color=brightgreen" alt="FastAPI Badge"/>
    <img src="https://img.shields.io/badge/Postgres-green?style=for-the-badge&logo=postgresql&logoColor=white&color=informational" alt="Postgresql Badge"/>
    <img src="https://img.shields.io/badge/Docker-blue?style=for-the-badge&logo=docker&logoColor=white&color=blue" alt="Docker Badge"/>
    <img src="https://img.shields.io/badge/Pytest-blue?style=for-the-badge&logo=pytest&logoColor=white&color=brightgreen" alt="Pytest Badge"/>
    <img src="https://img.shields.io/badge/Alembic-blue?style=for-the-badge&logo=alembict&logoColor=white&color=red" alt="Pytest Badge"/>
  </div>
  <h2>Запуск проекта</h2>
  <ul>
  <li>Скачать и установить <a href='https://docs.docker.com/get-docker/'>Docker</a></li>
  <li>Клонировать репозиторий: <code> git clone https://github.com/KLYMENKORUS/Test_API_Deribit</code></li>
  <li>Установить зависимости: <code>pip install -r requirements.txt</code></li>
  <li>На уровне с корневой директорией <code>src</code> создать файл .env и заполнить его по примеру .env.example</li>
  <li>Выполнить команду <code>docker compose -f docker-compose.yaml up -d</code></li>
  <li>Выполнить команду <code>alembic upgrade head</code></li>
  <li>Запустить тесты <code>pytest tests</code></li>
  <li>Запустить файлы: <code>main.py</code>, <code>utils.py</code></li>
  </ul>
