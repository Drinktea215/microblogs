## Корпоративный сервис микроблогов
### ТЕСТИРОВАНИЕ ПРОЕКТА
Чтобы протестировать проект необходимо выполнить несколько шагов:
#### 1. Развернуть тестовые базы данных (postgtresql + redis)
Для этого выполните команду: ```docker-compose -f docker-compose-dev.yaml up --build -d```

#### 2. Установить зависимости
Для этого выполните команду: ```pip install -r requirements.txt```

#### 3. Рабочий каталог
Так как рабочим каталогом проекта является директория "src" - нужно перейти в нее.
Для этого выполните команду: ```cd src```

#### 4. Запуск тестирования
Для этого выполните команду: ```pytest ../tests```

### РАБОТА ПРОЕКТА

Для запуска проекта выполните команду:
`docker-compose -f docker-compose-ci.yaml up --build`

Бэкенд принимает несколько запросов:

#### 1. Создать твит
```
POST /api/tweets
    HTTP-Params:
    api-key: str
{
    “tweet_data”: string
    “tweet_media_ids”: Array[int] // Опциональный параметр. Загрузка картинок происходит по endpoint /api/media. Фронтенд подгрузит картинки туда автоматически при отправке твита и подставит id оттуда в json. Если твит не содержит изображений - список будет пустым.
}
```
В ответ вернется id созданного твита.
```
{  
    “result”: true,  
    “tweet_id”: int  
}
```
#### 2. Загрузка файлов из твита.
Загрузка происходит через отправку формы.
```
POST /api/medias
    HTTP-Params:
    api-key: str
    form: file=”image.jpg”
```
В ответ должен вернуться id загруженного файла.
```
{
    “result”: true,
    “media_id”: int
}
```
#### 3. Удалить твит
```
DELETE /api/tweets/<id>
    HTTP-Params:
    api-key: str
```
В ответ должно вернуться сообщение о статусе операции.
```
{
    “result”: true
}
```
#### 4. Добавить твиту "лайк".
```
POST /api/tweets/<id>/likes
    HTTP-Params:
    api-key: str
```
В ответ должно вернуться сообщение о статусе операции.
```
{
    “result”: true
}
```
#### 5. Удалить "лайк".
```
DELETE /api/tweets/<id>/likes
    HTTP-Params:
    api-key: str
```
В ответ должно вернуться сообщение о статусе операции.
```
{
    “result”: true
}
```
#### 6. Зафоловить другого пользователя.
```
POST /api/users/<id>/follow
    HTTP-Params:
    api-key: str
```
В ответ должно вернуться сообщение о статусе операции.
```
{
    “result”: true
}
```
#### 7. Убрать подписку на другого пользователя.
```
DELETE /api/users/<id>/follow
    HTTP-Params:
    api-key: str
```
В ответ должно вернуться сообщение о статусе операции.
```
{
    “result”: true
}
```
#### 8. Получить ленту с твитами.
```
GET /api/tweets
    HTTP-Params:
    api-key: str
```
В ответ должен вернуться json со списком твитов для ленты этого пользователя.
```
{
    “result”: true,
    "tweets": [
        {
            "id": int,
            "content": string,
            "attachments" [
                link_1, // relative?
                link_2,
                ...
            ]
            "author": {
                "id": int
                "name": string
            }
            “likes”: [
            {
                “user_id”: int,
                “name”: string}
            ]
        },
        ...,
    ]
}
```
#### 9. Получить информацию о своём профиле.
```
GET /api/users/me
    HTTP-Params:
    api-key: str
```
В ответ получаем:
```
{
    "result":"true",
    "user":{
        "id":"int",
        "name":"str",
        "followers":[{
            "id":"int",
            "name":"str"
        }
        ],
        "following":[
        {
            "id":"int",
            "name":"str"
        }
        ]
    }
}
```
#### 10. Получить информацию о произвольном профиле по его id.
```
GET /api/users/<id>
```
В ответ получаем:
```
{
    "result":"true",
    "user":{
        "id":"int",
        "name":"str",
        "followers":[
        {
            "id":"int",
            "name":"str"
        }
        ],
        "following":[
        {
            "id":"int",
            "name":"str"
        }
        ]
    }
}
```

#### В случае любой ошибки на стороне бэкенда возвращается сообщение следующего формата:
```
{
    “result”: false,
    “error_type”: str,
    “error_message”: str
}
```