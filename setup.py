

import os
from setuptools import setup, find_packages

try:
    with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as file:
        readme = file.read()
except IOError:
    readme = __doc__

setup(
    name='django_psycopg2',
    description=readme.splitlines()[0],
    long_description="\n".join(readme.splitlines()[2:]).lstrip(),


)