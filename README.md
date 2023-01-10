### Настройка окружения

Скачать poetry

```bash
pip3 install poetry
```

Дальше поставить зависимости:

```bash
make install_c_libs
make install
```
### Команды

#### Подготовка
* `make install` - установка библиотек
* `make init_dvc` - подготовка двс репозитория 
* `make download_weights` - скачать веса моделек

#### Запуск сервиса
* `make run` - запустить сервис. Можно с аргументом `APP_PORT`

#### Сборка образа
* `make build` - собрать образ. Можно с аргументами `DOCKER_TAG`, `DOCKER_IMAGE`

#### Статический анализ
* `make lint` - запуск линтеров

#### Тестирование
* `make run_unit_tests` - запуск юнит-тестов
* `make run_integration_tests` - запуск интеграционных тестов
* `make run_all_tests` - запуск всех тестов
* `make generate_coverage_report` - test-coverage

## Основные запросы:

#### 1. Получить все классы, которые модель может предсказать

###### Формат запроса 
```http request
GET planet/classes
```
###### Пример ответа

```http request
200 OK
```

```json5
{
  "classes": [ <all_classes> ],
}
```

#### 2. Предсказание одного из классов POST-запрос

###### Формат запроса
```http request
POST planet/predict/image

Content-Type: image/jpeg
<binary-code-of-jpeg-encoded-image-here>
```
###### Пример ответа

```http request
200 OK
```

```json5
{
  "result": [
    "road",
    "water"
  ]
}
```

#### 3. Предсказание вероятности POST-запрос

###### Формат запроса
```http request
POST planet/predict_proba/image

Content-Type: image/jpeg
<binary-code-of-jpeg-encoded-image-here>
```
###### Пример ответа

```http request
200 OK
```

```json5
{
  "result": [ <probs> ]
}
```


