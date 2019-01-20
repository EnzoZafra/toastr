#######################################################################
#
# Utility for parsing input python text to runnable code.
#
# Notes:
#
# Usage:
#
#######################################################################
from typing import Dict
import subprocess
import os
import tempfile

environments = {
    "python2": "python2-docker-image",
    "python3": "python3-docker-image",
    "gcc": "gcc-docker-image",
    "g++": "g++-docker-image",
    "java": "java-docker-image",
    "ruby": "ruby-docker-image",
    "rust": "rust-docker-image",
}


def parse(input_path: str, content_file_name="contents.out"):
    """Parse the environment to run in and file contents from an input text file."""
    with open(input_path) as input_txt, open(content_file_name, "w+") as contents:
        environment = input_txt.readline().strip()
        contents.write(input_txt.read())

    return environment, content_file_name


def spawn(environment, input):
    """Lauch a  docker enviroment.
    
    Assume the docker image is built.
    """

    subprocess.run(["docker", "run", environments[environment]])
