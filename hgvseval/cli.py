#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import sys
import argparse
import pytest



def main(argv=sys.argv[1:]):
    """Main entry-point for HGVS-eval CLI."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--version',
        action='version',
        version='0.0.1'
    )
    parser.add_argument(
        '--html',
        help='Set the HTML output filename',
        default=None
    )
    parser.add_argument(
        '--json',
        help='Set the JSON output filename',
        default=None
    )
    parser.add_argument("endpoint")
    args = parser.parse_args(argv)

    print("Starting HGVS-eval tests for endpoint: {}"
          .format(args.endpoint))

    # Fixture file
    test_dir  = os.path.abspath(os.path.dirname(__file__)) + '/tests'

    test_args = [
        "--endpoint={}".format(args.endpoint),
        "--capture=no",
        test_dir,
    ]

    if args.html:
        test_args += [
            "--html={}".format(args.html),
            "--self-contained-html"
        ]

    if args.json:
        test_args += [
            "--json={}".format(args.json),
        ]

    pytest.main(test_args, plugins=[])


if __name__ == '__main__':
    main()
