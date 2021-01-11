# Copyright 2021 by dengxsh.
# All rights reserved.
#

"""Code to work with the KEGG Ligand/Compound database.
Classes:
 - Compound - A representation of a KEGG Ligand/Compound.
"""
from KEGG.utils import Entry


class Compound(Entry):
    """Holds info from a KEGG Ligand/Compound record.

    Attributes:
     - entry       The entry identifier.
     - name        A list of the compund names.
     - formula     The chemical formula for the compound
     - exact_mass  The molecular weight for the compound
     - pathway     A list of 3-tuples: ('PATH', pathway id, pathway)
     - enzyme      A list of the EC numbers.
     - structures  A list of 2-tuples: (database, list of struct ids)
     - dblinks     A list of 2-tuples: (database, list of link ids)

    """

    def __init__(self, entry: str, cache: bool= True) -> None:

        self.formula = ""
        self.exact_mass = 0.0
        self.mol_weight = 0.0
        # self.structure = []
        self.remark = []
        self.reaction = []
        self.pathway = []
        self.enzyme = []
        # self.reference = []
        self.dblinks = {}
        self.kcf_data = {
            "atom": [],
            "bond": [],
            "bracket": []
        }

        super().__init__(entry, cache)

    def _parse(self, text):
        key = ""
        for line in text.split("\n"):
            if line[:12].strip():
                key = line[:12].strip().lower()
            value = line[12:].strip()
            if key == "entry":
                self.entry = value.split()[0]
            elif key == "name":
                self.name.append(value.strip(";"))
            elif key == "enzyme":
                self.enzyme.extend(value.split())
            elif key == "formula":
                self.formula = value
            elif key == "remark":
                self.remark = value.split(": ")[-1]
            elif key == "exact_mass":
                self.exact_mass = float(value)
            elif key == "mol_weight":
                self.mol_weight = float(value)
            elif key == "reaction":
                self.reaction.extend(value.split())
            elif key == "pathway":
                self.pathway.append(value.split(maxsplit=1))
            elif key == "dblinks":
                k, v = value.split(": ")
                self.dblinks[k] = v.split()
            elif key in ["atom", "bond", "bracket"]:
                v = value.split()
                if len(v) > 1:
                    self.kcf_data[key].append(v[1:])