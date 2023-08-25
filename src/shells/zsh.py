from time import time
import os
from subprocess import Popen, PIPE
from tempfile import gettempdir
from uuid import uuid4
from ..utils import DEVNULL
from .generic import Generic


class Zsh(Generic):

    def app_alias(self, alias_name):
        # It is VERY important to have the variables declared WITHIN the function
        return '''
            {name} () {{
                export KELP_SHELL=zsh;
                export KELP_ALIAS={name};
                KELP_SHELL_ALIASES=$(alias);
                export KELP_SHELL_ALIASES;
                KELP_HISTORY="$(fc -ln -10)";
                export KELP_HISTORY;
                KELP_CMD=$(
                    command-kelp $@
                ) && eval $KELP_CMD;
                unset KELP_HISTORY;
            }}
        '''.format(
            name=alias_name)

    def _parse_alias(self, alias):
        name, value = alias.split('=', 1)
        if value[0] == value[-1] == '"' or value[0] == value[-1] == "'":
            value = value[1:-1]
        return name, value

    def get_aliases(self):
        raw_aliases = os.environ.get('KELP_SHELL_ALIASES', '').split('\n')
        return dict(self._parse_alias(alias)
                    for alias in raw_aliases if alias and '=' in alias)

    def _get_history_file_name(self):
        return os.environ.get("HISTFILE",
                              os.path.expanduser('~/.zsh_history'))

    def _get_history_line(self, command_script):
        return u': {}:0;{}\n'.format(int(time()), command_script)

    def _script_from_history(self, line):
        if ';' in line:
            return line.split(';', 1)[1]
        else:
            return ''

    def how_to_configure(self):
        return self._create_shell_configuration(
            content=u'eval $(kelp-alias)',
            path='~/.zshrc',
            reload='source ~/.zshrc')

    def _get_version(self):
        """Returns the version of the current shell"""
        proc = Popen(['zsh', '-c', 'echo $ZSH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        return proc.stdout.read().decode('utf-8').strip()