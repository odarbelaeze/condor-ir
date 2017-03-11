"""
Functions to work with a contributed set of queries from the command line.
"""

import collections
import sys
import os
import re

import click
import tabulate

from condor.dbutil import requires_db
from condor.models.bibliography import Bibliography
from condor.models.bibliography_set import BibliographySet
from condor.models.query import Query, QueryResult


QueryProps = collections.namedtuple(
    'QueryProps',
    [
        'path',
        'topic',
        'contributor',
        'query_string',
        'extension'
    ]
)


def query_props(path):
    """
    Extracts a QueryProps object from a file name.

    :param path: Path to a query file
    :return: QueryProps of the file
    """
    basename = os.path.basename(path)
    match = re.match(r'''
        (?P<topic>[^-]+?)
        (\s*-\s*)
        (?P<contributor>[A-Z]+)
        (\s*-\s*)?
        (?P<query_string>[^-]+)?
        (\.(?P<extension>[a-z]+))
    ''', basename, re.X)

    if not match:
        raise ValueError(
            '"{}" does not follow the file name convention.'.format(basename)
        )

    return QueryProps(path, **match.groupdict())


def prop_queries(file_names, warn):
    for file_name in file_names:
        try:
            props = query_props(file_name)
        except ValueError as e:
            color = 'yellow' if warn else 'red'
            click.echo(click.style(str(e), fg=color))
            if not warn:
                sys.exit(1)
            else:
                continue
        yield props


@click.group()
def contributor():
    """
    Manages contributor queries.
    """


@contributor.command()
@click.argument('kind', type=click.Choice(['xml', 'froac', 'bib', 'isi']))
@click.argument('files', nargs=-1, type=click.File(lazy=True))
@click.option('--description', '-d', type=str, default=None,
              help='Describe your bibliography set')
@click.option('--language', '-l', 'languages', multiple=True,
              help='Filter specific languages.')
@click.option('--warn', is_flag=True,
              help='Warn if file names do not follow the convention')
@click.option('--verbose/--quiet', default=False,
              help='Be more verbose')
@requires_db
def create(db, kind, files, description, languages, warn, verbose):
    """
    Loads a query set with the associated files.

    It will create the bibliography set, queries and query results that are
    necessary for an automatic benchmark of a search engine.

    The file names should have the following format: \n

        topic - CONTRIBUTOR - query string.ext \n
        topic - CONTRIBUTOR.ext \n

    the files with the first format will be associated to queries and the ones
    with the second format is used for not pertinent results, i.e., results
    that are not relevant to any of the contributor's queries, they will be
    added to the bibliography set just to add noise, the CONTRIBUTOR identifier
    should be uppercase and do not have spaces.
    """
    if verbose:
        click.echo('Parameters: \n' + '\n'.join([
            'kind {}'.format(kind),
            'files list of {}'.format(len(files)),
            'description {}'.format(description),
            'languages {}'.format(languages),
            'verbose {}'.format(verbose),
        ]))

    if not files:
        click.echo(
            click.style('No files to work with...', fg='red')
        )
        sys.exit(1)

    file_names = [f.name for f in files]

    if verbose:
        click.echo('Files: \n{}'.format('\n'.join(file_names)))

    description = description or (
        'Bibliography set for contributors from {count} {kind} files'
    ).format(count=len(files), kind=kind)
    bibliography_set = BibliographySet(description=description)
    db.add(bibliography_set)
    db.flush()

    if languages:
        click.echo(
            'Filter the following languages only: ' + ', '.join(languages)
        )
        bibliography_set.description += ' Filtered to {}.'.format(
            ', '.join(languages)
        )

    mappings_to_store = dict()
    mappings_for_results = dict()

    for props in prop_queries(file_names, warn):
        mappings = Bibliography.mappings_from_files([props.path], kind)
        if languages:
            mappings = [
                m
                for m in mappings
                if m.get('language', 'english').lower() in languages
            ]
        if not mappings:
            continue
        for mapping in mappings:
            mappings_to_store[mapping['hash']] = mapping
        if props.query_string is not None:
            mappings_for_results[props] = mappings

    # Store the documents
    db.bulk_insert_mappings(
        Bibliography,
        [
            dict(mapping, bibliography_set_eid=bibliography_set.eid)
            for mapping in mappings_to_store.values()
        ]
    )
    db.flush()

    bibliography_hash = {
        bibliography.hash: bibliography.eid
        for bibliography in bibliography_set.bibliographies
    }

    for props, results in mappings_for_results.items():
        query = Query(
            contributor=props.contributor,
            topic=props.topic,
            query_string=props.query_string,
            bibliography_set_eid=bibliography_set.eid
        )
        db.add(query)
        db.flush()
        db.bulk_insert_mappings(QueryResult, [
            {
                'bibliography_eid': bibliography_hash[result['hash']],
                'query_eid': query.eid,
            }
            for result in results
        ])

    click.echo(
        click.style('And we are done!', fg='green')
    )


@contributor.command()
@click.option('--count', default=10, help='Number of bibsets.')
@requires_db
def list(db, count):
    """
    List all the bibliography sets.
    """

    bibliography_sets = db.query(BibliographySet) \
        .join(Query, Query.bibliography_set_eid == BibliographySet.eid) \
        .filter(Query.eid) \
        .order_by(BibliographySet.created.desc()) \
        .distinct() \
        .limit(count)

    click.echo(
        tabulate.tabulate(
            [
                [
                    bibliography_set.eid[:8],
                    bibliography_set.description,
                    bibliography_set.modified.strftime('%b %d, %Y, %I:%M%p'),
                    len(bibliography_set.queries),
                    len(bibliography_set.bibliographies),
                ]
                for bibliography_set in bibliography_sets
            ],
            headers=[
                'Identifier',
                'Description',
                'Updated at',
                'Queries count',
                'Documents count',
            ],
            tablefmt='rst',
        )
    )

    total = db.query(BibliographySet) \
        .join(Query, Query.bibliography_set_eid == BibliographySet.eid) \
        .filter(Query.eid) \
        .distinct() \
        .count()

    if count >= total:
        click.echo('Showing all the contributor contributor bibliography sets')
    else:
        click.echo(
            'Sowing {count} out of {total} contributor bibliography sets.'
            .format(count=count, total=total)
        )
