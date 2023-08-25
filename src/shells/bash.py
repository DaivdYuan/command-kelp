import os
from subprocess import Popen, PIPE
from tempfile import gettempdir
from uuid import uuid4
from .generic import Generic
from ..utils import DEVNULL


class Bash(Generic):

    def app_alias(self, alias_name):
        # It is VERY important to have the variables declared WITHIN the function
        return '''
            function {name} () {{
                export KELP_SHELL=bash;
                export KELP_ALIAS={name};
                export KELP_SHELL_ALIASES=$(alias);
                export KELP_HISTORY=$(fc -ln -10);
                KELP_CMD=$(
                    command-kelp "$@"
                ) && eval "$KELP_CMD";
                unset KELP_HISTORY;
            }}
        '''.format(
            name=alias_name)

    def _parse_alias(self, alias):
        name, value = alias.replace('alias ', '', 1).split('=', 1)
        if value[0] == value[-1] == '"' or value[0] == value[-1] == "'":
            value = value[1:-1]
        return name, value

    def get_aliases(self):
        raw_aliases = os.environ.get('KELP_SHELL_ALIASES', '').split('\n')
        return dict(self._parse_alias(alias)
                    for alias in raw_aliases if alias and '=' in alias)

    def _get_history_file_name(self):
        return os.environ.get("HISTFILE",
                              os.path.expanduser('~/.bash_history'))

    def _get_history_line(self, command_script):
        return u'{}\n'.format(command_script)

    def how_to_configure(self):
        if os.path.join(os.path.expanduser('~'), '.bashrc'):
            config = '~/.bashrc'
        elif os.path.join(os.path.expanduser('~'), '.bash_profile'):
            config = '~/.bash_profile'
        else:
            config = 'bash config'

        return self._create_shell_configuration(
            content=u'eval "$(kelp-alias)"',
            path=config,
            reload=u'source {}'.format(config))

    def _get_version(self):
        """Returns the version of the current shell"""
        proc = Popen(['bash', '-c', 'echo $BASH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        return proc.stdout.read().decode('utf-8').strip()