FROM buildpack-deps:stretch

RUN echo 'deb http://apt.llvm.org/stretch/ llvm-toolchain-stretch-5.0 main' >> /etc/apt/sources.list         && wget -O - http://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add -         && apt-get update         && apt-get install -y         bc         bison         build-essential         curl         flex         clang-5.0         libncurses5-dev         python-dev         wget         && rm -rf /var/lib/apt/lists/*
        