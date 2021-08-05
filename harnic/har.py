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
