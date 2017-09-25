FROM grader
MAINTAINER radorado@hackbulgaria.com

RUN apt-get clean

RUN useradd -m -p grader grader && chsh -s /bin/bash grader | adduser grader sudo && usermod -u 1002 grader

USER grader
