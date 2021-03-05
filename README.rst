==================
Git Workflow Tools
==================

.. contents::

Overview
========

This package contains command line tools to streamline common tasks in our git workflow.

Start New Branch with Commit Template
-------------------------------------

.. todo DEMOS

To start a new branch, run:

::

    workflow start

This will prompt you for some information and create a new branch with the following name format:

::

    [<client>-]<brief-description>-<yyyymmdd>-<initials>

If you provide a ticket number, this will create a git commit message template for the branch. By default, the commit template will be in the following format:

::
    
    [<ticket#>] 

..
    TODO
    Finish a Branch
    ---------------
    Doc when implemented, include demos

Create a Commit Template for an Existing Branch
-----------------------------------------------

.. todo DEMOS

If you already have a branch created and would like to create a commit template, run:

::

    workflow set-template


Remove a Branch's Commit Template
---------------------------------

.. todo DEMOS

To remove a branch's commit template without deleting the branch, run:

::

    workflow unset-template

..
    TODO
    Tidy Up Commit Templates
    ------------------------
    Doc when implemented, include demos


Setup
=====

Prerequisites
-------------

Python 3.6+
~~~~~~~~~~~

This package was developed using features that require **Python 3.6 or greater** (developed using Python 3.9.2).

You can use `this guide to install Python 3 on macOS <https://docs.python-guide.org/starting/install3/osx/#doing-it-right>`_.

Git 2.23+
~~~~~~~~~

This package uses features that require **Git 2.23 or greater**.

To install an updated version of ``git`` on macOS using `Homebrew <https://brew.sh/>`_:

::

    brew install git

**Note:** Make sure ``/usr/local/bin`` is added to your ``PATH``. You can do this by adding the following to your ``.bashrc``:

::

    export PATH="/usr/local/bin:$PATH"


Installation
------------

Once you have the above prerequisites installed, clone this repo, then install it using ``pip`` (or ``pip3`` depending on how you installed Python 3):

::

    git clone https://github.com/connordelacruz/git-workflow.git
    cd git-workflow
    pip install -e .

.. note::

    Planning on adding this to `PyPI <https://pypi.org/>`_ once the basic
    functionality is complete. After that, you will be able to install it by
    running ``pip install git-workflow``.


Configure Git to Ignore Commit Template Files
---------------------------------------------

These commands generate files for commit templates, which you likely do not want to track in your repos.

Configure Global .gitignore (RECOMMENDED)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Create a global gitignore file, e.g. ``~/.gitignore_global``
2. Set the global git config for ``core.excludesfile`` to the path of your global gitignore, e.g.:

    ::

        git config --global core.excludesfile ~/.gitignore_global

3. Add the following to your global gitignore:

    ::

        # Commit message templates
        .gitmessage_local*

> For more information on ``core.excludesfile``:
>
> - `GitHub - Ignoring files <https://docs.github.com/en/github/using-git/ignoring-files#configuring-ignored-files-for-all-repositories-on-your-computer>`_
> - `Git Configuration - core.excludesfile <https://git-scm.com/book/en/v2/Customizing-Git-Git-Configuration#_core_excludesfile>`_


Ignore for a Single Repo
~~~~~~~~~~~~~~~~~~~~~~~~

To ignore generated template files in a single git repo, add the following to the ``.gitignore`` file:

::

    # Commit message templates
    .gitmessage_local*


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
    
