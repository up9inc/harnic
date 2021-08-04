import difflib
from collections import namedtuple

from objects import EntryDiff
from reader import load


DiffRecord = namedtuple('DiffEntry', ['pair', 'diff', 'tag'])

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
        # i_entries, j_entries = self.entries[:5], other.entries[:5]
        i_entries, j_entries = self.entries, other.entries
        sm = difflib.SequenceMatcher(None, i_entries, j_entries)
        opcodes = list(sm.get_opcodes())  # TODO: abuse iterator?
        sm.records = self._process_cmp_opcodes(opcodes, i_entries, j_entries)
        return sm

    def _process_cmp_opcodes(self, opcodes, i_entries, j_entries):
        result = []
        for permutation in opcodes:  # permutation(tag, i1, i2, j1, j2)
            tag, i1, i2, j1, j2 = permutation
            if tag == 'equal':
                for i, j in zip(range(i1, i2), range(j1, j2)):
                    pair = (i_entries[i], j_entries[j])
                    dr = DiffRecord(pair, EntryDiff(*pair), tag)
                    result.append(dr)
            elif tag == 'replace':
                for i in range(i1, i2):
                    dr = DiffRecord((i_entries[i], None), None, 'delete')
                    result.append(dr)
                for j in range(j1, j2):
                    dr = DiffRecord((None, j_entries[j]), None, 'insert')
                    result.append(dr)
            elif tag == 'delete':
                for i in range(i1, i2):
                    dr = DiffRecord((i_entries[i], None), None, tag)
                    result.append(dr)
            elif tag == 'insert':
                for j in range(j1, j2):
                    dr = DiffRecord((None, j_entries[j]), None, tag)
                    result.append(dr)
        return result