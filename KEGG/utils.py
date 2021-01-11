from KEGG.REST import kegg_get
import os


class Entry(object):

    def __init__(self, entry: str, cache: bool=True) -> None:
        self.entry = entry
        self.name = []

        info = get_cached(entry, cache)
        if info:
            self._parse(info)

    def __str__(self) -> str:
        return self.entry
    
    def __repr__(self) -> str:
        if self.entry and self.name:
            return "< Structure [ %s ], entry=%s, name=%s, ... >" %(self.__class__.__name__, self.entry, self.name[0])
        else:
            return "The input '%s' doesn't look like a valid gene entry!\nPlease try arain." % self.entry

    def _parse(self, text: str) -> None:
        pass

    

def get_cached(entry: str, cache: bool) -> str:
    """Get entry information, using API tools
    """
    pwd = os.path.dirname(__file__)
    data = os.path.join(pwd, 'data')
    if not os.path.exists(data):
        os.mkdir(data)
    file = os.path.join(data, entry.replace(":", "_") + '.txt')
    # if file exists, return this file
    if os.path.exists(file):
        with open(file, 'r') as f:
            return f.read()
    # otherwise, get information using API tools
    info = kegg_get(entry)
    # caching inforation in local file, if need.
    if info and cache:
        with open(file, 'w') as f: f.write(info)
    return info