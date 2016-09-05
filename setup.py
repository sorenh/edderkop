#!/usr/bin/env python
#
#   Copyright 2016 Soren Hansen
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
from setuptools import setup, find_packages

def load_requirements(fname):
    with open(fname, 'r') as fp:
        return [x.strip() for x in fp]

requirements = load_requirements('requirements.txt')
test_requirements = load_requirements('test-requirements.txt')

setup(
    name='edderkop',
    version='0.1',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    tests_require=test_requirements,
    test_suite='nose.collector',
    entry_points={'console_scripts': ['edderkop=edderkop.cli:main']}
)
