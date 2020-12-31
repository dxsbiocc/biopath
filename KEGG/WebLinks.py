# Copyright 2020 by dengxsh.
# All rights reserved.
#
"""
Provides code to access the KEGG WebLinks.
This module aims to make the KEGG webLink easier to use. See:
https://www.kegg.jp/kegg/docs/weblink.html
Use KEGG WebLink can easily retrieving html files from and 
creating links to KEGG at https://www.kegg.jp/.
"""
from urllib.parse import quote


def _link(operation, argument):
    """REST-style URL
    https://www.kegg.jp/<operation>/<argument>

    <operation> = entry | pathway | module | network | brite
    """
    URL = "https://www.kegg.jp/%s/%s" %(operation, argument)
    return URL


def _link_rest(operation, argument, option=None):
    """
    <operation> = pathway | module | network | brite
    """
    if not option:
        return _link(operation, argument)
    if isinstance(option, list):
        option = "+".join(option)
    
    return _link(operation, "+".join([argument, option]))


def link_entry(dbentries):
    """Entry – Retrieve database entries
    Arguments:
        - dbentries - Identifiers (single string, or list of strings), see below.

    Description:
        This URL returns the KEGG database entry page(s). It is equivalent to
            https://www.kegg.jp/dbget-bin/www_bget?<dbentries>
        or its GenomNet mirror
            https://www.genome.jp/dbget-bin/www_bget?<dbentries>
    Examples:
        >>> link_entry('map00010')
        [ 1 ]: 'https://www.kegg.jp/entry/map00010'
        >>> link_entry('C00022')
        [ 2 ]: 'https://www.kegg.jp/entry/C00022'
    """
    # https://www.kegg.jp/entry/<dbentries>

    # <dbentries> = Entries of the following <database>
    # <database> = pathway | brite | module | ko | genome | <org> | vg | ag | compound |
    #             glycan | reaction | rclass | enzyme | network | variant | disease |
    #             drug | dgroup | environ | <medicus>
    if isinstance(dbentries, list):
        dbentries = "+".join(dbentries)
    return _link("entry", dbentries)


def link_pathway(mapid, map_objects=None):
    """pathway - Retrieve pathway map with optional coloring of objects
    Arguments:
        - mapid - KEGG pathway map identifier
        - map_objects - map entry identifiers (single string, or list of strings)

    Description:
        This URL returns the KEGG pathway map page. It is equivalent to
            https://www.kegg.jp/kegg-bin/show_pathway?<mapid>[+<map_objects>]
        or its GenomNet mirror
            https://www.genome.jp/kegg-bin/show_pathway?<mapid>[+<map_objects>]
    Examples:
        >>> link_pathway('map00010')
        [ 1 ]: 'https://www.kegg.jp/pathway/map00010'
        >>> link_pathway('map00010', 'C00022')
        [ 2 ]: 'https://www.kegg.jp/pathway/map00010+C00022'
        >>> link_pathway('map00010', ['K00873', 'C00022'])
        [ 3 ]: 'https://www.kegg.jp/pathway/map00010+K00873+C00022'
    """
    # https://www.kegg.jp/pathway/<mapid>[+<map_objects>]

    # <mapid> = KEGG pathway map identifier
    # <map_objects> = <dbentry>1[+<dbentry>2...]
    return _link_rest("pathway", mapid, map_objects)


def link_module(modid, mod_objects=None):
    """Module - Retrieve module map with optional coloring of objects
    Arguments:
        - modid - KEGG module identifier
        - mod_objects - module entry identifiers (single string, or list of strings)

    Description:
        This URL returns the KEGG module page. It is equivalent to
            https://www.kegg.jp/kegg-bin/show_module?<modid>[+<mod_objects>]
        or its GenomNet mirror
            https://www.genome.jp/kegg-bin/show_module?<modid>[+<mod_objects>]
    Examples:
        >>> link_module('M00010')
        [ 1 ]: 'https://www.kegg.jp/module/M00010'
        >>> link_module('hsa_M00095', '3156')
        [ 2 ]: 'https://www.kegg.jp/module/hsa_M00095+3156'
    """
    # https://www.kegg.jp/module/<modid>[+<mod_objects>]

    # <modid> = KEGG module identifier
    # <mod_objects> = <dbentry>1[+<dbentry>2...]
    
    return _link_rest("module", modid, mod_objects)


def link_network(ntid, nt_objects=None):
    """Network - Retrieve network variation map with optional coloring of objects
    Arguments:
        - ntid - KEGG network variation map identifier
        - nt_objects - network entry identifiers (single string, or list of strings)

    Description:
        This URL returns the KEGG network variation map page. It is equivalent to
            https://www.kegg.jp/kegg-bin/show_network?<ntid>[+<nt_objects>]
        or its GenomNet mirror
            https://www.genome.jp/kegg-bin/show_network?<ntid>[+<nt_objects>]
    Examples:
        >>> link_network('nt06210')
        [ 1 ]: 'https://www.kegg.jp/network/nt06210'
        >>> link_network('nt06210', 'D07130')
        [ 2 ]: 'https://www.kegg.jp/network/nt06210+D07130'
    """
    # https://www.kegg.jp/network/<ntid>[+<nt_objects>]

    # <ntid> = KEGG network variation map identifier
    # <nt_objects> = <dbentry>1[+<dbentry>2...]
    return _link_rest("network", ntid, nt_objects)


