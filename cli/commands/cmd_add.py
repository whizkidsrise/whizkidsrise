import click
import random

#from datetime import datetime

# from faker import Faker

from snakeeyes.app import create_app
from snakeeyes.extensions import db
from snakeeyes.blueprints.user2.models import User2
from snakeeyes.blueprints.contact2.models import Projects

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
def users2():
    """
    Generate fake users.
    """
    random_emails = []

    skills = ['c, c++, java, .net, db',
              '.net, abap, testing, c#, web development',
              'sso, architecture, machine learning, big data, web develop',
              'project management, budget, design thinking, marketing',
              'strategy, finance, investment, pricing',
              'executive presentation, finance modeling, human resources',
              'leadership, .net, java, abap, archiecture, web development',
              'project management, strategy, architecture, sso',
              'accounting, corporate finance, governance, leadership, management',
              'operations, supply chain, performance management, HR policies',
              'c, c++, java, .net, db',
              '.net, abap, testing, c#, web development',
              'sso, architecture, machine learning, big data, web develop',
              'project management, budget, design thinking, marketing',
              'strategy, finance, investment, pricing',
              'executive presentation, finance modeling, human resources',
              'leadership, .net, java, abap, archiecture, web development',
              'project management, strategy, architecture, sso',
              'accounting, corporate finance, governance, leadership, management',
              'operations, supply chain, performance management, HR policies',
              'c, c++, java, .net, db',
              '.net, abap, testing, c#, web development',
              'sso, architecture, machine learning, big data, web develop',
              'project management, budget, design thinking, marketing',
              'strategy, finance, investment, pricing',
              'executive presentation, finance modeling, human resources',
              'leadership, .net, java, abap, archiecture, web development',
              'project management, strategy, architecture, sso',
              'accounting, corporate finance, governance, leadership, management',
              'operations, supply chain, performance management, HR policies'
              ]
    data = []
#    skills[0] = 'c, c++, java, .net, db'
#    skills[1] = '.net, abap, testing, c#, web development'
#    skills[2] = 'sso, architecture, machine learning, big data, web develop'
#    skills[3] = 'project management, budget, design thinking, marketing'
#    skills[4] = 'strategy, finance, investment, pricing'
#    skills[5] = 'executive presentation, finance modeling, human resources'
#    skills[6] = 'leadership, .net, java, abap, archiecture, web development'
#    skills[7] = 'project management, strategy, architecture, sso'
#    skills[8] = 'accounting, corporate finance, governance, leadership, management'
#    skills[9] = 'operations, supply chain, performance management, HR policies'
#    skills[10] = 'c, c++, java, .net, db'
#    skills[11] = '.net, abap, testing, c#, web development'
#    skills[12] = 'sso, architecture, machine learning, big data, web develop'
#    skills[13] = 'project management, budget, design thinking, marketing'
#    skills[14] = 'strategy, finance, investment, pricing'
#    skills[15] = 'executive presentation, finance modeling, human resources'
#    skills[16] = 'leadership, .net, java, abap, archiecture, web development'
#    skills[17] = 'project management, strategy, architecture, sso'
#    skills[18] = 'accounting, corporate finance, governance, leadership, management'
#    skills[19] = 'operations, supply chain, performance management, HR policies'
#    skills[20] = 'c, c++, java, .net, db'
#    skills[21] = '.net, abap, testing, c#, web development'
#    skills[22] = 'sso, architecture, machine learning, big data, web develop'
#    skills[23] = 'project management, budget, design thinking, marketing'
#    skills[24] = 'strategy, finance, investment, pricing'
#    skills[25] = 'executive presentation, finance modeling, human resources'
#    skills[26] = 'leadership, .net, java, abap, archiecture, web development'
#    skills[27] = 'project management, strategy, architecture, sso'
#    skills[28] = 'accounting, corporate finance, governance, leadership, management'
#    skills[29] = 'operations, supply chain, performance management, HR policies'
    click.echo('Working...')

    # Ensure we get about 100 unique random emails.

#    for j in range(0, 3):
#        skill1 = skills[j]
#        random_skills.append(skill1)
#        click.echo('Skill read {0} {1}'.format(j, skill1))
#        random_skills = list(set(random_skills))

    for i in range(0, 30):
        random_email = 'test' + str(int(i)) + '@abc.com'
        random_emails.append(random_email)

