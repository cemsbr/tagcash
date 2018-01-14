TagCash - Finances with tags in CLI
===================================

|semaphore| |coveralls|

Missing a practical and easy-to-learn solution to keep track of your finances? Use tagcash to do it with simple text files!

Quick Start
-----------

Let's choose 2 tags: ``wallet`` and ``bank`` for your checking account. Now, write the following in a file (e.g.: ``finances.txt``)::

 2018-01-13  100  Starting balance  bank
 2018-01-14   40  Withdrawal        wallet,-bank

As there's no starting balance for ``wallet``, it will be 0. In the second line, there is a ``-`` (minus) sign next to the ``bank`` tag to make it ``-40`` in the ``bank`` ledger. Now, let's see what *tagcash* does without any option::

 ~$ tagcash finances.txt
 ┌bank────────┬────────┬─────────┬───────────────────┐
 │ Date       │ Amount │ Balance │ Description       │
 ├────────────┼────────┼─────────┼───────────────────┤
 │ 2018-01-13 │ 100.00 │  100.00 │ Starting balance  │
 │ 2018-01-14 │ -40.00 │   60.00 │ Withdrawal        │
 └────────────┴────────┴─────────┴───────────────────┘
 ┌wallet──────┬────────┬─────────┬───────────────────┐
 │ Date       │ Amount │ Balance │ Description       │
 ├────────────┼────────┼─────────┼───────────────────┤
 │ 2018-01-14 │  40.00 │   40.00 │ Withdrawal        │
 └────────────┴────────┴─────────┴───────────────────┘


Tips
----

- You can use as many files as you wish;
- There's no need to keep the lines sorted by date. For example, you can keep together all the monthly installments of a payment.

How to Install
--------------
Tested with Python 3.6: ``pip3.6 install tagcash``.


Advanced Usage
--------------

To know how much money you have, including all accounts, add the ``--all`` option::

 $ tagcash --all finances.txt
 (...)
 ┌All Tags────┬────────┬─────────┬───────────────────┐
 │ Date       │ Amount │ Balance │ Description       │
 ├────────────┼────────┼─────────┼───────────────────┤
 │ 2018-01-13 │ 100.00 │  100.00 │ Starting balance  │
 │ 2018-01-14 │ -40.00 │   60.00 │ Withdrawal        │
 │ 2018-01-14 │  40.00 │  100.00 │ Withdrawal        │
 └────────────┴────────┴─────────┴───────────────────┘

As expected, because you withdrew money to your own wallet, the last table shows that you have $100 in total. To keep this overall balance consistent, adopt this simple rule: use negative numbers (or tags) whenever you spend money, and positive when you earn it.


.. |semaphore| image:: https://semaphoreci.com/api/v1/cemsbr/tagcash/branches/master/shields_badge.svg
              :target: https://semaphoreci.com/cemsbr/tagcash
.. |coveralls| image:: https://coveralls.io/repos/github/cemsbr/tagcash/badge.svg?branch=master
              :target: https://coveralls.io/github/cemsbr/tagcash?branch=master
