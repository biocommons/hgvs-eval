#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import sys
import argparse
import pytest
import json
import csv
import jinja2

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

    test_outcomes = {}
    html_output = []
    with open(os.path.abspath('report.json'), 'report.json') as f:
        data = json.load(f)
        for t in data.get('report', 'tests').get('tests'):
            key = t.get('name').partition('[')[-1].rpartition(']')[0]
            test_outcomes[key] = t.get('outcome')

    with open(os.path.join(test_dir, 'data', 'hgvs_eval_criteria_tests.tsv')) as f:
        infile = csv.reader(f, delimiter='\t')
        header = None
        for row in infile:
            if not header:
                header = row
                #add_headers = ['pytest_output', 'pytest_outcome']
                #header = header + add_headers
                header.append('pytest_outcome')
                continue
            if row[0].startswith("#"):
                continue
            criterias = []
            criterias.append(dict(zip(header, row)))
            test_id = '_'.join([
                criterias[0]['feature'],
                criterias[0]['operation'],
                criterias[0]['name'],
                criterias[0]['input']
            ])
            if test_id in test_outcomes:
                if test_outcomes[test_id] == 'passed':
                    test_outcomes[test_id] = "<span class='green'>" + test_outcomes[test_id] + "</span>"
                else:
                    test_outcomes[test_id] = "<span class='red'>" + test_outcomes[test_id] + "</span>"
                row.append(test_outcomes[test_id])
                html_output.append(row)

    html_str = """
        <html>
        <head>
        <style type='text/css'>
        .red{color: #f00;}
        .green{color: #0f0;}"
        </style>
        <title>hgvs-eval Report</title>
        </head>
        <body>
        <h1>hgvs-eval Report</h1>

        <table border=1> 

        <tr>
        {% for h in header %}
        <th>{{h}}</th>
        {% endfor %}
        </tr>

        {% for test in html_output %}
        <tr>
        {% for col in test %} 
        <td>{{col}}</td>
        {% endfor %}
        </tr>
        {% endfor %}

        </table>

        </body>
        </html>
        """

    template = jinja2.Template(html_str)
    Html_file= open("hgvs_eval_report.html","w")
    Html_file.write(template.render(html_output=html_output, header=header))
    Html_file.close()

if __name__ == '__main__':
    main()
