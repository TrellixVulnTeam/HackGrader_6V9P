FROM grader
MAINTAINER radorado@hackbulgaria.com

# install python3.5 flake8 and pip
RUN sudo add-apt-repository ppa:fkrull/deadsnakes && sudo apt-get update && sudo apt-get install -y python3.5 && curl -O https://bootstrap.pypa.io/get-pip.py && python3.5 get-pip.py && pip -V && pip install flake8

RUN python3.5 --version 
