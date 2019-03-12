#!/usr/bin/env python

import fnmatch
import os
import docker

def glob_recursive(d, pattern):
    matches = []
    for root, dirnames, filenames in os.walk(d):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append((root, filename))
    return matches

base = "munken/build-essential"
dfiles = glob_recursive('.', "Dockerfile")
for path,_ in dfiles:
    
    # parts = f.split('/')
    last = path.split('/')[1:]
    last = "-".join(last)
    tag = base + ":" + last
    print tag

    try:
        docker.build(path=path, tag=tag)
        docker.push(tag)
    except:
        print "Failed to build and push {}".format(tag)
    
        
