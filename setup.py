import os
from setuptools import setup, find_packages

base_path = os.path.dirname(os.path.abspath(__file__))
# Get metadata
about = {}
with open(os.path.join(base_path, 'git_workflow', '__about__.py')) as f:
    exec(f.read(), about)
# Parse README.rst for long_description
with open(os.path.join(base_path, 'README.rst')) as f:
    readme = f.read()

setup(
    name='git_workflow',
    version=about['__version__'],
    author='Connor de la Cruz',
    author_email='connor.c.delacruz@gmail.com',
    description='Utilities for streamlining our git workflow.',
    long_description=readme,
    url=about['__url__'],
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Environment :: Console :: Curses',
        'Topic :: Software Development :: Version Control :: Git',
        'Topic :: Software Development',
        'Development Status :: 4 - Beta',
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            about['__command__'] + ' = git_workflow.__main__:main',
        ]
    },
    install_requires=[
        'GitPython==3.1.11',
        'cmd-utils>=1.0.0,<1.1',
        'argcomplete>=1.12,<1.13',
    ],
    extras_require={
        'dev': [
            'Jinja2>=2.11,<2.12',
            'build',
            'vermin',
        ],
    },
    python_requires='>=' + about['__min_python_version__'],
)

