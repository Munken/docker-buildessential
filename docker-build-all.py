#!/usr/bin/env python

import fnmatch
import os
import subprocess
import shlex

def glob_recursive(d, pattern):
    matches = []
    for root, dirnames, filenames in os.walk(d):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append((root, filename))
    return matches

base = "munken/build-essential"
dfiles = glob_recursive('.', "Dockerfile")
failed = []
for path,_ in dfiles:
    
    # parts = f.split('/')
    last = path.split('/')[1:]
    last = "-".join(last)
    tag = base + ":" + last
    print tag

    cmd = "docker build {0} -t {1} && docker push {1}".format(path, tag)
    print cmd
    cmd = shlex.split(cmd)
    ret = subprocess.call(cmd)
    if ret:
        print "Failed to build and push {}".format(tag)
        failed.append(tag)

if len(failed) == 0:
    print "All images build and pushed"
else
    print "These images failed:"
    print failed
        
    
        
