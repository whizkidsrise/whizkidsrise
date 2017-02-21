from wtforms.validators import ValidationError

from snakeeyes.blueprints.user2.models import User2


def ensure_identity_exists(form, field):
    """
    Ensure an identity exists.

    :param form: wtforms Instance
    :param field: Field being passed in
    :return: None
    """
    user = User2.find_by_identity(field.data)

    if not user:
        raise ValidationError('Unable to locate account.')


def ensure_existing_password_matches(form, field):
    """
    Ensure that the current password matches their existing password.

    :param form: wtforms Instance
    :param field: Field being passed in
    :return: None
    """
    user = User2.query.get(form._obj.id)

    if not user.authenticated(password=field.data):
        raise ValidationError('Does not match.')