def link_brite(brid, br_objects=None):
    """Brite - Retrieve brite hierarchy with optional coloring of objects
    Arguments:
        - brid - KEGG brite hierarchy identifier
        - br_objects - brite hierarchy entry identifiers (single string, or list of strings)

    Description:
        This URL returns the KEGG BRITE hierarchy page. It is equivalent to
            https://www.kegg.jp/kegg-bin/get_htext?<brid>[+<br_objects>]
        or its GenomNet mirror
            https://www.genome.jp/kegg-bin/get_htext?<brid>[+<br_objects>]
    Examples:
        >>> link_brite('ko00001')
        [ 1 ]: 'https://www.kegg.jp/brite/ko00001'
        >>> link_brite('br08601', 'hsa')
        [ 2 ]: 'https://www.kegg.jp/brite/br08601+hsa'
    """
    # https://www.kegg.jp/brite/<brid>[+<br_objects>]

    # <brid> = KEGG brite hierarchy identifier
    # <br_objects> = <dbentry>1[+<dbentry>2...]
    return _link_rest("brite", brid, br_objects)



# Links to Analysis Tools
def _pathway_mapping_get(mapid, entry, bgcolor=None, fgcolor=None, default="pink"):
    """Pathway Mapping (get) - KEGG pathway map coloring by HTTP GET method
    Arguments:
        - mapid - KEGG pathway map identifier
        - entry - map entry identifiers
        - bgcolor - background color
        - fgcolor - foreground color
        - default - default background fill color
    Description
        This URL allows coloring of objects in a KEGG pathway map according to the 
        color specification given in single-line, slash(/)-delimited <dataset>. 
        Use "%23" in ASCII code instead of "#" for color specification.
    """
    # https://www.kegg.jp/kegg-bin/show_pathway?<mapid>/<dataset>[/default%3d<dcolor>]

    # <mapid> = KEGG pathway map identifier
    # <dataset> = <dbentry>1%09<bgcolor>1,<fgcolor>1[/<dbentry>2%09<bgcolor>2,<fgcolor>2...]

    # <bgcolor> = background color
    # <fgcolor> = foreground color             "%09" represents TAB in ASCII code
    # <dcolor> = default background color      "%3d" represents "=" in ASCII code
    to_list = lambda x: [x] if isinstance(x, str) else x
    entry = to_list(entry)
    bgcolor = to_list(bgcolor)
    fgcolor = to_list(fgcolor)

    if not bgcolor:
        bgcolor = [""] * len(entry)
    if not fgcolor:
        fgcolor = [""] * len(entry)
    if len(entry) != len(bgcolor) or len(entry) != len(fgcolor):
        raise ValueError("if you want to set color, the number of 'bgcolor' and 'fgcolor' must equal to 'entry'.")
    query_str = []
    for e, b, f in zip(entry, bgcolor, fgcolor):
        query_str.append("/")
        query_str.append(e)
        if b or f:
            query_str.append("\t")
        if b:
            query_str.append(b)
        if f:
            query_str.append(",")
            query_str.append(f)
    query_str.append("/default=%s" % default)
    query_str = "".join(query_str)
    URL = "https://www.kegg.jp/kegg-bin/show_pathway?%s%s" % ( mapid, quote(query_str) )
    return URL


def _pathway_mapping_post(mapid, entry, bgcolor=None, fgcolor=None):
    """Pathway Mapping (post) - KEGG pathway map coloring by HTTP POST method
    Arguments:
        - mapid - KEGG pathway map identifier
        - entry - map entry identifiers
        - bgcolor - background color
        - fgcolor - foreground color

    Description:
        This URL allows coloring of objects in a KEGG pathway map according 
        to the color specification given in multiple-line <dataset>, 
        which corresponds to the textarea in KEGG Mapper Search&Color Pathway. 
        To use uncolored diagram (rather than colored organism-specific diagram, 
        for example) specify the nocolor option.
    """
    # https://www.kegg.jp/kegg-bin/show_pathway?map=<mapid>&multi_query=<dataset>[&nocolor=1]

    # <mapid> = KEGG pathway map identifier
    # <dataset> = <dbentry>1+<bgcolor>1,<fgcolor>1[%0d%0a<dbentry>2+<bgcolor>2,<fgcolor>2...]

    # <bgcolor> = background color             "%0d" represents CR in ASCII code
    # <fgcolor> = foreground color             "%0a" represents LF in ASCII code
    to_list = lambda x: [x] if isinstance(x, str) else x
    entry = to_list(entry)
    bgcolor = to_list(bgcolor)
    fgcolor = to_list(fgcolor)

    if not bgcolor:
        bgcolor = [""] * len(entry)
    if not fgcolor:
        fgcolor = [""] * len(entry)
    if len(entry) != len(bgcolor) or len(entry) != len(fgcolor):
        raise ValueError("if you want to set color, the number of 'bgcolor' and 'fgcolor' must equal to 'entry'.")
    query_str = []
    for e, b, f in zip(entry, bgcolor, fgcolor):
        entry_str = e
        if b or f:
            entry_str += "+"
        if b:
            entry_str += quote(b)
        if f:
            entry_str += ",%s" % (quote(f))
        query_str.append(entry_str)
    query_str = quote("\r\n").join(query_str)
    URL = "https://www.kegg.jp/kegg-bin/show_pathway?map=%s&multi_query=%s" %( mapid, query_str )
    return URL


