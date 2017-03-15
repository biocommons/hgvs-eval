# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

package_name = "hgvseval"
short_description = open("doc/short_description.txt").read()
long_description = open("README.rst").read()

# namespace_package = "".join(package_name.split(".")[:-1])

setup(
    author = package_name + " Committers",
    description = short_description.replace("\n", " "),
    license = "Apache License 2.0 (http://www.apache.org/licenses/LICENSE-2.0)",
    long_description = long_description,
    name = package_name,
    # namespace_packages = [namespace_package],
    # package_data = {
    #     "biocommons.pkg": ["_data/migrations/*"],
    #     },
    packages = find_packages(),
    use_scm_version = True,
    zip_safe = True,

    author_email = "biocommons-dev@googlegroups.com",
    url = "https://github.com/biocommons/" + package_name,

    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Database :: Front-Ends",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
    ],

    keywords = [
        'bioinformatics',
    ],

    entry_points = {
        "console_scripts": [
            "hgvs-eval = hgvseval.cli:main",
        ],
    },

    install_requires = [
        "flask",
        "protobuf",
        "requests",
        "six",

        # Given the way we're using pytest, these belong in
        # install_requires (usually in setup_requires and
        # tests_require)
        "pytest",
        "pytest-runner",
        "pytest-json",
        "pytest-html",

        # hgvs -- should probably move to extras_require eventually
        "hgvs>=0.5dev",
        "biocommons.seqrepo",
    
        # This might belong in tests_require
        "suds",
    ],

    setup_requires = [
        "setuptools_scm",
        "wheel",
    ],

    tests_require = [
    ],
)

# <LICENSE>
# Copyright 2016 Source Code Committers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# </LICENSE>