#        random_emails.append(app.config['SEED_ADMIN_EMAIL'])
#        random_emails = list(set(random_emails))

    while True:
        if len(random_emails) == 0:
            break

        click.echo('Skill list {0}'.format(skills))

        created_on = '2016-12-29 06:51:46.429746+00:00'
        current_sign_in_on = '2016-12-29 07:51:46.429746+00:00'
#        fake_datetime = fake.date_time_between(
#            start_date='-1y', end_date='now').strftime('%s')

 #       created_on = datetime.utcfromtimestamp(
 #           float(fake_datetime)).strftime('%Y-%m-%dT%H:%M:%S Z')

        random_percent = random.random()

        if random_percent >= 0.05:
            role = 'member'
        else:
            role = 'admin'

        email = random_emails.pop()
        skill = skills.pop()

        random_percent = random.random()

        if random_percent >= 0.5:
            random_trail = str(int(round((random.random() * 1000))))
            username = 'test' + random_trail
        else:
            username = None

#        fake_datetime = fake.date_time_between(
#            start_date='-1y', end_date='now').strftime('%s')

#        current_sign_in_on = datetime.utcfromtimestamp(
#            float(fake_datetime)).strftime('%Y-%m-%dT%H:%M:%S Z')

        params = {
            'created_on': created_on,
            'updated_on': created_on,
            'role': role,
            'email': email,
            'username': username,
            'password': User2.encrypt_password('password'),
            'skills': skill,
            'train': 'machine learning, bigdata',
            'sign_in_count': random.random() * 100,
            'current_sign_in_on': current_sign_in_on,
            'current_sign_in_ip': '192.157.1.1',
            'last_sign_in_on': current_sign_in_on,
            'last_sign_in_ip': '192.157.1.1'
        }


        # Ensure the seeded admin is always an admin with the seeded password.
        if email == app.config['SEED_ADMIN_EMAIL']:
            password = User2.encrypt_password(app.config['SEED_ADMIN_PASSWORD'])

            params['role'] = 'admin'
            params['password'] = password

        data.append(params)

        click.echo('chosen skill {0}'.format(skill))      

    return _bulk_insert(User2, data, 'users2')


@click.command()
def projects():
    """
    Generate fake users.
    """
    random_emails = []
    random_projects = []

    skills = ['c, c++, java, .net, db',
              '.net, abap, testing, c#, web development',
              'sso, architecture, machine learning, big data, web develop',
              'project management, budget, design thinking, marketing',
              'strategy, finance, investment, pricing',
              'executive presentation, finance modeling, human resources',
              'leadership, .net, java, abap, archiecture, web development',
              'project management, strategy, architecture, sso',
              'accounting, corporate finance, governance, leadership, management',
              'operations, supply chain, performance management, HR policies',
              'c, c++, java, .net, db',
              '.net, abap, testing, c#, web development',
              'sso, architecture, machine learning, big data, web develop',
              'project management, budget, design thinking, marketing',
              'strategy, finance, investment, pricing',
              'executive presentation, finance modeling, human resources',
              'leadership, .net, java, abap, archiecture, web development',
              'project management, strategy, architecture, sso',
              'accounting, corporate finance, governance, leadership, management',
              'operations, supply chain, performance management, HR policies',
              'c, c++, java, .net, db',
              '.net, abap, testing, c#, web development',
              'sso, architecture, machine learning, big data, web develop',
              'project management, budget, design thinking, marketing',
              'strategy, finance, investment, pricing',
              'executive presentation, finance modeling, human resources',
              'leadership, .net, java, abap, archiecture, web development',
              'project management, strategy, architecture, sso',
              'accounting, corporate finance, governance, leadership, management',
              'operations, supply chain, performance management, HR policies'
              ]
    data = []
