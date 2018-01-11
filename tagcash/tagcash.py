"""
Tag Cash.

Usage:
  tagcash [-t <TAGS>] <FILE>...

Arguments:
  FILE  One or more transaction files

Options
  -t TAGS --tags=TAGS  Comma-separated tags to filter, no spaces.
                       Defaults to all.
"""
import re
from collections import defaultdict
from sys import stderr

from docopt import docopt


LINE_RE = re.compile(r"""^
                     (?P<date>\d{4}-\d{2}-\d{2}) \s{2,}
                     (?P<amount>[\d\.,]+)        \s{2,}
                     (?P<description>.+)         \s{2,}
                     (?P<tags>.+)
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


def parse_line(wanted_tags, line):
    match = LINE_RE.match(line)
    if match:
        parsed_line = match.groupdict()
        yield from create_entries(wanted_tags, parsed_line)
    else:
        print(f'Couldn\'t parse line "{line}".', file=stderr)


def parse_files(wanted_tags, files):
    for file_ in files:
        with open(file_) as lines:
            for line in lines:
                yield from parse_line(wanted_tags, line)


def parse_entries(tags, files):
    entries_by_tag = defaultdict(list)
    for entry in parse_files(tags, files):
        entries_by_tag[entry.tag].append(entry)
    return entries_by_tag


def update_balance(entry_lists):
    for entry_list in entry_lists:
        entry_list.sort(key=lambda entry: entry.date)
        balance = 0
        for entry in entry_list:
            entry.balance = balance + entry.amount
            balance = entry.balance


def get_max_lengths(entries):
    max_amount_len = max(len(f'{entry.amount:,.2f}') for entry in entries)
    max_balance_len = max(len(f'{entry.balance:,.2f}') for entry in entries)

    return (max(max_amount_len, len('Amount')),
            max(max_balance_len, len('Balance')),
            max(len(entry.description) for entry in entries))


def print_header(amount_len, balance_len, desc_len):
    header = f'{"Date":<10}  {"Amount":>{amount_len}}  ' \
        f'{"Balance":>{balance_len}}  {"Description":<{desc_len}}'
    print(header)
    print('-' * len(header))


def print_entries(entries):
    for tag in sorted(entries):
        print('\n' + tag)
        print('=' * len(tag))
        amount_len, balance_len, desc_len = get_max_lengths(entries[tag])
        print_header(amount_len, balance_len, desc_len)
        for entry in entries[tag]:
            print(f'{entry.date}  {entry.amount:>{amount_len},.2f}  '
                  f'{entry.balance:>{balance_len},.2f}  '
                  f'{entry.description:<{desc_len}}')


def main():
    args = docopt(__doc__, version='1.0.0a0')
    if args['--tags'] is None:
        tags = None
    else:
        tags = set(tag.lower() for tag in args['--tags'].split(','))

    entries = parse_entries(tags, args['<FILE>'])
    update_balance(entries.values())
    print_entries(entries)


if __name__ == '__main__':
    main()
