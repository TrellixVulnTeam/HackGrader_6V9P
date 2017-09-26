FROM grader
MAINTAINER radorado@hackbulgaria.com

RUN add-apt-repository ppa:openjdk-r/ppa && apt-get update && apt-get install -y openjdk-8-jdk

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME

RUN java -version
