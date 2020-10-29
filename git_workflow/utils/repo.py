"""Utilities for common interactions with git repo."""

from git.cmd import Git as GitCmd


def verify_git_version():
    # TODO DOC AND IMPLEMENT
    g = GitCmd()
    major, minor, patch = g.version_info
    version_float = float('{}.{}'.format(major, minor))
    # TODO raise exception instead of returning boolean?
    # TODO make required version values constants?
    return version_float >= 2.23


