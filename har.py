import difflib

from objects import EntryDiff
from reader import load


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

    def compare(self, other):
        # TODO: static can be junk
        i_entries, j_entries = self.entries[:5], other.entries[:5]
        # i_entries, j_entries = self.entries, other.entries
        sm = difflib.SequenceMatcher(None, i_entries, j_entries)
        opcodes = list(sm.get_opcodes())  # TODO: abuse iterator?
        sm.opcodes_advanced = self._process_cmp_opcodes(opcodes, i_entries, j_entries)
        return sm

    def _process_cmp_opcodes(self, opcodes, i_entries, j_entries):
        for permutation in opcodes:  # permutation(tag, i1, i2, j1, j2)
            tag, i1, i2, j1, j2 = permutation
            if tag == 'equal':
                for i, j in zip(range(i1, i2), range(j1, j2)):
                    i_entry = i_entries[i]
                    j_entry = j_entries[j]
                    diff = EntryDiff(i_entry, j_entry).diff

