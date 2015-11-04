#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="NagMe",
    version="0.1",
    description="Simple Notification Center nagger for OSX 10.8+",
    author="Sam Fries",
    author_email="fries2@llnl.gov",
    packages=find_packages(),
    scripts=["scripts/nagupdate", "scripts/nagme", "scripts/nagfreq"],
    install_requires=["python-dateutil", "pync"]
)

# Post install
import os
import shutil

user_home = os.path.expanduser("~")

# Install the addnag service
addnag = user_home + "/Library/Services/addnag.workflow"
if os.path.exists(addnag):
    print "Removing existing addnag workflow"
    shutil.rmtree(addnag)
print "Installing new addnag workflow"
shutil.copytree("scripts/addnag.workflow", user_home + "/Library/Services/addnag.workflow")

# Check if a launchd job exists already
if not os.path.exists(user_home + "/Library/LaunchAgents/com.nagme.donag.plist"):
    import nag
    print "Creating launchd script to run every 15 minutes"
    nag.create_launchd_script(60 * 15)
else:
    print "launchd script already exists; leaving in place."
