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
$ celery -A hacktester inspect active
```

Terminate running tasks:

```
$ celery -A hacktester purge
```