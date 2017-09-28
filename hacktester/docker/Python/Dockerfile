FROM grader
MAINTAINER radorado@hackbulgaria.com

# install python3.5 flake8 and pip
RUN add-apt-repository ppa:fkrull/deadsnakes && apt-get update && apt-get install -y python3.5 && curl -O https://bootstrap.pypa.io/get-pip.py && python3.5 get-pip.py && pip -V && pip install flake8

RUN python3.5 --version 

RUN apt-get clean

RUN useradd -m -p grader grader && chsh -s /bin/bash grader | adduser grader sudo && usermod -u 1002 grader

USER grader
