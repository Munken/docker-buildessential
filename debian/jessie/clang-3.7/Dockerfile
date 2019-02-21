FROM buildpack-deps:jessie

RUN echo 'deb http://apt.llvm.org/jessie/ llvm-toolchain-jessie-3.7 main' >> /etc/apt/sources.list         && wget -O - http://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add -         && apt-get update         && apt-get install -y         bc         bison         build-essential         curl         flex         clang-3.7         libncurses5-dev         python-dev         wget         && rm -rf /var/lib/apt/lists/*
        