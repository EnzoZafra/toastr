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

envitonments = {
    "python2": "Dockerfile-python2",
    "python3": "Dockerfile-python3",
    "gcc": "Dockerfile-gcc",
    "g++": "Dockerfile-g++",
    "java": "Dockerfile-java",
    "ruby": "Dockerfile-ruby",
    "rust": "Dockerfile-rust",
}


def parse(input_path: str, content_file_name="contents.out"):
    """Parse the environment to run in and file contents from an input text file."""
    with open(input_path) as input_txt, open(content_file_name, "w+") as contents:
        environment = input_txt.readline().strip()
        contents.write(input_txt.read())

    return environment, content_file_name


def spawn(environment, input):
    """Lauch a  docker enviroment."""
    # TODO: Start the docker file based on the specified inviroment

