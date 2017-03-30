"""
Implements the populate script.
"""

import glob
import os

import click
import sqlalchemy
import tabulate
import PyPDF2

from condor.config import FULL_TEXT_PATH
from condor.dbutil import requires_db
from condor.normalize import LatexAccentRemover
from condor.models import Bibliography
from condor.models import BibliographySet


def full_text_from_pdf(filename):
    """
    Tries to extract text from pdfs.
    """
    chunks = []
    with open(filename, 'rb') as handle:
        try:
            pdf_reader = PyPDF2.PdfFileReader(handle)
            for page in pdf_reader.pages:
                try:
                    chunks.append(page.extractText())
                except PyPDF2.utils.PyPdfError:
                    pass
                except Exception:
                    # Some exceptios leak from PyPDF2
                    pass
        except PyPDF2.utils.PyPdfError:
            pass
    return '\n'.join(chunks)


def get_fulltext(full_text_path, mappings, force=False):
    """
    Creates a full text path for the given mappings.
    """
    files = {
        os.path.basename(p): p
        for p in glob.glob(full_text_path + '/**/*.pdf', recursive=True)
    }
    accent_remover = LatexAccentRemover()
    new_mappings = mappings.copy()
    for i, mapping in enumerate(mappings):
        filename = accent_remover.apply_to(mapping.get('file'))
        if not filename:
            continue
        basename = os.path.basename(
            ':'.join(filename.split(':')[:-1])
        )
        full_text_path = os.path.join(FULL_TEXT_PATH, mapping.get('hash', 'lost'))
        # Cache those files
        if not force and os.path.exists(full_text_path):
            new_mappings[i]['full_text_path'] = full_text_path
            continue
        if basename in files:
            with open(full_text_path, 'w') as output:
                output.write(full_text_from_pdf(files[basename]))
            new_mappings[i]['full_text_path'] = full_text_path
    return new_mappings


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
@click.option('--full-text-path', '-f', 'fulltext', type=click.Path(exists=True),
              help='Try to find full text pdf files in this path.')
@click.option('--no-cache', is_flag=True,
              help='Do not cache the files for full text.')
@click.option('--description', '-d', type=str, default=None,
              help='Describe your bibliography set')
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

    description = description or 'Bibliography set from {count} {kind} files.'.format(
        count=len(files),
        kind=kind
    )
    bibliograpy_set = BibliographySet(
        description=description
    )
    db.add(bibliograpy_set)
    db.flush()

    click.echo('I\'m writting to {bibliograpy_set.eid}'.format(bibliograpy_set=bibliograpy_set))

    mappings = Bibliography.mappings_from_files(
        [file.name for file in files],
        kind,
        bibliography_set_eid=bibliograpy_set.eid
    )

    if fulltext:
        mappings = get_fulltext(fulltext, mappings, force=no_cache)

    if languages:
        click.echo('Filter the following languages only: ' + ', '.join(languages))
        bibliograpy_set.description += ' Filtered to {}.'.format(', '.join(languages))
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
        filter(BibliographySet.eid == bibliograpy_set.eid).
        count()
    ))


if __name__ == "__main__":
    bibset()
