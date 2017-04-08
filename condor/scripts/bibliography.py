"""
Implements the populate script.
"""

import click
import sqlalchemy
import tabulate

from condor.dbutil import requires_db
from condor.models import Document
from condor.models import Bibliography


default_list = list


@click.group()
def bibliography():
    """
    Document set related commands.
    """
    pass


@bibliography.command()
@click.option('--count', default=10, help='Number of bibsets.')
@requires_db
def list(db, count):
    """
    List all the document sets.
    """
    bibliography_sets = db.query(Bibliography).order_by(
        Bibliography.created.desc()
    ).limit(count)

    click.echo(
        tabulate.tabulate(
            [
                [
                    bibset.eid[:8],
                    bibset.description,
                    bibset.modified.strftime('%b %d, %Y, %I:%M%p'),
                    len(bibset.documents)
                ]
                for bibset in bibliography_sets
            ],
            headers=[
                'Identifier', 'Description', 'Updated at', 'Docs count',
            ],
            tablefmt='rst',
        )
    )
    total = db.query(Bibliography).count()
    if count >= total:
        click.echo('Showing all the document sets.')
    else:
        click.echo(
            'Showing {count} out of {total} document sets.'
            .format(count=count, total=total)
        )


@bibliography.command()
@click.argument('target')
@requires_db
def delete(db, target):
    """
    Delete the target document set.
    """
    try:
        bibliography = db.query(Bibliography).filter(
            Bibliography.eid.like(target + '%')
        ).one()
    except sqlalchemy.orm.exc.NoResultFound:
        click.echo('Could not find a result matching {}'.format(target))
        return
    except sqlalchemy.orm.exc.MultipleResultsFound:
        click.echo('Found many results matching {}'.format(target))
        return

    click.echo(
        'I will delete the document set {}.'
        .format(bibliography.eid)
    )
    click.echo('And also {} documents.'
               .format(len(bibliography.documents)))
    click.echo('And also {} term document matrices.'
               .format(len(bibliography.term_document_matrices)))
    click.echo('And also {} search engines.'
               .format(len([
                   rm
                   for tdm in bibliography.term_document_matrices
                   for rm in tdm.ranking_matrices
               ])))
    click.confirm('Do you want me to delete all this information?', abort=True)
    db.delete(bibliography)


@bibliography.command()
@click.argument('kind', type=click.Choice(['xml', 'froac', 'bib', 'isi']))
@click.argument('files', nargs=-1, type=click.File(lazy=True))
@click.option('--full-text-path', '-f', 'fulltext', type=click.Path(exists=True),
              help='Try to find full text pdf files in this path.')
@click.option('--no-cache', is_flag=True,
              help='Do not cache the files for full text.')
@click.option('--description', '-d', type=str, default=None,
              help='Describe your document set')
@click.option('--language', '-l', 'languages', multiple=True,
              help='Filter specific languages.')
@click.option('--verbose/--quiet', default=False,
              help='Be more verbose')
@requires_db
def create(db, kind, files, fulltext, no_cache, description, languages, verbose):
    """
    Populates the condor database with information from the given files
    kind parameter indicates what type of files you're working with.
    """

    if verbose:
        click.echo('I\'m looking for {} records in these files:\n{}'.format(
            kind, '\n'.join(file.name for file in files)
        ))

    description = description or 'Document set from {count} {kind} files.'.format(
        count=len(files),
        kind=kind
    )
    bibliography = Bibliography(
        description=description
    )
    db.add(bibliography)
    db.flush()

    click.echo('I\'m writing to {bibliography.eid}'.format(
        bibliography=bibliography))

    mappings = Document.mappings_from_files(
        default_list([file.name for file in files]),
        kind,
        full_text_path=fulltext,
        force=no_cache,
        bibliography_eid=bibliography.eid
    )

    if languages:
        click.echo(
            'Filter the following languages only: ' + ', '.join(languages)
        )
        bibliography.description += ' Filtered to {}.'.format(
            ', '.join(languages)
        )
        mappings = [
            m
            for m in mappings
            if m.get('language', 'english').lower() in languages
        ]

    db.bulk_insert_mappings(
        Document,
        mappings
    )

    db.flush()

    click.echo('And... I\'m done')
    click.echo('The database contains {} records'.format(
        db.query(Document).join(Bibliography).
        filter(Bibliography.eid == bibliography.eid).
        count()
    ))


if __name__ == "__main__":
    bibliography()
