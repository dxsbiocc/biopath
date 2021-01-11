# Copyright 2021 by dengxsh.
# All rights reserved.
#

"""Code to work with the KEGG Enzyme database.
Classes:
 - Enzyme - Store the information from a KEGG Enzyme record.
"""
from KEGG.utils import Entry
import re


class Enzyme(Entry):
    """Holds info from a KEGG Enzyme record.
    Attributes:
     - entry       The EC number (with the 'EC ').
     - name        A list of the enzyme names.
     - classname   A list of the classification terms.
     - sysname     The systematic name of the enzyme.
     - reaction    A list of the reaction description strings(IUBMB).
     - all_reac    A list of the reaction description strings(KEGG).
     - substrate   A list of the substrates.
     - product     A list of the products.

     - comment     A list of the comment strings.
     - pathway     A list of 3-tuples: (database, id, pathway)
     - genes       A dict: (organism, list of gene ids)
     - disease     A list of 3-tuples: (database, id, disease)
     - orthology   A list of 2-tuples: (orthology id, role)
     - dblinks     A dict: (database, list of db ids)
     - reference   A list of 3-tuples: (authors, title, journal)
    """
    def __init__(self, entry: str, cache: bool =True) -> None:
        """Initialize new enzyme."""
        self.classname = []
        self.sysname = ""
        self.reaction = []
        self.all_reac = []
        self.substrate = []
        self.product = []
        self.comment = ""

        self.pathway = []
        self.genes = {}
        self.disease = []
        self.reference = {}
        self.dblinks = {}
        self.orthology = []

        super().__init__(entry, cache)

    
    def _parse(self, text):
        """Parse a KEGG Enzyme informations.
        """
        key = ""
        sk = ""
        for line in text.split("\n"):
            if line[:12].strip():
                key = line[:12].strip().lower()
            value = line[12:].strip()
            if key == "entry":
                self.entry = value.rsplit(maxsplit=1)[0]
            elif key == "name":
                self.name.append(value.strip(";"))
            elif key == "class":
                self.classname.append(value.strip(";"))
            elif key == "sysname":
                self.sysname = value
            elif key == "reaction":
                self.reaction.append(value.strip(";"))
            elif key == "all_reac":
                self.all_reac.extend(re.findall("(R\d+)", value))
            elif key == "substrate":
                k, v = value.rsplit(maxsplit=1)
                self.substrate.append((k, re.findall("(C\d+)", v)))
            elif key == "product":
                k, v = value.rsplit(maxsplit=1)
                self.product.append((k, re.findall("(C\d+)", v)))
            elif key == "comment":
                self.comment += value
            elif key == "pathway":
                pid, pname = value.split(maxsplit=1)
                self.pathway.append((pid, pname))
            elif key == "orthology":
                ko, name = value.split(maxsplit=1)
                self.orthology.append((ko, name))
            elif key == "dblinks":
                k, v = value.split(": ")
                self.dblinks[k] = v.split()
            elif key == "genes":
                k, vs = value.split(": ")
                self.genes[k] = [v.split("(")[0] for v in vs.split()]
            elif key == "reference":
                self.reference[value] = {}
                sk = value
            elif key in ["authors", "title", "journal"]:
                self.reference[sk][key] = value
