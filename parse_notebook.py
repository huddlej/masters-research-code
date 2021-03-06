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
        sys.stderr.write("Usage: %s <notebook_file.csv> [experiments_file.tab] [parsed_actions.tab]\n" % sys.argv[0])
        sys.exit(1)

    notebook_filename = sys.argv[1]

    if len(sys.argv) == 4:
        experiments = parse_experiments(notebook_filename)
        actions_filename = sys.argv[2]
        parsed_actions_filename = sys.argv[3]
        all_actions = parse_actions(actions_filename, experiments)

        # Write out parsed actions to a file.
        oh = open(parsed_actions_filename, "w")

        for experiment, actions in all_actions.items():
            for action in actions:
                oh.write("%s\n" % "\t".join(
                    (str(experiment), action[0], str(action[1])))
                )

        oh.close()
    elif len(sys.argv) == 3:
        experiments = parse_experiments(notebook_filename)
        actions_filename = sys.argv[2]
        all_actions = parse_actions(actions_filename, experiments)

        experiment_fields = (
            "Id",
            "Date",
            "Species",
            "Sex",
            "Previously uncooperative",
            "Searched snowberry",
            "Searched apple",
            "Fed on apple",
            "Temperature (C)"
        )
        action_states = ("wall", "apple", "apple_search", "apple_rest",
                         "snowberry", "snowberry_search", "snowberry_rest")

        print "\t".join(tuple([field.lower().replace(" ", "_")
                               for field in experiment_fields]) + action_states)

        for experiment_id, actions in all_actions.items():
            times = {}

            # Remove the last wall instance which really marks the "end" of the
            # experiment.
            if len(actions) > 0 and actions[-1][0] == "wall":
                actions.pop()

            # Throw out start and first wall if it exists.
            if actions[0][0] == "start":
                actions.pop(0)

            if actions[0][0] == "wall":
                actions.pop(0)

            for action in actions:
                if action[0].startswith("wall"):
                    times["wall"] = times.get("wall", 0) + action[1]
                elif action[0].startswith(("apple", "snowberry")):
                    # Split times for fruit into rest and search.
                    times[action[0]] = times.get(action[0], 0) + action[1]

                    # Count totla time for the fruit.
                    fruit = action[0].split("_")[0]
                    times[fruit] = times.get(fruit, 0) + action[1]
                else:
                    pass

            experiment = experiments[experiment_id]
            print "\t".join([experiment.get(field, "?") for field in experiment_fields] +
                            [str(times.get(state, 0)) for state in action_states])
    else:
        print "Cooperative"
        experiments = parse_experiments(notebook_filename, print_counts=True)
        print "Uncooperative"
        experiments = parse_experiments(notebook_filename, uncooperative="Y", print_counts=True)
