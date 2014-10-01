from ConfigParser import RawConfigParser
import os
import sys
import readline

import click

from oktawave.commands.account import Account
from oktawave.commands.container import Container
from oktawave.commands.context import OktawaveCliContext, pass_context
from oktawave.commands.oci import OCI
from oktawave.commands.ocs import OCS
from oktawave.commands.opn import OPN
from oktawave.commands.ordb import ORDB
from oktawave.commands.ovs import OVS
from oktawave.commands.template import Template
from oktawave.commands.completer import Completer

VERSION = '0.9.0'


@click.group()
@click.option('-c', '--config', help='Specify configuration file', type=click.Path(dir_okay=False),
              default=os.path.expanduser('~/.oktawave-cli/config'))
@click.option('-d', '--debug/--no-debug', help='Debug output')
@click.option('-u', '--username', help='Oktawave username', required=False)
@click.option('-p', '--password', help='Oktawave password', required=False)
@click.option('-ocsu', '--ocs-username', help='OCS username', required=False)
@click.option('-ocsp', '--ocs-password', help='OCS password', required=False)
@click.option('-i', '--interactive/--no-interactive', help='Interactive mode', required=False)
@click.version_option(VERSION)
@pass_context
def cli(ctx, config=None, username=None, password=None, ocs_username=None, ocs_password=None, debug=False, interactive=False):
    cp = {}

    def get_config_value(section, key, override):
        if override:
            return override
        if 'cp' not in cp:
            cp['cp'] = RawConfigParser()
            cp['cp'].read(config)
        return cp['cp'].get(section, key)

    assert isinstance(ctx, OktawaveCliContext)
    api_username = get_config_value('Auth', 'username', username)
    api_password = get_config_value('Auth', 'password', password)
    if os.path.exists(config):
        ocs_username = get_config_value('OCS', 'username', ocs_username)
        ocs_password = get_config_value('OCS', 'password', ocs_password)
    ctx.init_output()
    ctx.init_api(api_username, api_password, debug)
    ctx.init_ocs(ocs_username, ocs_password)
    if interactive:
        interactive_cli(ctx)

def interactive_cli(ctx):
    print "Welcome to Oktawave CLI, version " + VERSION + '.'
    print 'Type a command or "help" to get help.'
    readline.parse_and_bind('tab: complete')
    readline.parse_and_bind('set editing-mode vi')
    while True:
        c = Completer(cli, ctx)
        readline.set_completer(lambda text, stage: c.complete(text, stage))
        try:
            line = raw_input(ctx.api.username + '@oktawave> ')
        except EOFError:
            line = 'exit'
        except KeyboardInterrupt:
            line = 'exit'
        words = c.tokenize(line)
        if len(words) >= 1:
            if words[0] == 'exit':
                print "Bye."
                sys.exit(0)
            if words[len(words) - 1] == 'help' and len(words) <= 2:
                words[len(words) - 1] = '--help'
        sys.argv = [sys.argv[0]] + words
        try:
            cli()
        except SystemExit:
            pass

cli.add_command(Account)
cli.add_command(OCI)
cli.add_command(OCS)
cli.add_command(OVS)
cli.add_command(ORDB)
cli.add_command(Container)
cli.add_command(OPN)
cli.add_command(Template)

if __name__ == '__main__':
    cli()
