"""Command line formatting, prompts, and other utilities."""

from blessings import Terminal

# Globals

_term = Terminal()
COLORS = {
    None: str,
    'error': _term.red,
    'error_title': _term.bold_red,
    'warning': _term.yellow,
    'success': _term.green,
    'info': _term.cyan,
    'prompt': _term.magenta,
}
INDENT = ' ' * 4


# Output Formatting

def print_error(*lines):
    lines = list(lines)
    line = lines.pop(0)
    print(COLORS['error_title'](str(line)))
    if lines:
        for line in lines:
            print(INDENT + COLORS['error'](line))


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
    text = COLORS['prompt']('> ' + (
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

