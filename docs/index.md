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

**After this:**

1. Run Django migrations.
2. Create superuser for admin.
3. Create API User from command: `$ python manage.py create_api_user education.hackbulgaria.com` - here, the URL should be the website that is going to make requests to the grader.
4. Take API key and API secret and give them to the client.
5. Add the initial data needed to run the grader to the database: `$ python manage.py provision_initial_data`
6. Run Django.
7. Run Celery: `$ celery -A hacktester worker -B -E --loglevel=info` .

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

## Communication data formats

### Format of the data sent to /grade

##### for unittest:

    {
    "test_type": "unittest",
    "language": language,   # currently supported {java, python, ruby, javascript/nodejs}
    "file_type": file_type, # plain or binary
    "code": code, # plain text or base_64 format
    "test": test_code, # plain text or base_64 format
    "extra_options": {
        'qualified_class_name': 'com.hackbulgaria.grader.Tests', # for java binary solutions
        'time_limit': number # set time limit for the test suite in seconds
    }}

#### Format of the **code** and **test** data for `JavaScript`

* Functions in `code` must be exported (e.g., module.exports = function() { };)
* Test functions must require the function from `code` in the **solution** file (e.g., var testedFunc = require('solution'))
* Use `describe` or `it`



##### for output_checking:

    {
    "test_type": "output_checking",
    "language": language,   # currently supported {java, python, ruby}
    "file_type": "plain",   # only plain are supported
    "code": code, # plain text or base_64 format
    "test": archive, # base_64 format
    "extra_options": {
        "archive_type": "tar_gz",
        "class_name": class_name # name of the class containing the main method for java
        "time_limit": number # set time limit for the test suite in seconds
    }}

### Archive

sample code for creating a .tar.gz archive with all the files in the current directory:


    def create_tar_gz_archive():
        test_files = os.listdir()
        with tarfile.open(name="archive.tar.gz", mode="w:gz") as tar:
            for file in test_files:
                tar.add(file)
        return tar.name

The test file names should be in format test\_number.in, test_number.out
Example:

 1.in the first input file that should be given to the program

 1.out the expected output after running solution with the given input(1.in)


### Format of the data returned by /check_result

for unittests:

    {
    'run_status': run.status,  # the status of the test run
    'result_status': result.status, # the status of the test result
    'run_id': run.id,
    'output': {"test_status": test_status,  # the status of the result ("OK", "compilation_error" etc..)
               "test_output": result.output} # the output of the result
    }


for output_checking:

    {
    'run_status': run.status,  # the status of the test run
    'result_status': result.status, # the status of the test result
    'run_id': run.id,
    'output': [{"test_status": test_status,
                "test_output": result.output},] # the list contains results for for each .in .out pair of tests
    }