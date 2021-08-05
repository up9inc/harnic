import difflib
from collections import namedtuple
from enum import Enum

from harnic.compare import EntryDiff

DiffRecord = namedtuple('DiffRecord', ['pair', 'diff', 'tag'])
Pair = namedtuple('Pair', ['a', 'b'])


class PermTag(Enum):
    EQUAL = 'equal'
    INSERT = 'insert'
    DELETE = 'delete'
    REPLACE = 'replace'
    DIFF = 'diff'


def har_compare(har1, har2):
    # TODO: static can be junk
    # i_entries, j_entries = self.entries[:5], other.entries[:5]
    i_entries, j_entries = har1.entries, har2.entries
    sm = difflib.SequenceMatcher(None, i_entries, j_entries)
    sm.records = _build_har_diff_records(sm.get_opcodes(), i_entries, j_entries)
    return sm


def _build_har_diff_records(opcodes, i_entries, j_entries):
    result = []
    for permutation in opcodes:
        tag, i1, i2, j1, j2 = permutation
        if tag == 'equal':
            for i, j in zip(range(i1, i2), range(j1, j2)):
                pair = Pair(i_entries[i], j_entries[j])
                entry_diff = EntryDiff(*pair)
                dr = DiffRecord(pair, entry_diff, PermTag.EQUAL if entry_diff.equal else PermTag.DIFF)
                result.append(dr)
        elif tag == 'replace':
            for i in range(i1, i2):
                dr = DiffRecord(Pair(i_entries[i], None), None, PermTag.DELETE)
                result.append(dr)
            for j in range(j1, j2):
                dr = DiffRecord(Pair(None, j_entries[j]), None, PermTag.INSERT)
                result.append(dr)
        elif tag == 'delete':
            for i in range(i1, i2):
                dr = DiffRecord(Pair(i_entries[i], None), None, PermTag(tag))
                result.append(dr)
        elif tag == 'insert':
            for j in range(j1, j2):
                dr = DiffRecord(Pair(None, j_entries[j]), None, PermTag(tag))
                result.append(dr)
    return result
