"""Utilities for interacting with git configs."""
from git.exc import GitCommandError
from . import repository


# Possible values for the --type argument in git config command.
TYPE_BOOL = 'bool'
TYPE_INT = 'int'
TYPE_PATH = 'path'
TYPE_EXPIRY_DATE = 'expiry-date'
TYPE_COLOR = 'color'


def convert_config_value(string_val, config_type):
    converted_val = string_val
    if config_type == TYPE_BOOL:
        converted_val = string_val == 'true'
    elif config_type == TYPE_INT:
        converted_val = int(string_val)
    return converted_val


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
        #: Regex representing the format of a valid ticket number. Default
        #: format is 1 or more letters, then a hyphen, then 1 or more numbers.
        #: To allow any format, set to '.*'.
        #:
        #: (Default: '[a-zA-Z]+-[0-9]+')
        self.TICKET_INPUT_FORMAT_REGEX = self.get_config('ticketInputFormatRegex',
                                                         '[a-zA-Z]+-[0-9]+')
        #: If true, letters in the ticket number will be capitalized after
        #: validation.
        #: (Default: true)
        self.TICKET_FORMAT_CAPITALIZE = self.get_config('ticketFormatCapitalize',
                                                        True, TYPE_BOOL)

    def get_config(self, key, default=None, config_type=None, section='workflow'):
        value = default
        config = section + '.' + key
        try:
            default_arg = None if default is None else str(default)
            value = self.repo.git.config(config, get=True, default=default_arg, type=config_type)
            if config_type:
                value = convert_config_value(value, config_type)
        except GitCommandError:
            pass
        return value
