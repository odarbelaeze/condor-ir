import click


@click.group()
def condor():
    pass


@condor.group()
def bibset():
    """
    Bibliography set related commands.
    """
    pass


@condor.group()
def matrix():
    """
    Term document matrix related commands.
    """
    pass


@condor.group()
def ranking():
    """
    Ranking matrix related commands.
    """
    pass


if __name__ == "__main__":
    condor()
