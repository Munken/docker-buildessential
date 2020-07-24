FROM philcryer/min-wheezy
RUN echo "deb http://archive.debian.org/debian wheezy main" > /etc/apt/sources.list
RUN apt-get update -y     && apt-get install -y     bc     bison     build-essential     curl     flex     clang     libncurses5-dev     python-dev     wget     && rm -rf /var/lib/apt/lists/*
