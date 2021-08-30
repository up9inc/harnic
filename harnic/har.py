from pathlib import Path

from termcolor import colored

from harnic.reader import load
from harnic.utils import sizeof_fmt


class HAR:

    def __init__(self, path):
        self.path = path
        self.entries = list(load(path))
        self._sort()

    def __repr__(self):
        return self.path

    def _sort(self, by='ts'):
        if by == 'ts':
            self.entries.sort(key=lambda e: e.request.get('_ts'))
        else:
            raise NotImplementedError()

    @property
    def size(self):
        return Path(self.path).stat().st_size

    def pretty_repr(self):
        name = colored(self.path, "yellow")
        num_entries = len(self.entries)
        return f'{name}: {num_entries} entries, {sizeof_fmt(self.size)}'
