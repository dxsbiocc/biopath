# Copyright 2021 by dengxsh.
# All rights reserved.
#

"""Code to work with the KEGG Reaction database.
Classes:
- Reaction - A representation of a KEGG Reaction.
"""
from KEGG.utils import Entry


class Reaction(Entry):
    
    def __init__(self, entry: str, cache: bool=True) -> None:
        """Initialize new Reaction."""
        self.definition = ""
        self.equation = ""
        self.remark = ""
        self.comment = ""
        self.rclass = ""
        self.enzyme = []
        self.pathway = []
        self.orthology = []
        self.dblinks = {}

        super().__init__(entry, cache)
        
    def _parse(self, text: str) -> None:
        """Parse a KEGG reaction informations.
        """
        key = ""
        for line in text.split('\n'):
            if line[:12].strip():
                key = line[:12].strip().lower()
            value = line[12:].strip()
            if key == "entry":
                self.entry = value.split()[0]
            elif key == "name":
                self.name.extend(value.split(', '))
            elif key == "definition":
                self.definition = value
            elif key == "equation":
                self.equation = value
            elif key == "remake":
                self.remark = value.split(": ")[-1]
            elif key == "rclass":
                self.rclass = value
            elif key == "enzyme":
                self.enzyme.extend(value.split())
            elif key == "pathway":
                self.pathway.append(value.split(maxsplit=1))
            elif key == "orthology":
                self.orthology.append(value.split(maxsplit=1))
            elif key == "dblinks":
                k, v = value.split(": ")
                self.dblinks[k] = v.split()
            