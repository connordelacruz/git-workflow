"""Utilities for interacting with git configs."""
from git.exc import GitCommandError
from . import repository


class Configs:
    """Object with variables representing git configs"""

    def __init__(self, repo):
        self.repo = repo
        # Make sure repo is initialized before proceeding
        repository.initialize(self.repo)

        # Internal -------------------------------------------------------------
        #: Path to workflow config
        self.CONFIG_PATH = self.get_config('workflow.configpath')

        # User Details ---------------------------------------------------------
        #: User initials
        self.INITIALS = self.get_config('workflow.initials')

        # Branches -------------------------------------------------------------
        #: Base branch (Default: master)
        self.BASE_BRANCH = self.get_config('workflow.baseBranch', 'master')

        # Commit Templates -----------------------------------------------------
        #: Format of commit template body. Supports the following placeholders:
        #:   {ticket} - Replaced with ticket number
        #:   {branch} - Replaced with branch name
        #:   {initials} - Replaced with branch name
        self.COMMIT_TEMPLATE_FORMAT = self.get_config('workflow.commitTemplateFormat', '[{ticket}] ')
        # TODO: Doc and implement; always prepend .gitmessage_local_
        self.COMMIT_TEMPLATE_FILENAME_FORMAT = self.get_config('workflow.commitTemplateFilenameFormat',
                                                               '.gitmessage_local_{ticket}_{branch}')

        # Ticket Numbers -------------------------------------------------------
        # TODO: TICKET_INPUT_FORMAT_REGEX and TICKET_FORMAT_CAPITALIZE

    def get_config(self, config, default=None):
        value = default
        try:
            # TODO default=default might not play nice with some values
            value = self.repo.git.config(config, get=True, default=default)
        except GitCommandError:
            pass
        return value
