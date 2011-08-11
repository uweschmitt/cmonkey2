"""motif.py - cMonkey motif related processing
This module captures the motif-specific scoring component
of cMonkey.

This file is part of cMonkey Python. Please see README and LICENSE for
more information and licensing details.
"""


DISTANCE_UPSTREAM_SEARCH = (-20, 150)
DISTANCE_UPSTREAM_SCAN = (-30, 150)


def __filter_sequences(meme_suite, sorted_feature_ids, seqs):
    print "filter_sequences"
    unique_seqs = {}
    for feature_id in sorted_feature_ids:
        if seqs[feature_id] not in unique_seqs.values():
            unique_seqs[feature_id] = seqs[feature_id]
    return meme_suite.remove_low_complexity(unique_seqs)


def compute_scores(meme_suite, organism, membership):
    """compute motif scores"""
    genes = sorted(membership.rows_for_cluster(1))
    feature_ids = organism.feature_ids_for(genes)
    seqs = organism.sequences_for_genes(genes, DISTANCE_UPSTREAM_SEARCH,
                                        upstream=True, motif_finding=True)
    seqs = __filter_sequences(meme_suite, feature_ids, seqs)
    print seqs
