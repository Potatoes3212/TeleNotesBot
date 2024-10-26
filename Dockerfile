#Начните с официального образа Python, который будет основой для образа приложения.
FROM python:3.11

#Укажите, что в дальнейшем команды запускаемые в контейнере, будут выполняться в директории /code.
#Инструкция создаст эту директорию внутри контейнера и мы поместим в неё файл requirements.txt и директорию app.
WORKDIR /code

#Скопируете файл с зависимостями из текущей директории в /code.
#Сначала копируйте только файл с зависимостями.
#Этот файл изменяется довольно редко, Docker ищет изменения при постройке образа и если не находит, то использует кэш, в котором хранятся предыдущие версии сборки образа.
COPY ./requirements.txt /code/requirements.txt

#Установите библиотеки перечисленные в файле с зависимостями.
#Опция --no-cache-dir указывает pip не сохранять загружаемые библиотеки на локальной машине для использования их в случае повторной загрузки. В контейнере, в случае пересборки этого шага, они всё равно будут удалены.
#Опция --no-cache-dir нужна только для pip, она никак не влияет на Docker или контейнеры.
#Опция --upgrade указывает pip обновить библиотеки, емли они уже установлены.
#Ка и в предыдущем шаге с копированием файла, этот шаг также будет использовать кэш Docker в случае отсутствия изменений.
#Использование кэша, особенно на этом шаге, позволит вам сэкономить кучу времени при повторной сборке образа, так как зависимости будут сохранены в кеше, а не загружаться и устанавливаться каждый раз.
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#Скопируйте директорию ./app внутрь директории /code (в контейнере).
#Так как в этой директории расположен код, который часто изменяется, то использование кэша на этом шаге будет наименее эффективно, а значит лучше поместить этот шаг ближе к концу Dockerfile, дабы не терять выгоду от оптимизации предыдущих шагов.
COPY . /code

#Укажите команду, запускающую сервер uvicorn.
#CMD принимает список строк, разделённых запятыми, но при выполнении объединит их через пробел, собрав из них одну команду, которую вы могли бы написать в терминале.
#Эта команда будет выполнена в текущей рабочей директории, а именно в директории /code, которая указана в команде WORKDIR /code.
#Так как команда выполняется внутри директории /code, в которую мы поместили папку ./app с приложением, то Uvicorn сможет найти и импортировать объект app из файла app.main.
EXPOSE 80
#CMD ["ls"]
CMD ["/bin/bash", "-c", "alembic upgrade head && python aiogram_run.py"]