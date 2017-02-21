import click

from sqlalchemy_utils import database_exists, create_database

from snakeeyes.app import create_app
from snakeeyes.extensions import db
from snakeeyes.blueprints.contact2.models import Projects

# Create an app context for the database connection.
app = create_app()
db.app = app


@click.group()
def cli():
    """ Run PostgreSQL related tasks. """
    pass


@click.command()
@click.option('--with-testdb3/--no-with-testdb3', default=False,
              help='Create a test db too?')
def init3(with_testdb3):
    """
    Initialize the database.

    :param with_testdb: Create a test database
    :return: None
    """
    db.reflect()
    db.drop_all()
    db.create_all()

    if with_testdb3:
        db_uri = '{0}_test'.format(app.config['SQLALCHEMY_DATABASE_URI'])

        if not database_exists(db_uri):
            create_database(db_uri)

    return None


@click.command()
def seed3():
    """
    Seed the database with an initial user.

    :return: User instance
    """
    if Projects.find_by_identity(app.config['SEED_PROJECT']) is not None:
        return None

    params = {
        'projectid': 'riteshtest1',
        'description': 'abc',
        'skills': 'java, c, c#',
        'email': 'er.ritesh.mehta@gmail.com'
    }

    return Projects(**params).save()


@click.command()
@click.option('--with-testdb3/--no-with-testdb3', default=False,
              help='Create a test db too?')
@click.pass_context
def reset3(ctx, with_testdb3):
    """
    Init and seed automatically.

    :param with_testdb: Create a test database
    :return: None
    """
    ctx.invoke(init3, with_testdb3=with_testdb3)
    ctx.invoke(seed3)

    return None


cli.add_command(init3)
cli.add_command(seed3)
cli.add_command(reset3)
