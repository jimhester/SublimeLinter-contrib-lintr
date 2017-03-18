#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by James Hester
# Copyright (c) 2014 James Hester
#
# License: MIT
#

"""This module exports the Lintr plugin class."""

from SublimeLinter.lint import Linter, util


class Lintr(Linter):

    """Provides an interface to lintr R package."""

    syntax = ['r', 'enhanced-r']
    executable = 'R'
    # version_args = '--slave --restore --no-save -e "packageVersion(\\\"lintr\\\")"'
    version_args = '--slave --restore --no-save -e "packageVersion(\'lintr\')"' # single quotes appear to work under Windows. Not sure for other OSes.
    version_re = r'(?P<version>\d+\.\d+\.\d+)'
    version_requirement = '>= 0.1.0'
    defaults = {
        'linters': 'default_linters',
        'cache': 'TRUE'
    }
    regex = (
        r'^.+?:(?P<line>\d+):(?P<col>\d+): '
        r'(?:(?P<error>error)|(?P<warning>warning|style)): '
        r'(?P<message>.+)'
    )
    multiline = False
    line_col_base = (1, 1)
    tempfile_suffix = None
    error_stream = util.STREAM_BOTH
    selectors = {}
    word_re = None
    inline_settings = None
    inline_overrides = None
    comment_re = r'#'
    tempfile_suffix = 'lintr'

    def cmd(self):
        """Return a list with the command line to execute."""

        settings = self.get_view_settings()
        command = 'library(lintr);lint(cache = {0}, commandArgs(TRUE), {1})'.format(settings['cache'],
                                                                                    settings['linters'])
        return [self.executable_path,
                '--slave',
                '--restore',
                '--no-save',
                '-e',
                command,
                '--args',
                '@']