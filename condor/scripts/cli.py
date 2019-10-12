import click
import sys


class CondorCommand(click.MultiCommand):

    @property
    def commands(self):
        try:
            from condor.scripts.bibliography import bibliography
            from condor.scripts.model import model
            from condor.scripts.query import query
            from condor.scripts.matrix import matrix
            from condor.scripts.ranking import ranking
            from condor.scripts.utils import utils
            from condor.scripts.contributor import contributor
            from condor.scripts.evaluate import evaluate
            return {
                'bibliography': bibliography,
                'contributor': contributor,
                'model': model,
                'matrix': matrix,
                'ranking': ranking,
                'query': query,
                'evaluate': evaluate,
                'utils': utils,
            }

    def list_commands(self, ctx):
        return list(self.commands.keys())

    def get_command(self, ctx, name):
        return self.commands.get(name)


condor = CondorCommand(
    help='Condor information retrieval software'
)


if __name__ == "__main__":
    condor()
