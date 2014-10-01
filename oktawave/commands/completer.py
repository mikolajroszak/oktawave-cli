import shlex
import readline
import click

class Completer(object):
    def __init__(self, cli, ctx):
        self.cli = cli
        self.ctx = ctx

    def tokenize(self, buf):
        try:
            tokens = shlex.split(buf, False, True)
        except ValueError:
            buf += '"'
        tokens = shlex.split(buf, False, True)
        return tokens
                
    def complete(self, text, stage):
        buf = ' ' + readline.get_line_buffer()
        tokens = self.tokenize(buf)
        if buf[-1].isspace():
            tokens.append('')
        while len(tokens) > 0 and tokens[0].startswith('-'):
            tokens.pop(0)
        if (len(tokens) == 1):
            return (sorted([n + ' ' for n in self.cli.commands.keys() if n.lower().startswith(tokens[-1].lower())]) + [None])[stage]
        elif (len(tokens) == 2):
            return (sorted([c + ' ' for c in self.cli.commands[tokens[0]].commands.keys() if c.lower().startswith(tokens[-1].lower())]) + [None])[stage]
        else:
            param = self.cli.commands[tokens[0]].commands[tokens[1]].params[len(tokens) - 3]
            completions = []
            if hasattr(param.type, 'list_completions') and callable(getattr(param.type, 'list_completions')):
                completions = param.type.list_completions(self.ctx.api)
            elif isinstance(param.type, click.types.Choice):
                completions = param.type.choices
            return (sorted([x + ' ' for x in completions if x.lower().startswith(tokens[-1].lower())]) + [None])[stage]
        return ([None])[stage]
