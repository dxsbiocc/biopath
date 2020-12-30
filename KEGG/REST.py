# Copyright 2020 by dengxsh.
# All rights reserved.
#

"""
Provides code to access the REST-style KEGG online API.
This module aims to make the KEGG online REST-style API easier to use. See:
http://www.kegg.jp/kegg/rest/keggapi.html
The KEGG REST-style API provides simple access to a range of KEGG databases.
This works using simple URLs (which this module will construct for you),
with any errors indicated via HTTP error levels.

References:
Kanehisa, M. and Goto, S.; KEGG: Kyoto Encyclopedia of Genes and Genomes.
Nucleic Acids Res. 28, 29-34 (2000).
"""
import requests

def _query(*args):
    """
    http://rest.kegg.jp/<operation>/<argument>[/<argument2[/<argument3> ...]]
    
    <operation> = info | list | find | get | conv | link | ddi
    """
    
    assert 1 < len(args) < 5, "arguments must larger than 1 and less than 5"

    URL = "http://rest.kegg.jp/%s" % ('/'.join(args))

    res = requests.get(URL)
    return res.text


def kegg_info(database):
    """KEGG info - Display database release information and linked db information.
    Arguments:
        - db - database or organism (string)
    The argument db can be a KEGG database name (e.g. 'pathway' or its
    official abbreviation, 'path'), or a KEGG organism code or T number
    (e.g. 'hsa' or 'T01001' for human).
    A valid list of organism codes and their T numbers can be obtained
    via kegg_info('organism') or http://rest.kegg.jp/list/organism
    """
    # TODO - return a string 
    # TODO - chache and validate the organism code / T numbers?
    # TODO - can we parse the somewhat formatted output?
    #
    # http://rest.kegg.jp/info/<database>
    #
    # <database> = kegg | pathway | brite | module | ko | genome | genes | <org> | vg | ag |
    #              ligand | compound | glycan | reaction | rclass | enzyme | network |
    #              variant | disease | drug | dgroup | environ
 
    # <org> = KEGG organism code or T number
    return _query("info", database)


def kegg_list(database, org=None):
    """KEGG list - Obtain a list of entry identifiers and associated definition.
    Arguments:
        - db - database or organism (string)
        - org - optional organism (string), see below.
    For the pathway and module databases the optional organism can be
    used to restrict the results.
    """
    # TODO - split into two functions (dbentries seems separate)?
    #
    #  http://rest.kegg.jp/list/<database>/<org>
    #
    #  <database> = pathway | module
    #  <org> = KEGG organism code
    res = ""
    if database in ["pathway", "module"] and org:
        res = _query("list", database, org)

    # http://rest.kegg.jp/list/<database>
    #
    # <database> = pathway | brite | module | ko | genome | <org> | vg | ag | compound |
    #              glycan | reaction | rclass | enzyme | network | variant | disease |
    #              drug | dgroup | environ | organism | <medicus>
    # <org> = KEGG organism code or T number
    elif isinstance(database, str):
        res = _query("list", database)
    
    # http://rest.kegg.jp/list/<dbentries>
    #
    # <dbentries> = KEGG database entries involving the following <database>
    # <database> = pathway | brite | module | ko | genome | <org> | vg | ag | compound |
    #              glycan | reaction | rclass | enzyme | network | variant | disease |
    #              drug | dgroup | environ | <medicus>
    # <org> = KEGG organism code or T number
    elif isinstance(database, list):
        if len(database) > 10:
            raise ValueError("Maximum number of databases is 10 for kegg list query.")
        res = _query("list", "+".join(database))
    else:
        raise ValueError("Invalid database arg for kegg list request.")
    return res


def kegg_find(database, query, option=None):
    """KEGG find - Find entries with matching query keyword or other query data.
    Arguments:
        - db - database or organism (string)
        - query - search terms (string)
        - option - search option (string), see below.
    For the compound and drug database, set option to the string 'formula',
    'exact_mass', 'nop' or 'mol_weight' to search on that field only. The
    chemical formula search is a partial match irrespective of the order
    of atoms given. The exact mass (or molecular weight) is checked by
    rounding off to the same decimal place as the query data. A range of
    values may also be specified with the minus(-) sign.
    """
    # TODO - return list of tuples?
    #
    # http://rest.kegg.jp/find/<database>/<query>/<option>
    #
    # <database> = compound | drug
    # <option> = formula | exact_mass | mol_weight | nop
    if database in ["compound", "drug"] and option in ["formula", "exact_mass", "mol_weight", "nop"]:
        res = _query("find", database, query, option)
    elif option:
        raise ValueError("Invalid option arg for kegg find request.")
    # http://rest.kegg.jp/find/<database>/<query>
    #
    # <database> = pathway | brite | module | ko | genome | genes | <org> | vg | ag |
    #              ligand | compound | glycan | reaction | rclass | enzyme | network |
    #              variant | disease | drug | dgroup | environ | <medicus>
    # <org> = KEGG organism code or T number
    else:
        if isinstance(query, list):
            query = "+".join(query)
        res = _query("find", database, query)
    return res


