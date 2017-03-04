"""
Implements the populate script.
"""

import click
import sqlalchemy
import tabulate

from condor.dbutil import requires_db

from condor.models import Bibliography
from condor.models import BibliographySet


@click.group()
def bibset():
    """
    Bibliography set related commands.
    """
    pass


@bibset.command()
@click.option('--count', default=10, help='Number of bibsets.')
@requires_db
def list(db, count):
    """
    List all the bibliography sets.
    """
    bibliography_sets = db.query(BibliographySet).order_by(
        BibliographySet.created.desc()
    ).limit(count)

    click.echo(
        tabulate.tabulate(
            [
                [
                    bibset.eid[:8],
                    bibset.description,
                    bibset.modified.strftime('%b %d, %Y, %I:%M%p'),
                    len(bibset.bibliographies)
                ]
                for bibset in bibliography_sets
            ],
            headers=[
                'Identifier', 'Description', 'Updated at', 'Docs count',
            ],
            tablefmt='rst',
        )
    )
    total = db.query(BibliographySet).count()
    if count >= total:
        click.echo('Showing all the bibliography sets.')
    else:
        click.echo(
            'Showing {count} out of {total} bibliography sets.'
            .format(count=count, total=total)
        )


@bibset.command()
@click.argument('target')
@requires_db
def delete(db, target):
    """
    Delete the target bibliography set.
    """
    try:
        bibliography_set = db.query(BibliographySet).filter(
            BibliographySet.eid.like(target + '%')
        ).one()
    except sqlalchemy.orm.exc.NoResultFound:
        click.echo('Could not find a result matching {}'.format(target))
        return
    except sqlalchemy.orm.exc.MultipleResultsFound:
        click.echo('Found many results matching {}'.format(target))
        return

    click.echo(
        'I will delete the bibliography set {}.'
        .format(bibliography_set.eid)
    )
    click.echo('And also {} bibliographies.'
               .format(len(bibliography_set.bibliographies)))
    click.echo('And also {} term document matrices.'
               .format(len(bibliography_set.term_document_matrices)))
    click.echo('And also {} search engines.'
               .format(len([
                   rm
                   for tdm in bibliography_set.term_document_matrices
                   for rm in tdm.ranking_matrices
               ])))
    click.confirm('Do you want me to delete all this information?', abort=True)
    db.delete(bibliography_set)


@bibset.command()
@click.argument('kind', type=click.Choice(['xml', 'froac', 'bib', 'isi']))
@click.argument('files', nargs=-1, type=click.File(lazy=True))
@click.option('--description', '-d', type=str, default=None,
              help='Describe your bibliography set')
@click.option('--language', '-l', 'languages', multiple=True,
              help='Filter specific languages.')
@click.option('--verbose/--quiet', default=False,
              help='Be more verbose')
@requires_db
def create(db, kind, files, description, languages, verbose):
    """
    Populates the condor database with information from the given files
    kind parameter indicates what type of files you're working with.
    """

    if verbose:
        click.echo('I\'m looking for {} records in these files:\n{}'.format(
            kind, '\n'.join(file.name for file in files))
        )

    description = description or 'Bibliography set from {count} {kind} files.'.format(
        count=len(files),
        kind=kind
    )
    bibset = BibliographySet(
        description=description
    )
    db.add(bibset)
    db.flush()

    click.echo('I\'m writting to {bibset.eid}'.format(bibset=bibset))

    mappings = Bibliography.mappings_from_files(
        [file.name for file in files],
        kind,
        bibliography_set_eid=bibset.eid
    )

    if languages:
        click.echo('Filter the following languages only: ' + ', '.join(languages))
        bibset.description += ' Filtered to {}.'.format(', '.join(languages))
        mappings = [
            m
            for m in mappings
            if m.get('language', 'english').lower() in languages
        ]

    db.bulk_insert_mappings(
        Bibliography,
        mappings
    )

    db.flush()

    click.echo('And... I\'m done')
    click.echo('The database contains {} records'.format(
        db.query(Bibliography).join(BibliographySet).
        filter(BibliographySet.eid == bibset.eid).
        count()
    ))


if __name__ == "__main__":
    bibset()
