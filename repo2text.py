#!/usr/bin/env python3

"""
Git2Text

Converts the contents of a Git repository into a text format.

(c) 2023 CCollective. Licensed under the GNU General Public License v3.0.
"""

import os
import sys
import fnmatch

def get_ignore_list(ignore_file_path):
    ignore_list = []
    with open(ignore_file_path, 'r') as ignore_file:
        for line in ignore_file:
            if sys.platform == "win32":
                line = line.replace("/", "\\")
            ignore_list.append(line.strip())
    return ignore_list

def should_ignore(file_path, ignore_list):
    for pattern in ignore_list:
        if fnmatch.fnmatch(file_path, pattern):
            return True
    return False

def process_repository(repo_path, ignore_list, output_file):
    for root, _, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            relative_file_path = os.path.relpath(file_path, repo_path)

            if not should_ignore(relative_file_path, ignore_list):
                with open(file_path, 'r', errors='ignore') as file:
                    contents = file.read()
                output_file.write("-" * 4 + "\n")
                output_file.write(f"{relative_file_path}\n")
                output_file.write(f"{contents}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python git2text.py /path/to/git/repository [-p /path/to/preamble.txt] [-o /path/to/output_file.txt]")
        sys.exit(1)

    repo_path = sys.argv[1]
    ignore_file_path = os.path.join(repo_path, ".gptignore")
    if sys.platform == "win32":
        ignore_file_path = ignore_file_path.replace("/", "\\")

    if not os.path.exists(ignore_file_path):
        # try and use the .gptignore file in the current directory as a fallback.
        HERE = os.path.dirname(os.path.abspath(__file__))
        ignore_file_path = os.path.join(HERE, ".gptignore")

    preamble_file = None
    if "-p" in sys.argv:
        preamble_file = sys.argv
