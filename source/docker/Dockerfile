FROM ubuntu:14.04
MAINTAINER radorado@hackbulgaria.com

RUN apt-get update && apt-get install -y git python-software-properties build-essential curl sudo
RUN apt-get install -y curl patch gawk g++ gcc make libc6-dev patch libreadline6-dev zlib1g-dev libssl-dev libyaml-dev libsqlite3-dev sqlite3 autoconf libgdbm-dev libncurses5-dev automake libtool bison pkg-config libffi-dev

# Install Java.
RUN \
  apt-get update && \
  apt-get install -y openjdk-7-jdk && \
  rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME /usr/lib/jvm/java-7-openjdk-amd64

RUN apt-get clean

RUN useradd -m -p grader grader && chsh -s /bin/bash grader | adduser grader sudo

USER grader
