## Django-Notes

### Description

Example RestApi with authorization using Django Rest Framework. Application allows users to create/view/delete private notes.
In addition you can filter/order/bookmark your notes.

### Technologies
* [Python] 3
* [Django]
* [django-rest-framework]
* [JWT] Auth

### Installation
In order to use this project, you need to setup the required python packages.

1. Create and activate a python virtual environment.

    ```shell
    $ virtualenv notesenv
    $ source notesenv/bin/activate
    ```

2. Clone this repository and cd into the new folder:

    ```shell
    (notesenv) $ git clone https://github.com/beautifulelen/notesapp.git
    (notesenv) $ cd notesapp
    ```

3. Install the python requirements:

    ```shell
    (notesenv) notesapp $ pip install -r requirements.txt
    ```

4. Setup the database (SQLite):

    ```shell
    (notesenv) notesapp $ python manage.py migrate --run-syncdb
    ```

5. Start the django development server:

    ```shell
    (notesenv) notesapp $ python manage.py runserver
    ```

6. Enjoy.

### Examples of API calls

#### Register a User

```shell
curl -X POST -H "Content-Type: application/json" \
-d '{"username":"helen","password":"12345678"}' \
http://localhost:8000/register/
```

#### Get Authentication Token

```shell
curl -X POST -H "Content-Type: application/json" \
-d '{"username":"helen","password":"12345678"}' \
http://localhost:8000/api-token-auth/
 
{"token":"token_here"}
```

#### Create a Note

```shell
curl -X POST -H 'Content-Type: application/json' \
-H 'Authorization: JWT token_here' \
 -d '{"content":"note content", "title": "Note title"}' \
http://localhost:8000/notes/ 
```

#### Get All Notes

```shell
curl -X GET -H 'Content-Type: application/json' \
-H 'Authorization: JWT token_here' \
http://localhost:8000/notes/
```

#### Get All Favorite Notes

```shell
curl -X GET -H 'Content-Type: application/json' \
-H 'Authorization: JWT token_here' \
http://localhost:8000/notes/?favorites=true
```

#### Update a Note / Make favorite

```shell
curl -X PUT -H 'Content-Type: application/json' \
-H 'Authorization: JWT token_here' \
-d '{"content":"some important note", "is_favorite":"True"}' \
http://localhost:8000/notes/1
```

#### Delete a Note

```shell
curl -X DELETE -H 'Content-Type: application/json' \
-H 'Authorization: JWT token_here' \
http://localhost:8000/notes/1 
```

#### Sorting notes on updating time ascending order

```shell
curl -X GET -H 'Content-Type: application/json' \
-H 'Authorization: JWT token_here' \
http://localhost:8000/notes/?sorting=updated_at
```

#### Sorting notes on updating time descending order

```shell
curl -X GET -H 'Content-Type: application/json' \
-H 'Authorization: JWT token_here' \
http://localhost:8000/notes/?sorting=-updated_at
```

#### Search on title and context of an note

```shell
curl -X GET -H 'Content-Type: application/json' \
-H 'Authorization: JWT token_here' \
http://localhost:8000/notes/?search='searching value hear'
```



[Python]: <https://www.python.org/>
[Django]: <https://www.djangoproject.com/>
[django-rest-framework]: <http://www.django-rest-framework.org/>
[JWT]: <https://jwt.io/introduction/>