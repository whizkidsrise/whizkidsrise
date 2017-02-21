import datetime

import pytz

from flask_login import UserMixin

from lib.util_sqlalchemy import ResourceMixin, AwareDateTime
from snakeeyes.extensions import db


class Projects(UserMixin, ResourceMixin, db.Model):
    #    ROLE = OrderedDict([
    #        ('member', 'Member'),
    #        ('admin', 'Admin')
    #    ])

    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)

    # Authentication.
    projectid = db.Column(db.String(24), unique=True, index=True)
    description = db.Column(db.String(4100), nullable=False, server_default='')
    skills = db.Column(db.String(4100), unique=False, server_default='')
    email = db.Column(db.String(255), unique=False, index=False,
                      nullable=False, server_default='')
    resource_email = db.Column(db.String(255), unique=False, index=False,
                      nullable=False, server_default='')
    whizcoin = db.Column(db.Integer, nullable=False, default=100)
    department = db.Column(db.String(255), unique=False, index=False,
                      nullable=False, server_default='')
    protype = db.Column(db.String(255), unique=False, index=False,
                      nullable=False, server_default='')
    startdate = db.Column(db.String(255), unique=False, index=False,
                      nullable=False, server_default='')
    enddate = db.Column(db.String(255), unique=False, index=False,
                      nullable=False, server_default='')
    interesting_participants = db.Column(db.String(4100), unique=False, server_default='')
    project_status = db.Column(db.String(255), unique=False, index=False,
                      nullable=False, server_default='')


    # Activity tracking.
    sign_in_count = db.Column(db.Integer, nullable=False, default=0)
    current_sign_in_on = db.Column(AwareDateTime())
    current_sign_in_ip = db.Column(db.String(45))
    last_sign_in_on = db.Column(AwareDateTime())
    last_sign_in_ip = db.Column(db.String(45))

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(Projects, self).__init__(**kwargs)

    @classmethod
    def find_by_identity(cls, identity):
        """
        Find a user by their e-mail or username.

        :param identity: Email or username
        :type identity: str
        :return: User instance
        """
        return Projects.query.filter(
          (Projects.projectid == identity)).first()

    def update_activity_tracking(self, ip_address):
        """
        Update various fields on the user that's related to meta data on their
        account, such as the sign in count and ip address, etc..

        :param ip_address: IP address
        :type ip_address: str
        :return: SQLAlchemy commit results
        """
        self.sign_in_count += 1

        self.last_sign_in_on = self.current_sign_in_on
        self.last_sign_in_ip = self.current_sign_in_ip

        self.current_sign_in_on = datetime.datetime.now(pytz.utc)
        self.current_sign_in_ip = ip_address

        return self.save()
