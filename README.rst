==================
Git Workflow Tools
==================

.. contents::

TODO
====

-  Copy over relevant items from old scripts readme
- Setup
    - Python 3.6 (developed using 3.9.2)
    - Git Version
- Demos

Overview
========

This package contains command line tools to streamline common tasks in our git workflow.

Start New Branch with Commit Template
-------------------------------------

To start a new branch, run:

::

    workflow start

This will prompt you for some information and create a new branch with the following name format:

::

    [<client>-]<brief-description>-<yyyymmdd>-<initials>

If you provide a ticket number, this will create a git commit message template for the branch. By default, the commit template will be in the following format:

::
    
    [<ticket#>] 

.. todo DEMOS


Finish a Branch
---------------

.. todo Doc when implemented, include demos

**NOT YET IMPLEMENTED**


Create a Commit Template for an Existing Branch
-----------------------------------------------

If you already have a branch created and would like to create a commit template, run:

::

    workflow set-template

.. todo DEMOS


Remove a Branch's Commit Template
---------------------------------

To remove a branch's commit template without deleting the branch, run:

::

    workflow unset-template

.. todo DEMOS


Tidy Up Commit Templates
------------------------

.. todo Doc when implemented, include demos

**NOT YET IMPLEMENTED**


Setup
=====

**TODO**


Commands
========

``start``
---------

Usage
-----

::

    usage: workflow start [-h] [-V] [-c <client> | -C] [-d <description>] [-i <initials>] [-s] [-t <ticket#> | -T] [-b <branch> | -B | -P]
    
    Create a new branch.
    
    General:
      -h, --help            Show this help message and exit
      -V, --version         Show version number and exit
    
    Branch Name Arguments:
      -c <client>, --client <client>
                            Specify client name
      -C, --no-client       No client name (skips prompt)
      -d <description>, --description <description>
                            Specify branch description
      -i <initials>, --initials <initials>
                            Specify developer initials
      -s, --skip-bad-name-check
                            Skip check for bad branch names
    
    Commit Template Arguments:
      -t <ticket#>, --ticket <ticket#>
                            Specify ticket number (will create commit template)
      -T, --no-ticket       Skip ticket number prompt, don't create commit template (overrides -t)
    
    Branching Arguments:
      -b <branch>, --base-branch <branch>
                            Specify branch to use as base for new branch (default: master)
      -B, --branch-from-current
                            Use currently checked out branch as base (overrides -b)
      -P, --no-pull         Skip pulling changes to base branch.
    
