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
    ids = []
    for row in reader:
        if row["Uncooperative"] != "Y":
            key = "%s%s" % (row["Species"], row["Sex"])
            counts[key] = counts.get(key, 0) + 1
            ids.append(row["Id"])

    fh.close()
    pprint.pprint(counts)
    return ids

def parse_experiments(filename, ids=None):
    """
    Read in actions from an experiments file, group them by experiment id, and
    convert absolute time to relative time.

    If ``ids`` is specified, only parse actions for experiments with an id in
    this list.
    """
    fh = open(filename, "r")
    reader = csv.reader(fh, delimiter="\t")

    experiments = {}
    for row in reader:
        if ids is None or row[0] in ids:
            experiments.setdefault(int(row[0]), []).append(row)

    return experiments

    fh.close()


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        sys.stderr.write("Usage: %s <notebook_file.csv> [experiments_file.tab]\n" % sys.argv[0])
        sys.exit(1)

    notebook_filename = sys.argv[1]
    ids = parse_notebook(notebook_filename)

    if len(sys.argv) > 2:
        experiments_filename = sys.argv[2]
        experiments = parse_experiments(experiments_filename, ids)
        pprint.pprint(experiments)