def color_mapping(mapid, entry, bgcolor=None, fgcolor=None, method="get", default="pink"):
    """Pathway Mapping - KEGG pathway map coloring by HTTP GET or POST method
    Arguments:
        - mapid - KEGG pathway map identifier
        - entry - map entry identifiers
        - bgcolor - background color, default None
        - fgcolor - foreground color, default None
        - default - default background fill color, don't use in 'post'
    Description:
        - get:
        This URL allows coloring of objects in a KEGG pathway map according to the color 
        specification given in single-line, slash(/)-delimited <dataset>. 
        - post: 
        This URL also allows coloring of objects in a KEGG pathway map according to the 
        color specification given in multiple-line <dataset>, which corresponds to the 
        textarea in KEGG Mapper Search&Color Pathway. 
    Examples:
        >>> mapid = "map00400"
        >>> entry = ['1.14.16.1', 'C00079', 'C00166']
        >>> bgcolor = ['green', 'blue', '']
        >>> fgcolor = ['red', '#005050', 'blue']
        >>> color_mapping(mapid, entry, bgcolor, fgcolor, method='get')
        [ 1 ]: 'https://www.kegg.jp/kegg-bin/show_pathway?map00400/1.14.16.1%09green%2Cred/C00079%09blue%2C%23005050/C00166%09%2Cblue/default%3Dpink'
        >>> color_mapping(mapid, entry, bgcolor, fgcolor, method='post')
        [ 2 ]: 'https://www.kegg.jp/kegg-bin/show_pathway?map=map00400&multi_query=1.14.16.1+green,red%0D%0AC00079+blue,%23005050%0D%0AC00166+,blue'
    """
    if method.lower() == "get":
        return _pathway_mapping_get(mapid=mapid, entry=entry, bgcolor=bgcolor, fgcolor=fgcolor, default=default)
    elif method.lower() == "post":
        return _pathway_mapping_post(mapid=mapid, entry=entry, bgcolor=bgcolor, fgcolor=fgcolor)
    else:
        raise ValueError("Unknown method, which not in ['get', 'post].")


def ssdb_search(database, org, gene):
    """SSDB Search - SSDB search for orthologs, paralogs and gene clusters
    Description
        These URLs retrieve data from the KEGG SSDB database containing amino acid 
        similarity scores and best-hit relations in genome pairs among all genes 
        in the KEGG GENES database.
    Examples:
        >>> ssdb_search('ortholog', 'syn', 'sll1450')
        [ 1 ]: 'https://www.kegg.jp/ssdb-bin/ssdb_best?org_gene=syn:sll1450'
        >>> ssdb_search('paralog', 'syn', 'sll1450')
        [ 2 ]: 'https://www.kegg.jp/ssdb-bin/ssdb_paralog?org_gene=syn:sll1450'
        >>> ssdb_search('gene_cluster', 'syn', 'sll1450')
        [ 3 ]: 'https://www.kegg.jp/ssdb-bin/ssdb_gclust?org_gene=syn:sll1450'
    """
    # (ortholog)     https://www.kegg.jp/ssdb-bin/ssdb_best?org_gene=<org>:<gene>
    # (paralog)      https://www.kegg.jp/ssdb-bin/ssdb_paralog?org_gene=<org>:<gene>
    # (gene cluster) https://www.kegg.jp/ssdb-bin/ssdb_gclust?org_gene=<org>:<gene>
    data_trans = {
        'ortholog' : 'ssdb_best',
        'paralog': 'ssdb_paralog',
        'gene_cluster': 'ssdb_gclust'
    }
    if database not in data_trans.keys():
        raise ValueError("The databse '%s' is not in %s" % (database, list(data_trans.keys())))

    URL = "https://www.kegg.jp/ssdb-bin/%s?org_gene=%s:%s" % (data_trans.get(database), org, gene)
    return URL
