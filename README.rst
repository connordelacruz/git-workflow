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

Finish a Branch
---------------

.. todo DEMOS

When you're finished with a project branch that has been merged, run:

::

    workflow finish

This will clean up configs, remove the branch's commit template, and delete the branch.

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


Cleanup Commit Templates in a Repo
----------------------------------

.. todo DEMOS

If you have a bunch of lingering commit templates and would like to tidy up, run:

::

    workflow cleanup

By default, this will clean up configs and template files for every branch except the one you have checked out. It will also look for orphaned commit templates with no associated branch and remove them.

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

Once you have the above prerequisites installed, you can install it using ``pip`` (or ``pip3`` depending on how you installed Python 3):

::

    pip install git-workflow


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


Workflow Commands
=================
.. todo insert sections for remaining commands 

**Usage:** ``workflow <command>``

``start``
---------

Create a new branch with the following name format:

::

    [<client>-]<brief-description>-<yyyymmdd>-<initials>

Where:

- ``<client>`` - (Optional) Client's name
- ``<brief-description>`` - Description of the work
- ``<yyyymmdd>`` - Today's date
- ``<initials>`` - Engineer's initials

Script will prompt for details and format appropriately (i.e. no
spaces/underscores, all lowercase).


Usage
~~~~~

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
    

Configs
~~~~~~~

Command uses the following configs:

- `workflow.initials`_
- `workflow.baseBranch`_
- `workflow.badBranchNamePatterns`_


``finish``
----------

Finish a project branch.

By default, this command will prompt for confirmation unless ``--force`` is
specified. Once confirmed, this command will:

- Unset the commit template of the project branch
- Checkout the base branch and pull latest updates
- Attempt to delete the project branch using ``git branch -d``, which may
  fail if the project branch has not been fully merged


Usage
~~~~~

::

    usage: workflow finish [-h] [-V] [-f | -c] [<branch>]
    
    Finish a project branch.
    
    General:
      -h, --help          Show this help message and exit
      -V, --version       Show version number and exit
    
    Positional Arguments:
      <branch>            Branch to finish (default: current)
    
    Confirmation Prompt Arguments:
      Override workflow.finishBranchConfirmationPrompt config.
    
      -f, --force         Skip confirmation prompt (if configured)
      -c, --confirmation  Prompt for confirmation before deleting
    

Configs
~~~~~~~

Command uses the following configs:

- `workflow.baseBranch`_
- `workflow.finishBranchConfirmationPrompt`_


``set-template``
----------------

Create and configure commit template for the current branch.

By default, the commit template includes the specified ticket number before
the commit message. E.g. for ticket number ``AB-12345``:

::

    [AB-12345] <commit message text starts here>

The commit template file will be created in the root of the git repository.
By default, the filename will be in this format:

::

    .gitmessage_local_<ticket>_<branch>

The format of the filename, commit template body, accepted ticket numbers,
and more can be customized with git configs (see the Configs section below
for details).


Usage
~~~~~

::

    usage: workflow set-template [-h] [-V] [<ticket>]
    
    Configure git commit template for a branch.
    
    General:
      -h, --help     Show this help message and exit
      -V, --version  Show version number and exit
    
    Positional Arguments:
      <ticket>       Ticket number to use in commit template
    

Configs
~~~~~~~

Command uses the following configs:

- `workflow.commitTemplateFilenameFormat`_
- `workflow.commitTemplateFormat`_
- `workflow.ticketInputFormatRegex`_
- `workflow.ticketFormatCapitalize`_
- `workflow.ticketInputFormatRegex`_
- `workflow.initials`_


``unset-template``
------------------

Remove commmit template for a branch.

By default, this command will prompt for confirmation before removing the
commit template unless ``--force`` is specified.


Usage
~~~~~

::

    usage: workflow unset-template [-h] [-V] [-f | -c] [<branch>]
    
    Remove commit template for a branch.
    
    General:
      -h, --help          Show this help message and exit
      -V, --version       Show version number and exit
    
    Positional Arguments:
      <branch>            Branch to unset template for (default: current)
    
    Confirmation Prompt Arguments:
      Override workflow.unsetTemplateConfirmationPrompt config.
    
      -f, --force         Skip confirmation prompt (if configured)
      -c, --confirmation  Prompt for confirmation before unsetting
    

Configs
~~~~~~~

Command uses the following configs:

- `workflow.unsetTemplateConfirmationPrompt`_


``cleanup``
-----------

