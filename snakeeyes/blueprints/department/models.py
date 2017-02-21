from collections import OrderedDict

from flask_login import UserMixin

from itsdangerous import TimedJSONWebSignatureSerializer

from lib.util_sqlalchemy import ResourceMixin, AwareDateTime
from snakeeyes.extensions import db


class Department(UserMixin, ResourceMixin, db.Model):
    
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True)

    # Authentication.
    active = db.Column('is_active', db.Boolean(), nullable=False,
                       server_default='1')
    departmentname = db.Column(db.String(24), unique=True, index=True)
    deptowneremail = db.Column(db.String(255), unique=True, index=True, nullable=False,
                      server_default='')
    parentid = db.Column(db.Integer, unique=True)
    whizcoin = db.Column(db.Integer, nullable=False, default=1000)
    # Activity tracking.
    current_sign_in_on = db.Column(AwareDateTime())
    current_sign_in_ip = db.Column(db.String(45))
    last_sign_in_on = db.Column(AwareDateTime())
    last_sign_in_ip = db.Column(db.String(45))

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(Department, self).__init__(**kwargs)

    @classmethod
    def find_by_identity(cls, identity):
        """
        Find a user by their e-mail or username.

        :param identity: Email or username
        :type identity: str
        :return: User instance
        """
        return Department.query.filter(
          (Department.departmentname == identity)).first()