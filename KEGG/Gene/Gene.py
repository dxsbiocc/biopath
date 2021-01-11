# Copyright 2021 by dengxsh.
# All rights reserved.
#

"""Code to work with the KEGG Gene database.
Classes:
- Gene - A representation of a KEGG Gene.
"""
from KEGG.utils import Entry


class Gene(Entry):
    """Holds info from a KEGG Gene record.
    Attributes:
     - entry       The entry identifier.
     - name        A list of the gene names.
     - definition  The definition for the gene.
     - orthology   A list of 2-tuples: (orthology id, role)
     - organism    A tuple: (organism id, organism)
     - position    The position for the gene
     - motif       A list of 2-tuples: (database, list of link ids)
     - dblinks     A dict: (database, list of link ids)

     - pathway     A list of 2-tuples: (pathway id, pathway name)
     - network     A list of 2-tuples: (network id, network name)
     - element     A list of 2-tuples: (element id, element name)
     - disease     A list of 2-tuples: (disease id, disease name)
     - drug_target A list of 2-tuples: (drug name, drug ids)
     - structure   A list of 2-tuples: (database, list of link ids)
    """

    def __init__(self, entry: str, cache: bool=True) -> None:
        """Initialize new gene."""
        self.definition = ""
        self.orthology = []
        self.organism = tuple()
        self.position = ""
        self.motif = {}
        self.dblinks = {}

        self.pathway = []
        self.network = []
        self.element = []
        self.disease = []
        self.drug_target = []
        self.structure = []

        self.AA = ""
        self.NT = ""

        super().__init__(entry, cache)
        

    def _parse(self, text):
        """Parse a KEGG Gene informations.
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
            elif key == "orthology":
                ko, name = value.split(maxsplit=1)
                self.orthology.append((ko, name))
            elif key == "organism":
                tid, tname = value.split(maxsplit=1)
                self.organism = (tid, tname)
            elif key == "pathway":
                pid, pname = value.split(maxsplit=1)
                self.pathway.append((pid, pname))
            elif key == "position":
                self.position = value
            elif key == "motif":
                k, v = value.split(": ")
                self.motif[k] = v.split()
            elif key == "dblinks":
                k, v = value.split(": ")
                self.dblinks[k] = v.split()
            elif key == "disease":
                did, dname = value.split(maxsplit=1)
                self.disease.append((did, dname))
            elif key == "network":
                nvid, nvname = value.split(maxsplit=1)
                self.network.append((nvid, nvname))
            elif key == "element":
                nid, nname = value.split(maxsplit=1)
                self.element.append((nid, nname))
            elif key == "drug_target":
                dgname, dg = value.split(": ")
                dgs = dg.split()
                self.drug_target.append((dgname, dgs))
            elif key == "structure":
                if ":" in value:
                    k, v = value.split(": ")
                    v = v.split()
                else:
                    k, v = self.structure.pop()
                    v.extend(value.split())
                self.structure.append((k, v))
            elif key == "aaseq":
                if value.isalpha():
                    self.AA += value
            elif key == "ntseq":
                if value.isalpha():
                    self.NT += value