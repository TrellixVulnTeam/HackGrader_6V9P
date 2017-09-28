FROM python
MAINTAINER radorado@hackbulgaria.com

USER root

#install nodejs and mocha,chai and sinon test tools
RUN curl -sL https://deb.nodesource.com/setup_7.x | sudo -E bash -
RUN apt-get install -y nodejs && npm install -g mocha \
						chai \
						sinon

RUN node -v

RUN apt-get clean

USER grader
