"""Utilities for common interactions with git repo."""
from git.cmd import Git as GitCmd

from git_workflow.__about__ import __min_git_version__


def verify_git_version():
    """Returns True if minimum git version is met for advanced features"""
    g = GitCmd()
    major, minor, patch = g.version_info
    version_float = float('{}.{}'.format(major, minor))
    return version_float >= __min_git_version__


