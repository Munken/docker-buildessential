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

distros = [
    Distro("debian", ["buster", "stretch", "wheezy", "jessie"],
           ["clang", "gcc"], debian_template),
    Distro("munken/debian", ["etch"],
           ["gcc"], debian_template, "debian"),
    Distro("ubuntu", ["trusty", "xenial", "bionic", "cosmic", "disco"],
           ["clang", "gcc"], debian_template),
    Distro("daald/ubuntu32", ["trusty"],
           ["clang", "gcc"], debian_template, "ubuntu32")
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
            
