import difflib
import uuid
from enum import Enum

from tqdm import tqdm

from harnic.compare import EntryDiff


class DiffRecord:
    def __init__(self, pair, diff, tag):
        self.pair = pair
        self.diff = diff
        self.tag = tag
        self.id = uuid.uuid4()


class Pair:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __iter__(self):
        return iter((self.a, self.b))

    @property
    def partial(self):
        return not (self.a and self.b)

    @property
    def partial_entry(self):
        if not self.partial:
            return None
        return self.a if self.a else self.b


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
    sm.records, sm.reorders, sm.stats = _build_har_diff(sm.get_opcodes(), har1, har2)

    return sm


def _build_har_diff(opcodes, har1, har2):
    i_entries, j_entries = har1.entries, har2.entries
    records = []
    stats = {
        'from_count': len(har1.entries),
        'to_count': len(har2.entries),
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

    reorders = _calculate_reorders(records)
    reorders_stats = _calculate_reorders_stats(reorders, stats)
    stats = {
        'original': stats,
        'with_reorders': reorders_stats
    }

    return records, reorders, stats


def _calculate_reorders(records):
    entry_reorders = {}
    record_reorders = {}
    for record in records:
        if record.tag not in (PermTag.INSERT, PermTag.DELETE):
            continue
        entry = record.pair.partial_entry
        assert entry
        if entry in entry_reorders:
            record_reorders[entry_reorders[entry][0]] = {
                'to': record.id,
                'entry_diff': EntryDiff(entry, entry_reorders[entry][1])
            }
        else:
            entry_reorders[entry] = (record.id, entry)

    return record_reorders


def _calculate_reorders_stats(reorders, stats):
    stats = stats.copy()
    num_reorders = len(reorders)
    stats[PermTag.INSERT] -= num_reorders
    stats[PermTag.DELETE] -= num_reorders
    for reorder in reorders.values():
        tag_selector = PermTag.EQUAL if reorder['entry_diff'].equal else PermTag.DIFF
        stats[tag_selector] += 1
    stats['ratio'] = 2.0 * stats[PermTag.EQUAL] / (stats['from_count'] + stats['to_count'])

    return stats
