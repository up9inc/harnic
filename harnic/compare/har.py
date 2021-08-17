import difflib
from collections import namedtuple
from enum import Enum

from tqdm import tqdm

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
    sm.records, sm.stats = _build_har_diff(sm.get_opcodes(), i_entries, j_entries)
    return sm


def _build_har_diff(opcodes, i_entries, j_entries):
    records = []
    stats = {
        PermTag.EQUAL: 0,
        PermTag.DIFF: 0,
        PermTag.INSERT: 0,
        PermTag.DELETE: 0,
    }
    for permutation in tqdm(opcodes):
        tag, i1, i2, j1, j2 = permutation
        if tag == 'equal':
            for i, j in zip(range(i1, i2), range(j1, j2)):
                pair = Pair(i_entries[i], j_entries[j])
                entry_diff = EntryDiff(*pair)
                tag_selector = PermTag.EQUAL if entry_diff.equal else PermTag.DIFF
                dr = DiffRecord(pair, entry_diff, tag_selector)
                records.append(dr)
                stats[tag_selector] += 1
        elif tag == 'replace':
            for i in range(i1, i2):
                dr = DiffRecord(Pair(i_entries[i], None), None, PermTag.DELETE)
                records.append(dr)
                stats[PermTag.DELETE] += 1
            for j in range(j1, j2):
                dr = DiffRecord(Pair(None, j_entries[j]), None, PermTag.INSERT)
                records.append(dr)
                stats[PermTag.INSERT] += 1
        elif tag == 'delete':
            for i in range(i1, i2):
                dr = DiffRecord(Pair(i_entries[i], None), None, PermTag(tag))
                records.append(dr)
                stats[PermTag.DELETE] += 1
        elif tag == 'insert':
            for j in range(j1, j2):
                dr = DiffRecord(Pair(None, j_entries[j]), None, PermTag(tag))
                records.append(dr)
                stats[PermTag.INSERT] += 1
        stats['ratio'] = 2.0 * stats[PermTag.EQUAL] / (len(i_entries) + len(j_entries))
    return records, stats
