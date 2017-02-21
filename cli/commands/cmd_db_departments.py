import click

from sqlalchemy_utils import database_exists, create_database

from snakeeyes.app import create_app
from snakeeyes.extensions import db
from snakeeyes.blueprints.department.models import Department

# Create an app context for the database connection.
app = create_app()
db.app = app


@click.group()
def cli():
    """ Run PostgreSQL related tasks. """
    pass


@click.command()
@click.option('--with-testdb4/--no-with-testdb4', default=False,
              help='Create a test db too?')
def init4(with_testdb4):
    """
    Initialize the database.

    :param with_testdb: Create a test database
    :return: None
    """
    db.reflect()
    db.drop_all()
    db.create_all()

    if with_testdb4:
        db_uri = '{0}_test'.format(app.config['SQLALCHEMY_DATABASE_URI'])

        if not database_exists(db_uri):
            create_database(db_uri)

    return None


@click.command()
def seed4():
    """
    Seed the database with an initial user.

    :return: User instance
    """
    if Department.find_by_identity(app.config['SEED_DEPARTMENT']) is not None:
        return None

    params = {
        'departmentname': 'testdept',
        'deptowneremail': 'er.ritesh.mehta@gmail.com'
    }

    return Department(**params).save()


@click.command()
@click.option('--with-testdb4/--no-with-testdb4', default=False,
              help='Create a test db too?')
@click.pass_context
def reset4(ctx, with_testdb4):
    """
    Init and seed automatically.

    :param with_testdb: Create a test database
    :return: None
    """
    ctx.invoke(init4, with_testdb4=with_testdb4)
    ctx.invoke(seed4)

    return None


cli.add_command(init4)
cli.add_command(seed4)
cli.add_command(reset4)
