"""Helpers to build a ranking matrix.

.. note:: this module can receive list of already resolved models but it should
    not use the database or anything related with sqlalchemy.
"""

import numpy
import collections
import hashlib
import json


BuildRankingResult = collections.namedtuple(
    'BuildRankingResult',
    ['ranking', 'options', 'hash']
)


def ranking_hash(td_matrix, ranking, options):
    """Builds a ranking hash.

    :param td_matix: term document matrix source of the model.
    :param ranking: ranking to hash
    :param options: build options of the ranking
    :returns: ranking hash
    :rtype: str
    """
    nwords, nrecs = ranking.shape
    bibset = td_matrix.bibliography_set
    return hashlib.sha1(
        '{}{}{}{}{}condor'.format(
            bibset.eid,
            bibset.modified,
            nrecs,
            nwords,
            options
        ).encode()
    ).hexdigest()


def build_lsa_ranking(td_matrix, covariance=0.8):
    """Builds an lsa ranking matrix.

    This will ccut the matrix so taht it keeps the given covariance.

    :param td_matrix: term document matrix to use
    :param float covariance: ammount of covariance to keep.
    :returns: the ranking matrix
    :rtype: numpy array
    """
    U, S, V = numpy.linalg.svd(td_matrix.matrix, full_matrices=False)
    ss = S / numpy.sum(S)
    ss = numpy.cumsum(ss)
    # Keep 80% of the covariance
    k = numpy.sum(ss < 0.8)
    acoted = numpy.dot(numpy.diag(S[:k]), V[:k, :])
    ranking = numpy.dot(U[:, :k], acoted)

    options = json.dumps({
        'covariance': covariance
    })

    return BuildRankingResult(
        ranking=ranking,
        options=options,
        hash=ranking_hash(td_matrix, ranking, options)
    )
