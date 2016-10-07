import click
import github_bot


@click.command()
@click.argument('auth_file', type=click.Path(exists=True))
@click.argument('label_file', type=click.Path(exists=True))
def process_args(auth_file, label_file):
    """Run the console app"""
    click.echo('Running the console app')
    bot = github_bot.GitHubBot(click.format_filename(auth_file), click.format_filename(label_file))
    bot.label_issues()

process_args()