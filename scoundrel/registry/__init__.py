from scoundrel import log
from scoundrel.registry import resource

LOG = log.LOG


class Registry(object):
    def __init__(self):
        self._resources = {}
        self._indices = {}

    def add(self, resource):
        self._resources[resource.name] = resource
        for tag in resource.tags:
            self._indices.setdefault(tag, [])
            self._indices[tag].append(resource)

    def remove(self, resource):
        if resource.name not in self._resources:
            LOG.error("Resource %s not in registry!" % resource.name)
            return
        for tag in resource.tags:
            for res in self._indices.get(tag, []):
                self._indices[tag].remove(res)

        self._resources.pop(resource.name)
        self._indices.remove(resource.name)

    def get_named(self, name):
        if name in self._resources:
            return self._resources[name]
        LOG.error("No resource named %s" % name)

    def get_one(self, *tags):
        matches = []
        for tag in tags:
            matches.extend(self._indices.get(tag, []))

        if len(matches) > 0:
            return matches[0]
        LOG.error("No resources match tags %s" % tags)
