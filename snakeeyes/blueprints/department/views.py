from flask import (
    Blueprint,
    redirect,
    request,
    flash,
    url_for,
    render_template)
from flask_login import (
    login_required,
    login_user,
    current_user,
    logout_user)

from lib.safe_next_url import safe_next_url
from snakeeyes.blueprints.user2.decorators import anonymous_required2
from snakeeyes.blueprints.user2.models import User2
from snakeeyes.blueprints.contact2.models import Projects
from snakeeyes.blueprints.user2.forms import (
    LoginForm2,
    BeginPasswordResetForm2,
    PasswordResetForm2,
    SignupForm2,
    WelcomeForm2,
    UpdateCredentials2)

user2 = Blueprint('user2', __name__, template_folder='templates')


@user2.route('/login2', methods=['GET', 'POST'])
@anonymous_required2()
def login():
    form = LoginForm2(next=request.args.get('next'))

    if form.validate_on_submit():
        u = User2.find_by_identity(request.form.get('identity'))

        if u and u.authenticated(password=request.form.get('password')):
            # As you can see remember me is always enabled, this was a design
            # decision I made because more often than not users want this
            # enabled. This allows for a less complicated login form.
            #
            # If however you want them to be able to select whether or not they
            # should remain logged in then perform the following 3 steps:
            # 1) Replace 'True' below with: request.form.get('remember', False)
            # 2) Uncomment the 'remember' field in user/forms.py#LoginForm
            # 3) Add a checkbox to the login form with the id/name 'remember'
            if login_user(u, remember=True) and u.is_active():
                u.update_activity_tracking(request.remote_addr)

                # Handle optionally redirecting to the next URL safely.
                next_url = request.form.get('next')
                if next_url:
                    return redirect(safe_next_url(next_url))

                return redirect(url_for('user2.settings'))
            else:
                flash('This account has been disabled.', 'error')
        else:
            flash('Identity or password is incorrect.', 'error')

    return render_template('user2/login.html', form=form)


@user2.route('/logout2')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('user2.login'))


@user2.route('/account/begin_password_reset2', methods=['GET', 'POST'])
@anonymous_required2()
def begin_password_reset():
    form = BeginPasswordResetForm2()

    if form.validate_on_submit():
        u = User2.initialize_password_reset(request.form.get('identity'))

        flash('An email has been sent to {0}.'.format(u.email), 'success')
        return redirect(url_for('user.login'))

    return render_template('user2/begin_password_reset.html', form=form)


@user2.route('/account/password_reset2', methods=['GET', 'POST'])
@anonymous_required2()
def password_reset():
    form = PasswordResetForm2(reset_token=request.args.get('reset_token'))

    if form.validate_on_submit():
        u = User2.deserialize_token(request.form.get('reset_token'))

        if u is None:
            flash('Your reset token has expired or was tampered with.',
                  'error')
            return redirect(url_for('user2.begin_password_reset'))

        form.populate_obj(u)
        u.password = User2.encrypt_password(request.form.get('password'))
        u.save()

        if login_user(u):
            flash('Your password has been reset.', 'success')
            return redirect(url_for('user2.settings'))

    return render_template('user2/password_reset.html', form=form)


@user2.route('/signup2', methods=['GET', 'POST'])
@anonymous_required2()
def signup():
    form = SignupForm2()

    if form.validate_on_submit():
        u = User2()

        form.populate_obj(u)
        u.password = User2.encrypt_password(request.form.get('password'))
        u.save()

        redurl = '/recommendprj/'+u.email
        return redirect(redurl)


 #       if login_user(u):
 #           flash('Awesome, thanks for signing up!', 'success')
 #           return redirect(url_for('user2.welcome'))

    return render_template('user2/signup.html', form=form)


@user2.route('/welcome2', methods=['GET', 'POST'])
@login_required
def welcome():
    if current_user.username:
        flash('You already picked a username.', 'warning')
        return redirect(url_for('user2.settings'))

    form = WelcomeForm2()

    if form.validate_on_submit():
        current_user.username = request.form.get('username')
        current_user.save()

        flash('Sign up is complete, enjoy our services.', 'success')
        return redirect(url_for('user2.settings'))

    return render_template('user2/welcome.html', form=form)


@user2.route('/settings2')
@login_required
def settings():
    return render_template('user2/settings.html')


@user2.route('/settings/update_credentials2', methods=['GET', 'POST'])
@login_required
def update_credentials():
    form = UpdateCredentials2(current_user, uid=current_user.id)

    if form.validate_on_submit():
        new_password = request.form.get('password', '')
        current_user.email = request.form.get('email')

        if new_password:
            current_user.password = User2.encrypt_password(new_password)

        current_user.save()

        flash('Your sign in settings have been updated.', 'success')
        return redirect(url_for('user2.settings'))

    return render_template('user2/update_credentials.html', form=form)


@user2.route('/userlist', defaults={'page': 1})
@user2.route('/userlist/page/<int:page>')

def history(page):
    paginated_bets = User2.query \
        .order_by(User2.created_on.desc()) \
        .paginate(page, 50, True)

    return render_template('user2/history.html', bets=paginated_bets)

@user2.route('/userinfo/<string:useremail>')

def userinfo(useremail):
#   paginated_bets = User2.find_by_identity(email)
    
    paginated_bets = User2.query \
        .order_by(User2.created_on.desc()) \
        .paginate(1, 50, True)

    return render_template('user2/history.html', bets=paginated_bets)

@user2.route('/recommendprj/<string:email>')

def recommendme(email):
    recommender = []

    user = User2.find_by_identity(email)

    user_skill = user.skills.split(',')

    projects = Projects.query \
        .order_by(Projects.created_on.desc())

    for project in projects:
        if project.resource_email == '':
            project_skills = project.skills.split(',')
            matching_skills = set(project_skills) & set(user_skill)
            if len(matching_skills) >= 0.6 * len(project_skills):
                recommender.append([project.projectid,user.email])    

    return render_template('contact2/userrecommend.html', bets=recommender)