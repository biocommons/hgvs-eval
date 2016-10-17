#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

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
        default='report.html'
    )
    # parser.add_argument(
    #     '--dir',
    #     help='Set the local tests directory'
    # )
    parser.add_argument("endpoint")
    args = parser.parse_args(argv)

    print("Starting HGVS-eval tests for endpoint: {}"
          .format(args.endpoint))

    # Fixture file
    import os
    test_dir  = os.path.abspath(os.path.dirname(__file__)) + '/tests'

    test_args = [
        "--html={}".format(args.html),
        "--endpoint={}".format(args.endpoint),
        "--self-contained-html",
        test_dir,
    ]

    pytest.main(test_args, plugins=[])


if __name__ == '__main__':
    main()
