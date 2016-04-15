#!/usr/bin/env python
# Copyright (c) 2016 by Ken Guyton.  All Rights Reserved.

"""Starting with N count digits seen for i * N for i = 1, 2, 3, ..., max."""

# coding: utf-8

from __future__ import print_function
from __future__ import absolute_import, division, unicode_literals

import argparse
import sys

ALL_DIGITS = set(str(1234567890))


def get_args():
  """Parse command line arguments."""

  parser = argparse.ArgumentParser()
  parser.add_argument('-n', '--num', type=int,
                      help='Run for multiples of this number.')
  parser.add_argument('-v', '--verbose', default=False, action='store_true',
                      help='Output the set for each number * i.')
  parser.add_argument('--data', default=False, action='store_true',
                      help='Process a sequence of input numbers.')
  return parser.parse_args()


def digits_seen(number):
  """Return a list of digits in the number num."""

  return set([str(d) for d in str(number)])


def track_digits(accumulated_digits_seen, digit_sets):
  """Keep track of digits seen.

  Args:
    accumulated_digits_seen: set of str(int) digits.  Digits seen so far.
    digit_sets: function.  A generator that produces sets of digits seen.
  Yields:
    A tuple of the int i, the current number, and thenew set of digits seen
    for every update with a set from digit_sets.
  """

  for i, a_num, digits in digit_sets():
    accumulated_digits_seen.update(digits)
    yield i, a_num, accumulated_digits_seen


def multiples(number):
  """Generate multiples of a number.

  Yields:
    A tuple pair of themultiple i and the number.
  """

  for i in range(1, 1000):
    yield i, i * number


def digits_seen_in_multiples(number):
  """Return a simple generator for the digits seen in each multiple.

  Yields:
    The multiplier i, the number and the digits seen set.
  """

  def generator():
    """A simple generator of multiples."""

    for i, a_num in multiples(number):
      yield i, a_num, digits_seen(a_num)

  return generator


def process_num(number, verbose):
  """Process a single number."""

  if number == 0:
    print('INSOMNIA')
  else:
    for i, a_num, accumulated_digits_seen in track_digits(
        set([]), digits_seen_in_multiples(number)):

      print(i, a_num, end='')

      if verbose:
        print('   {0}'.format(accumulated_digits_seen))
      else:
        print()

      if accumulated_digits_seen == ALL_DIGITS:
        break


def process_input_data_set():
  """Read a data set from stdin of a count and then numbers.

  The first line of the input is a count of the the upcoming input numbers
  then each line is one of those numbers to process.

  Output Case #n: <result>
  """

  count = int(sys.stdin.readline().strip())

  case = 0
  for number_raw in sys.stdin:
    case += 1
    if case > count:
      sys.exit(0)

    number = int(number_raw.strip())

    if number == 0:
      print('Case #{0}: INSOMNIA'.format(case))
    else:
      for unused_i, a_num, accumulated_digits_seen in track_digits(
          set([]), digits_seen_in_multiples(number)):
        if accumulated_digits_seen == ALL_DIGITS:
          break
      print('Case #{0}: {1}'.format(case, a_num))


def main():
  """Find the first multiple when all digits have been seen."""

  opts = get_args()

  if opts.num:
    process_num(opts.num, opts.verbose)
  elif opts.data:
    process_input_data_set()


if __name__ == '__main__':
  main()
