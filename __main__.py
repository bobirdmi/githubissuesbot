import click
import github_bot
import sched
import time


@click.command()
@click.argument('auth_file', type=click.Path(exists=True))
@click.argument('label_file', type=click.Path(exists=True))
@click.option('-u', '--user', prompt='Username', help='Username of repository owner.')
@click.option('-r', '--repo', prompt='Repo', help='This repository will be processed.')
@click.option('-p', '--period', default=30,
              help='How often issues in the given repository will be processed and labeled (in seconds).')
@click.option('-l', '--deflabel', default='default',
              help='Default label for those issues that do not satisfy any rules in the label_file.')
def process_args(auth_file, label_file, user, repo, period, deflabel):
    """Run the console app"""
    click.echo('Running the console app')

    url = 'https://api.github.com/repos/' + user + '/' + repo + '/issues'
    bot = github_bot.GitHubBot(click.format_filename(auth_file),
                               click.format_filename(label_file),
                               url, period, deflabel)

    my_scheduler = sched.scheduler(time.time, time.sleep)

    def repeated_labeling(sc):
        bot.label_issues()

        print(10 * '=')
        print("Labeling in", period, "seconds...")
        my_scheduler.enter(period, 1, repeated_labeling, (sc,))

    my_scheduler.enter(0, 1, repeated_labeling, (my_scheduler,))
    my_scheduler.run()


process_args()