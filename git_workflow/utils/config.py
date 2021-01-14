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
        # TODO workflow.enableCommitTemplate?
        #: Format of commit template body. Placeholders:
        #:   {ticket} - Replaced with ticket number
        self.COMMIT_TEMPLATE_FORMAT = self.get_config('workflow.commitTemplateFormat', '[{ticket}] ')

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
