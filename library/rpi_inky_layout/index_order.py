class IndexOrder():

    @classmethod
    def alternating(cls, count):
        """"Generate an list containing alternate indexes.
            For distributing adjustments.
        """
        if count < 1:
            return []
        if count == 1:
            return [0]
        _lowIndexes = [n for n in range(0, int(count / 2))]
        _highIndexes = [n + count - 1 for n in range(0, int(-count / 2), -1)]
        _indexes = [0] * (len(_lowIndexes)+len(_highIndexes))
        _indexes[::2] = _lowIndexes
        _indexes[1::2] = _highIndexes
        if count % 2 == 1:
            _indexes = _indexes + [int(count / 2)]
        return _indexes
