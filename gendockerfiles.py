#!/usr/bin/env python

from collections import namedtuple
from string import Template
import os
import sys

Distro = namedtuple("Distro", ["baseimage", "tag", "compiler", "template", "dir"])
Distro.__new__.__defaults__ = (None,) * len(Distro._fields)

debian_template = Template(
"""FROM $dist:$tag

RUN apt-get update -y \
    && apt-get install -y \
    bc \
    bison \
    build-essential \
    curl \
    flex \
    $compiler \
    libncurses5-dev \
    python-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*
"""    
)

wheezy_template = Template(
    """FROM philcryer/min-wheezy
RUN echo "deb http://archive.debian.org/debian wheezy main" > /etc/apt/sources.list 
RUN apt-get update -y \
    && apt-get install -y \
    bc \
    bison \
    build-essential \
    curl \
    flex \
    $compiler \
    libncurses5-dev \
    python-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*
"""    
)

class debian_clang_template:

    @staticmethod
    def substitute(dist, tag, compiler):
        template = Template(\
        """FROM buildpack-deps:jessie

        #https://unix.stackexchange.com/a/508948
RUN echo "deb [check-valid-until=no] http://cdn-fastly.deb.debian.org/debian jessie main" > /etc/apt/sources.list.d/jessie.list
RUN echo "deb [check-valid-until=no] http://archive.debian.org/debian jessie-backports main" > /etc/apt/sources.list.d/jessie-backports.list
RUN sed -i '/deb http:\/\/deb.debian.org\/debian jessie-updates main/d' /etc/apt/sources.list
RUN echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf        
RUN apt-get update
        
RUN echo 'deb http://apt.llvm.org/jessie/ llvm-toolchain-jessie-$version main' >> /etc/apt/sources.list \
        && wget -O - http://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add - \
        && apt-get update \
        && apt-get install -y \
        bc \
        bison \
        build-essential \
        curl \
        flex \
        $compiler \
        libncurses5-dev \
        python-dev \
        wget \
        && rm -rf /var/lib/apt/lists/*
        """)                   
        
        j = compiler.rfind("-")
        v = compiler[j+1:]
        return template.substitute(version=v, compiler=compiler)

class debian_stretch_clang_template:

    @staticmethod
    def substitute(dist, tag, compiler):
        template = Template(\
                            """FROM buildpack-deps:stretch

RUN echo 'deb http://apt.llvm.org/stretch/ llvm-toolchain-stretch-$version main' >> /etc/apt/sources.list \
        && wget -O - http://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add - \
        && apt-get update \
        && apt-get install -y \
        bc \
        bison \
        build-essential \
        curl \
        flex \
        $compiler \
        libncurses5-dev \
        python-dev \
        wget \
        && rm -rf /var/lib/apt/lists/*
        """)                   
        
        j = compiler.rfind("-")
        v = compiler[j+1:]
        return template.substitute(version=v, compiler=compiler)    


cc7_template = Template(
    """FROM $dist:$tag

RUN rpm --rebuilddb && yum -y install yum-plugin-ovl \
    && yum install -y git bison flex ncurses-devel make perl-Digest-MD5 gcc-c++ gcc $compiler
"""    
)

slc6_template = Template(
    """FROM $dist:$tag

RUN rpm --rebuilddb \
    && yum -y install yum-plugin-ovl  \
    && yum install -y sl-release-scl \
    && yum install -y \
    binutils \
    bison \
    cmake \
    curl \
    devtoolset-4-gcc-c++ \
    flex \
    git \
    ncurses-devel \
    perl-Digest-MD5 \
    python27 \
    && yum clean all
"""    
)

opensuse_template = Template(
    """FROM $dist:$tag

RUN zypper --non-interactive install git bison flex ncurses-devel \
      make $compiler cpp perl which gcc gcc-c++ wget curl
"""    
)

rh_template = Template(
    """FROM $dist:$tag

RUN yum install -y \
    bison \
    clang\
    curl \    
    flex \
    gcc \
    make \
    perl \
    perl-Digest-MD5 \
    tar \
    which
"""    
)


distros = [
    Distro("debian", ["buster", "stretch", "jessie"],
           ["clang", "gcc"], debian_template),
    Distro("munken/debian", ["etch"],
           ["gcc"], debian_template, "debian"),
    Distro("philcryer/min-wheezy", ["wheezy"],
           ["gcc", "clang"], wheezy_template, "debian"),    
    Distro("debian", ["jessie"],
           ["clang-3.6", "clang-3.7", "clang-3.8", "clang-3.9", "clang-4.0",
            "clang-5.0", "clang-6.0", "clang-7", "clang-8"
           ],
           debian_clang_template),
    Distro("debian", ["stretch"],
           ["clang-4.0","clang-5.0", "clang-6.0", "clang-7", "clang-8"],
           debian_stretch_clang_template),        
    Distro("ubuntu", ["trusty", "xenial", "bionic", "cosmic", "disco"],
           ["clang", "gcc"], debian_template),
    Distro("munken/docker-ubuntu", ["zesty", "artful"],
           ["clang", "gcc"], debian_template, "ubuntu"),    
    Distro("daald/ubuntu32", ["trusty"],
           ["clang", "gcc"], debian_template, "ubuntu32"),
    Distro("cern/cc7-base", ["latest"],
           [("gcc-c++", "gcc"), "clang"], cc7_template, "cc7"),
    Distro("cern/slc6-base", ["latest"],
           ["gcc"], slc6_template, "slc6"),
    Distro("opensuse", ["latest"],
           ["gcc", "clang"], opensuse_template),
    Distro("centos", ["latest"],
           ["gcc", "clang"], rh_template),
    Distro("fedora", ["latest"],
           ["gcc", "clang"], rh_template),    
]


basedir = sys.argv[1] if len(sys.argv) == 2 else "."


for d in distros:
    i = d.baseimage
    for t in d.tag:
        for c in d.compiler:

            if isinstance(c, tuple):
                c_name = c[0]
                c_path = c[1]
            else:
                c_path = c_name = c           
            
            image_dir = d.dir if d.dir is not None else i
            path = "{}/{}/{}/{}".format(basedir,image_dir,t,c_path)
            print path
            try:
                os.makedirs(path)
            except OSError:
                pass
            
            with open("{}/Dockerfile".format(path), "w") as f:
                s = d.template.substitute(dist=i, tag=t, compiler=c_name)
                f.write(s)
            
