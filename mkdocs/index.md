## Introduction

Code Tester(Grader) with `Django` & `Celery` for processing solutuons on `python`, `ruby`, `java` and `nodejs`.
Accepts different kinds of test and solution inputs and returns status of processed solution.

## Requirements

The following technologies are used:

* [RabbitMQ](https://www.rabbitmq.com/install-debian.html)
* [Celery](http://www.celeryproject.org/)
* [Docker](https://www.docker.com/)
* [Django](https://www.djangoproject.com/)

The grader uses HMAC based API Authentication. This means, you are going to need API keys to make requests.

## How to run

1. Install the needed requirements - RabbitMQ, Celery, Docker.
2. Install all pip requiremetns: `$ pip install -r requirements.txt`
3. Build Docker image:

```
$ cd docker
$ docker build -t grader .
```

Sanity check versions of Python, Ruby and Java:

**Python should be 3.5**

```
$ docker run grader /bin/bash --login -c "python3.5 --version"
```

**Ruby should be 2.3**

```
$ docker run grader /bin/bash --login -c "ruby --version"
```

**Java should be 1.8**

```
$ docker run grader /bin/bash --login -c "java -version"
```

**Run project:**

1. Run Django migrations.
2. Create superuser for admin.
3. Create API User from command: 
`$ python manage.py create_api_user <website-that-makes-request-to-the-grader>`
4. Take API key and API secret and give them to the client website.
5. Add the initial data needed to run the grader to the database: `$ python manage.py provision_initial_data`
6. Run Django with `$ python3 manage.py runserver`
7. Run Celery: `$ celery -A hacktester worker -B -E --loglevel=info`
