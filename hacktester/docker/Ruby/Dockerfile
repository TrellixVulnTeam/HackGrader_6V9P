FROM python
MAINTAINER radorado@hackbulgaria.com

USER root

#install ruby2.3-dev and rubocop
RUN apt-add-repository ppa:brightbox/ruby-ng && apt-get update && apt-get install -y ruby2.3 ruby2.3-dev && gem install rake && gem install minitest && gem install rubocop

RUN ruby --version

RUN apt-get clean

USER grader
