"""
Tag Cash.

Usage:
  tagcash [-t <TAGS>] [<FILE>... | -]

Arguments:
  FILE  One or more transaction files
  -     Use stdin (default)

Options
  -t TAGS --tags=TAGS  Comma-separated tags to filter, no spaces.
                       Defaults to use all tags.
"""
import fileinput
import re
from collections import defaultdict
from sys import stderr

from terminaltables import SingleTable
from docopt import docopt


LINE_RE = re.compile(r"""^
                     (?P<date>\d{4}-\d{2}-\d{2}) \s+
                     (?P<amount>-?[\d\.,]+)      \s+
                     (?P<description>.+)         \s+
                     (?P<tags>[-\w,]+)
                     $""", re.X)


class Entry:

    def __init__(self, tag, date, amount, description):
        self.date = date
        self.amount = self._parse_amount(amount)
        self.description = description
        self.balance = None
        # Negate value if tag is negative
        if tag[0] == '-':
            self.tag = tag[1:]
            self.amount *= -1
        else:
            self.tag = tag

    @staticmethod
    def _parse_amount(amount):
        try:
            return int(amount)
        except ValueError:
            pass  # let's try float
        try:
            return float(amount)
        except ValueError:
            pass  # let's try checking decimal point and thousand separator

        # digit + n digits, points or commas + dot or comma + 2 digits
        match = re.match(r'\d[\d\.,]+([\.,])\d\d', amount)
        if match:
            digits = re.sub(r'[\.,]', '', amount)
            return int(digits) / 100

        raise ValueError(f'Couldn\'t parse amount "{amount}"')


def create_entries(wanted_tags, parsed_line):
    tags = parsed_line.pop('tags').split(',')
    for tag in tags:
        abs_tag = tag[1:].lower() if tag[0] == '-' else tag.lower()
        if not wanted_tags or abs_tag in wanted_tags:
            yield Entry(tag, **parsed_line)


def parse_lines(wanted_tags):
    for line in fileinput.input():
        match = LINE_RE.match(line)
        if match:
            parsed_line = match.groupdict()
            yield from create_entries(wanted_tags, parsed_line)
        else:
            print(f'Couldn\'t parse line "{line.rstrip()}"', file=stderr)


def parse_entries(tags):
    entries_by_tag = defaultdict(list)
    for entry in parse_lines(tags):
        entries_by_tag[entry.tag].append(entry)
    return entries_by_tag


def update_balance(entry_lists):
    for entry_list in entry_lists:
        entry_list.sort(key=lambda entry: entry.date)
        balance = 0
        for entry in entry_list:
            entry.balance = balance + entry.amount
            balance = entry.balance


def print_tag_table(entries):
    header = ('Date', 'Amount', 'Balance', 'Description')
    rows = [(entry.date, f'{entry.amount:,.2f}', f'{entry.balance:,.2f}',
            entry.description) for entry in entries]
    table_data = [header] + rows
    table = SingleTable(table_data, title=entries[0].tag)
    table.justify_columns[1] = 'right'
    table.justify_columns[2] = 'right'
    print(table.table)


def main():
    args = docopt(__doc__, version='1.0.0a0')
    if args['--tags'] is None:
        tags = None
    else:
        tags = set(tag.lower() for tag in args['--tags'].split(','))

    entries = parse_entries(tags)
    update_balance(entries.values())
    for tag in sorted(entries):
        print_tag_table(entries[tag])


if __name__ == '__main__':
    main()
