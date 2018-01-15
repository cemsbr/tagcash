TagCash - Finances with tags in CLI
===================================

|semaphore| |coveralls|

Missing a practical and easy-to-learn solution to keep track of your finances? Use tagcash to do it with simple text files!

TagCash is a little hack that I'm currently using after trying several solutions like GnuCash and Financisto. These are some of the features that I was missing and that are found in TagCash:

- As simple as editing text files;
- Text files are easy to sync between devices and people;
- Simple CLI;
- Quickly copy and paste statements from CLI to e-mail;
- Simple and short Python source code.


Quick Start
-----------

Let's choose 2 tags: ``wallet``, and ``bank`` for your checking account. Now, write the following in a file (e.g.: ``finances.txt``)::

 2018-01-13  100  Starting balance  bank
 2018-01-14   40  Withdrawal        wallet,-bank

As there's no starting balance for ``wallet``, it will be $0.00. In the second line, there is a ``-`` (minus) sign next to the ``bank`` tag to make it ``-40`` in the ``bank`` ledger. Now, let's see what *tagcash* does without any option::

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

- The parser is flexible. Just don't use space in tags and separate them by comma;
- Align as you wish. Use 1 or more spaces between fields (date, amount, ...);
- You can use as many files as you want;
- There's no need to keep the lines sorted by date. Thus, you can keep together all the monthly installments of a payment;
- To choose tags, use for example ``--tags wallet`` (``-t`` for short).


How to Install
--------------
Tested with Python >= 3.5: ``pip3 install tagcash``.


Advanced Usage
--------------

To know how much money you have in total, including all specified tags, add the ``--all`` option::

 $ tagcash --all finances.txt
 (...)
 ┌All Tags────┬────────┬─────────┬───────────────────┐
 │ Date       │ Amount │ Balance │ Description       │
 ├────────────┼────────┼─────────┼───────────────────┤
 │ 2018-01-13 │ 100.00 │  100.00 │ Starting balance  │
 │ 2018-01-14 │ -40.00 │   60.00 │ Withdrawal        │
 │ 2018-01-14 │  40.00 │  100.00 │ Withdrawal        │
 └────────────┴────────┴─────────┴───────────────────┘

As expected, because you withdrew money to your own wallet, the last table shows that you have $100 in total. To keep this overall balance consistent, adopt the simple rule: use negative numbers (or tags) whenever you spend money, and positive when you earn it.


.. |semaphore| image:: https://semaphoreci.com/api/v1/cemsbr/tagcash/branches/master/shields_badge.svg
              :target: https://semaphoreci.com/cemsbr/tagcash
.. |coveralls| image:: https://coveralls.io/repos/github/cemsbr/tagcash/badge.svg?branch=master
              :target: https://coveralls.io/github/cemsbr/tagcash?branch=master
