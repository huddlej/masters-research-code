#!/usr/bin/env python

"""
Parse notebook
"""
import csv
import datetime
import pprint
import sys


def parse_experiments(filename, uncooperative="N", print_counts=False):
    """
    Read in a lab notebook from a CSV file and write out a parsed version of it.
    """
    fh = open(filename, "r")
    reader = csv.DictReader(fh)

    counts = {}
    experiments = {}
    for row in reader:
        if row["Uncooperative"] == uncooperative:
            key = "%s%s" % (row["Species"], row["Sex"])
            counts[key] = counts.get(key, 0) + 1
            experiments[row["Id"]] = row

    fh.close()

    if print_counts:
        pprint.pprint(counts)

    return experiments


def parse_actions(filename, experiments=None):
    """
    Read in actions from an experiments file, group them by experiment id, and
    convert absolute time to relative time.

    If ``experiments`` dictionary is specified, only parse actions for
    experiments with an "Id" in this list.
    """
    format = "%Y-%m-%d %H:%M:%S"
    fh = open(filename, "r")
    reader = csv.reader(fh, delimiter="\t")

    actions = {}
    start = None
    previous_timestamp = 0
    previous_row = None
    for row in reader:
        if experiments is None or row[0] in experiments:
            action_timestamp = datetime.datetime.strptime(row[2].split(".")[0], format)

            if previous_row is None or previous_row[0] != row[0]:
                start = action_timestamp
            else:
                delta = action_timestamp - previous_timestamp
                relative_timestamp = delta.seconds
                actions.setdefault(previous_row[0], []).append((previous_row[1], relative_timestamp))

            previous_row = row
            previous_timestamp = action_timestamp

    return actions

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
