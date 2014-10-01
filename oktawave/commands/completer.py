import shlex
import readline

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
        if (len(tokens) == 1):
            return (sorted([n + ' ' for n in self.cli.commands.keys() if n.lower().startswith(tokens[-1].lower())]) + [None])[stage]
        elif (len(tokens) == 2):
            return (sorted([c + ' ' for c in self.cli.commands[tokens[0]].commands.keys() if c.lower().startswith(tokens[-1].lower())]) + [None])[stage]
        else:
            param = self.cli.commands[tokens[0]].commands[tokens[1]].params[len(tokens) - 3]
            items = [x for x in param.type.list_items(self.ctx.api)]
            ret = []
            for item in items:
                for x in item:
                    ret.append(str(x))
            return (sorted([x + ' ' for x in ret if x.lower().startswith(tokens[-1].lower())]) + [None])[stage]
        return ([None])[stage]
