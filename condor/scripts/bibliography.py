"""
Implements the populate script.
"""

import click
import sqlalchemy
import tabulate

from condor.dbutil import requires_db
from condor.models import Document
from condor.models import Bibliography


@click.group()
def bibliography():
    """
    Document set related commands.
    """
    pass


@bibliography.command('list')
@click.option('--count', default=10, help='Number of bibsets.')
@requires_db
def list_bibliographies(database, count):
    """
    List all the document sets.
    """
    bibliography_sets = Bibliography.list(database, count)

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
    total = Bibliography.count(database)
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
def delete(database, target):
    """
    Delete the target document set.
    """
    try:
        bibliography = database.query(Bibliography).filter(
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
    database.delete(bibliography)


@bibliography.command()
@click.argument('kind', type=click.Choice(['xml', 'froac', 'bib', 'isi']))
@click.argument('files', nargs=-1, type=click.File(lazy=True))
@click.option('--full-text-path', '-f', 'full_text',
              type=click.Path(exists=True),
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
def create(database, **kwargs):
    """
    Populates the condor database with information from the given files
    kind parameter indicates what type of files you're working with.
    """
    verbose = kwargs.pop('verbose', False)
    if verbose:
        file_names = '\n'.join(
            f.name for f in kwargs.get('files', [])
            if hasattr(f, 'name')
            )
        kind = kwargs.get('kind')
        click.echo(f'I\'m looking for {kind} records in these files:')
        click.echo(f'{file_names}')

    kwargs['show_progress_bar'] = verbose
    _bibliography = Bibliography.from_files(**kwargs)
    database.add(_bibliography)
    database.flush()

    click.echo(f'I\'m writing to {_bibliography.eid}')
    click.echo('And... I\'m done')
    click.echo('The database contains {} records'.format(
        Document.count(database, _bibliography.eid)
    ))


if __name__ == "__main__":
    bibliography()
