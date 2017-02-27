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

#install rvm and ruby2.3.1
RUN  curl -#LO https://rvm.io/mpapis.asc
RUN  gpg --import mpapis.asc
RUN \curl -sSL https://get.rvm.io | bash -s stable
RUN echo "source /etc/profile.d/rvm.sh" >> /etc/bash.bashrc
RUN /bin/bash -c  "source /etc/profile.d/rvm.sh && rvm install ruby 2.3.1"

RUN curl -sL https://deb.nodesource.com/setup_7.x | sudo -E bash -
RUN sudo apt-get install -y nodejs
RUN node -v
RUN npm -v
RUN npm install -g mocha
RUN npm install -g chai

RUN apt-get clean

RUN useradd -m -p grader grader && chsh -s /bin/bash grader | adduser grader sudo
RUN usermod -a -G rvm grader

USER grader
