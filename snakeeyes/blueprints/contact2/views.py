import click
import json
import requests
import re
from nltk.stem import SnowballStemmer as SS
from collections import defaultdict

from flask import (
    Blueprint,
    redirect,
    url_for,
    flash,
    render_template)
from flask_login import current_user, login_required

from snakeeyes.blueprints.contact2.forms import ContactForm
from snakeeyes.blueprints.contact2.models import Projects
from snakeeyes.blueprints.user2.models import User2

contact2 = Blueprint('contact2', __name__, template_folder='templates')


@contact2.route('/contact2', methods=['GET', 'POST'])
@login_required
def index():
    # Pre-populate the email field if the user is signed in.
    form = ContactForm(obj=current_user)

    if form.validate_on_submit():
        # This prevents circular imports.
        u = Projects()
        form.populate_obj(u)
        u.whizcoin = 100
#        u.save()
        s = u.description        
        skillsneeded = re.findall(r"#(\w+)",s)
        u.skills = ",".join(skillsneeded)
        u.save()



#        webhook_url = 'https://hooks.slack.com/services/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'
#        slack_data = {'text': u.projectid + " " + u.description}

#        response = requests.post(
#        webhook_url, data=json.dumps(slack_data),
#        headers={'Content-Type': 'application/json'}
#        )

#        if response.status_code != 200:
#            raise ValueError(
#            'Request to slack returned an error %s, the response is:\n%s'
#            % (response.status_code, response.text)
#            )


#        return render_template('contact2/history.html', form=form)
        redurl = '/recommendme/'+u.projectid
        return redirect(redurl)

    return render_template('contact2/index.html', form=form)

@contact2.route('/history2', defaults={'page': 1})
@contact2.route('/history2/page/<int:page>')

def history(page):
    paginated_bets = Projects.query \
        .order_by(Projects.created_on.desc()) \
        .paginate(page, 50, True)

    click.echo('projects {0}'.format(paginated_bets))

#    webhook_url = 'https://hooks.slack.com/services/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'

#    projects = Projects.query \
#        .order_by(Projects.created_on.desc())

#    for project in projects:
#        slack_data = {'text': project.projectid + " " + project.description}

#        response = requests.post(
#        webhook_url, data=json.dumps(slack_data),
#        headers={'Content-Type': 'application/json'}
#        )

#        if response.status_code != 200:
#            raise ValueError(
#            'Request to slack returned an error %s, the response is:\n%s'
#            % (response.status_code, response.text)
#            )

    return render_template('contact2/history.html', bets=paginated_bets)

@contact2.route('/userrecommend', defaults={'page': 1})

def recommender(page):
    recommender = []

    projects = Projects.query \
        .order_by(Projects.created_on.desc())

    employees = User2.query \
        .order_by(User2.created_on.desc())


    for project in projects:
        if project.resource_email == '':
            project_skills = project.skills.split(',')
            for employee in employees:
               employee_skills = employee.skills.split(',')
               matching_skills = set(project_skills) & set(employee_skills)
               if len(matching_skills) >= 0.6 * len(project_skills):
                   recommender.append([project.projectid,employee.email])    

    return render_template('contact2/userrecommend.html', bets=recommender)

@contact2.route('/recommendme/<string:projectid>', defaults={'disinterested': ''})
@contact2.route('/recommendme/<string:projectid>/<string:disinterested>')

def recommendme(projectid,disinterested):
    recommender = []
    match = ''
    matching_skills = defaultdict(list)
#    matching_skills = []
    stemmer = SS('english')

    project = Projects.find_by_identity(projectid)

    employees = User2.query \
        .order_by(User2.created_on.desc())

    if project.resource_email == '':
        project_skills = project.skills.split(',')
        for employee in employees:
            matching_skills = []
            employee_skills = employee.skills.split(',')
            for project_skill in project_skills:
                s1 = stemmer.stem(project_skill)
                for employee_skill in employee_skills:
                    s2 = stemmer.stem(employee_skill)
                    if s1 == s2:
                        matching_skills.append(employee_skill)
