class Resource(object):
    def __init__(self, name, data, tags):
        self._name = name
        self._data = data
        self._tags = tags

    @property
    def name(self):
        return self._name

    @property
    def tags(self):
        return self._tags

    @property
    def data(self):
        return self._data
