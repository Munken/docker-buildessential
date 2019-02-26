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

class debian_clang_template:

    @staticmethod
    def substitute(dist, tag, compiler):
        template = Template(\
        """FROM buildpack-deps:jessie

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


cc7_template = Template(
    """FROM $dist:$tag

RUN rpm --rebuilddb && yum -y install yum-plugin-ovl \
    && yum install -y git bison flex ncurses-devel make perl-Digest-MD5 gcc-c++
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
      make $compiler cpp perl which
"""    
)

distros = [
    Distro("debian", ["buster", "stretch", "wheezy", "jessie"],
           ["clang", "gcc"], debian_template),
    Distro("munken/debian", ["etch"],
           ["gcc"], debian_template, "debian"),
    Distro("debian", ["jessie"],
           ["clang-3.6", "clang-3.7", "clang-3.8", "clang-3.9", "clang-4.0",
            "clang-5.0", "clang-6.0", "clang-7", "clang-8"
           ],
           debian_clang_template),    
    Distro("ubuntu", ["trusty", "xenial", "bionic", "cosmic", "disco"],
           ["clang", "gcc"], debian_template),
    Distro("daald/ubuntu32", ["trusty"],
           ["clang", "gcc"], debian_template, "ubuntu32"),
    Distro("cern/cc7-base", ["latest"],
           ["gcc"], cc7_template, "cc7"),
    Distro("cern/slc6-base", ["latest"],
           ["gcc"], slc6_template, "slc6"),
    Distro("opensuse", ["latest"],
           ["gcc-c++", "clang"], opensuse_template),    
]


basedir = sys.argv[1] if len(sys.argv) == 2 else "."


for d in distros:
    i = d.baseimage
    for t in d.tag:
        for c in d.compiler:
            image_dir = d.dir if d.dir is not None else i
            path = "{}/{}/{}/{}".format(basedir,image_dir,t,c)
            print path
            try:
                os.makedirs(path)
            except OSError:
                pass
            
            with open("{}/Dockerfile".format(path), "w") as f:
                s = d.template.substitute(dist=i, tag=t, compiler=c)
                f.write(s)
            
