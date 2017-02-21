import click
# import pandas as pd

# from datetime import datetime

# from faker import Faker

from snakeeyes.app import create_app
from snakeeyes.extensions import db
from snakeeyes.blueprints.contact2.models import Projects
from snakeeyes.blueprints.user2.models import User2

# Create an app context for the database connection.
app = create_app()
db.app = app

# fake = Faker()


def _log_status(count, model_label):
    """
    Log the output of how many records were created.

    :param count: Amount created
    :type count: int
    :param model_label: Name of the model
    :type model_label: str
    :return: None
    """
    click.echo('Created {0} {1}'.format(count, model_label))

    return None


def _bulk_insert(model, data, label):
    """
    Bulk insert data to a specific model and log it. This is much more
    efficient than adding 1 row at a time in a loop.

    :param model: Model being affected
    :type model: SQLAlchemy
    :param data: Data to be saved
    :type data: list
    :param label: Label for the output
    :type label: str
    :param skip_delete: Optionally delete previous records
    :type skip_delete: bool
    :return: None
    """
    with app.app_context():
        model.query.delete()

        db.session.commit()
        db.engine.execute(model.__table__.insert(), data)

        _log_status(model.query.count(), label)

    return None


@click.group()
def cli():
    """ Add items to the database. """
    pass


@click.command()
def recommend():
    """
    Generate fake users.
    """
recommender = []
# read projects file

#input_file = "/Users/riteshmehta/Documents/OrgRiseCode/wireframe/OrgRiseProjects.csv"
#df_projects = pd.read_csv(input_file, header=0)

# read employees file

#input_file = "/Users/riteshmehta/Documents/OrgRiseCode/wireframe/OrgRiseEmployees.csv"
#df_emp = pd.read_csv(input_file, header=0)

# showcase projects array

#projects = df_projects.values

projects = Projects.query \
        .order_by(Projects.created_on.desc())

employees = User2.query \
        .order_by(User2.created_on.desc())

#projects_out = projects.run()

for project in projects:
    for employee in employees:
        if project.skills == employee.skills:
            recommender.append([project.email,employee.email])
 
click.echo('Recommendations {0}'.format(recommender))

# showcase employees array

# employees = df_emp.values

# for project in projects:
#    for employee in employees:
#        print(sum(project[1:-1] * employee[1:]))
#        print(employee[1:])

#        employeescore = sum(project[1:-1]*employee[1:])
#        requiredscore = project[-1] * 0.8

#        if employeescore >= requiredscore:
#            recommender.append([project[0],employee[0]])

#    click.echo('Recommendations {0}'.format(recommender))     

#    return _bulk_insert(User2, data, 'users2')


@click.command()
@click.pass_context
def all(ctx):
    """
    Generate all data.

    :param ctx:
    :return: None
    """
    ctx.invoke(recommend)
    return None


cli.add_command(recommend)
cli.add_command(all)