#    skills[0] = 'c, c++, java, .net, db'
#    skills[1] = '.net, abap, testing, c#, web development'
#    skills[2] = 'sso, architecture, machine learning, big data, web develop'
#    skills[3] = 'project management, budget, design thinking, marketing'
#    skills[4] = 'strategy, finance, investment, pricing'
#    skills[5] = 'executive presentation, finance modeling, human resources'
#    skills[6] = 'leadership, .net, java, abap, archiecture, web development'
#    skills[7] = 'project management, strategy, architecture, sso'
#    skills[8] = 'accounting, corporate finance, governance, leadership, management'
#    skills[9] = 'operations, supply chain, performance management, HR policies'
#    skills[10] = 'c, c++, java, .net, db'
#    skills[11] = '.net, abap, testing, c#, web development'
#    skills[12] = 'sso, architecture, machine learning, big data, web develop'
#    skills[13] = 'project management, budget, design thinking, marketing'
#    skills[14] = 'strategy, finance, investment, pricing'
#    skills[15] = 'executive presentation, finance modeling, human resources'
#    skills[16] = 'leadership, .net, java, abap, archiecture, web development'
#    skills[17] = 'project management, strategy, architecture, sso'
#    skills[18] = 'accounting, corporate finance, governance, leadership, management'
#    skills[19] = 'operations, supply chain, performance management, HR policies'
#    skills[20] = 'c, c++, java, .net, db'
#    skills[21] = '.net, abap, testing, c#, web development'
#    skills[22] = 'sso, architecture, machine learning, big data, web develop'
#    skills[23] = 'project management, budget, design thinking, marketing'
#    skills[24] = 'strategy, finance, investment, pricing'
#    skills[25] = 'executive presentation, finance modeling, human resources'
#    skills[26] = 'leadership, .net, java, abap, archiecture, web development'
#    skills[27] = 'project management, strategy, architecture, sso'
#    skills[28] = 'accounting, corporate finance, governance, leadership, management'
#    skills[29] = 'operations, supply chain, performance management, HR policies'
    click.echo('Working...')

    # Ensure we get about 100 unique random emails.

#    for j in range(0, 3):
#        skill1 = skills[j]
#        random_skills.append(skill1)
#        click.echo('Skill read {0} {1}'.format(j, skill1))
#        random_skills = list(set(random_skills))

    for i in range(0, 30):
        random_email = 'test_mgr' + str(int(i)) + '@abc.com'
        random_emails.append(random_email)
        random_project = 'testprj' + str(int(i))
        random_projects.append(random_project)

#        random_emails.append(app.config['SEED_ADMIN_EMAIL'])
#        random_emails = list(set(random_emails))

    while True:
        if len(random_emails) == 0:
            break

#        click.echo('Skill list {0}'.format(skills))

        created_on = '2016-12-29 06:51:46.429746+00:00'
        current_sign_in_on = '2016-12-29 07:51:46.429746+00:00'
#        fake_datetime = fake.date_time_between(
#            start_date='-1y', end_date='now').strftime('%s')

 #       created_on = datetime.utcfromtimestamp(
 #           float(fake_datetime)).strftime('%Y-%m-%dT%H:%M:%S Z')

        email = random_emails.pop()
        skill = skills.pop()
        projectid = random_projects.pop()

#        random_percent = random.random()

#        if random_percent >= 0.5:
#        random_trail = str(int(round((random.random() * 1000))))
#        projectid = 'testprj' + random_trail
#        else:
#            projectid = None

#        fake_datetime = fake.date_time_between(
#            start_date='-1y', end_date='now').strftime('%s')

#        current_sign_in_on = datetime.utcfromtimestamp(
#            float(fake_datetime)).strftime('%Y-%m-%dT%H:%M:%S Z')

        params = {
            'created_on': created_on,
            'updated_on': created_on,
            'email': email,
            'projectid': projectid,
            'description': 'sample project',
            'skills': skill,
            'sign_in_count': random.random() * 100,
            'current_sign_in_on': current_sign_in_on,
            'current_sign_in_ip': '192.157.1.1',
            'last_sign_in_on': current_sign_in_on,
            'last_sign_in_ip': '192.157.1.1'
        }

        data.append(params)

#        click.echo('chosen skill {0}'.format(skill))      

    return _bulk_insert(Projects, data, 'projects')

@click.command()
@click.pass_context
def all(ctx):
    """
    Generate all data.

    :param ctx:
    :return: None
    """
    ctx.invoke(users2)
    ctx.invoke(projects)
    return None


cli.add_command(users2)
cli.add_command(projects)
cli.add_command(all)
