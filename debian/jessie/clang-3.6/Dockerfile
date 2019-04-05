FROM buildpack-deps:jessie

        #https://unix.stackexchange.com/a/508948
RUN echo "deb [check-valid-until=no] http://cdn-fastly.deb.debian.org/debian jessie main" > /etc/apt/sources.list.d/jessie.list
RUN echo "deb [check-valid-until=no] http://archive.debian.org/debian jessie-backports main" > /etc/apt/sources.list.d/jessie-backports.list
RUN sed -i '/deb http:\/\/deb.debian.org\/debian jessie-updates main/d' /etc/apt/sources.list
RUN apt-get -o Acquire::Check-Valid-Until=false update
        
RUN echo 'deb http://apt.llvm.org/jessie/ llvm-toolchain-jessie-3.6 main' >> /etc/apt/sources.list         && wget -O - http://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add -         && apt-get update         && apt-get install -y         bc         bison         build-essential         curl         flex         clang-3.6         libncurses5-dev         python-dev         wget         && rm -rf /var/lib/apt/lists/*
        