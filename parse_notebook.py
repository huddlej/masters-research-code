#!/usr/bin/env python

"""
Parse notebook
"""
import csv
import pprint
import sys


def parse_notebook(filename):
    """
    Read in a lab notebook from a CSV file and write out a parsed version of it.
    """
    fh = open(filename, "r")
    reader = csv.DictReader(fh)

    counts = {}
    for row in reader:
        if row["Uncooperative"] != "Y":
            key = "%s%s" % (row["Species"], row["Sex"])
            counts[key] = counts.get(key, 0) + 1

    pprint.pprint(counts)


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        sys.stderr.write("Usage: %s <notebook_file.csv>\n" % sys.argv[0])
        sys.exit(1)

    filename = sys.argv[1]
    parse_notebook(filename)
