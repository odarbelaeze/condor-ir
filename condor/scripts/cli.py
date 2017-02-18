import click
import enchant
import sys


class CondorCommand(click.MultiCommand):

    @property
    def commands(self):
        try:
            from condor.scripts.bibset import bibset
            from condor.scripts.model import model
            from condor.scripts.query import query
            from condor.scripts.matrix import matrix
            from condor.scripts.ranking import ranking
            from condor.scripts.utils import utils
            from condor.scripts.contributor import contributor
            return {
                'bibset': bibset,
                'contributor': contributor,
                'model': model,
                'matrix': matrix,
                'ranking': ranking,
                'query': query,
                'utils': utils,
            }
        except enchant.errors.DictNotFoundError:
            click.echo(
                click.style('There was an error retrieving dictionaries.',
                            fg='red')
            )
            sys.exit(1)

    def list_commands(self, ctx):
        click.echo(str(self.commands.keys()))
        return list(self.commands.keys())

    def get_command(self, ctx, name):
        return self.commands.get(name)


condor = CondorCommand(
    help='Condor information retrieval software'
)


if __name__ == "__main__":
    condor()
