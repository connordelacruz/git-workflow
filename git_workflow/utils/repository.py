"""Utilities for common interactions with git repo."""
import os
from git import GitCommandError
from git.cmd import Git as GitCmd
from git_workflow.__about__ import __min_git_version__


def verify_git_version(strict=True):
    """Returns True if minimum git version is met for advanced features"""
    g = GitCmd()
    major, minor, patch = g.version_info
    version_float = float(f'{major}.{minor}')
    is_version_requirement_met = version_float >= __min_git_version__
    if strict and not is_version_requirement_met:
        error_msg = f'Git version of {__min_git_version__} or higher required (current version: {version_float})'
        raise Exception(error_msg)
    return is_version_requirement_met


def get_workflow_config_path(repo):
    """Returns the full path for the git workflow config file."""
    return os.path.join(repo.git_dir, 'config_workflow')


def verify_workflow_config_file(repo):
    """Returns True if config_workflow file exists for this repo."""
    return os.path.exists(get_workflow_config_path(repo))


def verify_workflow_config_include(repo):
    """Returns True if config_workflow is included in local git config."""
    result = False
    try:
        included_paths = repo.git.config('include.path', get_all=True, local=True).split('\n')
        result = 'config_workflow' in included_paths
    except GitCommandError:
        pass
    return result


# Initialize

def create_workflow_config_file(repo):
    """Create config_workflow and configure workflow.configpath.

    :return: Result of verify function after attempting to create config
    """
    workflow_config_path = get_workflow_config_path(repo)
    repo.git.config('workflow.configpath', workflow_config_path, file=workflow_config_path)
    return verify_workflow_config_file(repo)


def include_config_workflow(repo):
    """Include config_workflow in repo's local config.

    :return: Result of verify function after attempting to include config
    """
    repo.git.config('include.path', 'config_workflow', add=True, local=True)
    return verify_workflow_config_include(repo)


def initialize(repo):
    """Initialize the repo for use with workflow scripts (unless already
    initialized).

    :return: True if initialized, False if attempted to initialize and
        something went wrong
    """
    workflow_config_file_exists = verify_workflow_config_file(repo)
    workflow_config_included = verify_workflow_config_include(repo)
    if not workflow_config_file_exists:
        print('Workflow config file not found for repo, creating...')
        workflow_config_file_exists = create_workflow_config_file(repo)
        if workflow_config_file_exists:
            print('Config created.')
            print('')
        else:
            pass # TODO ERROR
    if not workflow_config_included:
        print('Configuring local repo to include workflow config...')
        workflow_config_included = include_config_workflow(repo)
        if workflow_config_included:
            print('Repo configured.')
            print('')
        else:
            pass # TODO ERROR
    # TODO don't bother returning once exceptions are implemented
    return workflow_config_file_exists and workflow_config_included
