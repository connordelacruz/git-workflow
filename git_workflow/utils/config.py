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
        #: Path to workflow config for this repo.
        self.CONFIG_PATH = self.get_config('configpath')

        # User Details ---------------------------------------------------------
        #: User initials.
        self.INITIALS = self.get_config('initials')

        # Branches -------------------------------------------------------------
        #: Base branch.
        #: (Default: 'master')
        self.BASE_BRANCH = self.get_config('baseBranch', 'master')

        # Commit Templates -----------------------------------------------------
        #: Format of commit template body. Supports the following placeholders:
        #:   {ticket} - Replaced with ticket number
        #:   {branch} - Replaced with branch name
        #:   {initials} - Replaced with branch name
        #:
        #: (Default: '[{ticket}] ')
        self.COMMIT_TEMPLATE_FORMAT = self.get_config('commitTemplateFormat',
                                                      '[{ticket}] ')
        #: Format of commit template filenames. Supports same placeholders as
        #: commitTemplateFormat.
        #: NOTE: Resulting filenames will always begin with '.gitmessage_local_'.
        #:
        #: (Default: '{ticket}_{branch}')
        self.COMMIT_TEMPLATE_FILENAME_FORMAT = self.get_config('commitTemplateFilenameFormat',
                                                               '{ticket}_{branch}')

        # Ticket Numbers -------------------------------------------------------
        #: Regex representing the format of a valid ticket number.
        #: (Default: '[a-zA-Z]+-[0-9]+')
        self.TICKET_INPUT_FORMAT_REGEX = self.get_config('ticketInputFormatRegex',
                                                         '[a-zA-Z]+-[0-9]+')
        # TODO: TICKET_FORMAT_CAPITALIZE (figure out boolean)

    def get_config(self, key, default=None, section='workflow'):
        value = default
        config = section + '.' + key
        try:
            # TODO default=default might not play nice with some values
            value = self.repo.git.config(config, get=True, default=default)
        except GitCommandError:
            pass
        return value
