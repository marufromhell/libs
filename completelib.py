import os
import readline
import re
"""
Complib
This module provides a command line completion library for Python.
GPLv3
email: maru@lithium-dev.xyz (pgp attached)
signal: maru.222
BTC: 16innLYQtz123HTwNLY3vScPmEVP7tob8u
ETH: 0x48994D78B7090367Aa20FD5470baDceec42cAF62 
XMR: 49dNpgP5QSpPDF1YUVuU3ST2tUWng32m8crGQ4NuM6U44CG1ennTvESWbwK6epkfJ6LuAKYjSDKqKNtbtJnU71gi6GrF4Wh
"""
def compile(list): #list is the command list if not use globals()
    global commands
    commands = list
    comp = Completer()
    readline.set_completer_delims('\t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(comp.complete)
    return commands

RE_SPACE = re.compile('.*\\s+$', re.M)

class Completer(object):

        def _listdir(self, root):
            "List directory 'root' appending the path separator to subdirs."
            res = []
            for name in os.listdir(root):
                path = os.path.join(root, name)
                if os.path.isdir(path):
                    name += os.sep
                res.append(name)
            return res

        def _complete_path(self, path=None):
            "Perform completion of filesystem path."
            if not path:
                return self._listdir('.')
            dirname, rest = os.path.split(path)
            tmp = dirname if dirname else '.'
            res = [os.path.join(dirname, p)
                    for p in self._listdir(tmp) if p.startswith(rest)]
            # more than one match, or single match which does not exist (typo)
            if len(res) > 1 or not os.path.exists(path):
                return res
            # resolved to a single directory, so return list of files below it
            if os.path.isdir(path):
                return [os.path.join(path, p) for p in self._listdir(path)]
            # exact file match terminates this completion
            return [path + ' ']

        def complete_extra(self, args):
            "Completions for the 'extra' command."
            if not args:
                return self._complete_path('.')
            # treat the last arg as a path and complete it
            return self._complete_path(args[-1])

        def complete(self, text, state):
            "Generic readline completion entry point."
            buffer = readline.get_line_buffer()
            line = readline.get_line_buffer().split()
            # show all commands
            if not line:
                return [c + ' ' for c in commands][state]
            # account for last argument ending in a space
            if RE_SPACE.match(buffer):
                line.append('')
            # resolve command to the implementation function
            cmd = line[0].strip()
            if cmd in commands:
                impl = getattr(self, 'complete_%s' % cmd)
                args = line[1:]
                if args:
                    return (impl(args) + [None])[state]
                return [cmd + ' '][state]
            results = [c + ' ' for c in commands if c.startswith(cmd)] + [None]
            return results[state]

