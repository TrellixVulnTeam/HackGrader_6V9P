FROM grader
MAINTAINER radorado@hackbulgaria.com

RUN sudo add-apt-repository ppa:openjdk-r/ppa && sudo apt-get update && sudo apt-get install -y openjdk-8-jdk

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME

RUN java -version