#            matching_skills = set(project_skills) & set(employee_skills)
            if len(matching_skills) >= 0.6 * len(project_skills):
                 employee_projects = employee.interesting_projects.split(',')
                 for matching_skill in matching_skills:
                    match = matching_skill + ',' + match
                 if project.projectid in employee_projects:
                    recommender.append([project.projectid,employee.email,'X',disinterested,
                    employee.fullname,match,employee.department,employee.protype])
                 else:
                    recommender.append([project.projectid,employee.email,'',disinterested,
                    employee.fullname,match,employee.department,employee.protype]) 
    if project.project_status == 'Started':
        employee = User2.find_by_identity(project.resource_email)
        project_skills = project.skills.split(',')
        employee_skills = employee.skills.split(',')
        matching_skills = set(project_skills) & set(employee_skills) 
        for matching_skill in matching_skills:
            match = matching_skill + ',' + match       
        recommender.append([project.projectid,employee.email,'','E',
            employee.fullname,match,employee.department,employee.protype]) 

    return render_template('contact2/userrecommend.html', bets=recommender)

@contact2.route('/assign_resource/<string:projectid>/<string:email>/<string:action>', methods=['GET', 'POST'])
def assign_resource(projectid,email,action):

#    flash('Awesome, thanks for signing up!', 'success')

    u1 = Projects.find_by_identity(projectid)

    u2 = User2.find_by_identity(email)

    if action == 'I':

        u1.interesting_participants = email + ',' + u1.interesting_participants

        redurl = '/recommendme/'+projectid+'/X'

        u1.save()
        
        return redirect(redurl)

    elif action == 'A':

#        u1.whizcoin = 0

        u1.resource_email = email

        u1.project_status = 'Resource Identified'

#        u2 = User2.find_by_identity(email)
    
#        u2.whizcoin = u2.whizcoin + 100

        u2.current_project = u1.projectid

    elif action == 'R':

        u2_projects = u2.interesting_projects.split(',')

        u2_projects.remove(projectid)

        u2.interesting_projects = ''.join(u2_projects)

        u1_participants = u1.interesting_participants.split(',')

        u1_participants.remove(email)

        u1.interesting_participants = ''.join(u1_participants)

    elif action == 'E':

        u1.project_status = 'Completed'

        u2.whizcoin = u2.whizcoin + 100

        u1.whizcoin = u1.whizcoin - 100
    
    u1.save()

    u2.save()

#    recommender = []
#    recommender.append([projectid, email])

    return render_template('contact2/thankyou.html')

@contact2.route('/networkgraph')

def networkgraph():

    return render_template('contact2/networkgraph.html')

@contact2.route('/thankyou')

def thankyou():

    projects = []

    projects2 = Projects.query \
       .filter(Projects.email == current_user.email).all()

    for project2 in projects2:
        projects.append([project2.projectid])

    participants = []

    participants2 = User2.query \
       .filter(User2.email == current_user.email).all()

    for participant2 in participants2:
        participants.append([participant2.email,participant2.whizcoin])
 #       participants.append([participant2.email,10])

    return render_template('contact2/wizcoin.html' , bets=projects, participants=participants)

@contact2.route('/recommendinit')
@login_required
def recommendinit():

    projects = []

    projects2 = Projects.query \
       .filter(Projects.email == current_user.email).all()

    for project2 in projects2:
        projects.append([project2.projectid])

    return render_template('contact2/wizcoin2.html' , bets=projects)

@contact2.route('/recommendedprojects')
@login_required
def recommendedprojects():

#    u2 = User2.find_by_identity(current_user.email)

    redurl = '/recommendprj/'+current_user.email

    return redirect(redurl)

@contact2.route('/first')

def first():

    return render_template('contact2/first.html')

@contact2.route('/slacktest', methods=['GET', 'POST'])
def slacktest():
    webhook_url = 'https://hooks.slack.com/services/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'
    slack_data = {'text': "test outbound"}

    response = requests.post(
        webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
        )

    if response.status_code != 200:
            raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
            )

    return ('', 204)
    