import click

from sqlalchemy_utils import database_exists, create_database

from snakeeyes.app import create_app
from snakeeyes.extensions import db
from snakeeyes.blueprints.user2.models import User2

# Create an app context for the database connection.
app = create_app()
db.app = app


@click.group()
def cli():
    """ Run PostgreSQL related tasks. """
    pass


@click.command()
@click.option('--with-testdb2/--no-with-testdb2', default=False,
              help='Create a test db too?')
def init2(with_testdb2):
    """
    Initialize the database.

    :param with_testdb: Create a test database
    :return: None
    """
#    db.drop_all()
    db.create_all()

    if with_testdb2:
        db_uri = '{0}_test'.format(app.config['SQLALCHEMY_DATABASE_URI'])

        if not database_exists(db_uri):
            create_database(db_uri)

    return None


@click.command()
def seed2():
    """
    Seed the database with an initial user.

    :return: User instance
    """
    if User2.find_by_identity(app.config['SEED_ADMIN_EMAIL']) is not None:
        return None

    params = {
        'role': 'admin',
        'email': app.config['SEED_ADMIN_EMAIL'],
        'password': app.config['SEED_ADMIN_PASSWORD']
    }

    return User2(**params).save()


@click.command()
@click.option('--with-testdb2/--no-with-testdb2', default=False,
              help='Create a test db too?')
@click.pass_context
def reset2(ctx, with_testdb2):
    """
    Init and seed automatically.

    :param with_testdb: Create a test database
    :return: None
    """
    ctx.invoke(init2, with_testdb2=with_testdb2)
    ctx.invoke(seed2)

    return None


cli.add_command(init2)
cli.add_command(seed2)
cli.add_command(reset2)
