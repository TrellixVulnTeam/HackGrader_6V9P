FROM ubuntu:14.04
MAINTAINER radorado@hackbulgaria.com

RUN useradd -M -p grader grader && chsh -s /bin/bash grader

