from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from django.db import connection

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):

        cursor0 = connection.cursor()
        cursor0.execute(
            "SELECT "
            "id, "
            "username, "
            "email,"
            "email_confirmedflag_tblauth_user "

            "FROM auth_user "

            "WHERE id=%s ",
            [user.id])
        usernowrowfromtable = cursor0.fetchall()
        # import pdb;
        # pdb.set_trace()

        for instancesingle in usernowrowfromtable:
            email_confirmedflag = instancesingle[3]

        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(email_confirmedflag)
        )

account_activation_token = AccountActivationTokenGenerator()