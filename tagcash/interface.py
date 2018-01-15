"""
TagCash.

Usage:
  tagcash [-t <TAGS>] [-a] [<FILE>... | -]

Arguments:
  FILE  One or more transaction files
  -     Use stdin (default)

Options
  -t TAGS --tags=TAGS  Comma-separated tags to filter, no spaces.
                       Defaults to use all tags.
  -a --all             Show an extra table with all the tags.
"""
import fileinput
from collections import defaultdict

from docopt import docopt
from terminaltables import SingleTable

from .entry import parse_lines, update_balance


def parse_entries(tags, files):
    """Parse all lines of all files that have any tag of ``tags``."""
    entries_by_tag = defaultdict(list)
    lines = fileinput.input(files)
    for entry in parse_lines(lines, tags):
        entries_by_tag[entry.tag].append(entry)
    return entries_by_tag


def print_tag_table(title, entries):
    """Show entries as a table."""
    header = ('Date', 'Amount', 'Balance', 'Description')
    rows = [(entry.date,
             '{:,.2f}'.format(entry.amount),
             '{:,.2f}'.format(entry.balance),
             entry.description) for entry in entries]
    table_data = [header] + rows
    table = SingleTable(table_data, title=title)
    table.justify_columns[1] = 'right'
    table.justify_columns[2] = 'right'
    print(table.table)


def main():
    """Entry point."""
    args = docopt(__doc__, version='1.0.0b2')
    if args['--tags'] is None:
        tags = None
    else:
        tags = set(tag.lower() for tag in args['--tags'].split(','))

    entries = parse_entries(tags, args['<FILE>'])
    for tag in sorted(entries):
        update_balance(entries[tag])
        print_tag_table(tag, entries[tag])

    if args['--all']:
        all_entries = [entry for tag_entries in entries.values()
                       for entry in tag_entries]
        update_balance(all_entries)
        print_tag_table('All Tags', all_entries)
