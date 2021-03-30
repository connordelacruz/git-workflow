"""Utilities for interacting with git configs."""
import textwrap
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

    def __init__(self, repo, debug=False, no_init=False):
        self.repo = repo
        self.debug = debug
        # Make sure repo is initialized before proceeding
        if not no_init:
            repository.initialize(self.repo)

        # CONFIGS ==============================================================
        # Internal -------------------------------------------------------------
        # configPath
        self.CONFIG_PATH_DOC = (
            'Path to workflow config for this repo.'
        )
        self.CONFIG_PATH = self.get_workflow_config('configpath')

        # User Details ---------------------------------------------------------
        # initials
        self.INITIALS_DOC = textwrap.dedent(
            '''\
            The user's initials.

            If set, ``workflow start`` will skip the prompt for your initials and use this value.

            **E.g.:** To set your initials to "cd":

            ::

                git config --global workflow.initials cd
            ''')
        self.INITIALS = self.get_workflow_config('initials')

        # Branches -------------------------------------------------------------
        # baseBranch
        self.BASE_BRANCH_DOC = textwrap.dedent(
            '''\
            **Default:** ``master``

            Branch to use as a base when creating a new branch using ``workflow
            start``.

            **E.g.:** To base branches off of ``develop``:

            ::

                git config workflow.baseBranch develop
            ''')
        self.BASE_BRANCH = self.get_workflow_config(
            'baseBranch', default='master'
        )
        # badBranchNamePatterns
        self.BAD_BRANCH_NAME_PATTERNS_DOC = textwrap.dedent(
            '''\
            Set to a **space-separated** string of phrases or patterns that
            should not appear in a standard branch name. If set, ``workflow
            start`` will check for these before attempting to create a new
            branch.

            **E.g.:** if standard branch names shouldn't include the words
            ``-web`` or ``-plugins``:

            ::

                git config workflow.badBranchNamePatterns "-web -plugins"
            ''')
        self.BAD_BRANCH_NAME_PATTERNS = self.get_workflow_config(
            'badBranchNamePatterns',
            data_type=self.DATA_TYPE_LIST
        )

        # Commit Templates -----------------------------------------------------
        # TODO Document examples?
        # commitTemplateFormat
        self.COMMIT_TEMPLATE_FORMAT_DOC = textwrap.dedent(
            '''\
            **Default:** ``'[{ticket}] '``

            Format of commit template body. Supports the following placeholders:

              - ``{ticket}``: Replaced with ticket number
              - ``{branch}``: Replaced with branch name
              - ``{initials}``: Replaced with user initials (if configured)
            ''')
        self.COMMIT_TEMPLATE_FORMAT = self.get_workflow_config(
            'commitTemplateFormat', default='[{ticket}] '
        )
        # commitTemplateFilenameFormat
        self.COMMIT_TEMPLATE_FILENAME_FORMAT_DOC = textwrap.dedent(
            '''\
            **Default:** ``'{ticket}_{branch}'``

            Format of commit template filenames. Supports same placeholders as
            ``workflow.commitTemplateFormat``.

            **NOTE:** Resulting filenames will always begin with
            ``'.gitmessage_local_'``.
            ''')
        self.COMMIT_TEMPLATE_FILENAME_FORMAT = self.get_workflow_config(
            'commitTemplateFilenameFormat', default='{ticket}_{branch}'
        )

        # Ticket Numbers -------------------------------------------------------
        # TODO Document examples?
        # ticketInputFormatRegex
        self.TICKET_INPUT_FORMAT_REGEX_DOC = textwrap.dedent(
            '''\
            **Default:** ``'[a-zA-Z]+-[0-9]+'``

            Regex representing the format of a valid ticket number. Default
            format is 1 or more letters, then a hyphen, then 1 or more numbers.
            To allow any format, set to ``'.*'``.
            ''')
        self.TICKET_INPUT_FORMAT_REGEX = self.get_workflow_config(
            'ticketInputFormatRegex', default='[a-zA-Z]+-[0-9]+'
        )
        # ticketFormatCapitalize
        self.TICKET_FORMAT_CAPITALIZE_DOC = textwrap.dedent(
            '''\
            **Default:** ``true``

            If ``true``, letters in the ticket number will be capitalized after
            validation.
            ''')
        self.TICKET_FORMAT_CAPITALIZE = self.get_workflow_config(
            'ticketFormatCapitalize', default=True,
            config_type=self.TYPE_BOOL
        )

        # Confirmation Prompts -------------------------------------------------
        # finishBranchConfirmationPrompt
        self.FINISH_BRANCH_CONFIRMATION_PROMPT_DOC = textwrap.dedent(
            '''\
            **Default:** ``true``

            If ``true``, ``workflow finish`` will prompt for confirmation
            before unsetting unless ``-f`` is specified. If ``false``, will
            not prompt for confirmation unless ``-c`` is specified.
            ''')
        self.FINISH_BRANCH_CONFIRMATION_PROMPT = self.get_workflow_config(
            'finishBranchConfirmationPrompt', default=True,
            config_type=self.TYPE_BOOL
        )
        # unsetTemplateConfirmationPrompt
        self.UNSET_TEMPLATE_CONFIRMATION_PROMPT_DOC = textwrap.dedent(
            '''\
            **Default:** ``true``

            If ``true``, ``workflow unset-template`` will prompt for
            confirmation before unsetting unless ``-f`` is specified. If
            ``false``, will not prompt for confirmation unless ``-c`` is
            specified.
            ''')
        self.UNSET_TEMPLATE_CONFIRMATION_PROMPT = self.get_workflow_config(
            'unsetTemplateConfirmationPrompt', default=True,
            config_type=self.TYPE_BOOL
        )
        # cleanupConfirmationPrompt
        self.CLEANUP_CONFIRMATION_PROMPT_DOC = textwrap.dedent(
            '''\
            **Default:** ``true``

            If ``true``, ``workflow cleanup`` will prompt for confirmation 
            before cleaning unless ``-f`` is specified. If ``false``, will not 
            prompt for confirmation unless ``-c`` is specified.
            ''')
        self.CLEANUP_CONFIRMATION_PROMPT = self.get_workflow_config(
            'cleanupConfirmationPrompt', default=True,
            config_type=self.TYPE_BOOL
        )

        # END CONFIGS ==========================================================

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

    def call_config_command(self, *args, **kwargs):
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
        return self.call_config_command(*args, get=True, **kwargs)

    def unset_config(self, *args, **kwargs):
        return self.call_config_command(*args, unset=True, **kwargs)

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
