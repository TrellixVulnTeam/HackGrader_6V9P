FROM ubuntu:14.04
MAINTAINER radorado@hackbulgaria.com

RUN apt-get update && apt-get install -y git software-properties-common python-software-properties build-essential curl sudo
RUN apt-get install -y curl patch gawk g++ gcc make libc6-dev patch libreadline6-dev zlib1g-dev libssl-dev libyaml-dev libsqlite3-dev sqlite3 autoconf libgdbm-dev libncurses5-dev automake libtool bison pkg-config libffi-dev

RUN sudo add-apt-repository ppa:fkrull/deadsnakes
RUN sudo add-apt-repository ppa:openjdk-r/ppa

RUN sudo apt-get update

RUN sudo apt-get install -y openjdk-8-jdk
RUN sudo apt-get install -y python3.5

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME

RUN java -version

#install ruby2.3-dev and rubocop
RUN apt-add-repository ppa:brightbox/ruby-ng && apt-get update && apt-get install -y ruby2.3 ruby2.3-dev && gem install rake && gem install rubocop

#install nodejs and mocha,chai and sinon test tools
RUN curl -sL https://deb.nodesource.com/setup_7.x | sudo -E bash -
RUN sudo apt-get install -y nodejs && npm install -g mocha chai sinon

#install flake8
RUN apt-get update && apt-get install -y python3-pip python-dev && pip3 install flake8

#virtualenvs
RUN pip3 install virtualenv
RUN mkdir -p /virtualenvs
RUN virtualenv --python=python3.5 /virtualenvs/current
RUN /bin/bash -c "source /virtualenvs/current/bin/activate"

RUN apt-get clean

RUN useradd -m -p grader grader && chsh -s /bin/bash grader | adduser grader sudo

USER grader