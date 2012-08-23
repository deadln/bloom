"""
Provides common utility functions for bloom.
"""
import sys

from subprocess import check_call, check_output, CalledProcessError, PIPE

_ansi = {}


def create_temporary_directory(prefix_dir=None):
    """Creates a temporary directory and returns its location"""
    from tempfile import mkdtemp
    return mkdtemp(prefix='bloom_', dir=prefix_dir)


def ansi(key):
    """Returns the escape sequence for a given ansi color key"""
    global _ansi
    return _ansi[key]


def enable_ANSI_colors():
    """
    Populates the global module dictionary `ansi` with ANSI escape sequences.
    """
    global _ansi
    colors = [
        'black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white'
    ]
    _ansi = {
        'escape': '\033', 'reset': 0,
        'boldon': 1, 'italicson': 3, 'ulon': 4, 'invon': 7,
        'boldoff': 22, 'italicsoff': 23, 'uloff': 24, 'invoff': 27,
    }

    # Convert plain numbers to escapes
    for key in _ansi:
        if key != 'escape':
            _ansi[key] = '{0}[{1}m'.format(_ansi['escape'], _ansi[key])

    # Foreground
    for index, color in enumerate(colors):
        _ansi[color + 'f'] = '{0}[{1}m'.format(_ansi['escape'], 30 + index)

    # Background
    for index, color in enumerate(colors):
        _ansi[color + 'b'] = '{0}[{1}m'.format(_ansi['escape'], 40 + index)


def disable_ANSI_colors():
    """
    Sets all the ANSI escape sequences to empty strings, effectively disabling
    console colors.
    """
    global _ansi
    for key in _ansi:
        _ansi[key] = ''

enable_ANSI_colors()


def maybe_continue(default='y'):
    """Prompts the user for continuation"""
    default = default.lower()
    msg = "{0}Continue ".format(ansi('boldon'))
    if default == 'y':
        msg += "{0}[Y/n]? {1}".format(ansi('yellowf'), ansi('reset'))
    else:
        msg += "{0}[y/N]? {1}".format(ansi('yellowf'), ansi('reset'))

    while True:
        response = raw_input(msg)
        if not response:
            response = default

        response = response.lower()
        if response not in ['y', 'n']:
            error_msg = ansi('redf') + 'Reponse `' + response
            error_msg += '` was not recognized, please use one of y, Y, n, N.'
            error_msg += ansi('reset')
            print(error_msg)
        else:
            break

    if response == 'n':
        return False
    return True


def get_version():
    """Returns the version number from a given tag/branch"""
    pass  # TODO: implement this


def get_upstream_version():
    """Returns the upstream version number from a given upstream tag/branch"""
    pass  # TODO: implement this


def bailout(reason='Exiting.'):
    """Exits bloom for a given reason"""
    print(ansi('redf') + ansi('boldon') + reason + ansi('reset'))
    sys.exit(1)


def read_stack_xml(file_path):
    """
    Returns a dictionary representation of a stack xml file.

    :param file_path: path to stack xml file to be converted
    :returns: dictionary representation of the stack xml file
    """
    pass  # TODO: implement this


def execute_command(cmd, shell=True, autofail=True, silent=True):
    """
    Executes a given command using vcstools' run_shell_command function.
    """
    io_type = None
    if silent:
        io_type = PIPE
    try:
        result = check_call(cmd, shell=True, stdout=io_type, stderr=io_type)
    except CalledProcessError as cpe:
        result = cpe.returncode
    if result != 0 and autofail:
        raise RuntimeError("Failed to execute the command: {0}".format(cmd))
    return result


def get_current_git_branch(directory=None):
    """
    Returns the current git branch by parsing the output of `git branch`

    This will raise a RuntimeError if the current working directory is not
    a git repository.  If no branch could be determined it will return None,
    i.e. (no branch) will return None.
    """
    cmd = 'git branch --no-color'
    output = check_output(cmd, shell=True, cwd=directory)
    output = output.splitlines()
    for token in output:
        if token.strip().startswith('*'):
            token = token[2:]
            if token == '(no branch)':
                return None
            return token

    return None


def error(msg):
    """Prints a message as an error"""
    print(ansi('redf') + ansi('boldon') + 'Error: ' + msg + ansi('reset'))
