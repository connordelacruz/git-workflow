import os
from setuptools import setup

# Get metadata
base_path = os.path.dirname(os.path.abspath(__file__))
about = {}
with open(os.path.join(base_path, 'git_workflow', '__about__.py')) as f:
    exec(f.read(), about)

# TODO parse README.rst for long_description

# TODO move more stuff to __about__
setup(
    name='git_workflow',
    version=about['__version__'],
    description='Utilities for streamlining our git workflow.',
    # url='',
    author='Connor de la Cruz',
    author_email='connor.c.delacruz@gmail.com',
    # license='MIT',
    packages=['git_workflow'],
    entry_points={
        'console_scripts': [
            about['__command__'] + ' = git_workflow.__main__:main',
        ]
    },
    install_requires=[
        'GitPython>=3.1,<3.2',
        'blessings>=1.7,<1.8',
    ],
    extras_require={
        'dev': ['Jinja2>=2.11,<2.12',],
    },
    python_requires='>=' + about['__min_python_version__'],
)

