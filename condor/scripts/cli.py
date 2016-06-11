import click


from condor.scripts.bibset import bibset
from condor.scripts.model import model


@click.group()
def matrix():
    """
    Term document matrix related commands.
    """
    pass


@click.group()
def ranking():
    """
    Ranking matrix related commands.
    """
    pass


class CondorCommand(click.MultiCommand):

    COMMANDS = {
        'bibset': bibset,
        'model': model,
        'matrix': matrix,
        'ranking': ranking,
    }

    def list_commands(self, ctx):
        return list(self.COMMANDS.keys())

    def get_command(self, ctx, name):
        return self.COMMANDS.get(name)


condor = CondorCommand(
    help='Condor information retrieval software'
)


if __name__ == "__main__":
    condor()
