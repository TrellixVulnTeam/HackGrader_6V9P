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

ENV RUBY_MAJOR 2.3
ENV RUBY_VERSION 2.3.0

# Set $PATH so that non-login shells will see the Ruby binaries
ENV PATH $PATH:/opt/rubies/ruby-$RUBY_VERSION/bin

# Install MRI Ruby $RUBY_VERSION
RUN curl -O http://ftp.ruby-lang.org/pub/ruby/$RUBY_MAJOR/ruby-$RUBY_VERSION.tar.gz && \
    tar -zxvf ruby-$RUBY_VERSION.tar.gz && \
    cd ruby-$RUBY_VERSION && \
    ./configure --disable-install-doc && \
    make && \
    make install && \
    cd .. && \
    rm -r ruby-$RUBY_VERSION ruby-$RUBY_VERSION.tar.gz && \
    echo 'gem: --no-document' > /usr/local/etc/gemrc

# ==============================================================================
# Rubygems and Bundler
# ==============================================================================

ENV RUBYGEMS_MAJOR 2.6
ENV RUBYGEMS_VERSION 2.6.1

# Install rubygems and bundler
ADD http://production.cf.rubygems.org/rubygems/rubygems-$RUBYGEMS_VERSION.tgz /tmp/
RUN cd /tmp && \
    tar -zxf /tmp/rubygems-$RUBYGEMS_VERSION.tgz && \
    cd /tmp/rubygems-$RUBYGEMS_VERSION && \
    ruby setup.rb && \
    /bin/bash -l -c 'gem install bundler --no-rdoc --no-ri' && \
    echo "gem: --no-ri --no-rdoc" > ~/.gemrc
