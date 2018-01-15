"""Parse and manage transactions."""
import re
from sys import stderr


_LINE_RE = re.compile(r"""^
                      (?P<date>\d{4}-\d{2}-\d{2}) \s+
                      (?P<amount>-?[\d\.,]+)      \s+
                      (?P<description>.+)         \s+
                      (?P<tags>[-\w,]+)
                      $""", re.X)


class Entry:  # pylint: disable=too-few-public-methods
    """One event of one tag."""

    def __init__(self, tag, date, amount, description):
        """Set all instance variables."""
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
        match = re.match(r'-?\d[\d\.,]+([\.,])\d\d', amount)
        if match:
            digits = re.sub(r'[\.,]', '', amount)
            return int(digits) / 100

        raise ValueError('Couldn\'t parse amount "{}"'.format(amount))


def update_balance(entries):
    """Sort entries by date and update balances."""
    entries.sort(key=lambda entry: entry.date)
    balance = 0
    for entry in entries:
        entry.balance = balance + entry.amount
        balance = entry.balance


def parse_lines(lines, wanted_tags):
    """Parse lines having specific tags or all if none specified."""
    for line in lines:
        match = _LINE_RE.match(line)
        if match:
            parsed_line = match.groupdict()
            yield from _create_entries(wanted_tags, parsed_line)
        else:
            print('Couldn\'t parse line "{}"'.format(line.rstrip()),
                  file=stderr)


def _create_entries(wanted_tags, parsed_line):
    """Yield entries having selected tags."""
    tags = parsed_line.pop('tags').split(',')
    for tag in tags:
        abs_tag = tag[1:].lower() if tag[0] == '-' else tag.lower()
        if not wanted_tags or abs_tag in wanted_tags:
            yield Entry(tag, **parsed_line)
