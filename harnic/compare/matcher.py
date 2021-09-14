import difflib
import uuid
from collections import defaultdict, deque
from enum import Enum

from tqdm import tqdm

from harnic.compare import EntryDiff
from harnic.difflib_patcher import patch as difflib_patcher

difflib_patcher()


class DiffRecord:
    def __init__(self, pair, diff, tag, reordering=None):
        self.pair = pair
        self.diff = diff
        self.tag = tag
        self.reordering = reordering
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


def files_compare(file1, file2):
    # TODO: static can be junk
    i_entries, j_entries = file1.entries, file2.entries
    sm = difflib.SequenceMatcher(None, i_entries, j_entries)
    sm.records, sm.reorders, sm.stats = _build_files_diff(sm.get_opcodes(), file1, file2)
    sm.file1, sm.file2 = file1, file2

    return sm


def _build_files_diff(opcodes, file1, file2):
    i_entries, j_entries = file1.entries, file2.entries
    records = []
    stats = {
        PermTag.EQUAL: 0,
        PermTag.DIFF: 0,
        PermTag.INSERT: 0,
        PermTag.DELETE: 0,
        '_diff_scores_sum': 0,
    }
    perms_total = _calculate_permutations_total_number(opcodes)
    with tqdm(total=perms_total, desc='Constructing diff records') as pbar:
        for permutation in opcodes:
            tag, i1, i2, j1, j2 = permutation
            if tag == 'equal':
                for i, j in zip(range(i1, i2), range(j1, j2)):
                    pair = Pair(i_entries[i], j_entries[j])
                    entry_diff = EntryDiff(*pair)
                    tag_selector = PermTag.EQUAL if entry_diff.equal else PermTag.DIFF
                    dr = DiffRecord(pair, entry_diff, tag_selector)
                    records.append(dr)
                    stats[tag_selector] += 1
                    if tag_selector == PermTag.DIFF:
                        stats['_diff_scores_sum'] += entry_diff.score['final']
                    pbar.update()
            elif tag == 'replace':
                for i in range(i1, i2):
                    dr = DiffRecord(Pair(i_entries[i], None), None, PermTag.DELETE)
                    records.append(dr)
                    stats[PermTag.DELETE] += 1
                    pbar.update()
                for j in range(j1, j2):
                    dr = DiffRecord(Pair(None, j_entries[j]), None, PermTag.INSERT)
                    records.append(dr)
                    stats[PermTag.INSERT] += 1
                    pbar.update()
            elif tag == 'delete':
                for i in range(i1, i2):
                    dr = DiffRecord(Pair(i_entries[i], None), None, PermTag(tag))
                    records.append(dr)
                    stats[PermTag.DELETE] += 1
                    pbar.update()
            elif tag == 'insert':
                for j in range(j1, j2):
                    dr = DiffRecord(Pair(None, j_entries[j]), None, PermTag(tag))
                    records.append(dr)
                    stats[PermTag.INSERT] += 1
                    pbar.update()

    stats['ratio'] = 2.0 * (stats[PermTag.EQUAL] + stats['_diff_scores_sum']) / (len(file1) + len(file2))

    reorders = _calculate_reorders(records)
    reorders_stats = _calculate_reorders_stats(reorders, stats, (file1, file2))
    stats = {
        'with_reorders': reorders_stats,
        'strict_order': stats,
    }
    return records, reorders, stats


def _calculate_permutations_total_number(opcodes):
    total = 0
    for permutation in opcodes:
        tag, i1, i2, j1, j2 = permutation
        if tag == 'equal':
            total += i2 - i1
        elif tag == 'replace':
            total += (i2 - i1 + j2 - j1)
        elif tag == 'delete':
            total += i2 - i1
        elif tag == 'insert':
            total += j2 - i1
    return total


def _calculate_reorders(records):
    entry_reorders = {}
    record_reorders = []
    inserts = [record for record in records if record.tag == PermTag.INSERT]
    deletes = [record for record in records if record.tag == PermTag.DELETE]

    inserts_idx = defaultdict(deque)
    for insert in inserts:
        inserts_idx[insert.pair.partial_entry].append(insert)

    deletes_idx = defaultdict(deque)
    for delete in deletes:
        deletes_idx[delete.pair.partial_entry].append(delete)

    reorders_keys = inserts_idx.keys() & deletes_idx.keys()

    pairs = []
    for key in reorders_keys:
        try:
            insert = inserts_idx[key].pop()
            delete = deletes_idx[key].pop()
        except IndexError:
            continue
        insert_first = insert.pair.partial_entry.request['_ts'] >= delete.pair.partial_entry.request['_ts']
        pairs.append((insert, delete) if insert_first else (delete, insert))

    for pair in pairs:
        from_record, to_record = pair
        record_reorders.append({
            'from': from_record.id,
            'to': to_record.id,
            'entry_diff': EntryDiff(from_record.pair.partial_entry, to_record.pair.partial_entry)
        })

    return record_reorders


def _calculate_reorders_stats(reorders, stats, files):
    file1, file2 = files
    stats = stats.copy()
    num_reorders = len(reorders)
    stats[PermTag.INSERT] -= num_reorders
    stats[PermTag.DELETE] -= num_reorders
    for reorder in reorders:
        tag_selector = PermTag.EQUAL if reorder['entry_diff'].equal else PermTag.DIFF
        stats[tag_selector] += 1
        if tag_selector == PermTag.DIFF:
            stats['_diff_scores_sum'] += reorder['entry_diff'].score['final']
    stats['ratio'] = 2.0 * (stats[PermTag.EQUAL] + stats['_diff_scores_sum']) / (len(file1) + len(file2))

    return stats


def create_compact_records_index(diff):
    reordering_records = [
        DiffRecord(
            Pair(reordering['entry_diff'].a, reordering['entry_diff'].b),
            reordering['entry_diff'],
            PermTag.EQUAL if reordering['entry_diff'].equal else PermTag.DIFF,
            reordering
        )
        for reordering in diff.reorders
    ]
    reorders_index_reverse_lookup = {r.reordering['from']: r for r in reordering_records}

    reorders_index = {r.id: r for r in reordering_records}
    original_index = {r.id: r for r in diff.records}
    index = {**original_index, **reorders_index}

    strict_order_records = [record.id for record in diff.records]
    reordered_records = []

    # helps to clean reordered_records from destinations
    destinations = [r['to'] for r in diff.reorders]

    assert len(reordering_records) == len(reorders_index_reverse_lookup) == len(destinations)  # sanity check

    for record in diff.records:
        if record.id in reorders_index_reverse_lookup:
            reordered_records.append(reorders_index_reverse_lookup[record.id].id)
        elif record.id in destinations:
            continue
        else:
            reordered_records.append(record.id)

    return {
        'index': index,
        'strict_order_records': strict_order_records,
        'reordered_records': reordered_records,
    }
