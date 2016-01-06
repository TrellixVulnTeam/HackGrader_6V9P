# Simple Code Tester with Django and Celery

## How to run

1. [Install RabbitMQ](https://www.rabbitmq.com/install-debian.html) - `$ sudo apt-get install rabbitmq-server`
2. Install all pip requiremetns: `$ pip install -r requirements.txt`
3. Build Docker image:

```
$ cd docker
$ docker build -t grader .
```

4. Run Django
5. Run Celery: `$ celery -A HackTester worker -B -E --loglevel=info` where `HackTester` is the main Django app.

## Celery readings

* https://www.reddit.com/r/django/comments/1wx587/how_do_i_return_the_result_of_a_celery_task_to/
* http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html
* https://github.com/mikeumus/django-celery-example
* http://stackoverflow.com/questions/20164688/celery-and-django-simple-examplehttp://stackoverflow.com/questions/20164688/celery-and-django-simple-example
* https://realpython.com/blog/python/asynchronous-tasks-with-django-and-celery/

## Docker readings

* <https://coderwall.com/p/ewk0mq/stop-remove-all-docker-containers>
* <http://stackoverflow.com/questions/22907231/copying-files-from-host-to-docker-container>
* <https://docs.docker.com/mac/step_four/>
* <https://docs.docker.com/engine/articles/dockerfile_best-practices/>
