# Конвертер Валют

Этот проект представляет собой конвертер валют на Python, который позволяет конвертировать заданную сумму из одной валюты в другую, используя предопределенные курсы обмена ([`data/exchange_rates.csv`](data/exchange_rates.csv)). История всех выполненных конвертаций сохраняется в MongoDB.

## Структура Проекта

- [`src/currency_converter.py`](src/currency_converter.py): Содержит класс `CurrencyConverter` для выполнения логики конвертации валют.
- [`src/history_manager.py`](src/history_manager.py): Содержит класс `HistoryManager` для управления сохранением и загрузкой истории операций.
- [`src/main.py`](src/main.py): Главный исполняемый скрипт, демонстрирующий использование конвертера и менеджера истории.
- [`src/http_server.py`](src/http_server.py): Реализует HTTP-сервер для предоставления API конвертации валют.
- [`data/exchange_rates.csv`](data/exchange_rates.csv): CSV-файл с курсами обмена валют.
- [`data/operations.json`](data/operations.json): JSON-файл, используемый для хранения истории конвертаций.
- [`static/`](static/): Каталог со статическими файлами.
- [`tests/`](tests/): Каталог с тестами.

## Установка и Запуск

Для запуска проекта выполните следующие шаги:

1.  Убедитесь, что у вас установлен Docker.

2.  Скопируйте содержимое файла `.env.example` в новый файл с именем `.env`.

    ```bash
    cp .env.example .env
    ```

3.  Запустите приложение:

    ```bash
    docker compose up -d
    ```
