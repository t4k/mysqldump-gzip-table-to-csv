#!/usr/bin/env python

import csv
import gzip
import sys

# This prevents prematurely closed pipes from raising an exception in Python.
from signal import signal, SIGPIPE, SIG_DFL

signal(SIGPIPE, SIG_DFL)

# Allow large content in the dump.
csv.field_size_limit(sys.maxsize)


def is_insert(line):
    """
    Returns true if the line begins a SQL insert statement.
    """
    return line.startswith("INSERT INTO")


def parse_table_name(line):
    start = line.find("INSERT INTO `") + len("INSERT INTO `")
    end = line.find("` VALUES")
    table = line[start:end]
    return table


def get_values(line):
    """
    Returns the portion of an INSERT statement containing values.
    """
    return line.partition(" VALUES ")[2]


def values_sanity_check(values):
    """
    Ensures that values from the INSERT statement meet basic checks.
    """
    assert values
    assert values[0] == "("
    # Assertions have not been raised.
    return True


def parse_values(values, outfile):
    """
    Given a file handle and the raw values from a MySQL INSERT statement, write
    the equivalent CSV to the file.
    """
    latest_row = []

    reader = csv.reader(
        [values],
        delimiter=",",
        doublequote=False,
        escapechar="\\",
        quotechar="'",
        strict=True,
    )

    writer = csv.writer(outfile)
    for reader_row in reader:
        for column in reader_row:
            # If our current string is empty...
            if len(column) == 0 or column == "NULL":
                latest_row.append("")
                continue
            # If our string starts with an opening parenthesis...
            if column[0] == "(":
                # If we've been filling out a row...
                if len(latest_row) > 0:
                    # Check if the previous entry ended in a close paren. If so,
                    # the row we've been filling out has been COMPLETED as:
                    #    1) the previous entry ended in a )
                    #    2) the current entry starts with a (
                    if latest_row[-1][-1] == ")":
                        # Remove the closing parenthesis.
                        latest_row[-1] = latest_row[-1][:-1]
                        writer.writerow(latest_row)
                        latest_row = []
                # If we're beginning a new row, eliminate the opening
                # parenthesis.
                if len(latest_row) == 0:
                    column = column[1:]
            # Add our column to the row we're working on.
            latest_row.append(column)
        # At the end of an INSERT statement, we'll have the semicolon. Make sure
        # to remove the semicolon and the closing parenthesis.
        if latest_row[-1][-2:] == ");":
            latest_row[-1] = latest_row[-1][:-2]
            writer.writerow(latest_row)


def main(gzip_file, table):
    """
    Parse arguments and start the program.
    """
    # Iterate over all lines in gzip_file.
    try:
        with gzip.open(gzip_file, "rt") as f:
            for line in f:
                # Look for an INSERT statement and parse it.
                if not is_insert(line):
                    continue
                if parse_table_name(line) != table:
                    continue
                values = get_values(line)
                if not values_sanity_check(values):
                    raise Exception(
                        "Getting substring of SQL INSERT statement after ' VALUES ' failed!"
                    )
                parse_values(values, sys.stdout)
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        gzip_file = sys.argv[1]
        table = sys.argv[2]
    else:
        sys.exit("USAGE: python mysqldump_gzip_table_to_csv.py /path/to/db.sql.gz table_name")
    main(gzip_file, table)
