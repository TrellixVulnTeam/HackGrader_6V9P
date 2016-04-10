FROM ubuntu:14.04
MAINTAINER radorado@hackbulgaria.com

RUN apt-get update && apt-get install -y git python-software-properties build-essential curl sudo
RUN apt-get install -y curl patch gawk g++ gcc make libc6-dev patch libreadline6-dev zlib1g-dev libssl-dev libyaml-dev libsqlite3-dev sqlite3 autoconf libgdbm-dev libncurses5-dev automake libtool bison pkg-config libffi-dev

# Install Java.
RUN sudo apt-get install openjdk-8-jdk
RUN sudo apt-get install openjdk-8-jre

RUN apt-get clean

RUN useradd -m -p grader grader && chsh -s /bin/bash grader | adduser grader sudo

USER grader

# keys.gnupg.net
RUN gpg --keyserver hkp://5.135.158.148 --recv-keys D39DC0E3

RUN /bin/bash -l -c "curl -L get.rvm.io | bash -s stable --ruby"
RUN /bin/bash -l -c "rvm install 2.2"
RUN /bin/bash -l -c "echo 'gem: --no-ri --no-rdoc' > ~/.gemrc"
RUN /bin/bash -l -c "gem install bundler --no-ri --no-rdoc"
RUN /bin/bash --login -c "rvm use 2.2"
