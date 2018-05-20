# redis-messages

Простая очередь сообщений, использующая Python 3.6 и Redis.

Копия приложения может быть и обработчиком сообщений или генератором, 
но в конкретный момент времени среди всех копий только одна может быть генератором.
Если генератор внезапно выключается - один из обработчиков становится генератором вместо него.
С вероятностью 5% сообщение будет помечено как ошибочное, и помещено в Redis с ключом 
'errors' 

Установка: 
```shell
git clone git@github.com:aseevlx/redis-messages.git
cd redis-messages
virtualenv --python=python3.6 venv
source venv/bin/activate
pip install -r requirements.txt
```
Redis можно легко поднять с помощью [Docker-контейнера](https://hub.docker.com/_/redis/)

Если нужно - изменяем хост, порт и базу данных в config.py

Запуск:
```shell
python run.py
```

Для тестирования функционала должно быть запущено минимум 2 копии приложения - генератор и обработчик.

Если запустить приложение с параметром '-getErrors', то оно выведет в терминал все сообщения с ошибками, 
удалит их из Redis и завершит свою работу.
```shell
python run.py -getErrors
``` 