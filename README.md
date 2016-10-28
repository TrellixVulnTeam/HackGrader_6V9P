# Code Tester with Django & Celery

## Requirements

This project uses the following technologies:

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

**After this:**

1. Run Django migrations.
2. Create superuser for admin.
3. Create API User from command: `$ python manage.py create_api_user education.hackbulgaria.com` - here, the URL should be the website that is going to make requests to the grader.
4. Take API key and API secret and give them to the client.
5. Add the initial data needed to run the grader to the database: `$ python manage.py provision_initial_data`
6. Run Django.
7. Run Celery: `$ celery -A HackTester worker -B -E --loglevel=info` where `HackTester` is the main Django app.

## Management commands

### Docker

Check if there are any running docker containers:

```
$ docker ps
```

Check all docker containers:

```
$ docker ps -a
```

To kill all docker containers:

```
$ docker rm $(docker ps -aq)
```

### Celery

Check for currently running tasks:

```
$ celery -A HackTester inspect active
```

Terminate running tasks:

```
$ celery -A HackTester purge
```
