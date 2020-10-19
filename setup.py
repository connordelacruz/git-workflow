from setuptools import setup

setup(
    name='git_workflow',
    version='0.1',
    description='Utilities for streamlining our git workflow.',
    # url='',
    author='Connor de la Cruz',
    author_email='connor.c.delacruz@gmail.com',
    # license='MIT',
    packages=['git_workflow'],
    install_requires=['GitPython>=3.1,<3.2'],
)

