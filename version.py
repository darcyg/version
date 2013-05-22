#!/usr/bin/python

# Copyright 2013 Sano Intelligence, Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import pickle
import subprocess
from subprocess import check_output

def gitDirty():
    output = check_output('git status -s'.split())
    return(output != "")

def gitRoot():
    return(check_output('git rev-parse --show-toplevel'.split()).strip())

def gitDescribe():
    return(check_output('git describe'.split(), stderr=subprocess.STDOUT).strip())

def gitClosestTag():
    onlyAnnotated = True

    if(onlyAnnotated):
        return(check_output('git describe --abbrev=0'.split(), stderr=subprocess.STDOUT).strip())
    else:
        return(check_output('git describe --abbrev=0 --tags'.split(), stderr=subprocess.STDOUT).strip())

def gitShortHash():
    return(check_output("git log --pretty=format:%h -n 1".split()).strip())

def gitLongHash():
    return(check_output("git log --pretty=format:%H -n 1".split()).strip())

def gitLongHashNoThrow():
    try:
        return(gitLongHash())
    except subprocess.CalledProcessError:
        return("no-repo")

def makeAutoBuildNumber():

    os.chdir(gitRoot())

    fileName = ".version.build.info"

    try:
        buildInfo = pickle.load(open(fileName, "rb" ))
    except IOError:
            buildInfo = { "lastCommit" : "no-repo-default", "buildNumber" : 0 }

    currentCommit = gitLongHashNoThrow()

    if(buildInfo["lastCommit"] == currentCommit):
        buildInfo["buildNumber"] += 1
    else:
        buildInfo["buildNumber"] = 0
        buildInfo["lastCommit"] = currentCommit

    pickle.dump(buildInfo, open(fileName, "wb" ))

    return(str(buildInfo["buildNumber"]))

def makeVersionNumber():

    isDirty = gitDirty()

    try:
        versionNumber = gitClosestTag()

        # if the current commit is the tagged commit
        if(versionNumber == gitDescribe() and not isDirty):
            return(versionNumber)

    except subprocess.CalledProcessError:
        versionNumber = "0.0"

    versionNumber += "."

    try:
        versionNumber += gitShortHash()
    except subprocess.CalledProcessError:
        versionNumber += "no-changeset"

    if(isDirty):
        versionNumber += '.dirty'
        versionNumber += "." + makeAutoBuildNumber()
 
    return(versionNumber)

def main():
    print(makeVersionNumber())

main()