def kegg_get(dbentries, option=None):
    """KEGG get - Retrieve given database entries.
    Arguments:
        - dbentries - Identifiers (single string, or list of strings), see below.
        - option - One of "aaseq", "ntseq", "mol", "kcf", "image", "conf", "json", 
                   "kgml" (string)
    The input is limited up to 10 entries.
    The input is limited to one pathway entry with the image or kgml option.
    The input is limited to one compound/glycan/drug entry with the image option.
    Returns a string.
    """
    if isinstance(dbentries, list) and len(dbentries) <= 10:
        dbentries = "+".join(dbentries)
    elif isinstance(dbentries, list) and len(dbentries) > 10:
        raise ValueError("Maximum number of dbentries is 10 for kegg get query.")
    # http://rest.kegg.jp/get/<dbentries>[/<option>]
    #
    # <dbentries> = KEGG database entries involving the following <database>
    # <database> = pathway | brite | module | ko | genome | <org> | vg | ag | compound |
    #              glycan | reaction | rclass | enzyme | network | variant | disease |
    #              drug | dgroup | environ | disease_ja | drug_ja | dgroup_ja | environ_ja |
    #              compound_ja
    # <org> = KEGG organism code or T number
    #
    # <option> = aaseq | ntseq | mol | kcf | image | conf | kgml | json
    if option in ["aaseq", "ntseq", "mol", "kcf", "image", "conf", "kgml", "json"]:
        res = _query("get", dbentries, option)
    elif option:
        raise ValueError("Invalid option arg for kegg get request.")
    else:
        res = _query("get", dbentries)
    return res


def kegg_conv(target_db, source_db):
    """KEGG conv - convert KEGG identifiers to/from outside identifiers.
    Arguments:
     - target_db - Target database
     - source_db_or_dbentries - source database or database entries
    """
    # http://rest.kegg.jp/conv/<target_db>/<source_db>

    # (<target_db> <source_db>) = (<kegg_db> <outside_db>) | (<outside_db> <kegg_db>)

    # For gene identifiers:
    # <kegg_db> = <org>
    # <org> = KEGG organism code or T number
    # <outside_db> = ncbi-geneid | ncbi-proteinid | uniprot

    # For chemical substance identifiers:
    # <kegg_db> = compound | glycan | drug
    # <outside_db> = pubchem | chebi

    # http://rest.kegg.jp/conv/<target_db>/<dbentries>

    # For gene identifiers:
    # <dbentries> = database entries of the following <database>
    # <database> = <org> | genes | ncbi-geneid | ncbi-proteinid | uniprot
    # <org> = KEGG organism code or T number

    # For chemical substance identifiers:
    # <dbentries> = database entries of the following <database>
    # <database> = compound | glycan | drug | pubchem | chebi
    if isinstance(source_db, list):
        source_db = "+".join(source_db)
        res = _query("conv", target_db, source_db)
        return res
    
    if (
        target_db in ["ncbi-proteinid", "ncbi-geneid", "uniprot"]
        or source_db in ["ncbi-proteinid", "ncbi-geneid", "uniprot"]
        or (
            target_db in ["drug", "compound", "glycan"]
            and source_db in ["pubchem", "chebi"]
        )
        or (
            target_db in ["pubchem", "chebi"]
            and source_db in ["drug", "compound", "glycan"]
        )
    ):
        res = _query("conv", target_db, source_db)
        return res
    else:
        raise ValueError("Bad argument target_db or source_db for kegg conv request.")


def kegg_link(target_db, source_db):
    """KEGG link - find related entries by using database cross-references.
    Arguments:
        - target_db - Target database
        - source_db_or_dbentries - source database
    """
    # http://rest.kegg.jp/link/<target_db>/<source_db>
    #
    # <target_db> = <database>
    # <source_db> = <database>
    #
    # <database> =  pathway | brite | module | ko | genome | <org> | vg | ag | compound |
    #               glycan | reaction | rclass | enzyme | network | variant | disease |
    #               drug | dgroup | environ | atc | jtc | ndc | yj | pubmed

    # http://rest.kegg.jp/link/<target_db>/<dbentries>
    #
    # <dbentries> = KEGG database entries involving the following <database>
    # <database> = pathway | brite | module | ko | genome | <org> | vg | ag | compound |
    #              glycan | reaction | rclass | enzyme | network | variant | disease |
    #              drug | dgroup | environ | genes | atc | jtc | ndc | yj | pubmed
    
    if isinstance(source_db, list):
        source_db = "+".join(source_db)

    res = _query("link", target_db, source_db)

    return res


def kegg_ddi(dbentries):
    """KEGG ddi - find adverse drug-drug interactions.
    Arguments:
        - dbentries - entries of the database, drug | ndc | yj
    """
    # http://rest.kegg.jp/ddi/<dbentry>

    # <dbentry> = Single entry of the following <database>
    # <database> = drug | ndc | yj

    # http://rest.kegg.jp/ddi/<dbentries>

    # <dbentries> = Multiple entries of the following <database>
    # <database> = drug | ndc | yj
    if isinstance(dbentries, list):
        dbentries = "+".join(dbentries)

    res = _query("ddi", dbentries)
    return res
