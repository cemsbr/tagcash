"""Test entries and parsing."""
import unittest

from tagcash.interface import parse_lines
from tagcash.entry import update_balance


class TestParser(unittest.TestCase):
    """Test line parsing."""

    def test_one_tag(self):
        """Line with one tag should return one entry."""
        entries = self.parse_lines(
            '2018-01-14  12  My description  mytag'
        )
        self.assertEqual(1, len(entries))
        self.assertEqual('mytag', entries[0].tag)

    def test_two_tags(self):
        """Line with two tag should return two entries."""
        entries = self.parse_lines(
            '2018-01-14  12  My description  mytag1,mytag2')
        self.assertEqual(2, len(entries))
        self.assertEqual('mytag1', entries[0].tag)
        self.assertEqual('mytag2', entries[1].tag)

    def test_positive_tag(self):
        """Amount should not be changed when tag is positive."""
        entries = self.parse_lines(
            '2018-01-14   12  My description  mytag',
            '2018-01-15  -12  My description  mytag')
        self.assertEqual(12, entries[0].amount)
        self.assertEqual(-12, entries[1].amount)

    def test_negative_tag(self):
        """Amount should be the opposite when tag has minus sign."""
        entries = self.parse_lines(
            '2018-01-14   12  My description  -mytag',
            '2018-01-15  -12  My description  -mytag')
        self.assertEqual(-12, entries[0].amount)
        self.assertEqual(12, entries[1].amount)

    @staticmethod
    def parse_lines(*lines):
        """Return entries for the given lines."""
        return list(parse_lines(lines, []))


class TestAmountParsing(unittest.TestCase):
    """Test number conversion from string."""

    def test_integer(self):
        """Integer string."""
        actual = self._parse_amount('42')
        self.assertEqual(42, actual)

    def test_float_dot(self):
        """Float string with dot decimal separator."""
        actual = self._parse_amount('12.30')
        self.assertEqual(12.30, actual)

    def test_float_comma(self):
        """Float string with comma decimal separator."""
        actual = self._parse_amount('12,30')
        self.assertEqual(12.30, actual)

    def test_thousand_comma(self):
        """Comma thousand separator."""
        actual = self._parse_amount('1,000.00')
        self.assertEqual(1000, actual)

    def test_thousand_dot(self):
        """Dot thousand separator."""
        actual = self._parse_amount('1.000,00')
        self.assertEqual(1000, actual)

    @staticmethod
    def _parse_amount(amount_str):
        entries = TestParser.parse_lines(
            f'2018-01-14  {amount_str}  Description  mytag'
        )
        return entries[0].amount


class TestBalance(unittest.TestCase):
    """Test balance calculation."""

    def setUp(self):
        self._entries = TestParser.parse_lines(
            '2018-01-13  12  Description  mytag',
            '2018-01-14  34  Description  mytag'
        )

    def test_initial_balance(self):
        """Initial balance should be None."""
        self.assertIsNone(self._entries[0].balance)

    def test_first_balance(self):
        """First balance should equal amount."""
        update_balance(self._entries)
        self.assertEqual(12, self._entries[0].balance)

    def test_second_balance(self):
        """2nd balance should be the previous' balance plus current amount."""
        update_balance(self._entries)
        self.assertEqual(46, self._entries[1].balance)