Tidy up workflow-related files and configs.

This command will first list all branches and files that will be affected.
By default, it will then prompt for confirmation unless ``--force`` is
specified. Once confirmed, this command will:

- Unset the commit templates of all configured branches
- Remove any orphan commit template files that have no associated branch

By default, the current branch is omitted from cleanup unless
``--include-current-branch`` is specified.


Usage
~~~~~

::

    usage: workflow cleanup [-h] [-V] [-B] [-o] [-f | -c]
    
    Tidy up workflow-related files and configs.
    
    General:
      -h, --help            Show this help message and exit
      -V, --version         Show version number and exit
    
    Cleanup Options:
      -B, --include-current-branch
                            Unset template for current branch too
      -o, --orphans-only    Only clean up templates without a branch
    
    Confirmation Prompt Arguments:
      Override workflow.cleanupConfirmationPrompt config.
    
      -f, --force           Skip confirmation prompt (if configured)
      -c, --confirmation    Prompt for confirmation before cleaning up templates
    

Configs
~~~~~~~

Command uses the following configs:

- `workflow.cleanupConfirmationPrompt`_


Git Configurations
==================

Workflow commands will use the following git configs if set:

User Details
------------

``workflow.initials``
~~~~~~~~~~~~~~~~~~~~~

The user's initials.

If set, ``workflow start`` will skip the prompt for your initials and use this value.

**E.g.:** To set your initials to "cd":

::

    git config --global workflow.initials cd


Branches
--------

``workflow.baseBranch``
~~~~~~~~~~~~~~~~~~~~~~~

**Default:** ``master``

Branch to use as a base when creating a new branch using ``workflow
start``.

**E.g.:** To base branches off of ``develop``:

::

    git config workflow.baseBranch develop


``workflow.badBranchNamePatterns``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Set to a **space-separated** string of phrases or patterns that
should not appear in a standard branch name. If set, ``workflow
start`` will check for these before attempting to create a new
branch.

**E.g.:** if standard branch names shouldn't include the words
``-web`` or ``-plugins``:

::

    git config workflow.badBranchNamePatterns "-web -plugins"


Commit Templates
----------------

``workflow.commitTemplateFormat``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Default:** ``'[{ticket}] '``

Format of commit template body. Supports the following placeholders:

  - ``{ticket}``: Replaced with ticket number
  - ``{branch}``: Replaced with branch name
  - ``{initials}``: Replaced with user initials (if configured)


``workflow.commitTemplateFilenameFormat``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Default:** ``'{ticket}_{branch}'``

Format of commit template filenames. Supports same placeholders as
``workflow.commitTemplateFormat``.

**NOTE:** Resulting filenames will always begin with
``'.gitmessage_local_'``.


Ticket Numbers
--------------

``workflow.ticketInputFormatRegex``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Default:** ``'[a-zA-Z]+-[0-9]+'``

Regex representing the format of a valid ticket number. Default
format is 1 or more letters, then a hyphen, then 1 or more numbers.
To allow any format, set to ``'.*'``.


``workflow.ticketFormatCapitalize``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Default:** ``true``

If ``true``, letters in the ticket number will be capitalized after
validation.


Confirmation Prompts
--------------------

``workflow.finishBranchConfirmationPrompt``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Default:** ``true``

If ``true``, ``workflow finish`` will prompt for confirmation
before unsetting unless ``-f`` is specified. If ``false``, will
not prompt for confirmation unless ``-c`` is specified.


``workflow.unsetTemplateConfirmationPrompt``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Default:** ``true``

If ``true``, ``workflow unset-template`` will prompt for
confirmation before unsetting unless ``-f`` is specified. If
``false``, will not prompt for confirmation unless ``-c`` is
specified.


``workflow.cleanupConfirmationPrompt``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Default:** ``true``

If ``true``, ``workflow cleanup`` will prompt for confirmation 
before cleaning unless ``-f`` is specified. If ``false``, will not 
prompt for confirmation unless ``-c`` is specified.


Future Updates
==============

New Commands
------------

- ``workflow rename``: Rename a branch while maintaining its current commit template.

Enhancements
------------

- Support ``--verbosity`` argument on all commands.
- Support using a git tag for a base instead of a branch with ``workflow start``.
- Support command tab completion with `argcomplete <https://kislyuk.github.io/argcomplete/>`_.

Documentation
-------------

- Add demo GIFs of commands in action to README.
- Generate API docs using Sphinx.
