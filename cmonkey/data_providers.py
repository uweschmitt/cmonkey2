"""The data_providers module contains functionality related to
integrating with 3rd party data providers"""


def get_kegg_organism_for_code(kegg_taxonomy_file, code):
    """using a KEGG taxonomy file, lookup the organism code to
    return the full name. taxonomy_file should be an instance of
    DelimitedFile"""
    for line in kegg_taxonomy_file.get_lines():
        if line[1] == code:
            return line[3]
    return None


def get_go_taxonomy_id(go_taxonomy_file, organism_name):
    """using a GO proteome2taxid file, look up the taxonomy id for a given
    organism name. Note that organism names are not necessarily unique.
    This will return the first one found"""
    for line in go_taxonomy_file.get_lines():
        if line[0] == organism_name:
            return line[1]
    return None

__all__ = ['get_organism_for_code', 'get_go_taxonomy_id']
