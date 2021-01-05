"""File-related utilities"""
import re


def sanitize_filename(filename, allow_spaces=False):
    """Strips invalid characters from a filename.

    Considers `POSIX "fully portable filenames"
    <http://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap03.html#tag_03_282>`__
    valid. These include:

        A-Z a-z 0-9 ._-

    Filenames cannot begin with a hyphen.

    :param filename: The desired file name (without path)
    :param allow_spaces: (Default = False) If True, spaces will be considered
        valid characters

    :return: Filename with invalid characters removed
    """
    regex = r'^-|[^\d\w\. -]' if allow_spaces else r'^-|[^\d\w\.-]'
    return re.sub(regex, '', filename)
