# Copyright 2021 by dengxsh.
# All rights reserved.
#

"""Code to work with the KEGG Glycan database.
Classes:
 - Glycan - Store the information from a KEGG Glycan record.
"""
from KEGG.utils import Entry


class Glycan(Entry):
    
    def __init__(self, entry: str, cache: bool) -> None:
        
        self.composition = []
        self.mass = ""
        # self.structure = []
        # self.remark = ""
        # self.comment = ""
        # self.reaction = []
        # self.pathway = []
        # self.enzyme = []
        # self.orthology = []
        # self.reference = []
        self.dblinks = {}
        # self.kcf_data = {
        # }

        super().__init__(entry, cache=cache)


    def _parse(self, text: str) -> None:
        key = ""
        for line in text.split("\n"):
            if line[:12].strip():
                key = line[:12].strip().lower()
            value = line[12:].strip()
            if key == "entry":
                self.entry = value.split()[0]
            elif key == "name":
                self.name.append(value.strip(";"))
            elif key == "composition":
                self.composition.extend(value.split())
            elif key == "mass":
                self.mass = value
            elif key == "dblinks":
                k, v = value.split(": ")
                self.dblinks[k] = v.split()