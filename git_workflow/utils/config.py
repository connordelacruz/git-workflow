"""Utilities for interacting with git configs."""
from git.exc import GitCommandError
from . import repository


class Configs:
    """Object with variables representing git configs"""

    # Possible values for the --type argument in git config command.
    TYPE_BOOL = 'bool'
    TYPE_INT = 'int'
    TYPE_PATH = 'path'
    TYPE_EXPIRY_DATE = 'expiry-date'
    TYPE_COLOR = 'color'
    # Custom data types (used in convert_config_value())
    # Space separated list:
    DATA_TYPE_LIST = 'list'

    def __init__(self, repo, debug=False):
        self.repo = repo
        self.debug = debug
        # Make sure repo is initialized before proceeding
        repository.initialize(self.repo)

        # Internal -------------------------------------------------------------
        #: Path to workflow config for this repo.
        self.CONFIG_PATH = self.get_workflow_config('configpath')

        # User Details ---------------------------------------------------------
        #: User initials.
        self.INITIALS = self.get_workflow_config('initials')

        # Branches -------------------------------------------------------------
        #: Base branch.
        #: (Default: 'master')
        self.BASE_BRANCH = self.get_workflow_config(
            'baseBranch', default='master'
        )
        #: Space-separated list of words that should not appear in a branch name
        self.BAD_BRANCH_NAME_PATTERNS = self.get_workflow_config(
            'badBranchNamePatterns',
            data_type=self.DATA_TYPE_LIST
        )

        # Commit Templates -----------------------------------------------------
        #: Format of commit template body. Supports the following placeholders:
        #:   {ticket} - Replaced with ticket number
        #:   {branch} - Replaced with branch name
        #:   {initials} - Replaced with branch name
        #:
        #: (Default: '[{ticket}] ')
        self.COMMIT_TEMPLATE_FORMAT = self.get_workflow_config(
            'commitTemplateFormat', default='[{ticket}] '
        )
        #: Format of commit template filenames. Supports same placeholders as
        #: commitTemplateFormat.
        #: NOTE: Resulting filenames will always begin with '.gitmessage_local_'.
        #:
        #: (Default: '{ticket}_{branch}')
        self.COMMIT_TEMPLATE_FILENAME_FORMAT = self.get_workflow_config(
            'commitTemplateFilenameFormat', default='{ticket}_{branch}'
        )
        #: If true, unset-template will prompt before unsetting unless -f is
        #: specified. If false, will not prompt for confirmation unless -i is
        #: specified.
        #:
        #: (Default: true)
        self.UNSET_TEMPLATE_CONFIRMATION_PROMPT = self.get_workflow_config(
            'unsetTemplateConfirmationPrompt', default=True,
            config_type=self.TYPE_BOOL
        )

        # Ticket Numbers -------------------------------------------------------
        #: Regex representing the format of a valid ticket number. Default
        #: format is 1 or more letters, then a hyphen, then 1 or more numbers.
        #: To allow any format, set to '.*'.
        #:
        #: (Default: '[a-zA-Z]+-[0-9]+')
        self.TICKET_INPUT_FORMAT_REGEX = self.get_workflow_config(
            'ticketInputFormatRegex', default='[a-zA-Z]+-[0-9]+'
        )
        #: If true, letters in the ticket number will be capitalized after
        #: validation.
        #: (Default: true)
        self.TICKET_FORMAT_CAPITALIZE = self.get_workflow_config(
            'ticketFormatCapitalize', default=True,
            config_type=self.TYPE_BOOL
        )

    def get_workflow_config(self, key, default=None,
                            config_type=None, data_type=None,
                            section='workflow'):
        """Retrieve a git config value.

        :param key: The config to retrieve
        :param default: (Optional) Value to return if not configured

        :param config_type: (Optional) Use for --type argument when calling git
            config command
        :param data_type: (Default: config_type or None) Passed to
            convert_config_value(), will alter the type of the returned value

        :param section: (default: 'workflow') Section config key is defined in

        :return: The config value if it exists, otherwise the value of default,
            or None if no default is specified. If data_type is set, will be
            passed through convert_config_value()
        """
        value = default
        config = f'{section}.{key}' if section else key
        if data_type is None and config_type is not None:
            data_type = config_type
        default_arg = None if default is None else str(default)
        value = self.get_config(config,
                                default=default_arg, type=config_type)
        if value is not None and data_type:
            value = self.convert_config_value(value, data_type)
        # Show config name and value in debug mode
        if self.debug:
            print(f'{config}: "{value}"')
        return value

    def _call_config_command(self, *args, **kwargs):
        """Wrapper around repo.git.config(). Catches GitCommandError and
        returns None if unsuccessful. Passes all positional and keyword
        arguments to config().
        """
        value = None
        try:
            value = self.repo.git.config(*args, **kwargs)
        except GitCommandError:
            pass
        return value

    def get_config(self, *args, **kwargs):
        return self._call_config_command(*args, get=True, **kwargs)

    def unset_config(self, *args, **kwargs):
        return self._call_config_command(*args, unset=True, **kwargs)

    @classmethod
    def convert_config_value(cls, string_val, data_type):
        """Convert a string value returned from git config command to a python
        data type.

        :param string_val: The result of the call to git config command (should be
            string)
        :param data_type: TYPE_ or DATA_TYPE_ constant defining what type of data
            this should be converted to

        :return: The converted value
        """
        converted_val = string_val
        if data_type == cls.TYPE_BOOL:
            converted_val = string_val == 'true'
        elif data_type == cls.TYPE_INT:
            converted_val = int(string_val)
        elif data_type == cls.DATA_TYPE_LIST:
            converted_val = string_val.split()
        return converted_val
