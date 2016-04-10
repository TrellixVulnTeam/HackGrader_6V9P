FROM ubuntu:14.04
MAINTAINER radorado@hackbulgaria.com

RUN apt-get update && apt-get install -y git software-properties-common python-software-properties build-essential curl sudo
RUN apt-get install -y curl patch gawk g++ gcc make libc6-dev patch libreadline6-dev zlib1g-dev libssl-dev libyaml-dev libsqlite3-dev sqlite3 autoconf libgdbm-dev libncurses5-dev automake libtool bison pkg-config libffi-dev

RUN sudo add-apt-repository ppa:openjdk-r/ppa
RUN sudo apt-get update
RUN sudo apt-get install -y openjdk-8-jdk

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME

RUN java -version

RUN apt-get clean

RUN useradd -m -p grader grader && chsh -s /bin/bash grader | adduser grader sudo

USER grader
