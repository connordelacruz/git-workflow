"""Command line formatting, prompts, and other utilities."""

from blessings import Terminal

# Globals

_term = Terminal()

# Keys into COLORS
ERROR = 'error'
ERROR_TITLE = 'error_title'
WARNING = 'warning'
SUCCESS = 'success'
INFO = 'info'
PROMPT = 'prompt'
#: Dictionary mapping indices to formatting functions
COLORS = {
    None: str,
    ERROR: _term.red,
    ERROR_TITLE: _term.bold_red,
    WARNING: _term.yellow,
    SUCCESS: _term.green,
    INFO: _term.cyan,
    PROMPT: _term.magenta,
}
#: String to use when indenting output
INDENT = ' ' * 4


# Output Formatting

def print_error(*lines):
    lines = list(lines)
    line = lines.pop(0)
    print(COLORS[ERROR_TITLE](str(line)))
    if lines:
        for line in lines:
            print(INDENT + COLORS[ERROR](line))


# User Input Prompts

def sanitize_input(val):
    return val.strip()

class ValidationError(Exception):
    """Raised if input validation fails"""
    pass


def validate_optional_prompt(val, error_msg=None):
    # TODO doc
    return val

def validate_nonempty(val, error_msg=None):
    """Raises ValidationError if val is empty

    :param val: Input to validate
    :param error_msg: (Optional) Custom error text to print if val is invalid

    :return: Validated input
    """
    if not val:
        raise ValidationError(error_msg or 'Please enter some text.')
    return val


def prompt(prompt_text, *extended_description,
           default_val=None, validate_function=validate_nonempty,
           sanitize_function=sanitize_input, format_function=None,
           invalid_msg=None, initial_input=None, trailing_newline=True):
    # TODO DOC
    # If input for this prompt was given via an argument, attempt to validate
    # it and bypass prompt
    if initial_input is not None:
        try:
            initial_input = sanitize_function(initial_input)
            if format_function is not None:
                initial_input = format_function(initial_input)
            val = validate_function(initial_input, invalid_msg)
        except ValidationError as e:
            print_error(e)
        else:
            return val

    if extended_description:
        print(*extended_description, sep='\n')
    text = COLORS[PROMPT]('> ' + (
        '{} [{}]'.format(prompt_text, default_val) if default_val is not None else prompt_text
    ) + ': ')

    while True:
        val = sanitize_function(input(text))
        if default_val is not None and not val:
            val = default_val
        if format_function is not None:
            val = format_function(val)
        try:
            val = validate_function(val, invalid_msg)
        except ValidationError as e:
            print_error(e)
            continue
        break
    if trailing_newline:
        print('')
    return val

