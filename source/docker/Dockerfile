FROM ubuntu:14.04
MAINTAINER radorado@hackbulgaria.com

RUN useradd -p grader grader && chsh -s /bin/bash grader
RUN apt-get update && apt-get install -y ruby ruby-dev make
RUN gem install minitest
