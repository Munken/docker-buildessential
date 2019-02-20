FROM cern/slc6-base:latest

RUN rpm --rebuilddb     && yum -y install yum-plugin-ovl      && yum install -y sl-release-scl     && yum install -y     binutils     bison     cmake     curl     devtoolset-4-gcc-c++     flex     git     ncurses-devel     perl-Digest-MD5     python27     && yum clean all
