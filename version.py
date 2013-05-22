#!/usr/bin/python

# version number format: [closest git tag].[git changeset].[auto increment build number]
# portions that aren't needed are dropped
# git status -s must return nothing for the auto increment build number to drop
# suggested use: [major].[minor].[release].[build]
# use git tags for major.minor: eg 1.2

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

def gitClosestTag():
    return(check_output('git describe --abbrev=0 --tags'.split()).strip())

def gitShortHash():
    return(check_output("git log --pretty=format:'%h' -n 1".split()).strip())

def gitLongHash():
    return(check_output("git log --pretty=format:'%H' -n 1".split()).strip())

def gitLongHashNoThrow():
    try:
        return(gitLongHash())
    except subprocess.CalledProcessError:
        return("no-repo")

def gitDescribe():
    return(check_output('git describe'.split()).strip())

def makeAutoBuildNumber():

    os.chdir(gitRoot())

    fileName = ".version.build.info"

    try:
        buildInfo = pickle.load(open(fileName, "rb" ))
    except IOError:
            buildInfo = { "lastCommit" : gitLongHashNoThrow(), "buildNumber" : 0 }

    currentCommit = gitLongHashNoThrow()

    if(buildInfo["lastCommit"] == currentCommit):
        buildInfo["buildNumber"] += 1
    else:
        buildInfo["buildNumber"] = 1
        buildInfo["lastCommit"] = currentCommit

    pickle.dump(buildInfo, open(fileName, "wb" ))

    return(str(buildInfo["buildNumber"]))

def makeVersionNumber():
    try:
        versionNumber = gitClosestTag()
        
        # if the current commit is the tagged commit
        if(versionNumber == gitDescribe()):
            return(versionNumber)

    except subprocess.CalledProcessError:
        versionNumber = "0.0"

    versionNumber += "."

    try:
        versionNumber += gitShortHash()
    except subprocess.CalledProcessError:
        versionNumber += "no-changeset"

    if(gitDirty()):
        versionNumber += "." + makeAutoBuildNumber()

    print("'" + versionNumber + "'")

    return(versionNumber)

def main():
    print(makeVersionNumber())

main()
